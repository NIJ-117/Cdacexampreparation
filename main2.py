import streamlit as st
import pandas as pd
import random

# Function to load and shuffle the CSV file
@st.experimental_memo
def load_and_shuffle_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    # Shuffle the DataFrame
    df = df.sample(frac=1).reset_index(drop=True)
    return df

# Title of the app
st.title('Quiz App')

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Using the memoized function to load and shuffle the CSV file
    shuffled_df = load_and_shuffle_csv(uploaded_file)

    # Ensuring the file has the necessary columns
    if all(col in shuffled_df.columns for col in ['Question', 'Option_A', 'Option_B', 'Option_C', 'Option_D', 'Correct_Answer']):
        # Display each question, options, and a button to show the answer
        for q_index in shuffled_df.index:
            question = shuffled_df.iloc[q_index]
            st.markdown(f"<h3 style='text-align: left; color: black;'>{question['Question']}</h3>", unsafe_allow_html=True)
            options = [question["Option_A"], question["Option_B"], question["Option_C"], question["Option_D"]]
            st.radio(f"Options for question {q_index + 1}", options, key=q_index)

            # Button to show the answer
            if st.button(f'Show Answer for question {q_index + 1}', key=f'button{q_index}'):
                correct_answer = question[f"Option_{question['Correct_Answer'].upper()}"]
                st.info(f"The correct answer is: {correct_answer}")

    else:
        st.error("The CSV file does not have the required columns. Please upload a file with the required format.")
else:
    st.info("Please upload a CSV file to start the quiz.")

# To run the app, save this script as `quiz_app.py` and run `streamlit run quiz_app.py`.
