import sqlite3
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "users.db")

def add_invitation(code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO invitations (code) VALUES (?)", (code,))
        conn.commit()
        print(f"Kod zaproszenia '{code}' został dodany pomyślnie!")
    except sqlite3.IntegrityError as e:
        print("Błąd: Kod zaproszenia już istnieje lub wystąpił inny problem:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Użycie: python add_invitation.py <kod_zaproszenia>")
        sys.exit(1)
    code = sys.argv[1]
    add_invitation(code)
