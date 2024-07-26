import os
import streamlit as st

class Config:
    def __init__(self):
        self.openai_api_key = st.secrets["OPENAI_API_KEY"]
config = Config()
