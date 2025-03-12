import sqlite3
import bcrypt
import streamlit as st
import os
from db_setup import create_tables

# Ustal absolutną ścieżkę do bazy danych
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "users.db")

# Upewnij się, że tabele istnieją
create_tables()

def signup(email: str, password: str, invitation_code: str) -> bool:
    invitation_code = invitation_code.strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT used FROM invitations WHERE code = ?", (invitation_code,))
    result = cursor.fetchone()
    st.write("Sprawdzony kod zaproszenia:", invitation_code, "Wynik:", result)
    if not result:
        st.error("Nieprawidłowy kod zaproszenia.")
        conn.close()
        return False
    elif result[0] == 1:
        st.error("Kod zaproszenia został już użyty.")
        conn.close()
        return False

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_str = hashed.decode('utf-8')
    
    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed_str))
        cursor.execute("UPDATE invitations SET used = 1 WHERE code = ?", (invitation_code,))
        conn.commit()
        st.success("Rejestracja zakończona pomyślnie!")
        conn.close()
        return True
    except sqlite3.IntegrityError:
        st.error("Użytkownik o tym emailu już istnieje.")
        conn.close()
        return False

def login(email: str, password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        st.error("Użytkownik o tym emailu nie istnieje.")
        return False

    stored_hash = result[0]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        st.success("Zalogowano pomyślnie!")
        return True
    else:
        st.error("Niepoprawne hasło.")
        return False
