from tap_datadog.client import DatadogPageStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/roles/list-roles/

class RolesStream(DatadogPageStream):
    name = 'roles'
    path = '/api/v2/roles'
    primary_keys = ['id']
    page_size = 100

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('created_at', DateTimeType, description="Creation time of the role.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('modified_at', DateTimeType, description="Time of last role modification.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('name', StringType, description="The name of the role. The name is neither unique nor a stable identifier of the role.", examples=["string"]),
            Property('receives_permissions_from', ArrayType(StringType), description="The managed role from which this role automatically inherits new permissions. Specify one of the following: \"Datadog Admin Role\", \"Datadog Standard Role\", or \"Datadog Read Only Role\". If empty or not specified, the role does not automatically inherit permissions from any managed role.", examples=["[]"]),
            Property('user_count', IntegerType, description="Number of users with that role.", examples=[0]),
        ), description="Attributes of the role."),
        Property('id', StringType, description="The unique identifier of the role.", examples=["string"]),
        Property('relationships', ObjectType(
            Property('permissions', ObjectType(
                Property('data', ArrayType(
                    ObjectType(
                        Property('id', StringType, description="ID of the permission.", examples=["string"]),
                        Property('type', StringType, description="Permissions resource type. Allowed enum values: permissions, default: permissions", examples=["permissions"]),
                    )
                ), description="Relationships to permission objects.")
            ), description="Relationship to multiple permissions objects."),
        ), description="Relationships of the role object returned by the API."),
        Property('type', StringType, description="Roles type. Allowed enum values: roles, default: roles", examples=["roles"]),
    ).to_dict()
