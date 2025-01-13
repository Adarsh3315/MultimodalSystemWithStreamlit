import streamlit as st
from googletrans import Translator


def translate_text(text, target_language):
    translator = Translator()
    try:
        translated_message = translator.translate(text, dest=target_language).text
        return translated_message
    except Exception as e:
        return f"Error: {str(e)}"


def clear_output():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""


def translator_app():
    st.subheader("Enter English Text:")
    input_text = st.text_area("English Text:", value="", key="input_text", height=150)

    st.subheader("Select Target Language:")
    target_language = st.radio(
        "Choose Language", options=["Hindi", "Gujarati"], horizontal=True
    )
    target_language_code = "hi" if target_language == "Hindi" else "gu"

    translate_button = st.button("Translate")
    clear_button = st.button("Clear", on_click=clear_output)

    if translate_button:
        if not input_text.strip():
            st.error("Please Enter English Words To Translate.")
        else:
            translated_text = translate_text(input_text, target_language_code)
            st.session_state.translated_text = translated_text

    if "translated_text" in st.session_state and st.session_state.translated_text:
        st.subheader("Translated Text:")
        st.text_area(
            "Translation",
            value=f"Translated: {st.session_state.translated_text}",
            height=150,
            disabled=True,
        )


def main():
    st.title("English To Hindi-Gujarati Translator")

    menu = ["English To Hindi-Gujarati Translator"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "English To Hindi-Gujarati Translator":
        translator_app()


if __name__ == "__main__":
    main()
