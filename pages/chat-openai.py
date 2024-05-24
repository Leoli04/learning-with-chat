import streamlit as st
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

def generate_response(uploaded_file, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode()]
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))


# Page title
st.set_page_config(page_title='💬learning with chat by openai')
st.title('💬 openai chat🦜🔗')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.sidebar.warning(
    "Enter your OpenAI API key in the sidebar. You can get a key at"
    " https://platform.openai.com/account/api-keys.",icon='⚠'
)

# File upload
uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",)


# Query text
result = []
with st.form('myform'):
    query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.')
    submitted = st.form_submit_button('Submit')

    if not (query_text and openai_api_key):
        st.warning("Enter your OpenAI API key in the sidebar and Enter your question",icon="⚠")
        st.stop()

    if submitted and openai_api_key.startswith('sk-') and not uploaded_file:
        result.append(generate_response(query_text))

    if submitted and uploaded_file and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)

if len(result):
    st.info(response)