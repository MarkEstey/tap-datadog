from tap_datadog.client import DatadogCursorStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/rum/get-a-list-of-rum-events/

class RumEventsStream(DatadogCursorStream):
    name = 'rum_events'
    path = '/api/v2/rum/events'
    primary_keys = ['id']
    replication_key = '_replication_timestamp'
    replication_key_jsonpath = '$.attributes.timestamp'
    sort_attribute = 'timestamp'

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('attributes', ObjectType(), description="JSON object of attributes from RUM events."),
            Property('service', StringType, description="The name of the application or service generating RUM events. It is used to switch from RUM to APM, so make sure you define the same value when you use both products."),
            Property('tags', ArrayType(StringType), description="Array of tags associated with your event."),
            Property('timestamp', DateTimeType, description="Timestamp of your event."),
        ), description="JSON object containing all event attributes and their associated values."),
        Property('id', StringType, description="Unique ID of the event."),
        Property('type', StringType, description="Type of the event. Allowed enum values: rum, default: rum"),
        Property('_replication_timestamp', DateTimeType, description="Replication timestamp for internal use (same as attributes.timestamp)"),
    ).to_dict()
