# import streamlit as st
# import cv2
# import tempfile
# from src.main import main  # Your main pose detection code

# st.title("🏋️ Human Pose Estimation with Counter")

# st.write("Upload a video or use your webcam to track movements and count reps.")

# option = st.radio("Choose Input Source", ("Webcam", "Upload Video"))

# if option == "Upload Video":
#     video_file = st.file_uploader("Upload a video", type=["mp4", "avi"])
#     if video_file:
#         tfile = tempfile.NamedTemporaryFile(delete=False) 
#         tfile.write(video_file.read())

#         st.video(video_file)
#         st.write("Processing video...")

#         main(tfile.name, use_webcam=False)

# elif option == "Webcam":
#     st.write("Click 'Start' below to begin tracking via webcam.")
#     if st.button("Start Webcam"):
#         main(use_webcam=True)


import streamlit as st
from src.main import main
import tempfile
import os

st.title("Human Pose Estimation App")
st.write("Track your squats in real-time or analyze a video file.")

# Option selection
option = st.radio("Choose input source:", ("Webcam", "Upload Video"))

if option == "Webcam":
    st.write("Click the button below to start tracking using your webcam.")
    if st.button("Start Webcam Tracking"):
        st.info("Press 'q' in the OpenCV window to quit.")
        main(use_webcam=True)

else:
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        # Save file temporarily
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(uploaded_file.read())
        temp_video.close()

        st.success(f"Uploaded video saved at {temp_video.name}")

        if st.button("Start Video Analysis"):
            st.info("Press 'q' in the OpenCV window to quit.")
            main(use_webcam=False, video_path=temp_video.name)

        # Clean up temp file after use
        if st.button("Clear Video"):
            os.unlink(temp_video.name)
            st.success("Temporary video deleted.")
