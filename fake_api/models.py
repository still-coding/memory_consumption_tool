from pydantic import BaseModel, PositiveInt
from typing import Optional
from datetime import datetime

class Alarm(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    host: str
    message: str
    value: PositiveInt
    