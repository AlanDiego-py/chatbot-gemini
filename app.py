# Aplicativo de ChatBot que utiliza a APi do Google Gemini
# O frontend é feito com Streamlit
# O aplicativo mantém o contexto da conversa

# Importante:
# Para rodar o aplicativo:
# 1) Instale as dependências: pip install -r requirements.txt
# 2) Execute o aplicativo: streamlit run app.py
# 3) Acesse o aplicativo no navegador: http://localhost:8501
# 4) Configure a variável de ambiente GOOGLE_API_KEY com sua chave de API do Google

import streamlit as st
import os
import google.generativeai as genai


# Confirguração da Página
st.set_page_config(
    page_title="ChatBot com Google Gemini", 
    page_icon="🤖",
    layout="centered",
)


# Titulo e descrição
st.title("🤖 ChatBot com Google Gemini")
st.caption("Um chatbot simples que utiliza a API do Google Gemini para responder suas perguntas.")
st.markdown("---")

# Carregamento e Validação da API Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except (KeyError, Exception):
    st.error("Chave de API do Google não encontrada. Por favor, configure a variável de ambiente GOOGLE_API_KEY ou adicione a chave no arquivo .streamlit/secrets.toml.")
    st.info("Para mais informações, consulte a documentação: https://cloud.google.com/generative-ai/docs/quickstarts")
    st.stop()
        

# Função principal do chatbot
def main():
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe o histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Entrada do usuário
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Resposta do modelo
        try:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                
                for chunk in model.generate_content(prompt, stream=True):
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response)   
                
                ##response_stream = model.generate_content(prompt, stream=True)
                ##response = st.write_stream(response_stream)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})    
            
        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")
            st.stop()

# Rodar o aplicativo
if __name__ == "__main__":
    main()  