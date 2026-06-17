import math
import json

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
    replication_key_jsonpath = None
    sort_attribute = None

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

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        if self.replication_key:
            params['filter[from]'] = self.get_starting_timestamp(context).isoformat()

        if self.sort_attribute:
            params['sort'] = self.sort_attribute

        return params

    def parse_response(self, response):
        warnings = response.json().get('warnings', [])

        for warning in warnings:
            self.logger.warning(f"API warning: {json.dumps(warning)}", extra=warning)

        return super().parse_response(response)

    # Meltano SDK does not support nested replication keys, see: https://github.com/meltano/sdk/issues/1198
    def post_process(self, row, context):
        row = super().post_process(row, context)

        # Clone value from replication_key_jsonpath to top level as _replication_timestamp
        if self.replication_key_jsonpath:
            row['_replication_timestamp'] = next(extract_jsonpath(self.replication_key_jsonpath, row), None)

        return row

    # Datadog API Rate Limit, see: https://docs.datadoghq.com/api/latest/rate-limits/
    def backoff_wait_generator(self):
        def _backoff_from_headers(retriable_api_error):
            response_headers = retriable_api_error.response.headers
            return math.ceil(float(response_headers.get('X-RateLimit-Reset', 0)))

        return self.backoff_runtime(value=_backoff_from_headers)

class DatadogPageStream(DatadogStream):
    page_size = None

    def get_new_paginator(self):
        return PageNumberPaginator(start_value=0)

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        if self.page_size:
            params['page[size]'] = self.page_size

        if next_page_token:
            params['page[number]'] = next_page_token

        return params

class DatadogCursorPaginator(BaseAPIPaginator):
    def __init__(self, *args, **kwargs):
        super().__init__(start_value=None, *args, **kwargs)

    def get_next(self, response):
        return next(extract_jsonpath('$.meta.page.after', response.json()), None)

    def has_more(self, response):
        return self.get_next(response) is not None

class DatadogCursorStream(DatadogStream):
    def get_new_paginator(self):
        return DatadogCursorPaginator()

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        if next_page_token:
            params['page[cursor]'] = next_page_token

        return params
