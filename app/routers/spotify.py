from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.services.service_factory import ServiceFactory
import dotenv, os


dotenv.load_dotenv()
redirect_uri = os.getenv('REDIRECT_URI')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class LoginRequest(BaseModel):
    auth_code: str

class LoginResponse(BaseModel):
    user: User
    token: SpotifyToken


@router.post("/login", tags=["users"], status_code=status.HTTP_201_CREATED)
async def login(request: LoginRequest) -> LoginResponse:
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    token = api_service.login(request.auth_code, redirect_uri)
    user = api_service.get_user_info(token)
    return LoginResponse(user=user, token=token)


@router.get("user/{user_id}/playlists", tags=["users", "playlists"])
async def get_user_playlists(user_id: str, spotify_token: SpotifyToken, token: str = Depends(oauth2_scheme)):
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    if user_id != spotify_token.user_id:
        raise HTTPException(status_code=403, detail="User does not have access to this resource")
    elif not api_service.validate_token():
        raise HTTPException(status_code=401, detail="Invalid Token")

    return api_service.get_user_playlists(spotify_token)
