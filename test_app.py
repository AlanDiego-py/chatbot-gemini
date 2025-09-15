import pytest
import streamlit as st
import google.generativeai as genai
from app import main


# testando se a chave do Gemini está configurada corretamente
def test_gemini_key():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    assert api_key is not None and isinstance(api_key, str) 

# testando se a função main roda sem erros
def test_main_function(monkeypatch):
    monkeypatch.setattr("streamlit.chat_input", lambda *args, **kwargs: None)
    main()