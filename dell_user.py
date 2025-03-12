import sqlite3
import os

def delete_user_data(user_email: str):
    # Ustal ścieżkę do bazy danych (przyjmujemy, że plik bazy znajduje się w tym samym folderze)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "users.db")
    
    # Połącz się z bazą danych
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Usuń historię rozmów dla danego użytkownika
    cursor.execute("DELETE FROM conversation_history WHERE user_email = ?", (user_email,))
    print(f"Usunięto historię rozmów dla użytkownika: {user_email}")
    
    # Usuń konto użytkownika (rekord w tabeli users)
    cursor.execute("DELETE FROM users WHERE email = ?", (user_email,))
    print(f"Usunięto konto użytkownika: {user_email}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    user_email = input("Podaj email użytkownika, którego dane chcesz usunąć: ").strip()
    delete_user_data(user_email)
    print("Dane użytkownika zostały usunięte z bazy.")
