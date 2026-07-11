from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import Settings
from db.db import create_db_and_tables
from lists.routers.lists import router as lists_router
from products.routers.products import router as products_router
from shared.list_products.routers.list_products import router as list_products_router
from shared.list_shares.routers.list_shares import router as list_shares_router
from users.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(debug=Settings().DEBUG, lifespan=lifespan)

v1 = FastAPI()
v1.include_router(router=lists_router)
v1.include_router(router=list_products_router)
v1.include_router(router=list_shares_router)
v1.include_router(router=products_router)
v1.include_router(router=users_router)

app.mount("/v1", v1)


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
