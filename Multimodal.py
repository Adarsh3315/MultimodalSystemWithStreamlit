import streamlit as st
from streamlit_lottie import st_lottie
import Multimodal1
import Multimodal2
import Multimodal3
import Multimodal4
import Multimodal5
import Multimodal6

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(-45deg, #ff6f61, #e57373, #ffd54f, #4db6ac, #9575cd, #ff8a65, #ffcc80, #dce775, #a5d6a7, #f8bbd0);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            font-family: 'Arial', sans-serif;
            min-height: 100vh;
            padding: 20px;
            margin: 0;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .footer {
            background: transparent;
            color: #000;
            padding: 15px;
            text-align: center;
            font-size: 1rem;
            margin-top: 20px;
            border-radius: 10px;
        }

        .stButton>button {
            background-color: #009500;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
            width: 340px; 
            height: 50px; 
        }

        .stButton>button:hover {
            background-color: #004d40;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Multimodal System")

st.write(
    """
    Welcome To The **Multimodal System** Developed By **A&J**. This Platform Lets You Explore Different Modals, Such As Facial Analysis, Language Translation, Stock Market Price Checking, Hand Detection, Brightness Control And Advanced Image Analyzer. 

Please Choose Any Modal Below To Get Started!
"""
)

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

st.subheader("Available Modals:")

col1, col2 = st.columns(2)

model_placeholder = st.empty()


def display_model(model_function):
    with model_placeholder.container():
        model_function()


with col1:
    if st.button("DeepFace Analysis"):
        st.session_state.selected_model = "DeepFace"

    if st.button("English To Hindi-Gujarati Translator"):
        st.session_state.selected_model = "Translator"

    if st.button("Stock Market Price Checker"):
        st.session_state.selected_model = "Stock Market"

with col2:
    if st.button("Enhanced Hand Detection Program"):
        st.session_state.selected_model = "Hand Detection"

    if st.button("Hand Tracking & Brightness Control System"):
        st.session_state.selected_model = "Hand Tracking"

    if st.button("Advanced Image Analyzer"):
        st.session_state.selected_model = "Image Analyzer"

if st.session_state.selected_model == "DeepFace":
    with st.spinner("Running DeepFace Analysis"):
        display_model(Multimodal1.main)

elif st.session_state.selected_model == "Translator":
    with st.spinner("Running English To Hindi-Gujarati Translator"):
        display_model(Multimodal2.main)

elif st.session_state.selected_model == "Stock Market":
    with st.spinner("Running Stock Market Price Checker"):
        display_model(Multimodal3.main)

elif st.session_state.selected_model == "Hand Detection":
    with st.spinner("Running Enhanced Hand Detection Program"):
        display_model(Multimodal4.main)

elif st.session_state.selected_model == "Hand Tracking":
    with st.spinner("Running Hand Tracking & Brightness Control System"):
        display_model(Multimodal5.main)

elif st.session_state.selected_model == "Image Analyzer":
    with st.spinner("Running Advanced Image Analyzer"):
        display_model(Multimodal6.main)

st.markdown('<p class="footer">Developed By A&J</p>', unsafe_allow_html=True)
