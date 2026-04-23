from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List
from math import ceil

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total_records: int
    total_pages: int
    current_page: int
    data: List[T]

def paginate(query, page: int, limit: int):
    total_records = query.count()
    total_pages = ceil(total_records / limit) if total_records > 0 else 1
    data = query.offset((page - 1) * limit).limit(limit).all()
    return {
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "data": data
    }
