from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Union

from pydantic import BaseModel, Field


class ResponseTypes(str, Enum):
    TYPE_1 = "ERROR"
    TYPE_2 = "SUCCESS"


class StatusMessage(BaseModel):
    text: str = Field(..., description="Status message text")
