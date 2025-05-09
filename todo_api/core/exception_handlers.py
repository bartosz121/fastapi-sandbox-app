import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from todo_api.core import exceptions as core_exceptions
from todo_api.core.service import exceptions as service_exceptions

log: structlog.BoundLogger = structlog.get_logger()


def configure(app: FastAPI) -> None:
    @app.exception_handler(ResponseValidationError)
    async def response_validation_error(
        request: Request, exc: ResponseValidationError
    ) -> JSONResponse:
        log.error(str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "msg": "Internal response validation error",
                "code": core_exceptions.Codes.RESPONSE_VALIDATION_ERROR,
            },
        )

    @app.exception_handler(core_exceptions.TodoApiError)
    async def base_error_handler(
        request: Request, exc: core_exceptions.TodoApiError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error", "code": None},
        )

    @app.exception_handler(service_exceptions.NotFoundError)
    async def service_notfound_error_handler(
        request: Request, exc: service_exceptions.NotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg": "Not found", "code": None},
        )

    @app.exception_handler(service_exceptions.ConflictError)
    async def service_conflict_error_handler(
        request: Request, exc: service_exceptions.ConflictError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"msg": "Conflict", "code": None},
        )


__all__ = ("configure",)
