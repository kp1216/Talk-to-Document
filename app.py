from dotenv import load_dotenv
load_dotenv() # load env variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GEMINI_API"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_responnse(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {"mime_type":uploaded_file.type,
             "data":bytes_data}
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded")



st.header("Talk To Document")
input = st.text_input("Input Prompt : ")
uploaded_file = st.file_uploader("Choose the image of the document...",type = ["jpg","jpeg","png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption = "Uploaded Image",use_column_width=True)

submit = st.button("Get Response")

input_prompt = f"""
You are an expert in understanding any kind of document. we will upload a image of any document and 
you have to answer any question based on the uploaded image"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_responnse(input_prompt,image_data,input)
    st.subheader("Response : ")
    st.write(response)
