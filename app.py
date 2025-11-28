import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Page Configuration
st.set_page_config(page_title="Corporate Knowledge Base", layout="wide")
st.title("🤖 Enterprise Knowledge Base Agent")

# 2. Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# 3. Main Logic
if uploaded_file and api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        with st.spinner("Processing document..."):
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            
            # Embeddings & Vector Store
            vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
            retriever = vectorstore.as_retriever()

            # Retrieval Chain
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            
            system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}"),
            ])
            
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            
            st.success("Document Loaded!")

        # Q&A Area
        user_question = st.text_input("Ask a question about your document:")
        if user_question:
            response = rag_chain.invoke({"input": user_question})
            st.write("### Answer")
            st.write(response["answer"])

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

elif not api_key:
    st.warning("Please enter your OpenAI API Key.")
else:
    st.info("Upload a PDF to start.")
