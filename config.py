# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Załaduj zmienne z pliku .env

# Pobierz klucz API z zmiennych środowiskowych
API_KEY = os.getenv("API_KEY")
