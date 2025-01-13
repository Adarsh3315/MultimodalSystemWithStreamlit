import cv2
import mediapipe as mp
import screen_brightness_control as sbc
import streamlit as st
import numpy as np
from math import hypot

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85,
    max_num_hands=2,
)
mp_draw = mp.solutions.drawing_utils


def process_frame(frame):
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = [
                (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]))
                for lm in hand_landmarks.landmark
            ]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = landmarks[4]
            index_tip = landmarks[8]

            cv2.circle(frame, thumb_tip, 7, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, index_tip, 7, (0, 255, 0), cv2.FILLED)
            cv2.line(frame, thumb_tip, index_tip, (0, 255, 0), 3)

            length = hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            brightness_level = np.interp(length, [15, 220], [0, 100])
            sbc.set_brightness(int(brightness_level))

    return frame


def webcam_stream():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Unable To Capture Video. Make Sure Your Webcam Is Enabled.")
            break

        frame = process_frame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()


def hand_tracking_brightness_control():
    st.markdown(
        """
        <p style="font-size: 18px; color: #333;">
        Click 'Start Video' To Begin Hand Tracking & Screen Brightness Control By Pinching Your Thumb And Index Finger. Click 'Stop Video' To End.
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
    st.title("Hand Tracking & Brightness Control System")

    menu = ["Hand Tracking & Brightness Control System"]
    choice = st.sidebar.selectbox("Select Model", menu)

    if choice == "Hand Tracking & Brightness Control System":
        hand_tracking_brightness_control()


if __name__ == "__main__":
    main()
