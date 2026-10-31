from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# CORS Middleware (Frontend မှ လှမ်းချိတ်ခွင့်ပြုရန်)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "success", "message": "Video Downloader Bot API is running perfectly!"}

@app.post("/get-video")
def get_video(req: VideoRequest):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            return {
                "success": True,
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url')
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
