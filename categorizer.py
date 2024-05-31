from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = openai.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """
            Classifique o produto abaixo em uma das categorias: Higiene Pessoal, Moda ou Casa de uma descrição da categoria.
            """
        },
        {
            "role": "user",
            "content": """
            Escova de dentes de bambu
            """
        }
    ],
    model="gpt-4",
    temperature=0,
    max_tokens=200,
    n=3
)

for i in range(0, 3):
    print(response.choices[i].message.content)
