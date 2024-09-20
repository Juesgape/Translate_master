import requests
import os
from src.clean_response import clean_response

def translate_content(data_in_array, is_title = False):
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Set API key from environment variables

    prompt = ""

    if is_title:
        prompt = "Actúa como una persona encargada de mejorar el SEO de una página web e-commerce de ropa y mejora todos estos textos en inglés, haciendo que suenen natural para los usuarios estadounidenses manteniendo su estructura html. Separa cada respuesta con el identificador ---"
    else:
        prompt = "Actúa como una persona encargada de mejorar el SEO de una página web e-commerce de ropa y mejora todos estos textos en inglés, haciendo que suenen natural para los usuarios estadounidenses y que lleven la misma estructura Men's... o Women's... Separa cada respuesta con el identificador ---"

    if not openai_api_key:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"{prompt}"
            },
            {
                "role": "user",
                "content": f"{data_in_array}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        raw_response = response.json()['choices'][0]['message']['content']
        processed_response = clean_response(raw_response)
        return processed_response
    else:
        print("Error:", response.status_code, response.text)
        return None