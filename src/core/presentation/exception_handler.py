from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..domain.errors import BaseError, InvalidFieldError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseError)
    async def base_error_handler(  # type: ignore
        request: Request,
        err: BaseError,
    ):
        return JSONResponse(
            status_code=err.http_status_code,
            content={"details": err.message},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(  # type: ignore
        request: Request,
        err: RequestValidationError,
    ):
        ORIGINS = {"body", "query", "path", "header", "cookie"}

        error = err.errors()[0]

        field = ".".join(str(x) for x in error["loc"] if x not in ORIGINS)
        message = (
            error["ctx"]["reason"]
            if "ctx" in error and "reason" in error["ctx"]
            else error["msg"]
        )

        domain_error = InvalidFieldError(
            field_name=field,
            message=message,
        )

        return JSONResponse(
            status_code=domain_error.http_status_code,
            content={
                "field": domain_error.field_name,
                "details": domain_error.message,
            },
        )
