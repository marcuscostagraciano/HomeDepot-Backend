import uvicorn
from fastapi import FastAPI
from dotenv import dotenv_values
from db.db import create_db_and_tables
from contextlib import asynccontextmanager

from routers import lists, products

config = dotenv_values(".env")

DEBUG = config.get("DEBUG", "False").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(debug=DEBUG, lifespan=lifespan)

app.include_router(lists.router)
app.include_router(products.router)


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
