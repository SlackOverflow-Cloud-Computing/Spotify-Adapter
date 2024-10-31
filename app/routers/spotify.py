from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from app.models.user import User
from app.models.token import Token
from app.services.service_factory import ServiceFactory
import dotenv, os

dotenv.load_dotenv()
redirect_uri = os.getenv('REDIRECT_URI')

router = APIRouter()

class LoginRequest(BaseModel):
    auth_code: str

class LoginResponse(BaseModel):
    user: User
    token: Token


@router.post("/login", tags=["users"], status_code=status.HTTP_201_CREATED)
async def login(request: LoginRequest) -> LoginResponse:
    api_service = ServiceFactory.get_service("SpotifyAPIService")
    token = api_service.login(request.auth_code, redirect_uri)
    user = api_service.get_user_info(token)
    return LoginResponse(user=user, token=token)
