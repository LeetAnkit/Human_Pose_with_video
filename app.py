import streamlit as st
from src.main import main
import tempfile
import os
from datetime import datetime

# Streamlit Page Config
st.set_page_config(
    page_title="Human Pose Estimation",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZyvyVpRvKEYPdg0R-2cFHUDqZFGbWXboyeqXrxx1foI33o0DYd-_qXW4Hcv-RyslrC5E&usqp=CAU",
    layout="centered",
)

# Custom CSS Styling
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

        div[data-baseweb="radio"] label {
            color: #ffffff !important;
            font-size: 18px;
            font-weight: 500;
        }
        div[data-baseweb="radio"] > div {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 10px;
        }

        .stButton>button {
            background-color: #1976d2 !important;
            color: #ffffff !important;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            border: 2px solid #1565c0;
            box-shadow: 0 2px 8px rgba(21,101,192,0.15);
        }
        .stButton>button:hover {
            background-color: #1565c0 !important;
            transform: translateY(-2px);
            border: 2px solid #1976d2;
            box-shadow: 0 4px 12px rgba(21,101,192,0.25);
        }

        .footer {
            text-align: center;
            padding-top: 10px;
            font-size: 0.9rem;
            color: #bbb;
            margin-top: 20px;
        }

        ul {
            color: #eeeeee !important;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-text"> Human Pose Estimation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Real-time curl tracking with smart video insights. Every rep, perfectly captured.</div>', unsafe_allow_html=True)
st.write("---")

# Layout for Input Options
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card"><h3 style="color:#1976d2; text-align:center;">Choose Input Source</h3></div>', unsafe_allow_html=True)
    option = st.radio("", ("Webcam", "Upload Video"), index=0)

with col2:
    st.markdown("""
        <div class="card">
            <h3 style="color:#1976d2;">Instructions</h3>
            <ul>
                <li><b>Webcam Mode:</b> Live tracking will open a new window. Press <b>Q</b> to quit.</li>
                <li><b>Video Upload Mode:</b> Upload a pre-recorded video and analyze it frame by frame.</li>
                <li>Ensure <b>good lighting</b> and that your <b>full body is visible</b> for best results.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# Webcam Mode
if option == "Webcam":
    st.markdown('<div class="card" style="text-align:center;"><b>Live tracking will open in a new window.</b></div>', unsafe_allow_html=True)
    st.write("")
    if st.button("🎥 Start Webcam Tracking"):
        st.info("Initializing webcam... Please wait.")
        main(use_webcam=True)

# Video Upload Mode
else:
    uploaded_file = st.file_uploader("🎥 Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(uploaded_file.read())
        temp_video.close()

        st.success(f"Uploaded video saved at `{temp_video.name}`")

        start_col, clear_col = st.columns([1, 1])
        with start_col:
            if st.button("▶️ Start Video Analysis"):
                st.info("Analyzing video... Please wait.")
                main(use_webcam=False, video_path=temp_video.name)

        with clear_col:
            if st.button("🗑️ Clear Video"):
                os.unlink(temp_video.name)
                st.success("Temporary video deleted.")

# Footer
st.write("---")
st.markdown(
    f'<div class="footer">© {datetime.now().year} Human Pose Estimation | Built by Ankit with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)
