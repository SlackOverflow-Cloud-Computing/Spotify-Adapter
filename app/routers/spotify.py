from fastapi import APIRouter, status, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.models.song import Song, Traits
from app.services.service_factory import ServiceFactory
import dotenv
import os


dotenv.load_dotenv()
redirect_uri = os.getenv('REDIRECT_URI')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class LoginRequest(BaseModel):
    auth_code: str


class LoginResponse(BaseModel):
    user: User
    token: SpotifyToken

class CreatePlaylistRequest(BaseModel):
    token: SpotifyToken
    name: str
    song_ids: List[str]


@router.post("/auth/login", tags=["users"], status_code=status.HTTP_201_CREATED)
async def login(request: LoginRequest) -> LoginResponse:
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    token = api_service.login(request.auth_code, redirect_uri)
    user = api_service.get_user_info(token)
    return LoginResponse(user=user, token=token)


@router.get("/users/{user_id}/playlists", tags=["users", "playlists"])
async def get_user_playlists(user_id: str, spotify_token: SpotifyToken, token: str = Depends(oauth2_scheme)):
    api_service = ServiceFactory.get_service("SpotifyAPIService")

    if not api_service.validate_token(token, id=user_id, scope=("/users/{user_id}/playlists", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    return api_service.get_user_playlists(spotify_token)

@router.post("/users/{user_id}/playlists", tags=["playlists"])
async def create_playlist(user_id: str, request: CreatePlaylistRequest, token: str = Depends(oauth2_scheme)):
    api_service = ServiceFactory.get_service("SpotifyAPIService")

    if not api_service.validate_token(token, id=user_id, scope=("/users/{user_id}/playlists", "POST")):
        raise HTTPException(status_code=401, detail="Invalid Token")

    api_service.create_playlist(user_id, request.token, request.name, request.song_ids)

@router.get("/users/{user_id}/refreshed_token", tags=["users"])
async def get_refreshed_token(user_id: str,
                              access_token: str,
                              token_type: str,
                              scope: str,
                              expires_in: int,
                              refresh_token: str,
                              token: str = Depends(oauth2_scheme)):
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    spotify_token = SpotifyToken(access_token=access_token, token_type=token_type,
                                 scope=scope, expires_in=expires_in, refresh_token=refresh_token)

    if not api_service.validate_token(token, scope=("/users/{user_id}/refreshed_token", "GET")):
        raise HTTPException(status_code=401, detail="Invalid Token")
    return api_service.refresh_token(spotify_token)


@router.get("/recommendations", tags=["recommendations"], status_code=status.HTTP_200_OK)
async def get_recommendations(  # TODO: better way to do this? dont want to use a payload because it is a get request
    min_acousticness: Optional[float] = None,
    max_acousticness: Optional[float] = None,
    target_acousticness: Optional[float] = None,
    min_danceability: Optional[float] = None,
    max_danceability: Optional[float] = None,
    target_danceability: Optional[float] = None,
    min_duration_ms: Optional[int] = None,
    max_duration_ms: Optional[int] = None,
    target_duration_ms: Optional[int] = None,
    min_energy: Optional[float] = None,
    max_energy: Optional[float] = None,
    target_energy: Optional[float] = None,
    min_instrumentalness: Optional[float] = None,
    max_instrumentalness: Optional[float] = None,
    target_instrumentalness: Optional[float] = None,
    min_key: Optional[int] = None,
    max_key: Optional[int] = None,
    target_key: Optional[int] = None,
    min_liveness: Optional[float] = None,
    max_liveness: Optional[float] = None,
    target_liveness: Optional[float] = None,
    min_loudness: Optional[float] = None,
    max_loudness: Optional[float] = None,
    target_loudness: Optional[float] = None,
    min_mode: Optional[int] = None,
    max_mode: Optional[int] = None,
    target_mode: Optional[int] = None,
    min_popularity: Optional[int] = None,
    max_popularity: Optional[int] = None,
    target_popularity: Optional[int] = None,
    min_speechiness: Optional[float] = None,
    max_speechiness: Optional[float] = None,
    target_speechiness: Optional[float] = None,
    min_tempo: Optional[float] = None,
    max_tempo: Optional[float] = None,
    target_tempo: Optional[float] = None,
    min_time_signature: Optional[int] = None,
    max_time_signature: Optional[int] = None,
    target_time_signature: Optional[int] = None,
    min_valence: Optional[float] = None,
    max_valence: Optional[float] = None,
    target_valence: Optional[float] = None,
    limit: Optional[int] = None,
    market: Optional[str] = None,
    genres: Optional[List[str]] = Query(default=None),
    seed_tracks: Optional[List[str]] = None,
    token: str = Depends(oauth2_scheme),
    spotify_access_token: str = None
) -> List[Song]:
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    traits = Traits(
        min_acousticness=min_acousticness,
        max_acousticness=max_acousticness,
        target_acousticness=target_acousticness,
        min_danceability=min_danceability,
        max_danceability=max_danceability,
        target_danceability=target_danceability,
        min_duration_ms=min_duration_ms,
        max_duration_ms=max_duration_ms,
        target_duration_ms=target_duration_ms,
        min_energy=min_energy,
        max_energy=max_energy,
        target_energy=target_energy,
        min_instrumentalness=min_instrumentalness,
        max_instrumentalness=max_instrumentalness,
        target_instrumentalness=target_instrumentalness,
        min_key=min_key,
        max_key=max_key,
        target_key=target_key,
        min_liveness=min_liveness,
        max_liveness=max_liveness,
        target_liveness=target_liveness,
        min_loudness=min_loudness,
        max_loudness=max_loudness,
        target_loudness=target_loudness,
        min_mode=min_mode,
        max_mode=max_mode,
        target_mode=target_mode,
        min_popularity=min_popularity,
        max_popularity=max_popularity,
        target_popularity=target_popularity,
        min_speechiness=min_speechiness,
        max_speechiness=max_speechiness,
        target_speechiness=target_speechiness,
        min_tempo=min_tempo,
        max_tempo=max_tempo,
        target_tempo=target_tempo,
        min_time_signature=min_time_signature,
        max_time_signature=max_time_signature,
        target_time_signature=target_time_signature,
        min_valence=min_valence,
        max_valence=max_valence,
        target_valence=target_valence,
        limit=limit,
        market=market,
        genres=genres,
        seed_tracks=seed_tracks
    )
    try:
        if not api_service.validate_token(token, scope=("/recommendations", "GET")):
            raise HTTPException(status_code=401, detail="Invalid Token")
        return api_service.get_recommendations(traits, spotify_access_token)
    except Exception as e:
        # raise nested exception instead of generic 500
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
