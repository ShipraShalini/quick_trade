from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.response_types import APIResponse

DEFAULT_PROD_SERVER_ERROR_MESSAGE = "Internal server error while placing the order"
DEFAULT_PROD_CLIENT_ERROR_MESSAGE = "Invalid Input"


def generic_http_500_exception_handler(request: Request, exception: HTTPException) -> APIResponse:
    """
    Handle 500 Internal Server Error.

    It will return a 500 Internal Server Error response with a default error message.

    Args:
        request (Request): The FastAPI request object.
        exception (HTTPException): The exception which was raised.

    Returns:
        APIResponse: A response object which will be returned to the client.
    """
    return APIResponse(
        content=_get_content(exception),
        status_code=getattr(exception, "status_code", HTTP_500_INTERNAL_SERVER_ERROR),
        success=False,
        headers=getattr(exception, "headers", None),
    )


def request_validation_exception_handler(request: Request, exception: HTTPException) -> APIResponse:
    # content = (
    #     {"message": DEFAULT_PROD_CLIENT_ERROR_MESSAGE}
    #     if settings.ENVIRONMENT == ENV_PROD
    #     else exception.__dict__["_errors"]
    # )

    """
    Handle Request Validation Error.

    This function is an exception handler for Request Validation Errors.
    It will return a 400 Bad Request response with a default error message.

    Args:
        request (Request): The FastAPI request object.
        exception (HTTPException): The exception which was raised.

    Returns:
        APIResponse: A response object which will be returned to the client.
    """
    response = APIResponse(
        content={"message": DEFAULT_PROD_CLIENT_ERROR_MESSAGE},
        status_code=getattr(exception, "status_code", HTTP_400_BAD_REQUEST),
        success=False,
        headers=getattr(exception, "headers", None),
    )

    return response


def _get_content(exception: HTTPException) -> dict:
    """
    Return a dictionary containing an error message.

    This function is used by the exception handlers to return a default error message
    when an exception is raised. The error message is only returned if the environment is
    production. Otherwise, the full exception object is returned.

    Args:
        exception (HTTPException): The exception which was raised.

    Returns:
        dict: A dictionary containing an error message.
    """
    return {"message": DEFAULT_PROD_SERVER_ERROR_MESSAGE}
    # if settings.ENVIRONMENT == ENV_PROD:
    #     return {"message": DEFAULT_PROD_SERVER_ERROR_MESSAGE}
    # msg = getattr(exception, "detail", str(exception))
    # return getattr(exception, "error_data", None) or {"msg": msg}


def generic_http_exception_handler(request: Request, exception: HTTPException) -> APIResponse:
    """
    Handle generic HTTP exceptions.

    This function handles HTTP exceptions that do not have a specific handler.
    It creates an API response with the error details and an appropriate status code.

    Args:
        request (Request): The FastAPI request object.
        exception (HTTPException): The exception that was raised.

    Returns:
        APIResponse: A response object containing the error details.
    """
    return APIResponse(
        content=getattr(exception, "error_data", None) or {"msg": getattr(exception, "detail", str(exception))},
        status_code=getattr(exception, "status_code", HTTP_500_INTERNAL_SERVER_ERROR),
        success=False,
        headers=getattr(exception, "headers", None),
    )


EXCEPTION_HANDLERS_DICT = {
    HTTPException: generic_http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    403: generic_http_exception_handler,
    404: generic_http_exception_handler,
    500: generic_http_500_exception_handler,
    503: generic_http_exception_handler,
    550: generic_http_exception_handler,
    551: generic_http_exception_handler,
    552: generic_http_exception_handler,
    553: generic_http_exception_handler,
    554: generic_http_exception_handler,
}
