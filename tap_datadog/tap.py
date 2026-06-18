from singer_sdk import Tap
from singer_sdk.typing import *
from tap_datadog.streams import *

class TapDatadog(Tap):
    name = 'tap-datadog'

    config_jsonschema = PropertiesList(
        Property('url_base', StringType, default='https://api.datadoghq.com', description='Base url for the Datadog API. Default: https://api.datadoghq.com'),
        Property('api_key', StringType, required=True, secret=True, description='API key (see: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys)'),
        Property('application_key', StringType, secret=True, description='Application key (see: https://docs.datadoghq.com/account_management/api-app-keys/#application-keys)'),
        Property('max_incremental_pages', IntegerType, default=2, description='Maximum number of pages to read from incremental endpoints in a single sync. Default: 0 (unlimited)'),
        Property('start_date', DateTimeType, default='2010-01-01T00:00:00Z', description='The earliest record date to sync'),
        Property(
            'stream_type_conformance',
            StringType,
            allowed_values=['none', 'root_only', 'recursive'],
            default='root_only',
            description='The level of type conformance to apply to streams '
                '(see: https://sdk.meltano.com/en/latest/classes/singer_sdk.Stream.html#singer_sdk.Stream.TYPE_CONFORMANCE_LEVEL). '
                'Defaults to root_only. Must be one of: none, root_only, recursive',
        ),
        Property('stream_maps', ObjectType(), description='Inline stream maps (see: https://sdk.meltano.com/en/latest/stream_maps.html)'),
        Property('stream_map_config', ObjectType(), description='Inline stream maps config (see: https://sdk.meltano.com/en/latest/stream_maps.html)'),
    ).to_dict()

    def discover_streams(self):
        return [
            EventsStream(self),
            PermissionsStream(self),
            RolesStream(self),
            RumApplicationsStream(self),
            RumEventsStream(self),
            UsersStream(self),
        ]

if __name__ == '__main__':
    TapDatadog.cli()
