"""
Utility functions for the prescription parser application.
"""

import json
import os
import streamlit as st
from pyngrok import ngrok
import pandas as pd
from PIL import Image

def load_css():
    """Load custom CSS for styling the Streamlit app."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_app_logo():
    """
    Return None to disable app logo loading.
    This removes the logo display from the app UI.
    """
    return None

def setup_ngrok(port, auth_token):
    """
    Set up ngrok tunnel to expose the Streamlit app.
    
    Args:
        port: Port to expose
        auth_token: Ngrok authentication token
        
    Returns:
        Public URL or None if setup fails
    """
    if not auth_token:
        st.error("Ngrok authentication token is required.")
        return None
    
    ngrok.set_auth_token(auth_token)
    
    try:
        ngrok.kill()  # Close existing tunnels if any
        public_url = ngrok.connect(port)
        return public_url
    except Exception as e:
        st.error(f"Failed to establish ngrok tunnel: {str(e)}")
        return None

def download_json_data(data, filename="prescription_analysis.json"):
    """
    Create a download button for JSON data.
    
    Args:
        data: Data to download as JSON
        filename: Filename for the downloaded file
    """
    json_str = json.dumps(data, indent=2)
    st.download_button(
        label="📥 Download Results as JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        key="download_json"
    )
    
def convert_df_to_csv(df):
    """
    Convert pandas DataFrame to CSV for download.
    
    Args:
        df: DataFrame to convert
        
    Returns:
        CSV string encoded in UTF-8
    """
    return df.to_csv(index=False).encode('utf-8')

def download_table_as_csv(df, filename="prescription_data.csv", button_text="📥 Download as CSV"):
    """
    Create a download button for DataFrame data.
    
    Args:
        df: DataFrame to download
        filename: Filename for the downloaded file
        button_text: Text for the download button
    """
    csv = convert_df_to_csv(df)
    st.download_button(
        label=button_text,
        data=csv,
        file_name=filename,
        mime="text/csv",
        key=f"download_{filename}"
    )

def load_sample_images():
    """
    Load sample prescription images from the assets folder.
    
    Returns:
        List of (image_path, image_name) tuples
    """
    samples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sample_images')
    sample_images = []
    
    if os.path.exists(samples_dir):
        image_files = [f for f in os.listdir(samples_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for img_file in image_files:
            img_path = os.path.join(samples_dir, img_file)
            sample_images.append((img_path, img_file))
    
    return sample_images
