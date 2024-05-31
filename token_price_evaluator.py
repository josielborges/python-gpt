import tiktoken

# Token prices at 2024-05-31
# See more at https://openai.com/api/pricing/
token_prices = {
    "gpt-4o": 0.005 / 1000,
    "gpt-4-turbo": 0.01 / 1000,
    "gpt-4": 0.03 / 1000,
    "gpt-3.5-turbo": 0.0005 / 1000
}


def calculate_token_prices(prompt, detailed=False):
    print(f"Prompt: {prompt}")
    print("------ ")
    if not detailed:
        print(f"Modelo        | Tokens | Custo")
    for model, price in token_prices.items():
        encoder = tiktoken.encoding_for_model(model)
        token_list = encoder.encode(prompt)

        if detailed:
            print("Modelo: ", model.upper())
            print("Lista de Tokens: ", token_list)
            print("Número de tokens: ", len(token_list))
            print(f"Custo: ${(len(token_list) * price):.7f}".rstrip("0"))
            print("------ ")
        else:
            print(
                f"{model.upper().ljust(14, ' ')}| "
                f"{str(len(token_list)).rjust(6, ' ')} | "
                f"${(len(token_list) * price):.7f}".rstrip('0'))


prompt = '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to 
make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, 
remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem 
Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem 
Ipsum.'''

calculate_token_prices(prompt)
