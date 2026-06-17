from tap_datadog.client import DatadogPageStream
from singer_sdk.typing import *

# API Reference: https://docs.datadoghq.com/api/latest/users/list-all-users/

class UsersStream(DatadogPageStream):
    name = 'users'
    path = '/api/v2/users'
    primary_keys = ['id']
    page_size = 1000

    schema = PropertiesList(
        Property('attributes', ObjectType(
            Property('created_at', DateTimeType, description="The ISO 8601 timestamp of when the user account was created.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('disabled', BooleanType, description="Whether the user account is deactivated. Disabled users cannot log in.", examples=[False]),
            Property('email', StringType, description="The email address of the user, used for login and notifications.", examples=["string"]),
            Property('handle', StringType, description="The unique handle (username) of the user, typically matching their email prefix.", examples=["string"]),
            Property('icon', StringType, description="URL of the user's profile icon, typically a Gravatar URL derived from the email address.", examples=["string"]),
            Property('last_login_time', DateTimeType, description="The ISO 8601 timestamp of the user's most recent login, or null if the user has never logged in.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('mfa_enabled', BooleanType, description="Whether multi-factor authentication (MFA) is enabled for the user's account.", examples=[False]),
            Property('modified_at', DateTimeType, description="The ISO 8601 timestamp of when the user account was last modified.", examples=["2019-09-19T10:00:00.000Z"]),
            Property('name', StringType, description="The full display name of the user as shown in the Datadog UI.", examples=["string"]),
            Property('service_account', BooleanType, description="Whether this is a service account rather than a human user. Service accounts are used for programmatic API access.", examples=[False]),
            Property('status', StringType, description="The current status of the user account (for example, Active, Pending, or Disabled).", examples=["string"]),
            Property('title', StringType, description="The job title of the user (for example, \"Senior Engineer\" or \"Product Manager\").", examples=["string"]),
            Property('uuid', StringType, description="The globally unique identifier (UUID) of the user.", examples=["string"]),
            Property('verified', BooleanType, description="Whether the user's email address has been verified.", examples=[False]),
        ), description="Attributes of user object returned by the API."),
        Property('id', StringType, description="ID of the user.", examples=["string"]),
        Property('relationships', ObjectType(
            Property('org', ObjectType(
                Property('data', ObjectType(
                    Property('id', StringType, description="ID of the organization.", examples=["00000000-0000-beef-0000-000000000000"]),
                    Property('type', StringType, description="Organizations resource type. Allowed enum values: orgs, default: orgs", examples=["orgs"]),
                ), description="Relationship to organization object."),
            ), description="Relationship to an organization."),
            Property('other_orgs', ObjectType(
                Property('data', ArrayType(
                    ObjectType(
                        Property('id', StringType, description="ID of the organization.", examples=["00000000-0000-beef-0000-000000000000"]),
                        Property('type', StringType, description="Organizations resource type. Allowed enum values: orgs, default: orgs", examples=["orgs"]),
                    )
                ), description="Relationships to organization objects."),
            ), description="Relationship to organizations."),
            Property('other_users', ObjectType(
                Property('data', ArrayType(
                    ObjectType(
                        Property('id', StringType, description="A unique identifier that represents the user.", examples=["00000000-0000-0000-2345-000000000000"]),
                        Property('type', StringType, description="Users resource type. Allowed enum values: users, default: users", examples=["users"]),
                    )
                ), description="Relationships to user objects."),
            ), description="Relationship to users."),
            Property('roles', ObjectType(
                Property('data', ArrayType(
                    ObjectType(
                        Property('id', StringType, description="The unique identifier of the role.", examples=["3653d3c6-0c75-11ea-ad28-fb5701eabc7d"]),
                        Property('type', StringType, description="Roles type. Allowed enum values: roles, default: roles", examples=["roles"]),
                    )
                ), description="An array containing type and the unique identifier of a role."),
            ), description="Relationship to roles."),
        ), description="Relationships of the user object returned by the API."),
        Property('type', StringType, description="Users resource type. Allowed enum values: users, default: users", examples=["users"]),
    ).to_dict()
