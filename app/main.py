from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import spotify

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


app.include_router(spotify.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


handler = Mangum(app=app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
