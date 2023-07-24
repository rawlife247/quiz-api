from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def user_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a list of users."
    )


def user_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a new user."
    )


def user_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a specific user.",
    )


def user_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a specific user.",
    )


def user_destroy_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a specific user.",
        responses={204: openapi.Response(
            description="User has been deleted.",
            examples={
                'application/json': {
                    'message': '"User with name {instance.username} has been deleted."',
                },
            },
        )}
    )


def user_log_in_swagger_schema():
    return swagger_auto_schema(
        operation_description="Authenticate user and obtain authentication token.",
        responses={
            200: openapi.Response(
                description="Authentication successful.",
                examples={
                    'application/json': {
                        'token': 'token'
                    },
                }
            ),
            400: openapi.Response(
                description="Invalid credentials provided.",
                examples={
                    'application/json': {
                        'non_field_errors': [
                            "Unable to log in with provided credentials."
                        ]
                    }
                }
            ),
        }
    )


def user_log_out_swagger_schema():
    return swagger_auto_schema(
        operation_description="Logout user and delete token.",
        responses={200: openapi.Response(
            description="Logged out successfully.", examples={
                'application/json': {
                    'detail': 'Logged out successfully.'
                },
            },
        )}
    )


def verify_token_swagger_schema():
    return swagger_auto_schema(
        operation_description="Provide token in header to verify user.",
        responses={
            200: openapi.Response(
                description="User data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                            }
                        )
                    }
                ),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided or invalid."
            )
        }
    )


def forgot_password_swagger_schema():
    return swagger_auto_schema(
        operation_description="Initiate password reset.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL)
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset link will be sent to email",
                examples={
                    'application/json': {
                        'message': 'Reset link is sent to your email'
                    },
                }
            ),
            400: openapi.Response(description="Bad request"),
            500: openapi.Response(description="Internal server error")
        }
    )


def forgot_password_confirm_swagger_schema():
    return swagger_auto_schema(
        operation_description="Confirm password reset.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['password', 'confirm_password'],
            properties={
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD
                ),
                'confirm_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
        responses={
            200: openapi.Response(description="Password reset successful."),
            400: openapi.Response(description="Bad request"),
        }
    )
