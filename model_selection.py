from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

encoder = tiktoken.encoding_for_model(model)


def load(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro: {e}")


system_prompt = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

user_prompt = load("data/lista_de_compras_100_clientes.csv")

token_list = encoder.encode(system_prompt + user_prompt)
tokens_size = len(token_list)
print(f"Número de tokens na entrada: {tokens_size}")
maximum_token_size = 2048

if tokens_size >= 4096 - maximum_token_size:
    model = "gpt-4-1106-preview"

print(f"Modelo escolhido: {model}")

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]

respose = client.chat.completions.create(
    messages=messages,
    model=model
)

print(respose.choices[0].message.content)
