from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = "gpt-4"


def categorize_product(product_name, categories):
    system_prompt = f"""
            Você é um categorizador de produtos.
            Você deve assumir as categorias presentes na lista abaixo.
    
            # Lista de Categorias Válidas
                {categories.split(',')}
    
            # Formato da Saída
            Produto: Nome do Produto
            Categoria: apresente a categoria do produto
    
            # Exemplo de Saída
            Produto: Escova elétrica com recarga solar
            Categoria: Eletrônicos Verdes
        """

    response = openai.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": product_name
            }
        ],
        model=model,
        temperature=0,
        max_tokens=200
    )

    return response.choices[0].message.content


categories = input("Informe o nome das categorias")

while (True):
    product_name = input("Apresente o nome de um produto: ")
    if product_name == '':
        print("Encerrando o programa")
        break
    response = categorize_product(product_name, categories)
    print(response)
