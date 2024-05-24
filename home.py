import streamlit as st

from core.HF_handle import generate_response

st.set_page_config(page_title="learning-with-chat", page_icon="👀", layout="wide")
st.header("👀learning-with-chat home")

def init_chat():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# 侧边栏展示信息
with st.sidebar:
    st.header("model")
    #模型选择
    selectModel = st.selectbox("choose a model: ",
                 ("meta-llama/Meta-Llama-3-8B-Instruct","impira/layoutlm-document-qa","aya-23-8B"),
                  placeholder="meta-llama/Meta-Llama-3-8B-Instruct")
    hf_api_key=st.text_input(
        "HuggingFace API key",
        help="- [get HuggingFace API key](https://huggingface.co/settings/tokens)",
    )
    # 模型参数
    st.subheader('Models and parameters')
    temperature = st.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    st.button('Clear Chat History', on_click=init_chat)

    # 模型地址
    st.header("resource")
    st.write('''
    - [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B)
    - [impira/layoutlm-document-qa](https://huggingface.co/impira/layoutlm-document-qa)
    - [aya-23-8B](https://huggingface.co/CohereForAI/aya-23-8B)
    ''')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    init_chat()

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input("your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)




# 根据输入做出响应
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt,selectModel,hf_api_key)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                # 响应过程中展示
                placeholder.markdown(full_response)
            # 展示完整响应
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)




#
# def query(payload):
#  	with open(payload["image"], "rb") as f:
#   		img = f.read()
# 		payload["image"] = base64.b64encode(img).decode("utf-8")
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
#
# output = query({
#     "inputs": {
# 		"image": "cat.png",
# 		"question": "What is in this image?"
# 	},
# })





