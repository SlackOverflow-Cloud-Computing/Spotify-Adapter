from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):

    # Spotify based information
    id: str                                 # Spotify ID
    username: str                           # Spotify username (display_name)
    email: str                              # Spotify email
    profile_image: Optional[str] = None     # Spotify profile image URL
    country: Optional[str] = None           # Spotify country

    # Our own information
    jwt: Optional[str] = None               # JWT token
    created_at: Optional[datetime] = None   # Date format as string
    last_login: Optional[datetime] = None   # Date format as string
