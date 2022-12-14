from datetime import datetime
import pydantic


class BaseGetRequests(pydantic.BaseModel):
    index: int
    date: datetime
    speal_width: float | None
    speal_length: float | None
    petal_length: float | None
    petal_width: float | None
    message: str

    class Config:
        orm_mode = True
