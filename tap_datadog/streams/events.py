from tap_datadog.client import DatadogCursorStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/rum/get-a-list-of-rum-events/

class EventsStream(DatadogCursorStream):
    name = 'events'
    path = '/api/v2/events'
    primary_keys = ['id']
    replication_key = '_replication_timestamp'
    replication_key_jsonpath = '$.attributes.timestamp'
    sort_attribute = 'timestamp'

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('attributes', ObjectType(
                Property('aggregation_key', StringType, description="Aggregation key of the event."),
                Property('date_happened', IntegerType, description="POSIX timestamp of the event. Must be sent as an integer (no quotation marks). Limited to events no older than 18 hours."),
                Property('device_name', StringType, description="A device name."),
                Property('duration', IntegerType, description="The duration between the triggering of the event and its recovery in nanoseconds."),
                Property('event_object', StringType, description="The event title."),
                Property('evt', ObjectType(
                    Property('id', StringType, description="Event ID."),
                    Property('name', StringType, description="The event name."),
                    Property('source_id', IntegerType, description="Event source ID."),
                    Property('type', StringType, description="Event type."),
                ), description="The metadata associated with a request."),
                Property('hostname', StringType, description="Host name to associate with the event. Any tags associated with the host are also applied to this event."),
                Property('monitor', ObjectType(
                    Property('created_at', IntegerType, description="The POSIX timestamp of the monitor's creation in nanoseconds."),
                    Property('group_status', IntegerType, description="Monitor group status used when there is no result_groups."),
                    Property('groups', ArrayType(StringType), description="Groups to which the monitor belongs."),
                    Property('id', IntegerType, description="The monitor ID."),
                    Property('message', StringType, description="The monitor message."),
                    Property('modified', IntegerType, description="The monitor's last-modified timestamp."),
                    Property('name', StringType, description="The monitor name."),
                    Property('query', StringType, description="The query that triggers the alert."),
                    Property('tags', ArrayType(StringType), description="A list of tags attached to the monitor."),
                    Property('templated_name', StringType, description="The templated name of the monitor before resolving any template variables."),
                    Property('type', StringType, description="The monitor type."),
                ), description="Attributes from the monitor that triggered the event."),
                Property('monitor_groups', ArrayType(StringType), description="List of groups referred to in the event."),
                Property('monitor_id', IntegerType, description="ID of the monitor that triggered the event. When an event isn't related to a monitor, this field is empty."),
                Property('priority', StringType, description="The priority of the event's monitor. For example, normal or low. Allowed enum values: normal, low"),
                Property('related_event_id', IntegerType, description="Related event ID."),
                Property('service', StringType, description="Service that triggered the event."),
                Property('source_type_name', StringType, description="The type of event being posted. For example, nagios, hudson, jenkins, my_apps, chef, puppet, git or bitbucket. The list of standard source attribute values is available [here](https://docs.datadoghq.com/integrations/faq/list-of-api-source-attribute-value)."),
                Property('sourcecategory', StringType, description="Identifier for the source of the event, such as a monitor alert, an externally-submitted event, or an integration."),
                Property('status', StringType, description="If an alert event is enabled, its status is one of the following: failure, error, warning, info, success, user_update, recommendation, or snapshot. Allowed enum values: failure, error, warning, info, success, user_update, recommendation, snapshot"),
                Property('tags', ArrayType(StringType), description="A list of tags to apply to the event."),
                Property('timestamp', IntegerType, description="POSIX timestamp of your event in milliseconds."),
                Property('title', StringType, description="The event title."),
            ), description="Object description of attributes from your event."),
            Property('message', StringType, description="The message of the event."),
            Property('tags', ArrayType(StringType), description="An array of tags associated with the event."),
            Property('timestamp', DateTimeType, description="The timestamp of the event."),
        ), description="The object description of an event response attribute."),
        Property('id', StringType, description="The unique ID of the event."),
        Property('type', StringType, description="Type of the event. Allowed enum values: event, default: event"),
        Property('_replication_timestamp', DateTimeType, description="Replication timestamp for internal use (same as attributes.timestamp)"),
    ).to_dict()
