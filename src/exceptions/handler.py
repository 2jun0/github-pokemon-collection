from logging import getLogger

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler

from src.exceptions.common import (
    BadRequestError,
    CommonException,
    InternalServerError,
    NotFoundError,
    ServiceUnavailableError,
)
from src.exceptions.error_codes import ErrorCode

# INFO
"""
[🔵INFO: ERROR_CODE_NAME] - (POST /info)

"""

# WARN
"""
[🟠WARN: ERROR_CODE_NAME] - (POST /warn)
... error traceback ...
"""

# ERROR
"""
[🔴ERROR] - (POST /error)
... error traceback ...
"""

logger = getLogger("error logger")
LOG_FORMAT_INFO = "\n[🔵INFO: %s] - (%s %s)\n%s\n %s: %s"
LOG_FORMAT_WARN = "\n[🟠WARN: %s] - (%s %s)"
LOG_FORMAT_ERROR = "\n[🔴ERROR: %s] - (%s %s)"


def _log_info(e: CommonException, request: Request):
    logger.info(LOG_FORMAT_INFO, request.method, request.url, e.error_code.name, e.__class__, e.detail)


def _log_warn(e: Exception, request: Request):
    logger.warning(LOG_FORMAT_WARN, request.method, request.url, e)


def _log_error(e: Exception, request: Request):
    logger.error(LOG_FORMAT_ERROR, request.method, request.url, e)


def install_exception_handlers(app: FastAPI):

    @app.exception_handler(BadRequestError)
    async def handle_bad_request_error(request: Request, error: BadRequestError):
        _log_info(error, request)
        http_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail)
        return await http_exception_handler(request, http_exception)

    @app.exception_handler(NotFoundError)
    async def handle_not_found_error(request: Request, error: NotFoundError):
        _log_info(error, request)
        http_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.detail)
        return await http_exception_handler(request, http_exception)

    @app.exception_handler(InternalServerError)
    async def handle_internal_server_error(request: Request, error: InternalServerError):
        _log_error(error, request)
        http_exception = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error.detail)
        return await http_exception_handler(request, http_exception)

    @app.exception_handler(ServiceUnavailableError)
    async def handle_service_unavailable_error(request: Request, error: ServiceUnavailableError):
        _log_warn(error, request)
        http_exception = HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=error.detail)
        return await http_exception_handler(request, http_exception)

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, error: Exception):
        _log_error(error, request)
        http_exception = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorCode.INTERNAL_SERVER_ERROR.detail
        )
        return await http_exception_handler(request, http_exception)
