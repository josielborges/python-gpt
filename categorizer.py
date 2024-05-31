from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = "gpt-4"

system_prompt = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.

        # Lista de Categorias Válidas
            - Moda Sustentável
            - Produtos para o Lar
            - Beleza Natural
            - Eletrônicos Verdes
            - Higiene Pessoal

        # Formato da Saída
        Produto: Nome do Produto
        Categoria: apresente a categoria do produto

        # Exemplo de Saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes
    """

user_prompt = input("Apresente o nome de um produto: ")


response = openai.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    model=model,
    temperature=0,
    max_tokens=200
)

print(response.choices[0].message.content)
