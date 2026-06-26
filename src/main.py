from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.utils import get_dotenv_config
from db.db import create_db_and_tables
from lists import router as lists_router
from products import router as products_router
from users import router as users_router

DEBUG = get_dotenv_config("DEBUG", "False").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(debug=DEBUG, lifespan=lifespan)

app.include_router(router=lists_router)
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
