from contextlib import asynccontextmanager

import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI

from db.db import create_db_and_tables
from lists import router as lists_router
from products import router as products_router
from users import router as users_router

config = dotenv_values(".env")

DEBUG = config.get("DEBUG", "False").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(debug=DEBUG, lifespan=lifespan)

# app.include_router(lists_router)
app.include_router(router=products_router)
app.include_router(router=users_router)


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
