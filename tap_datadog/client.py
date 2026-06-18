import json
import math

from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.helpers._typing import TypeConformanceLevel
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, PageNumberPaginator
from singer_sdk.streams import RESTStream

# Base API documentation: https://docs.datadoghq.com/api/latest

class DatadogAuthenticator(APIAuthenticatorBase):
    def __init__(self, api_key, application_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.auth_headers is None:
            self.auth_headers = {}

        self.auth_headers['DD-API-KEY'] = api_key

        if application_key is not None:
            self.auth_headers['DD-APPLICATION-KEY'] = application_key

class DatadogStream(RESTStream):
    records_jsonpath = '$.data[*]'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TYPE_CONFORMANCE_LEVEL = {
            'none': TypeConformanceLevel.NONE,
            'root_only': TypeConformanceLevel.ROOT_ONLY,
            'recursive': TypeConformanceLevel.RECURSIVE,
        }.get(self.config['stream_type_conformance'])

    @property
    def url_base(self):
        return self.config['url_base']

    @property
    def authenticator(self):
        return DatadogAuthenticator(self.config['api_key'], self.config.get('application_key'))

    def parse_response(self, response):
        warnings = response.json().get('warnings', [])

        for warning in warnings:
            self.logger.warning(f"API warning: {json.dumps(warning)}", extra=warning)

        return super().parse_response(response)

    # Datadog API Rate Limit, see: https://docs.datadoghq.com/api/latest/rate-limits/
    def backoff_wait_generator(self):
        def _backoff_from_headers(retriable_api_error):
            response_headers = retriable_api_error.response.headers
            return math.ceil(float(response_headers.get('X-RateLimit-Reset', 0)))

        return self.backoff_runtime(value=_backoff_from_headers)

class DatadogPageStream(DatadogStream):
    page_size = 100

    def get_new_paginator(self):
        return PageNumberPaginator(start_value=0)

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        params['page[size]'] = self.page_size

        if next_page_token:
            params['page[number]'] = next_page_token

        return params

class DatadogCursorPaginator(BaseAPIPaginator):
    def __init__(self, max_incremental_pages=None, *args, **kwargs):
        super().__init__(start_value=None, *args, **kwargs)
        self.pages_remaining = max_incremental_pages

    def get_next(self, response):
        return next(extract_jsonpath('$.meta.page.after', response.json()), None)

    def has_more(self, response):
        # Note: This may not be a perfect indicator of number of pages actually read, but method is typically called once per page
        if self.pages_remaining is not None:
            self.pages_remaining -= 1
            if self.pages_remaining <= 0:
                return False

        return self.get_next(response) is not None

class DatadogCursorStream(DatadogStream):
    replication_key_jsonpath = None
    sort_attribute = None

    def get_new_paginator(self):
        if self.config['max_incremental_pages'] == 0:
            return DatadogCursorPaginator()
        else:
            return DatadogCursorPaginator(max_incremental_pages=self.config['max_incremental_pages'])

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        params['page[limit]'] = 1000

        if self.replication_key:
            params['filter[from]'] = self.get_starting_timestamp(context).isoformat()

        if self.sort_attribute:
            params['sort'] = self.sort_attribute

        if next_page_token:
            params['page[cursor]'] = next_page_token

        return params

    # Meltano SDK does not support nested replication keys, see: https://github.com/meltano/sdk/issues/1198
    def post_process(self, row, context):
        row = super().post_process(row, context)

        # Clone value from replication_key_jsonpath to top level as _replication_timestamp
        if self.replication_key_jsonpath:
            replication_timestamp = next(extract_jsonpath(self.replication_key_jsonpath, row), None)

            if replication_timestamp:
                # Incremental stream state only uses literal string comparison (see: https://github.com/meltano/sdk/issues/2753)
                # This doesn't work with mixed precision timestamps i.e: '2000-01-01T00:00:00.001Z' is smaller than '2000-01-01T00:00:00Z' as strings but not as timestamps
                # Reformat lower precision timestamp strings to fix state sort check
                if len(replication_timestamp) > 19 and replication_timestamp[19] != '.':
                    replication_timestamp = replication_timestamp[:19] + '.000' + replication_timestamp[19:]

                row['_replication_timestamp'] = replication_timestamp

        return row

    @property
    def is_sorted(self):
        return bool(self.sort_attribute)
