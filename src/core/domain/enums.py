from enum import StrEnum


class SortField(StrEnum):
    ID = "id"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
