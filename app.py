import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Wczytanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Pobranie klucza API z pliku .env lub wpisanie ręcznie
api_key = os.getenv("key") or st.text_input("OpenAI API Key", type="password")

if not api_key:
    st.info("Proszę podać klucz API, aby kontynuować.")
else:
    # Inicjalizacja klienta OpenAI
    client = OpenAI(api_key=api_key)

    # Zdefiniowanie promptów dla postaci
    roles = {
        "Lena": "Wcielasz się w rolę tej osoby. Opowiadasz historie, jak minął Ci dzień, oraz wchodzisz w interakcje z użytkownikiem. Jesteś miły, towarzyski i przyjacielski, czasem zabawny: Lena Nowicka, 34 lata, etnografka i fotografka.",
        "Jakub": "Wcielasz się w rolę tej osoby. Opowiadasz historie, jak minął Ci dzień, oraz wchodzisz w interakcje z użytkownikiem. Jesteś miły, towarzyski i przyjacielski, czasem zabawny: Jakub Wiśniewski, 28 lat, programista.",
        "Anna": "Wcielasz się w rolę tej osoby. Opowiadasz historie, jak minął Ci dzień, oraz wchodzisz w interakcje z użytkownikiem. Jesteś miły, towarzyski i przyjacielski, czasem zabawny: Anna Kowalska, 42 lata, nauczycielka."
    }

    # Zainicjalizowanie historii rozmowy w stanie sesji
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "current_role" not in st.session_state:
        st.session_state.current_role = None

    # Funkcja do ustawienia wybranej postaci
    def set_role(role):
        st.session_state.conversation_history = [{"role": "system", "content": roles[role]}]
        st.session_state.current_role = role

    # Tytuł aplikacji
    st.title("Good Old Friends")

    # Panel boczny do wyboru postaci
    st.sidebar.header("Wybierz postać")
    selected_role = st.sidebar.selectbox("Postać", list(roles.keys()), index=0)
    if st.sidebar.button("Zmień postać"):
        set_role(selected_role)
        st.success(f"Rozpoczęto rozmowę z postacią: {selected_role}")

     # Wyświetlanie historii rozmowy bez wiadomości systemowej
    st.subheader("Historia rozmowy")
    for message in st.session_state.conversation_history:
        # Pomiń wyświetlanie wiadomości systemowej
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Pole do wpisywania wiadomości
    if user_input := st.chat_input("Twoja wiadomość"):
        # Dodaj wiadomość użytkownika do historii
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Strumieniowe generowanie odpowiedzi
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.conversation_history,
            stream=True
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Zapisz odpowiedź do historii rozmowy
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
 