from openai import OpenAI
from dotenv import load_dotenv
import os
import json

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


def analyze_transaction(transactions):
    print("1. Executando a análise de transação")

    system_prompt = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Considere o CSV abaixo, onde cada linha é uma transação diferente: {transactions}. "
                       f"Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0
    )

    content = response.choices[0].message.content.replace("'", '"')
    print(f"Conteúdo: {content}")
    json_result = json.loads(content)
    print(f"\nJSON: {json_result}")
    return json_result


def generate_opinion(transaction):
    print("2. Gerando um parecer para cada transação")

    system_prompt = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer 
    uma justificativa para que você identifique uma fraude.
    Transação: {transaction}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """

    messages = [
        {
            "role": "user",
            "content": system_prompt
        }
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=model
    )

    content = response.choices[0].message.content
    print("Finalizou a geração do parecer")
    return content


def generate_recommendation(opinion):
    print("3. Gerando recomendações")

    system_prompt = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da 
    Transação: {opinion}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável. 
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=model
    )

    content = response.choices[0].message.content
    print("Finalizou a geração da recomendação")
    return content


transactions = load("data/transacoes.csv")
analyzed_transactions = analyze_transaction(transactions)

for transaction in analyzed_transactions["transacoes"]:
    if transaction["status"] == "Possível Fraude":
        opinion = generate_opinion(transaction)
        recommendation = generate_recommendation(opinion)
        transaction_id = transaction["id"]
        transaction_product = transaction["nome_produto"]
        transaction_status = transaction["status"]
        save(f"data/transacao-{transaction_id}-{transaction_product}-{transaction_status}.txt", recommendation)
