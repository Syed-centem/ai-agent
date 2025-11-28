import streamlit as st
import os
import tempfile

# MODERN IMPORTS (Works with latest LangChain)
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Page Configuration
st.set_page_config(page_title="Corporate Knowledge Base Agent", layout="wide")
st.title("🤖 Enterprise Knowledge Base Agent")
st.markdown("### Ask questions from your company documents (HR Policy, Technical Docs, etc.)")

# 2. Sidebar for API Key & File Upload
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload a PDF Document", type="pdf")

# 3. Main Application Logic
if uploaded_file is not None and api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # A. Load and Process Document
        with st.spinner("Indexing document... please wait..."):
            loader = PyPDFLoader(tmp_file_path)
            data = loader.load()
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            text_chunks = text_splitter.split_documents(data)
            
            # Create Embeddings & Vector Store
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_documents(text_chunks, embeddings)
            
            st.success("Document successfully indexed!")

        # B. User Query Interface
        query = st.text_input("What do you want to know from the document?")
        
        if query:
            with st.spinner("Thinking..."):
                # Setup LLM
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
                
                # Define the prompt template (Modern approach)
                prompt = ChatPromptTemplate.from_template("""
                Answer the following question based only on the provided context:
                
                <context>
                {context}
                </context>
                
                Question: {input}
                """)

                # Create the Retrieval Chain (Modern LCEL way)
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = vector_store.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                # Get Answer
                response = retrieval_chain.invoke({"input": query})
                
                st.write("### Answer:")
                st.write(response["answer"])

    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

elif not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
else:
    st.info("Please upload a PDF document to start.")
