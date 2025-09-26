import os
import re
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load environment variables from .env file

# It's critical to use environment variables for security.
# In your terminal: export GEMINI_API_KEY="YOUR_API_KEY"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

# --- Templates ---
# This tells FastAPI where to find your HTML file
templates = Jinja2Templates(directory="..")

# --- Pydantic Models for Data Validation ---
class SummarizeRequest(BaseModel):
    video_url: str

class SummarizeResponse(BaseModel):
    summary: str

# --- Helper Function ---
def extract_video_id(url: str) -> str | None:
    """Extracts YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main index.html file."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_video(request: SummarizeRequest):
    """Receives a video URL, gets the transcript, and returns an AI summary."""
    video_id = extract_video_id(request.video_url)
    
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL provided.")

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'th'])
        full_transcript = " ".join([item['text'] for item in transcript_list])
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No transcript found for this video. It might be disabled or in an unsupported language.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the transcript: {e}")

    # Generate summary with Gemini
    prompt = f"""
    You are an expert summarizer. Analyze the following video transcript and provide a concise, insightful summary.
    Structure your output with a main title and 3-5 key bullet points.

    Transcript:
    ---
    {full_transcript}
    ---
    """
    try:
        response = model.generate_content(prompt)
        return SummarizeResponse(summary=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary with AI: {e}")
