import chainlit as cl
import requests

# URL do servidor Flask
FLASK_SERVER_URL = "http://localhost:8080"

@cl.on_message
def main(message: str):
    # Rota para a API de pergunta no PDF
    response = requests.post(f"{FLASK_SERVER_URL}/ask_pdf", json={"query": message})

    if response.status_code == 200:
        result = response.json()
        answer = result.get("answer", "Nenhuma resposta encontrada.")
        sources = result.get("sources", [])
        
        # Enviar resposta para o usuário
        cl.Message(
            content=answer,
            author="PDF QA System"
        ).send()

        # Enviar fontes se disponíveis
        if sources:
            sources_message = "\n\n".join([f"Fonte: {source['source']}\nConteúdo: {source['page_content']}" for source in sources])
            cl.Message(
                content=sources_message,
                author="PDF QA System"
            ).send()
    else:
        cl.Message(
            content="Houve um erro ao processar a sua pergunta.",
            author="PDF QA System"
        ).send()

# Iniciar o Chainlit
if __name__ == "__main__":
    cl.run()
