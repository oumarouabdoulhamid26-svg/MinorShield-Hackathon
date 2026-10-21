
# app/schemas/history.py

from pydantic import BaseModel
from typing import Optional


class DetectionItem(BaseModel):
    id            : int
    request_id    : str
    nsfw_score    : float
    image_score   : float
    text_score    : float
    label         : str
    category      : Optional[str] = None
    extracted_text: Optional[str]
    app_package   : Optional[str]
    app_name      : Optional[str] = None
    timestamp     : str

    class Config:
        from_attributes = True


class DetectionHistoryResponse(BaseModel):
    child_id  : str
    child_name: str
    detections: list[DetectionItem]
    total     : int
    page      : int
    page_size : int
