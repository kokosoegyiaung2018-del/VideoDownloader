from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os

app = FastAPI()

# CORS ကို ဖွင့်ပေးခြင်း (Telegram Mini App ကနေ API ကို လှမ်းခေါ်လို့ရအောင်)
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
async def get_video_info(data: VideoRequest):
    url = data.url
    
    # yt-dlp options (ဗီဒီယို လင့်ခ်နဲ့ အချက်အလက်များကို ဆွဲထုတ်ရန်)
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ဗီဒီယို အချက်အလက်များကို ရယူခြင်း
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)  # တိုက်ရိုက်ဒေါင်းလုပ်ဆွဲနိုင်သော Direct Link
            title = info.get('title', 'Downloaded Video')
            thumbnail = info.get('thumbnail', '')
            
            if not video_url:
                raise HTTPException(status_code=400, detail="ဗီဒီယိုလင့်ခ် ရယူ၍ မရပါ။")
                
            return {
                "success": True,
                "title": title,
                "thumbnail": thumbnail,
                "download_url": video_url
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
