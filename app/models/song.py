from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime


class Song(BaseModel):
    # TODO: add more info here
    id: str
    name: str
    artists: List[str]
    
class Traits(BaseModel):
    min_acousticness: Optional[float] = None
    max_acousticness: Optional[float] = None
    target_acousticness: Optional[float] = None
    min_danceability: Optional[float] = None
    max_danceability: Optional[float] = None
    target_danceability: Optional[float] = None
    min_duration_ms: Optional[int] = None
    max_duration_ms: Optional[int] = None
    target_duration_ms: Optional[int] = None
    min_energy: Optional[float] = None
    max_energy: Optional[float] = None
    target_energy: Optional[float] = None
    min_instrumentalness: Optional[float] = None
    max_instrumentalness: Optional[float] = None
    target_instrumentalness: Optional[float] = None
    min_key: Optional[int] = None
    max_key: Optional[int] = None
    target_key: Optional[int] = None
    min_liveness: Optional[float] = None
    max_liveness: Optional[float] = None
    target_liveness: Optional[float] = None
    min_loudness: Optional[float] = None
    max_loudness: Optional[float] = None
    target_loudness: Optional[float] = None
    min_mode: Optional[int] = None
    max_mode: Optional[int] = None
    target_mode: Optional[int] = None
    min_popularity: Optional[int] = None
    max_popularity: Optional[int] = None
    target_popularity: Optional[int] = None
    min_speechiness: Optional[float] = None
    max_speechiness: Optional[float] = None
    target_speechiness: Optional[float] = None
    min_tempo: Optional[float] = None
    max_tempo: Optional[float] = None
    target_tempo: Optional[float] = None
    min_time_signature: Optional[int] = None
    max_time_signature: Optional[int] = None
    target_time_signature: Optional[int] = None
    min_valence: Optional[float] = None
    max_valence: Optional[float] = None
    target_valence: Optional[float] = None
    limit: Optional[int] = None
    market: Optional[str] = None
    genres: Optional[List[str]] = None
    seed_tracks: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "min_acousticness": None,
                "max_acousticness": 0.2,
                "target_acousticness": None,
                "min_danceability": 0.7,
                "max_danceability": None,
                "target_danceability": 0.9,
                "min_duration_ms": None,
                "max_duration_ms": None,
                "target_duration_ms": None,
                "min_energy": 0.8,
                "max_energy": None,
                "target_energy": 0.9,
                "min_instrumentalness": 0.5,
                "max_instrumentalness": None,
                "target_instrumentalness": None,
                "min_key": None,
                "max_key": None,
                "target_key": None,
                "min_liveness": None,
                "max_liveness": None,
                "target_liveness": None,
                "min_loudness": None,
                "max_loudness": None,
                "target_loudness": None,
                "min_mode": None,
                "max_mode": None,
                "target_mode": None,
                "min_popularity": None,
                "max_popularity": None,
                "target_popularity": None,
                "min_speechiness": 0.1,
                "max_speechiness": None,
                "target_speechiness": None,
                "min_tempo": 120,
                "max_tempo": None,
                "target_tempo": 140,
                "min_time_signature": None,
                "max_time_signature": None,
                "target_time_signature": None,
                "min_valence": 0.7,
                "max_valence": None,
                "target_valence": 0.9,
                "limit": 3,
                "market": "US",
                "genres": ["country", "pop"]
            }
        }
