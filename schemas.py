from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class FeedbackIn(BaseModel):
    service_name: str
    tag: str
    data: str

class Feedback(BaseModel):
    id: int
    service_name: str
    tag: str
    created_at: Optional[datetime] 
    data: str
   