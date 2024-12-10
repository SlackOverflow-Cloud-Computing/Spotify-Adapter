import os
import requests
import base64
from typing import Optional, List

import jwt
from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError
import dotenv

from app.models.user import User
from app.models.spotify_token import SpotifyToken
from app.models.playlist import Playlist
from app.models.song import Song, Traits

dotenv.load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

class SpotifyAPIService:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def validate_token(self, token: str, id: Optional[str]=None, scope: Optional[tuple[str, str]]=None) -> bool:
        """Validate a JWT token.

        Optionally checks if the token's user ID matches the given ID, and
        if the token has the required scope for the endpoint.
        Scope is of the form ("/endpoint", "METHOD").
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            if id is not None and payload.get("sub") != id:
                return False
            if scope is not None and scope[1] not in payload.get("scopes").get(scope[0]):
                return False
            return True

        except jwt.exceptions.InvalidTokenError:
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
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_header}"
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token,
        }

        try:
            response = requests.post(url, data=data, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")

            response = response.json()
            response["refresh_token"] = token.refresh_token
            return SpotifyToken.parse_obj(response)

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

    def get_recommendations(self, traits: Traits, spotify_access_token: str) -> List[Song]:
        # Unfortunately, Spotify just decided to remove the recommendations endpoint from their API. So we have to use this workaround:
        url = "https://api.spotify.com/v1/search?"
        headers = {
            "Authorization": f"Bearer {spotify_access_token}"
        }
        traits = traits.model_dump()
        genres = traits["genres"]
        q = "".join(["genre:" + g + "%20OR" for g in genres])
        q = q[:-5]
        url += f"q={q}&type=track&limit=3"
        print(url)

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(response.status_code)
                print(response.text)                
                raise Exception(f"Failed to fetch recommendations: {response.status_code}")

            recommendations = response.json()
            print(recommendations)
            songs = []
            for track in recommendations.get("tracks"):
                song = Song(
                    id=track.get("id"),
                    name=track.get("name"),
                    artists=[artist.get("name") for artist in track.get("artists")],
                )
                songs.append(song)
            return songs

        except Exception as e:
            raise Exception(f"An error occurred while fetching song recommendations: {str(e)}")
        
        # OLD:
        url = "https://api.spotify.com/v1/recommendations?"
        headers = {
            "Authorization": f"Bearer {spotify_access_token}"
        }
        traits = traits.model_dump()
        for param in traits:
            if isinstance(traits[param], list):
                url += f"{param}={'%2'.join(traits[param])}&"
            elif traits[param] is not None:
                url += f"{param}={traits[param]}&"
        url = url[:-1] 

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:                
                raise Exception(f"Failed to fetch recommendations: {response.status_code}")

            recommendations = response.json()
            songs = []
            for track in recommendations.get("tracks"):
                song = Song(
                    id=track.get("id"),
                    name=track.get("name"),
                    artists=[artist.get("name") for artist in track.get("artists")],
                )
                songs.append(song)
            return songs

        except Exception as e:
            raise Exception(f"An error occurred while fetching song recommendations: {str(e)}")
