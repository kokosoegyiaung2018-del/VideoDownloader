from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pytubefix import YouTube

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.post("/get-video")
def get_video(req: VideoRequest):
    try:
        yt = YouTube(req.url)
        stream = yt.streams.get_highest_resolution()
        return {
            "success": True,
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "download_url": stream.url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
