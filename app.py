import streamlit as st
import json
from PIL import Image
from code_util import execute_code
from solar import solar_grade
from gpt_util import gpt_grade
from hw_parser import get_head_contents

hw_dict = get_head_contents("hw.md")

hw_keys = ["Home"] + list(hw_dict.keys())
page = st.sidebar.selectbox("Select a quiz:", hw_keys)

# Home Display the student codes
if page == "Home":
    image = Image.open('qr.jpg')
    st.title("AI-TA Page")
    st.write("Welcome to the AI-TA platform!")
    st.image(image, caption="QR Code for AI-TA platform!")
elif page in hw_keys:
    st.title(page)
    st.write("Please enter Python code.")
    hw_desc = hw_dict[page]['description']
    st.markdown(hw_desc)

    # student_id = st.text_input("Student ID:")
    student_code = st.text_area("Write Code:", height=300)

    if st.button("Consult AI-TA"):
        if student_code:
            test_output, error = execute_code(student_code)
            if error:
                st.error(f"Code execution failed: {error}")
            elif test_output is not None:
                st.success(f"Code execution successful: {test_output}")
                if page != 'Tic-tac-toe':
                    st.info("⏳ Checking your code with AI-TA (SOLAR)...")
                    ta_comments = solar_grade(hw_desc, student_code, test_output, error)
                    st.markdown(ta_comments)
    
                    st.info("⏳ Checking your code with AI-TA (GPT)...")
                    ta_comments = gpt_grade(hw_desc, student_code, test_output, error)
                    st.markdown(ta_comments)

                    st.success("🎉 AI-TA finished grading your code!")
            else:
                st.error("Code execution failed. Please check your code.")
