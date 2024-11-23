from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Playlist(BaseModel):

    # Spotify based information
    id: str                                 # Spotify ID
    name: str                               # Name of the playlist
    description: Optional[str] = None       # Description of the playlist
    owner_id: str                           # Spotify ID of the owner
    image_url: Optional[str] = None         # URL of the playlist image
    spotify_branch: Optional[str] = None    # Spotify branch ID
    tracks: Optional[list[str]] = None      # List of Spotify track IDs
