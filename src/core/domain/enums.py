from enum import StrEnum


class SortFieldEnum(StrEnum):
    ID = "id"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"


class SortOrderEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"
