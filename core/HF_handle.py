import requests
import streamlit as st


@st.cache_data
def getHeaders(hf_api_key):
    # API_KEY = st.secrets["API_KEY"]
    return {"Authorization": f"Bearer {hf_api_key}"}

@st.cache_data
def getApi_url(selectModel: str):
    return f"https://api-inference.huggingface.co/models/{selectModel}"

def query(payload,api_url,hf_api_key):
    response = requests.post(api_url, headers=getHeaders(hf_api_key), json=payload)
    return response.json()


def generate_response(prompt_input, selectModel,hf_api_key):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"


    output = query({
        "inputs": f" {prompt_input}  ",
    },getApi_url(selectModel),hf_api_key)
    generated_text:str = output[0]['generated_text']
    if generated_text:
        lines = generated_text.split('\n')
    return lines[1:]
