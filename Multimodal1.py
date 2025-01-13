import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np
from retinaface import RetinaFace
from PIL import Image


def preprocess_image(img):
    gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    normalized_img = gray_img / 255.0
    resized_img = cv2.resize(normalized_img, (224, 224))
    return resized_img


def weighted_average_results(results):
    avg_result = results[0].copy()
    weights = [1.0] * len(results)

    for i, res in enumerate(results[1:], start=1):
        avg_result["age"] += res["age"] * weights[i]
        if res["gender"] == "Woman":
            avg_result["gender"] = "Woman"
        for key in avg_result["race"]:
            avg_result["race"][key] += res["race"][key] * weights[i]
        for key in avg_result["emotion"]:
            avg_result["emotion"][key] += res["emotion"][key] * weights[i]

    total_weight = sum(weights)
    avg_result["age"] /= total_weight
    for key in avg_result["race"]:
        avg_result["race"][key] /= total_weight
    for key in avg_result["emotion"]:
        avg_result["emotion"][key] /= total_weight

    return avg_result


def analyze_with_models(img_array):
    results = []
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepID", "ArcFace", "Dlib"]
    for model in models:
        try:
            result = DeepFace.analyze(
                img_path=img_array,
                actions=("age", "gender", "race", "emotion"),
                enforce_detection=True,
                detector_backend="retinaface",
            )
            if isinstance(result, list):
                result = result[0]
            results.append(result)
        except Exception as e:
            st.error(f"Error Analyzing With Model {model}: {str(e)}")
    return results


def face_analyze(img):
    try:
        img_array = np.array(img)

        faces = RetinaFace.extract_faces(img_array)
        if not faces:
            st.error(
                "Face Could Not Be Detected In The Image. Please Use Clear Face Image."
            )
            return

        results = analyze_with_models(img_array)

        if not results:
            st.error("No Results From Analysis!")
            return

        result_dict = weighted_average_results(results)

        st.write(f'**Age**: {round(result_dict["age"], 2)}')
        st.write(f'**Gender**: {result_dict["gender"]}')
        st.write("**Race**:")
        for k, v in result_dict["race"].items():
            st.write(f"{k}: {round(v, 2)}%")
        st.write("**Emotion**:")
        for k, v in result_dict["emotion"].items():
            st.write(f"{k}: {round(v, 2)}%")

        st.info("Model: DeepFace Analysis\nDeveloped By A&J")

    except Exception as e:
        st.error(f"An error occurred {str(e)}")


def real_time_emotion_detection():
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = RetinaFace.detect_faces(rgb_frame)

        for face in faces.values():
            x, y, w, h = face["facial_area"]
            face_roi = rgb_frame[y : y + h, x : x + w]
            result = DeepFace.analyze(
                face_roi, actions=["age", "emotion"], enforce_detection=False
            )
            age = result[0]["age"]
            emotion = result[0]["dominant_emotion"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                frame,
                f"{emotion}, {age}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2,
            )

        stframe.image(frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    st.title("DeepFace Analysis")

    menu = ["Image Analysis", "Real-Time Emotion Detection"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Image Analysis":
        st.subheader("Upload Image For Face Analysis")
        img_file = st.file_uploader("Choose An Image:", type=["jpg", "jpeg", "png"])
        if img_file is not None:
            img = Image.open(img_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)
            if st.button("Analyze"):
                face_analyze(img)

    elif choice == "Real-Time Emotion Detection":
        st.subheader("Real-Time Emotion Detection")
        if st.button("Start Detection"):
            real_time_emotion_detection()


if __name__ == "__main__":
    main()
