import os
import requests
import base64
from typing import Optional, List

import jwt
from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.models.playlist import Playlist

JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

class SpotifyAPIService:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def validate_token(self, token: str) -> bool:
        """Validate a JWT token."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            return True
        except jwt.JWTError:
            return False

    def login(self, auth_code, redirect_uri) -> SpotifyToken:
        url = "https://accounts.spotify.com/api/token"

        # Prepare the authorization header (Base64 encoded client_id:client_secret)
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        # Prepare the POST data for the token request
        token_data = {
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Send a POST request to Spotify to exchange the authorization code for tokens
        try:
            response = requests.post(url, data=token_data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to retrieve token")

            data = response.json()
            # print(f"Login Response: {data}")
            token = SpotifyToken.parse_obj(data)
            return token

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching token: {str(e)}")


    def refresh_token(self, token: SpotifyToken) -> SpotifyToken:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token,
        }

        try:
            response = requests.post(url, data=data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")

            return SpotifyToken.parse_obj(response.json())

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error refreshing token: {str(e)}")

    def get_user_info(self, token: SpotifyToken) -> User:
        url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {token.access_token}"
        }

        # Send a GET request to the Spotify API
        try:
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code != 200:
                raise Exception(f"Failed to fetch user info: {response.status_code} - {response.text}")

            # Parse the JSON response
            user_data = response.json()

            # Map the relevant fields to your User model
            user = User(
                id=user_data.get("id"),
                username=user_data.get("display_name"),
                email=user_data.get("email"),
                country=user_data.get("country"),
                profile_image=user_data.get("images")[0].get("url") if user_data.get("images") else None,
                created_at=None,
                last_login=None
            )

            return user

        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching user info: {str(e)}")


    def get_user_playlists(self, token: SpotifyToken) -> List[Playlist]:
        url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {token.access_token}"
        }

        # Send a GET request to the Spotify API
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch user playlists: {response.status_code} - {response.text}")

            # Parse the JSON response
            playlists = []
            items = response.json().get("items")
            for item in items:
                playlist = Playlist.parse_obj(item)
                track_info = requests.get(item.get("tracks").get("href"), headers=headers)
                print(track_info)
                # TODO: Insert tracks into playlist object

            # playlists = [Playlist(
            #     id = playlist.get("id"),
            #     name = playlist.get("name"),
            #     descrption = playlist.get("description"),
            #     owner_id = playlist.get("owner").get("id"),
            #     image_url = playlist.get("images")[0].get("url") if playlist.get("images") else None,
            #     tracks = None
            # ) for playlist in playlists]

            return playlists

        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching user playlists: {str(e)}")
