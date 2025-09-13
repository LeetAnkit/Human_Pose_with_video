import streamlit as st
from src.main import main
import tempfile
import os
from datetime import datetime

st.set_page_config(
    page_title="Human Pose Estimation",
    page_icon="🧍",
    layout="centered",
)

st.markdown("""
    <style>
        .stApp {
            background: url('https://images.pexels.com/photos/1229356/pexels-photo-1229356.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .stApp:before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: -1;
        }
        .title-text {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 700;
            color: #1976d2;
            margin-bottom: 0.5rem;
        }
        .subtitle-text {
            text-align: center;
            font-size: 1.2rem;
            color: #eeeeee;
            margin-bottom: 2rem;
        }
        .card {
            background: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            margin-top: 10px;
        }
        ul {
            color: #eeeeee !important;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Human Pose Estimation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Real-time curl tracking with smart video insights. Every rep, perfectly captured.</div>', unsafe_allow_html=True)
st.write("---")

option = st.radio("Choose Input Source", ("Webcam", "Upload Video"))

if option == "Webcam":
    st.info("Live tracking will open in a new window. Press Q to quit.")
    if st.button("🎥 Start Webcam Tracking"):
        main(use_webcam=True)
else:
    uploaded_file = st.file_uploader("🎥 Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file:
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(uploaded_file.read())
        temp_video.close()

        st.success("Video uploaded successfully.")
        if st.button("▶️ Start Video Analysis"):
            main(use_webcam=False, video_path=temp_video.name)
        if st.button("🗑️ Clear Video"):
            os.unlink(temp_video.name)
            st.success("Temporary video deleted.")

st.write("---")
st.markdown(f'<div style="text-align:center; color:#bbb;">© {datetime.now().year} Built by Ankit with ❤️ using Streamlit</div>', unsafe_allow_html=True)
