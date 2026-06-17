from tap_datadog.client import DatadogStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/rum/list-all-the-rum-applications/

class RumApplicationsStream(DatadogStream):
    name = 'rum_applications'
    path = '/api/v2/rum/applications'
    primary_keys = ['id']

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('application_id', StringType, description="ID of the RUM application.", examples=["abcd1234-0000-0000-abcd-1234abcd5678"]),
            Property('created_at', IntegerType, description="Timestamp in ms of the creation date.", examples=[1659479836169]),
            Property('created_by_handle ', StringType, description="Handle of the creator user.", examples=["john.doe"]),
            Property('hash', StringType, description="Hash of the RUM application. Optional.", examples=["string"]),
            Property('is_active', BooleanType, description="Indicates if the RUM application is active.", examples=[True]),
            Property('name', StringType, description="Name of the RUM application.", examples=["my_rum_application"]),
            Property('org_id', IntegerType, description="Org ID of the RUM application.", examples=[999]),
            Property('product_scales', ObjectType(
                Property('product_analytics_retention_scale', ObjectType(
                    Property('last_modified_at', IntegerType, description="Timestamp in milliseconds when this scale was last modified.", examples=[1747922145974]),
                    Property('state', StringType, description="Controls the retention policy for Product Analytics data derived from RUM events. Allowed enum values: MAX,NONE", examples=["MAX"]),
                ), description="Product Analytics retention scale configuration."),
                Property('rum_event_processing_scale', ObjectType(
                    Property('last_modified_at', IntegerType, description="Timestamp in milliseconds when this scale was last modified.", examples=[1721897494108]),
                    Property('state', StringType, description="Configures which RUM events are processed and stored for the application. Allowed enum values: ALL,ERROR_FOCUSED_MODE,NONE", examples=["ALL"]),
                ), description="RUM event processing scale configuration."),
            ), description="Product Scales configuration for the RUM application."),
            Property('type', StringType, description="Type of the RUM application. Supported values are browser, ios, android, react-native, flutter, roku, electron, unity, kotlin-multiplatform.", examples=["browser"]),
            Property('updated_at', IntegerType, description="Timestamp in ms of the last update date.", examples=[1659479836169]),
            Property('updated_by_handle', StringType, description="Handle of the updater user.", examples=["jane.doe"]),
        ), description="RUM application list attributes."),
        Property('id', StringType, description="RUM application ID.", examples=["abcd1234-0000-0000-abcd-1234abcd5678"]),
        Property('type', StringType, description="RUM application list type. Allowed enum values: rum_application, default: rum_application", examples=["rum_application"]),
    ).to_dict()
