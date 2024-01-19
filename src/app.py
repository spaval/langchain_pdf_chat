from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from src.templates import css, user_template, bot_template

class ResidentialAssistant:
    def __init__(self):
        self.setup_config()
        self.setup_ui()

    def setup_config(self):
        load_dotenv()

    def setup_ui(self):
        st.set_page_config(page_title="Origen P.H.", page_icon="🏢")
        st.write(css, unsafe_allow_html=True)

        if "conversation" not in st.session_state:
            st.session_state.conversation = None

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        st.header("Asistente Unidad Residencial Origen")
        question = st.text_input("¿Qué deseas saber?")
        if question:
            self.handle_user_input(question)

        with st.sidebar:
            st.subheader("Documentos")
            docs = st.file_uploader("Sube tus documentos para proveer de contexto a tu asistente", accept_multiple_files=True)
            
            if st.button("Adjuntar"):
                with st.spinner("Procesando..."):
                    documents_content = self.get_documents_content(docs)
                    documents_chunks = self.get_documents_chunks(documents_content)
                    vector_store_index = self.get_vector_store_index(documents_chunks)
                    st.session_state.conversation = self.get_conversation(vector_store_index)
        
    def get_documents_content(self, docs):
        document_content = ""

        for doc in docs:
            reader = PdfReader(doc)
            for page in reader.pages:
                document_content += page.extract_text()

        return document_content
    
    def get_documents_chunks(self, documents_content):
        text_sppliter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_sppliter.split_text(documents_content)

        return chunks
    
    def get_vector_store_index(self, documents_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(documents_chunks, embeddings)

        return vector_store
    

    def get_conversation(self, vector_store_index):
        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.7)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store_index.as_retriever(),
            memory=memory
        )

        return conversation_chain
    
    def handle_user_input(self, question):
        response = st.session_state.conversation({'question': question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{message}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{message}}", message.content), unsafe_allow_html=True)