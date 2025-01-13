import cv2
import mediapipe as mp
import streamlit as st
from google.protobuf.json_format import MessageToDict

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85,
    max_num_hands=2,
)

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            label = MessageToDict(hand_handedness)["classification"][0]["label"]
            position = (20, 50) if label == "Left" else (460, 50)
            cv2.putText(
                frame,
                f"{label} Hand",
                position,
                cv2.FONT_HERSHEY_COMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )

            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    return frame

def webcam_stream():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.error("Unable To Capture Video. Make Sure Your Webcam Is Enabled.")
            break

        frame = process_frame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()

def enhanced_hand_detection():
    st.markdown(
        """
        <p style="font-size: 18px; color: #333;">
        Click 'Start Video' To Begin Hand Detection. Click 'Stop Video' To End The Detection.
        </p>
        """,
        unsafe_allow_html=True,
    )

    start_video = st.button("Start Video")
    stop_video = st.button("Stop Video")

    if start_video:
        webcam_stream()
    if stop_video:
        st.stop()

def main():
    st.title("Enhanced Hand Detection Program")

    menu = ["Enhanced Hand Detection Program"]
    choice = st.sidebar.selectbox("Select Model", menu)

    if choice == "Enhanced Hand Detection Program":
        enhanced_hand_detection()

if __name__ == "__main__":
    main()
