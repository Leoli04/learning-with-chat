import streamlit as st
import requests

st.set_page_config(page_title="learning-with-chat", page_icon="👀", layout="wide")
st.header("👀learning-with-chat home")

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

submit=''

if submit:
    API_KEY = st.secrets["API_KEY"]
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    output = query({
        "inputs": "Can you please let us know more details about your ",
    })





