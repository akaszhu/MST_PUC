
# Installing Whisper
# pip install git+ https://github.com/openai/whisper.git -q
# pip install streamlit
import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import easyocr
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY =  os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)
st.title("Whisper App")
# upload audio file with streamlit
def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    print("uploaded_file.name ",uploaded_file.name )
    return uploaded_file.name 
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
if audio_file is not None:
        audio_file = save_uploaded_file(audio_file)
# print(audio_file.name, "tesss")
# upload audio file with streamlit


# st.text("Whisper Model Loaded")
if st.sidebar.button ("Transcribe Audio"):
    if audio_file is not None:
        st.sidebar.success ("Transcribing Audio")
        # transcription = model.transcribe ("C:/Users/Akash/Downloads/This is the leadership quality Dr. APJ Abdul Kalam speech [TubeRipper.com].mp3")
        audio_file = open(audio_file, 'rb')
        transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
        )
        st. sidebar.success ("Transcription Complete")
        prompt = transcript.text + "format this text in dict format,Note:the punctuations are in words. make sure the references are in correct format " 
        response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0,
        )
        messages = [choice.message.content for choice in response.choices]
        print(transcript.text,'\n' ,messages[0])
        st.markdown (messages[0])
    else:
        st.sidebar.error("Please upload an audio file")
st.sidebar.header ("Play Original Audio File")
st.sidebar.audio (audio_file)