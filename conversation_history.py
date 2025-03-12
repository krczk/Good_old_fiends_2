# conversation_history.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "users.db")

def save_message(user_email: str, agent: str, role: str, content: str):
    """
    Zapisuje pojedynczą wiadomość do tabeli conversation_history.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation_history (user_email, agent, role, content)
        VALUES (?, ?, ?, ?)
    """, (user_email, agent, role, content))
    conn.commit()
    conn.close()

def get_conversation(user_email: str, agent: str):
    """
    Pobiera historię rozmów dla danego użytkownika i wybranej postaci (agenta).
    Zwraca listę słowników.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, created_at FROM conversation_history
        WHERE user_email = ? AND agent = ?
        ORDER BY created_at ASC
    """, (user_email, agent))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1], "created_at": row[2]} for row in rows]
