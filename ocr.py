# Installing Whisper
# pip install git+ https://github.com/openai/whisper.git -q
# pip install streamlit
import streamlit as st
import openai
from openai import OpenAI
import matplotlib.pyplot as plt
import cv2
import easyocr
from pylab import rcParams
from IPython.display import Image
rcParams['figure.figsize'] = 8, 16
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY =  os.getenv('API_KEY')
client = OpenAI(api_key=API_KEY)
st.title("Whisper App")
# upload audio file with streamlit
def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    print("uploaded_file.name ",uploaded_file.name )
    return uploaded_file.name 
image_file = st.file_uploader("Upload Image", type=["png", "jpeg", "jpg"])
if image_file is not None:
        image_file = save_uploaded_file(image_file)
def extract_text(data):
    extracted_text = []
    for entry in data:
        text = entry[1]  # Extracting the text from the tuple
        extracted_text.append(text)
    return extracted_text
print(image_file, "tesss")
# upload audio file with streamlit
reader = easyocr.Reader(['en'])

# st.text("Whisper Model Loaded")
if st.sidebar.button ("Extract text from image"):
    if image_file is not None:
        st.sidebar.success ("Extracting image")
        # transcription = model.transcribe ("C:/Users/Akash/Downloads/This is the leadership quality Dr. APJ Abdul Kalam speech [TubeRipper.com].mp3")
        # image_file = open(image_file, 'rb')
        output = reader.readtext(image_file)
        output = extract_text(output)
        print("output",output)
        st. sidebar.success ("Extraction Complete")
        prompt = f"""
the below content is extracted from a doctor prescription can you analyze and find the drug names from the list. in a list format
in this format list:
\n doctor name:
\n patient name:
\n patient age:
\n mediceans:
the extracted content:
{output}"""
        response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        messages = [choice.message.content for choice in response.choices]
        print(messages[0])
        st.markdown (messages[0])
    else:
        st.sidebar.error("Please upload an Image")
# st.sidebar.header ("Play Original Audio File")
# st.sidebar.audio (image_file)