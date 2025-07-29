import os
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Load Gemini API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit setup
st.set_page_config(page_title="DOTCOD Interview Bot", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .main {background: linear-gradient(to bottom, #f7f8fc, #e0e7ff);}
    header, footer {visibility: hidden;}
    .stButton button {
        background-color: #6366f1; color: white; border-radius: 8px; padding: 0.5em 1.5em; font-weight: 600;
    }
    .stButton button:hover {background-color: #4f46e5;}
    .stTextInput>div>div>input, .stTextArea textarea {
        border-radius: 8px; border: 1px solid #cbd5e1; padding: 0.5em;
    }
    .stDownloadButton button {
        background-color: #10b981; color: white; border-radius: 8px; padding: 0.5em 1.5em; font-weight: 600;
    }
    .stDownloadButton button:hover {background-color: #059669;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='color:#4f46e5; text-align:center;'>DOTCOD Interview Bot 🤖💬</h1>", unsafe_allow_html=True)

# Upload
resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
process_files = st.button("Process Documents")

# Gemini models
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.7, max_output_tokens=300)

# Process documents
if process_files and resume_file and jd_file:
    try:
        with open("resume_temp.pdf", "wb") as f:
            f.write(resume_file.getbuffer())
        with open("jd_temp.pdf", "wb") as f:
            f.write(jd_file.getbuffer())

        loader_resume = PyPDFLoader("resume_temp.pdf")
        loader_jd = PyPDFLoader("jd_temp.pdf")
        docs = loader_resume.load() + loader_jd.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(split_docs, embeddings)
        vectorstore.save_local("faiss_index")
        st.success("✅ Documents processed and vector store created!")
    except Exception as e:
        st.error(f"Error: {e}")

# Interview Section
if os.path.exists("faiss_index/index.faiss"):
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

    # Session state
    if "qa_pairs" not in st.session_state:
        st.session_state.qa_pairs = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = ""
    if "interview_finished" not in st.session_state:
        st.session_state.interview_finished = False

    st.subheader("Automated Interview Session 💬")

    if not st.session_state.interview_finished:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Generate Next Question"):
                prompt = "Generate an interview question based on the resume and job description."
                result = chain({"question": prompt, "chat_history": []})
                st.session_state.current_question = result["answer"]
                st.session_state.current_answer = ""

        with col2:
            if st.button("Finish Interview"):
                st.session_state.interview_finished = True

        if st.session_state.current_question:
            st.markdown(f"**Question:** {st.session_state.current_question}")
            st.session_state.current_answer = st.text_area("Your Answer", value=st.session_state.current_answer, height=150)

            if st.button("Submit Answer"):
                st.session_state.qa_pairs.append((st.session_state.current_question, st.session_state.current_answer))
                st.session_state.current_question = ""
                st.session_state.current_answer = ""

    if st.session_state.interview_finished:
        st.subheader("Interview Summary 📝")
        summary = ""
        for i, (q, a) in enumerate(st.session_state.qa_pairs, 1):
            st.markdown(f"### Q{i}: {q}")
            st.write(f"Answer: {a}\n")
            summary += f"Q{i}: {q}\nAnswer: {a}\n\n"

        st.success("🎉 You have successfully completed the interview! Thank you for your answers. We wish you all the best from DOTCOD! 🌟")
        st.balloons()
        st.download_button("Download Summary", summary, file_name="interview_summary.txt")
else:
    st.info("Upload resume & JD and click 'Process Documents'.")
