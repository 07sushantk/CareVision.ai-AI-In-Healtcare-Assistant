import streamlit as st
import google.generativeai as genai
from api_key import api_key

# Configure Generative AI
genai.configure(api_key=api_key)

# Define the model generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 30,
    "max_output_tokens": 1024,  # Increased output tokens
    "response_mime_type": "text/plain",
}

# Streamlit page configuration
st.set_page_config(
    page_title="Medicine Info",
    page_icon=":pill:",
    layout="centered",  # Ensures the layout is centered
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    *{
        color:#fff;
    }
    body {
        background-color: rgb(22, 20, 24);
        color: #eee;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    .stApp {
        background: linear-gradient(0deg, rgba(40, 44, 52, 1) 0%, rgba(17, 0, 32, 0.5) 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff !important; /* High contrast for all text */
    }

    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 80%;
        max-width: 600px;
        margin-top: 2rem;
        text-align: center;
    }

    .stTextInput {
        width: 100%; 
        border: 1px solid #444;
        background-color: rgba(255, 255, 255, 0.1);
        color: #eee;
        border-radius: 0.5rem;
        padding: 0.6rem;
        margin-bottom: 1rem; 
    }

    .stButton>button {
        background-color: #ee83e5;
        color: #fff;
        padding: 0.5rem 1.5rem; 
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        width: auto; 
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #d673c3;
        box-shadow: 0 4px 15px rgba(238, 131, 229, 0.5);
    }

    .nft-card {
        max-width: 400px;
        margin: 2rem auto;
        background-color: rgba(40, 44, 52, 0.85);
        border-radius: 1rem;
        box-shadow: 0 7px 20px 5px rgba(0, 0, 0, 0.7);
        padding: 2rem;
        color: #fff;
        text-align: center;
        transition: all 0.3s ease;
    }

    .nft-card:hover {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9);
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App header
st.markdown('<div class="nft-card"> Medicine Info</div>', unsafe_allow_html=True)

# User input section
st.title("Medicine Information")
st.write("Enter the name of the medicine to get its information.")

# Input area for user medicine name within a centered container
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    medicine_name = st.text_input("Enter Medicine Name:")
    submit_button = st.button("Get Info")
    st.markdown('</div>', unsafe_allow_html=True)

# Check if button is pressed and medicine name is provided
if submit_button and medicine_name:
    try:
        # Define the prompt for the AI
        prompt = f"""
        Provide detailed information about the medicine '{medicine_name}' in the following format:
        1. Description: A short description of the medicine.
        2. Advantages: List the key benefits of this medicine.
        3. Disadvantages: Mention potential side effects or disadvantages.
        4. Recommended Times: Suggest the best times to take it (e.g., morning, afternoon, evening).
        Ensure the response includes these headings exactly.
        """

        # Generate response
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-002",
            generation_config=generation_config,
        )
        response = model.generate_content([prompt])

        if response:
            raw_text = response.text.strip()

            # Split the response based on sections
            sections = {"Description": "", "Advantages": "", "Disadvantages": "", "Recommended Times": ""}
            current_section = None

            # Parsing the response into the predefined sections
            for line in raw_text.splitlines():
                line = line.strip()

                # Check for section headings
                if "description" in line.lower():
                    current_section = "Description"
                elif "advantages" in line.lower():
                    current_section = "Advantages"
                elif "disadvantages" in line.lower():
                    current_section = "Disadvantages"
                elif "recommended times" in line.lower():
                    current_section = "Recommended Times"
                elif current_section:
                    sections[current_section] += line + " "

            # Display results in expandable sections
            for section, content in sections.items():
                with st.expander(section):
                    st.write(content.strip() if content.strip() else "No information provided.")

        else:
            st.error("No response received. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
