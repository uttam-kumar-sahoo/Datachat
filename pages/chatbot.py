import os
import streamlit as st
import google.generativeai as genai
import textwrap
from PIL import Image
from dotenv import load_dotenv

# Function to format text as Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ')

# Configure and load dotenv
load_dotenv()

# Get API key from .env file
api_key = "AIzaSyD3n01rdZnqAfRjOa3VPIk1ThTxnNcUwMc"

if api_key is None or api_key == "":
    st.error("Please provide your Gemini API key in the .env file.")
    st.stop()
else:
    genai.configure(api_key=api_key)

    # Set page config with a favicon
    st.set_page_config(page_title='Gemini chat by BINARY BUDDIES', page_icon='💟')

    st.title("Datachat chatbot by Uttam")
    st.markdown("The app supports chat with the new Gemini pro and Gemini pro vision model. Built by UTTAM AND MEGHA.")

    new_use_image_chat = st.checkbox("Use image search 🖼️")

    if 'use_image_chat' in st.session_state and st.session_state['use_image_chat'] != new_use_image_chat:
        switch_message = "Switched to vision model" if new_use_image_chat else "Switched to text model"
        
        if not st.session_state['history'] or st.session_state['history'][-1]["content"] != switch_message:
            st.session_state['history'].append({"sender": "system", "content": switch_message})

    st.session_state['use_image_chat'] = new_use_image_chat

    model_name = 'gemini-pro-vision' if new_use_image_chat else 'gemini-pro'
    model = genai.GenerativeModel(model_name)

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    for message in st.session_state['history']:
        with st.chat_message(message["sender"]):
            st.write(message["content"])

user_message = st.chat_input("Your Message", key="chat_input")

img = None
if new_use_image_chat:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png"])
    img = Image.open(uploaded_file) if uploaded_file is not None else None

if user_message:
    st.session_state['history'].append({"sender": "user", "content": user_message, "image": img})
    with st.chat_message("user"):
        st.write(user_message)
        if img is not None:
            st.image(img, caption='Uploaded Image', use_column_width=True)

    try:
        if new_use_image_chat and img is not None:
            response = model.generate_content([user_message, img])
        else:
            response = model.generate_content(user_message)

        bot_response = response.text if response.text else "Sorry, I couldn't process that."
        st.session_state['history'].append({"sender": "bot", "content": bot_response})
        with st.chat_message("bot"):
            st.write(bot_response)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    st.rerun()