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
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
}

# Streamlit page configuration
st.set_page_config(
    page_title="Health Analysis Chatbot",
    page_icon=":hospital:",
    layout="centered",  # Ensures the layout is centered
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    *
    {
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

    /* Main Text Styling */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff !important; /* High contrast for all text */
    }

    /* Adjusted Input Box and Button Styling */
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
        width: 100%; /* Full width of container */
        border: 1px solid #444;
        background-color: rgba(255, 255, 255, 0.1);
        color: #eee;
        border-radius: 0.5rem;
        padding: 0.6rem;
        margin-bottom: 1rem; /* Reduced space between input and button */
    }

    .stButton>button {
        background-color: #ee83e5;
        color: #fff;
        padding: 0.5rem 1.5rem; /* Adjusted button size */
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        width: auto; /* Button should only be as wide as its content */
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #d673c3;
        box-shadow: 0 4px 15px rgba(238, 131, 229, 0.5);
    }

    /* Card Design */
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
    .bg {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 10rem;
        color: rgba(150, 72, 112, 0.9);
        font-weight: bold;
        z-index: -1;
    }

    .nft-card:hover {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9);
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Background overlay
st.markdown('<div class="bg">Health Analysis</div>', unsafe_allow_html=True)

# App header
st.markdown('<div class="nft-card"> Health Analysis Chatbot </div>', unsafe_allow_html=True)

# User input section
st.title("Health Analysis Chatbot")
st.write("Enter your symptoms to receive a concise health analysis.")

# Input area for user symptoms within a centered container
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    symptoms = st.text_input("Enter symptoms (e.g., headache, nausea):")
    submit_button = st.button("Analyze")
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button and symptoms:
    try:
        # Define the prompt for the AI
        prompt = f"""
        Based on the symptoms '{symptoms}', provide the following:
        1. Disease and Description: Briefly identify the most likely disease and describe it.
        2. Treatment: Suggest a short treatment plan.
        3. Medication: Recommend a few key medications.
        4. Workout: Suggest a workout plan for managing these symptoms.
        5. Diet: Provide a suitable diet plan.

        Use the exact labels (Disease and Description, Treatment, Medication, Workout, Diet) in your response.
        """

        # Generate response
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-002",
            generation_config=generation_config,
        )
        response = model.generate_content([prompt])

        if response:
            # Parse the response using predefined labels
            sections = {
                "Disease and Description": "",
                "Treatment": "",
                "Medication": "",
                "Workout": "",
                "Diet": "",
            }

            current_section = None
            for line in response.text.strip().splitlines():
                line = line.strip()

                # Check for section headings
                if any(keyword in line.lower() for keyword in ["disease", "treatment", "medication", "workout", "diet"]):
                    for section in sections:
                        if section.lower() in line.lower():
                            current_section = section
                            break
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
