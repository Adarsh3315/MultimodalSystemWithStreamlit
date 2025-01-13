import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import logging


logging.basicConfig(level=logging.INFO)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@st.cache_resource
def load_blip_model():
    try:
        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-large"
        )
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-large"
        ).to(device)
        logging.info("Model & Processor Loaded Successfully.")
        return model, processor
    except Exception as e:
        logging.error(f"Error Loading Model: {e}")
        st.error(f"Failed To Load Model: {e}")
        return None, None


def generate_image_description(image, processor, model, context=""):
    try:
        inputs = processor(images=image, text=context, return_tensors="pt").to(device)

        generated_ids = model.generate(
            pixel_values=inputs["pixel_values"],
            max_length=250,
            num_beams=10,
            repetition_penalty=2.5,
            length_penalty=1.0,
            temperature=1.0,
            early_stopping=True,
        )

        description = processor.decode(generated_ids[0], skip_special_tokens=True)

        return description

    except KeyError as e:
        logging.error(f"Input Error: {e}")
        st.error(f"Input Processing Error: {e}")
        return "Error: Input Processing Issue."
    except Exception as e:
        logging.error(f"Error In Generating Image Description: {e}")
        st.error(f"Error In Generating Image Description: {e}")
        return "Error: Failed To Generate Description."


def image_analyzer_ui(blip_model, blip_processor):
    """Streamlit UI For The Advanced Image Analyzer."""
    st.title("Advanced Image Analyzer")
    st.write("Upload An Image To Generate Detailed Description.")

    uploaded_file = st.file_uploader("Choose An Image:", type=["jpg", "jpeg", "png"])

    context = st.text_input("Provide Some Context (Optional):", key="user_input")

    if st.button("Generate Description") and uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.header("Image Description:")
        if blip_model is not None and blip_processor is not None:
            try:
                description = generate_image_description(
                    image, blip_processor, blip_model, context
                )
                st.write(f"Generated Description: **{description}**")
            except Exception as e:
                st.error(f"Error In Generating Image Description: {e}")
                logging.error(f"Error In Generating Image Description: {e}")
        else:
            st.error("Model Or Processor Is Not Loaded.")
            logging.error("Model Or Processor Is Not Loaded.")
    elif uploaded_file is None:
        st.warning("Please Upload An Image Before Generating The Description.")


def main():
    """Main Function To Run The Streamlit App."""
    blip_model, blip_processor = load_blip_model()

    image_analyzer_ui(blip_model, blip_processor)


if __name__ == "__main__":
    main()
