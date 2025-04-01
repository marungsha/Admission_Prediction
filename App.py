import streamlit as st
import pickle
import pandas as pd
import time

# Load the model
with open('admission_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #00000;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextInput>div>div>label {
        font-weight: bold;
        color: #4CAF50;
    }
    .stMarkdown>div>div>p {
        font-size: 18px;
        color: #333;
    }
    .result {
        font-size: 24px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .title {
        font-size: 24px;
        color: white;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>\U0001F393 StudyVerse AI - Admission Guide \U0001F393</div>", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)

# Input fields with placeholders and validation
GREScore = st.text_input('GRE Score (out of 340):', placeholder='Enter your GRE Score')
TOEFLScore = st.text_input('TOEFL Score (out of 120):', placeholder='Enter your TOEFL Score')
UniversityRating = st.text_input('University Rating (out of 10):', placeholder='Enter University Rating')
SOP = st.text_input('SOP Score (out of 10):', placeholder='Enter SOP Score')
LOR = st.text_input('LOR Score (out of 10):', placeholder='Enter LOR Score')
CGPA = st.text_input('CGPA Score (out of 10):', placeholder='Enter CGPA Score')

if st.button('Predict'):
    # Convert inputs to float and validate
    try:
        GREScore = float(GREScore)
        TOEFLScore = float(TOEFLScore)
        UniversityRating = float(UniversityRating)
        SOP = float(SOP)
        LOR = float(LOR)
        CGPA = float(CGPA)
        
        # Check if values are within the specified range
        if not (0 <= GREScore <= 340):
            st.write("GRE Score must be between 0 and 340.")
        elif not (0 <= TOEFLScore <= 120):
            st.write("TOEFL Score must be between 0 and 120.")
        elif not (0 <= UniversityRating <= 10):
            st.write("University Rating must be between 0 and 10.")
        elif not (0 <= SOP <= 10):
            st.write("SOP score must be between 0 and 10.")
        elif not (0 <= LOR <= 10):
            st.write("LOR score must be between 0 and 10.")
        elif not (0 <= CGPA <= 10):
            st.write("CGPA score must be between 0 and 10.")
        else:
            # Create a DataFrame from the input
            data = pd.DataFrame([[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA]], columns=['Gre score:', 'toefl score:', 'university rating:', 'sop score:', 'lor score:', 'cgpa score:'])
            
            with st.spinner('Calculating...'):
                time.sleep(2)  # Simulate a delay for loading screen
                prediction = model.predict(data)
                prediction_clamped = max(0, min(prediction[0], 1))
                st.markdown(f"<div class='result'>Chances of Admission: {prediction_clamped*100:.2f}%</div>", unsafe_allow_html=True)

                # Predict university based on chances
                if prediction_clamped > 80:
                    university = "MIT, Stanford, Harvard"
                elif prediction_clamped > 60:
                    university = "UC Berkeley, UCLA, Michigan"
                elif prediction_clamped > 40:
                    university = "Texas A&M, Ohio State, Purdue"
                else:
                    university = "Arizona State, SUNY Buffalo, UIC"

                st.markdown(f"**Suggested University Category: {university}**")
    except ValueError:
        st.write("Please enter valid numerical values for all fields.")

st.markdown("</div>", unsafe_allow_html=True)