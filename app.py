import os
import streamlit as st
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from modules import (
    ImageProcessor,
    PrescriptionParser,
    load_css,
    setup_ngrok,
    download_json_data,
    download_table_as_csv
)

load_dotenv()

st.set_page_config(
    page_title="MediScript: Medical Prescription Analyser",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "")

def display_header():
    st.markdown('<h1 class="main-title">🏥 Medical Prescription Analyser</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-desc">Extract medication information from prescription images using Computer Vision and AI-powered processing</p>', unsafe_allow_html=True)
    st.markdown("---")

def display_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        if not GEMINI_API_KEY:
            st.warning("⚠️ Gemini API key not found in .env file. The app won’t function properly.")
        st.subheader("Processing Options")
        show_steps = st.checkbox("Show image processing steps", value=True)
        processing_quality = st.select_slider(
            "Image Processing Quality:",
            options=["Fast", "Balanced", "High Quality"],
            value="Balanced",
            help="Higher quality may take longer but provides better results"
        )
        if st.checkbox("Enable public sharing (Ngrok)", value=False):
            if not NGROK_AUTH_TOKEN:
                st.error("⚠️ Ngrok auth token not found in .env file. Public sharing is disabled.")
            else:
                if st.button("🌐 Start Public Sharing"):
                    public_url = setup_ngrok(8501, NGROK_AUTH_TOKEN)
                    if public_url:
                        st.success(f"✅ App is publicly available at: {public_url}")
                        st.session_state["public_url"] = public_url
            if "public_url" in st.session_state:
                st.info(f"🔗 Active public URL: {st.session_state['public_url']}")
    return show_steps, processing_quality

def upload_and_display_image():
    uploaded_file = st.file_uploader("Choose a prescription image to upload", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.session_state["uploaded_image"] = image
            st.image(image, width=400, caption="Uploaded Prescription Image")
        except Exception as e:
            st.error(f"Error loading uploaded image: {str(e)}")

def display_processing_section(show_steps, processing_quality):
    if "uploaded_image" not in st.session_state:
        st.info("Please upload a prescription image to start processing.")
        return

    image = st.session_state["uploaded_image"]
    # st.header("🔍 Image Processing")
    # st.image(image, width=400)

    if show_steps:
        processed_image, steps_images, steps_titles = ImageProcessor.enhance_prescription(image, return_steps=True)
    else:
        processed_image = ImageProcessor.enhance_prescription(image, return_steps=False)

    if show_steps:
        st.subheader("Processing Steps")
        ImageProcessor.display_processing_steps(steps_images, steps_titles)

    st.subheader("Processed Image")
    st.image(processed_image, width=400)

    parser = PrescriptionParser(api_key=GEMINI_API_KEY)
    with st.spinner("Analyzing prescription..."):
        parsed_data = parser.parse_prescription(processed_image)

    if parsed_data:
        with st.container():
            st.subheader("Patient Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Patient Name:** {parsed_data.get('patient_name', 'N/A')}")
                st.markdown(f"**Address:** {parsed_data.get('address', 'N/A')}")
                st.markdown(f"**Diagnosis:** {parsed_data.get('diagnosis', 'N/A')}")
            with col2:
                st.markdown(f"**Date:** {parsed_data.get('date', 'N/A')}")
                st.markdown(f"**Doctor's Name:** {parsed_data.get('doctor_name', 'N/A')}")
                st.markdown(f"**History/Symptoms:** {parsed_data.get('history_symptoms', 'N/A')}")
                st.markdown(f"**Remarks:** {parsed_data.get('remarks', 'N/A')}")

        medications = parsed_data.get("medications", [])
        if medications:
            st.subheader("Medications")
            df = pd.DataFrame(medications)
            for col in ['name', 'dosage', 'frequency']:
                if col not in df.columns:
                    df[col] = ''
            df = df[['name', 'dosage', 'frequency']]
            df.columns = ['Medicine Name', 'Dosage', 'Frequency']
            st.table(df)
        else:
            st.info("No medication details found in the parsed data.")

        download_table_as_csv(pd.DataFrame(medications))
        download_json_data(parsed_data)
    else:
        st.warning("No data extracted. Please try another image or adjust processing settings.")

def main():
    display_header()
    show_steps, processing_quality = display_sidebar()
    upload_and_display_image()
    display_processing_section(show_steps, processing_quality)

if __name__ == "__main__":
    main()
