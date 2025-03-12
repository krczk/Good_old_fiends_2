# chatgpt_client.py
from openai import OpenAI
from config import API_KEY as default_api_key

def get_client(api_key=None):
    """
    Zwraca instancję klienta OpenAI.
    Jeśli nie podano klucza, użyje wartości z config.py.
    """
    if api_key is None:
        api_key = default_api_key
    return OpenAI(api_key=api_key)

def get_chat_response(conversation_history, api_key=None, model="gpt-4o-mini", stream=True):
    """
    Wysyła historię rozmowy do API ChatGPT i zwraca strumień odpowiedzi.
    """
    client = get_client(api_key)
    return client.chat.completions.create(
        model=model,
        messages=conversation_history,
        stream=stream
    )
