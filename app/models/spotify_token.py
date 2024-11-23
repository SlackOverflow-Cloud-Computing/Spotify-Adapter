from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class SpotifyToken(BaseModel):
    access_token: str
    token_type: str
    scope: str
    expires_in: int  # num seconds
    refresh_token: str
