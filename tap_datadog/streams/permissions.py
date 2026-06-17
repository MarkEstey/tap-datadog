from tap_datadog.client import DatadogStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/roles/list-permissions/

class PermissionsStream(DatadogStream):
    name = 'permissions'
    path = '/api/v2/permissions'
    primary_keys = ['id']

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('created', DateTimeType, description="Creation time of the permission.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('description', StringType, description="Description of the permission.", examples=["string"]),
            Property('display_name', StringType, description="Displayed name for the permission.", examples=["string"]),
            Property('display_type', StringType, description="Display type.", examples=["string"]),
            Property('group_name', StringType, description="Name of the permission group.", examples=["string"]),
            Property('name', StringType, description="Name of the permission.", examples=["string"]),
            Property('name_aliases', ArrayType(StringType), description="List of alias names for the permission.", examples=["[]"]),
            Property('restricted', BooleanType, description="Whether or not the permission is restricted.", examples=[False]),
        ), description="Attributes of a permission."),
        Property('id', StringType, description="ID of the permission.", examples=["string"]),
        Property('type', StringType, description="Permissions resource type. Allowed enum values: permissions, default: permissions", examples=["permissions"]),
    ).to_dict()
