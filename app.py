"""
Resume Experience App

Description: This app compares a job description to a resume and extracts
the number of years of relevant work experience from
the resume.
"""
import streamlit as st
from llm_agent.pdf_chat import pdf_chat_client
from streamlit_pdf_viewer import pdf_viewer
import PyPDF2

def display_chat_history(chat_container, messages):
    with chat_container:
        for _, message_ in enumerate(messages):
            with st.chat_message(message_["role"]):
                st.html(f"<span class='chat-{message_['role']}'></span>")
                st.write(message_["message"])

        st.html(
            """
            <style>
                .stChatMessage:has(.chat-user) {
                    flex-direction: row-reverse;
                    text-align: right;
                }
            </style>
            """
        )

def messages_to_string(messages):
    result = []
    for message in messages:
        role = message.get('role', 'unknown')
        content = message.get('message', '')
        result.append(f"{role}: {content}")
    return "\n".join(result)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.set_page_config(page_title="DocuBot by 3B", layout="wide", page_icon='📚')

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("Chat with your Documents 📝")
st.write("Upload your PDF documents and have conversation with them")

uploaded_file = st.file_uploader("Upload PDF document to chat with", type=["pdf"], key='pdf')

if 'pdf_ref' not in st.session_state or not uploaded_file:
    st.session_state.pdf_ref = None

if uploaded_file and 'resume_content' not in st.session_state:
    resume_content = extract_text_from_pdf(uploaded_file)
    st.session_state['resume_content'] = resume_content
    st.session_state.pdf_ref = uploaded_file
elif not uploaded_file:
    if 'resume_content' in st.session_state:
        del st.session_state.resume_content


input_and_chat, pdf_preview = st.columns([1, 0.9])
with input_and_chat:
    if uploaded_file:
        with st.expander('Chat with PDF', expanded=True):
            chat_container = st.container()
            display_chat_history(chat_container, st.session_state.messages)
            if uploaded_file is not None:
                prompt = st.chat_input('Ask anything about your PDF')
                if prompt:
                    with st.spinner("Generating Response"):
                        results = pdf_chat_client.answer_question(st.session_state.resume_content, prompt, messages_to_string(st.session_state.messages))
                        st.session_state.messages += [{'role': 'user', 'message': prompt}]
                        st.session_state.messages += [{'role': 'assistant', 'message': results}]
                        display_chat_history(chat_container,st.session_state.messages[-2:])

if st.session_state.pdf_ref:
    with pdf_preview:
        with st.expander('PDF Preview',expanded=True):
            binary_data = st.session_state.pdf_ref.getvalue()
            pdf_viewer(input=binary_data,height=800)
