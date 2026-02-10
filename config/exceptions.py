"""
Custom exception handler for consistent API responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """Return consistent JSON error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc) if str(exc) else 'An error occurred',
                'code': response.status_code,
                'details': response.data,
            },
            'data': None,
        }
        response.data = custom_response_data

    return response
