# config.py
import os
from dotenv import load_dotenv
import streamlit as st



# Pobierz klucz API z zmiennych środowiskowych
API_KEY = st.secrets["API_KEY"]
