# Spotify-Adapter
Service for interfacing with the Spotify API


## Usage

You need to configure a .env file with your Spotify App information like this:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

```

For the people on our team, you can copy this information at https://developer.spotify.com/dashboard

`uvicorn app.main:app --reload --port 8005`

This services currently runs on `http://127.0.0.1:8005` by default for testing.
