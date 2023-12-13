from pydantic import BaseModel


class File(BaseModel):
    name: str
    date: float | None
