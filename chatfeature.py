import streamlit as st
import requests
import speech_recognition as sr


BASE_URL = "http://localhost:8080"

def ai_query(query):
    endpoint = f"{BASE_URL}/ai"
    try:
        response = requests.post(endpoint, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Não foi possível se conectar ao servidor para consulta de IA.")
        return {"answer": "Erro na conexão com o servidor."}

def ask_pdf(query):
    endpoint = f"{BASE_URL}/ask_pdf"
    try:
        response = requests.post(endpoint, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Não foi possível se conectar ao servidor para buscar no PDF.")
        return {"answer": "Erro na conexão com o servidor.", "sources": []}

def recognize_speech():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        st.info("Fale alguma coisa...")
        audio = rec.listen(mic)
        try:
            texto = rec.recognize_google(audio, language="pt-BR")
            return texto
        except sr.UnknownValueError:
            st.error("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            st.error(f"Erro ao conectar com o serviço de reconhecimento de fala; {e}")
    return ""

def main():
    st.title("Pergunte sobre o PDF")
    st.header("Consulta em PDF")
    pdf_query = st.text_area("Digite sua consulta em PDF:")
    if st.button("Buscar em PDF"):
        if pdf_query:
            result = ask_pdf(pdf_query)
            st.write("Resposta:", result["answer"])
            if "sources" in result and result["sources"]:
                st.write("Fontes encontradas:")
                for source in result["sources"]:
                    st.write(f"Fonte: {source['source']}")

    # Seção para consulta em PDF usando voz
    st.header("Consulta em PDF via Voz")
    if st.button("Gravar Consulta"):
        query_text = recognize_speech()
        if query_text:
            st.write("Você disse:", query_text)
            result = ask_pdf(query_text)
            st.write("Resposta:", result["answer"])
            if "sources" in result and result["sources"]:
                st.write("Fontes encontradas:")
                for source in result["sources"]:
                    st.write(f"Fonte: {source['source']}")

if __name__ == "__main__":
    main()
