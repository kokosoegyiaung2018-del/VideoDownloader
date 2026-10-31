from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI(title="Video Downloader Bot API")

# Request Body အတွက် Data Model
class VideoRequest(BaseModel):
    url: str

# ၁။ ပင်မလင့်ခ် (404 Error မတက်အောင် ကာကွယ်ရန်)
@app.get("/")
def read_root():
    return {"status": "success", "message": "Video Downloader Bot API is running perfectly!"}

# ၂။ ဗီဒီယို အချက်အလက် သို့မဟုတ် Download လิงค์ ထုတ်ပေးမည့် API Endpoint
@app.post("/get-video")
def get_video_info(data: VideoRequest):
    video_url = data.url
    
    if not video_url:
        raise HTTPException(status_code=400, detail="URL is required")

    # yt-dlp options
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ဗီဒီယို အချက်အလက်များကို ဆွဲထုတ်ခြင်း
            info = ydl.extract_info(video_url, download=False)
            
            # လိုအပ်မယ့် ချက်လက်များကို ယူထုတ်ခြင်း
            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)
            thumbnail = info.get('thumbnail', '')
            
            # တိုက်ရိုက်ဒေါင်းလို့ရမည့် URL (သို့မဟုတ် formats များ)
            download_url = info.get('url', '')
            
            # အကယ်၍ formats တွေထဲကမှ ရှာချင်ရင်
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('url') and f.get('ext') == 'mp4':
                        formats.append({
                            'resolution': f.get('format_note', 'hd/sd'),
                            'url': f.get('url')
                        })

            return {
                "success": True,
                "title": title,
                "duration": duration,
                "thumbnail": thumbnail,
                "download_url": download_url,
                "formats": formats[:5] # အများဆုံး ၅ ခု ပြန်ပေးမည်
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
