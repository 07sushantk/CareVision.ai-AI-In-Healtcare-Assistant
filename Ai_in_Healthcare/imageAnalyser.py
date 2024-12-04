import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
import time

# Configure Generative AI
genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_setting = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.

2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.

3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.

4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.

2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.

3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above
"""

# Streamlit page configuration
st.set_page_config(
    page_title="VitalImage Analytics",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dynamic text effect and consistent background
st.markdown("""
    <style>
        body {
            background: linear-gradient(145deg, #141e30, #243b55);
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: linear-gradient(145deg, #141e30, #243b55);
        }

        /* Typing Effect */
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink {
            50% { border-color: transparent }
        }

        .typing {
            font-size: 3rem;
            font-weight: bold;
            color: white;
            display: inline-block;
            border-right: 4px solid white;
            white-space: nowrap;
            overflow: hidden;
            width: fit-content;
            margin: 20px auto;
            animation: typing 4s steps(40, end), blink 0.75s step-end infinite;
        }

        /* Card Center */
        .nft-card {
            width: 300px;
            height: auto;
            margin: 3rem auto;
            background: rgba(255, 255, 255, 0.1); /* Glass effect */
            border-radius: 15px;
            backdrop-filter: blur(10px); /* Blur effect */
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            padding: 1.5rem;
            color: white;
            font-weight: bold;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .nft-card:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(255, 255, 255, 0.5);
        }

        /* Improved text visibility */
        h1, h2, h3, h4, h5, h6, p, label, li {
            color: #ffffff !important;
        }

        /* Upload Button */
        .stButton > button {
            background-color: #ff5e7a;
            color: white;
            border: none;
            padding: 0.7rem 1.2rem;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #d673c3;
            box-shadow: 0 4px 15px rgba(238, 131, 229, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# Typing effect header
st.markdown('<div class="typing">VitalImage Analytics - AI Medical Insights</div>', unsafe_allow_html=True)

# Header Section
st.title("Welcome to VitalImage Analytics")
st.subheader("Empowering healthcare through AI-driven insights into medical images")

# File upload and processing
uploaded_file = st.file_uploader("Upload a medical image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Medical Image", use_column_width=False, width=300)

# Submit button
if st.button("Generate Analysis"):
    if uploaded_file:
        # Process the uploaded image
        image_data = uploaded_file.getvalue()

        # Prepare image parts
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], system_prompt]

        # Generate AI response
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-002", generation_config=generation_config, safety_settings=safety_setting)
        response = model.generate_content(prompt_parts)

        # Display results
        if response:
            st.success("Analysis generated successfully!")
            st.markdown("### Detailed Analysis")
            st.markdown(response.text)  # Assumes response.text contains analysis
        else:
            st.error("Failed to generate analysis. Please try again.")
    else:
        st.warning("Please upload an image first.")
