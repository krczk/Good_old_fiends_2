# config.py
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # Załaduj zmienne z pliku .env

# Pobierz klucz API z zmiennych środowiskowych
API_KEY = st.secrets["API_KEY"]
