from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from core.config import Settings
from db.db import create_db_and_tables
from lists.routers import router as lists_router
from products.routers import router as products_router
from security.routers import router as security_router
from users.routers import router as users_router


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    for path in schema["paths"].values():
        for operation in path.values():
            operation.get("responses", {}).pop("422", None)

    app.openapi_schema = schema
    return schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(debug=Settings().DEBUG, lifespan=lifespan)

app.include_router(router=lists_router)
app.include_router(router=products_router)
app.include_router(router=users_router)
app.include_router(router=security_router)
app.openapi = custom_openapi


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
