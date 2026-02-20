from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)


def get_gemini_response(input_text, image, prompt):
    """
    Function to get response from Gemini model.

    Args:
        input_text: User input text
        image: List containing image data in the format required by Gemini
        prompt: The prompt to send to the model

    Returns:
        str: The text response from the model
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    try:
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"


def input_image_setup(uploaded_file):
    """
    Function to read the uploaded image and format it for Gemini Pro model.

    Args:
        uploaded_file: The uploaded file object from Streamlit

    Returns:
        list: A list containing image data formatted for Gemini API

    Raises:
        FileNotFoundError: If no file is uploaded
    """
    if uploaded_file is not None:
        # Read the file's binary data
        bytes_data = uploaded_file.getvalue()

        # Create image parts in the required format
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def setup_page():
    st.set_page_config(page_title="Civil Engineering Insight Studio", layout="wide", page_icon="🏗️")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            font-weight: bold;
            border: none;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            color: white;
        }
        .header-title {
            text-align: center;
            font-size: 3em;
            font-weight: 800;
            color: #2c3e50;
            margin-bottom: 0.5em;
        }
        .sub-header {
            text-align: center;
            font-size: 1.2em;
            color: #7f8c8d;
            margin-bottom: 2em;
        }
        .feature-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main function to run the Streamlit application."""
    setup_page()

    # Sidebar for configuration and info
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/engineer.png", width=100)
        st.title("Settings & Info")
        
        if not api_key:
            st.error("⚠️ API Key Missing")
            st.info("Please add GOOGLE_API_KEY to your .env file.")
        else:
            st.success("✅ API Key Configured")
        
        st.markdown("---")
        st.subheader("How to use:")
        st.markdown("""
        1. **Upload an image** of a civil engineering structure.
        2. **Enter a prompt** describing what you want to analyze.
        3. Click **Analyze Structure**.
        """)
        st.markdown("---")
        st.caption("Powered by Google Gemini AI")

    # Main Content Area
    st.markdown('<div class="header-title">Civil Engineering Insight Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced AI Analysis for Structural Engineering</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("### 📤 Upload & Prompt")
        uploaded_file = st.file_uploader(
            "Choose a structure image...",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            help="Supported formats: JPG, PNG, WEBP"
        )

        input_prompt = st.text_area(
            "Analysis Prompt",
            value="Analyze this civil engineering structure image. Provide a detailed breakdown including: type of structure, materials used, estimated dimensions, construction method, notable features, and any engineering challenges visible.",
            height=200,
            help="This prompt guides the AI analysis."
        )
        
        analyze_button = st.button("🔍 Analyze Structure", type="primary")

    with col2:
        st.markdown("### 🖼️ Preview")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        else:
            st.info("Upload an image to see a preview here.")

    # Analysis Results Section (Full Width below columns)
    if analyze_button and uploaded_file:
         if not api_key:
             st.error("Please configure your API key first.")
         elif input_prompt.strip() == "":
             st.warning("Please enter a prompt.")
         else:
             with st.spinner("🚀 Analyzing structure structure... This may take a moment."):
                 try:
                    image_data = input_image_setup(uploaded_file)
                    response = get_gemini_response(input_text="Analyze the following image:", image=image_data, prompt=input_prompt)
                    
                    st.markdown("---")
                    st.subheader("📊 Analysis Report")
                    st.markdown(response)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Report",
                        data=response,
                        file_name="structural_analysis_report.md",
                        mime="text/markdown"
                    )

                 except FileNotFoundError as e:
                     st.error(f"File Error: {e}")
                 except Exception as e:
                     st.error(f"Analysis Failed: {str(e)}")


if __name__ == "__main__":
    main()
