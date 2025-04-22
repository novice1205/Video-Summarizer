import streamlit as st
import google.generativeai as genai
from google.generativeai import upload_file, get_file
from dotenv import load_dotenv
from pathlib import Path
import time
import tempfile
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page Configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="📹",
    layout="wide"
)

# Title & Header
st.markdown('<div class="title">Video Summarization using Agentic AI 🎥🎤🖬</div>', unsafe_allow_html=True)
st.markdown('<div class="header">Powered by Gemini 2.0 Flash</div><br><br>', unsafe_allow_html=True)

# File uploader
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")  # You can change to "gemini-pro" if needed

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.video(video_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
        help="Provide specific questions or insights you want from the video."
    )

    if st.button("🔍 Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    # Upload and process video file
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    # Generate prompt for analysis
                    analysis_prompt = (
                        f"""
                        Analyze the uploaded video for content and context.
                        Respond to the following query using video insights:
                        {user_query}

                        Provide a detailed, user-friendly, and actionable response.
                        """
                    )

                    # Gemini model call
                    response = model.generate_content(
                        analysis_prompt,
                        generation_config=genai.types.GenerationConfig(temperature=0.7),
                        safety_settings={"HARASSMENT": "block_none"},
                        tools=[],
                        files=[processed_video]
                    )

                # Display the result
                st.subheader("Analysis Result")
                st.markdown(response.text)

            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
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
    </style>
    """,
    unsafe_allow_html=True
)
