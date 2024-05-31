from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"


def load(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro: {e}")


def save(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def analyze_sentiment(product):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

    user_prompt = load(f"./data/avaliacoes-{product}.txt")
    print(f"Iniciou a análise de sentimentos do produto {product}")

    messages = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model
        )

        response_text = response.choices[0].message.content
        save(f"./data/analise-{product}.txt", response_text)
        print(f"Processo concluído.\nResultado salvo em ./data/analise-{product}.txt")
    except openai.AuthenticationError as e:
        print(f"Erro de Autenticação: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")


analyze_sentiment("Maquiagem mineral")
