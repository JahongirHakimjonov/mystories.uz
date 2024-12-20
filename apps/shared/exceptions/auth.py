from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    MethodNotAllowed,
)
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response.data = {"success": False, "detail": "Credentials were not provided."}

    elif isinstance(exc, NotAuthenticated):
        response.data = {
            "success": False,
            "detail": "You do not have permission to perform this action.",
        }

    elif isinstance(exc, MethodNotAllowed):
        response.data = {"success": False, "detail": "Method not allowed."}

    return response
