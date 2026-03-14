from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema used by the other `schemas` in the project.

    Inherently supports conversion from SQLAlchemy ORM models to Pydantic models, making it easier to work with
    database records in endpoints.
    """

    model_config = ConfigDict(from_attributes=True)
