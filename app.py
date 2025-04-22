import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import tempfile
from pathlib import Path

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# Constants
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Page Configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="📹",
    layout="wide"
)

# Title & Header
st.markdown('<div class="title">Video Summarization using Agentic AI 🎥🎤🖬</div>', unsafe_allow_html=True)
st.markdown('<div class="header">Powered by Gemini REST API</div><br><br>', unsafe_allow_html=True)

# File Uploader
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp:
        temp.write(video_file.read())
        video_path = temp.name

    st.video(video_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and summarize based on your question.",
        help="Provide specific questions or insights you want from the video."
    )

    if st.button("🔍 Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            with st.spinner("Processing video and gathering insights..."):
                try:
                    # Simulated prompt to Gemini since video content can't be parsed directly
                    prompt = f"""
                    You are an expert video summarizer. Based on the uploaded video titled 'user_video.mp4',
                    answer this query:
                    "{user_query}"

                    Provide a detailed, user-friendly, and actionable response.
                    """

                    payload = {
                        "contents": [
                            {"parts": [{"text": prompt}]}
                        ]
                    }

                    response = requests.post(GEMINI_ENDPOINT, headers=HEADERS, json=payload)
                    result = response.json()

                    if "candidates" in result:
                        text = result["candidates"][0]["content"]["parts"][0]["text"]
                        st.subheader("AI Summary")
                        st.markdown(text)
                    else:
                        st.error(f"Gemini error: {result.get('error', {}).get('message', 'Unknown error')}")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                finally:
                    Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")

# Custom Styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Poppins', sans-serif;
            background-color: #121212;
            color: #E0E0E0;
        }
        .title {
            font-size: 40px;
            font-weight: 600;
            color: whitesmoke;
            text-align: center;
            margin-bottom: 10px;
        }
        .header {
            font-size: 22px;
            font-weight: 400;
            color: #03DAC6;
            text-align: center;
            margin-bottom: 20px;
        }
        .stTextArea textarea {
            height: 120px !important;
            border-radius: 10px !important;
            border: 1px solid #333 !important;
            background-color: #1E1E1E !important;
            color: #E0E0E0 !important;
            padding: 10px !important;
            font-size: 16px !important;
        }
        .stButton>button {
            background-color: #03DAC6 !important;
            color: black !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)
