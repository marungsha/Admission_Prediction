import streamlit as st
import pickle
import pandas as pd
# Load the model
with open('admission_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title('StudyVerse AI - Study Abroad Companion')

# Input fields (customize based on your model's input)
#Example for two numerical features.
GREScore = st.number_input('GRE Score (out of 340):')
TOEFLScore = st.number_input('TOEFL Score (out of 120):')
UniversityRating = st.number_input('University Rating (out of 10):')
SOP = st.number_input('SOP score (out of 10):')
LOR = st.number_input('LOR score (out of 10):')
CGPA = st.number_input('CGPA score (out of 10):')

if st.button('Predict'):
    # Create a DataFrame from the input
    data = pd.DataFrame([[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA]], columns=['Gre score:', 'toefl score:', 'university rating:', 'sop score:', 'lor score:', 'cgpa score:'])
    prediction = model.predict(data)
    prediction_clamped = max(0, min(prediction[0], 1))
    st.write(f'Chances of Admission: {prediction_clamped*100:.2f}%')