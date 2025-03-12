# app.py
import streamlit as st
from auth import signup, login
from chatgpt_client import get_chat_response
from conversation import set_role, roles, welcome_messages
from config import API_KEY as config_api_key
from conversation_history import get_conversation, save_message

st.title("Aplikacja Chat z rejestracją na zaproszenie oraz historią rozmów")

# JEŚLI UŻYTKOWNIK NIE JEST ZALOGOWANY – INTERFEJS LOGOWANIA/REJESTRACJI
if "user" not in st.session_state:
    st.subheader("Logowanie / Rejestracja")
    auth_mode = st.radio("Wybierz opcję:", ("Logowanie", "Rejestracja"))
    email = st.text_input("Email")
    password = st.text_input("Hasło", type="password")
    
    if auth_mode == "Rejestracja":
        invitation_code = st.text_input("Kod zaproszenia")
        if st.button("Zarejestruj"):
            if signup(email, password, invitation_code):
                st.session_state["user"] = email
    else:  # Logowanie
        if st.button("Zaloguj"):
            if login(email, password):
                st.session_state["user"] = email

# JEŚLI UŻYTKOWNIK JEST ZALOGOWANY – INTERFEJS CZATU
else:
    user_email = st.session_state["user"]
    st.write("Zalogowany jako:", user_email)
    
    # Ustawienie klucza API, jeśli nie jest ustawiony
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.session_state.api_key = config_api_key

    st.title("Porozmawiajmy!")
    st.subheader("Wybierz postać, z którą chcesz porozmawiać")
    
    st.sidebar.header("Wybierz postać")
    available_agents = list(roles.keys())

    # Jeśli aktualny agent nie jest ustawiony, wybieramy pierwszego i ładujemy historię rozmowy
    if "current_agent" not in st.session_state:
        first_agent = available_agents[0]
        st.session_state.current_agent = first_agent
        set_role(first_agent, st.session_state)
        conv_history = get_conversation(user_email, first_agent)
        if not conv_history:
            conv_history = [
                {"role": "system", "content": roles.get(first_agent, "")},
                {"role": "assistant", "content": welcome_messages.get(first_agent, "czesc jak sie masz")}
            ]
        st.session_state.conversation_history = conv_history

    # Selectbox ustawiony na aktualnego agenta
    selected_role = st.sidebar.selectbox(
        "Osoby do wyboru:", 
        available_agents, 
        index=available_agents.index(st.session_state.current_agent)
    )
    
    # Jeśli użytkownik wybierze innego agenta, odświeżamy kontekst rozmowy
    if st.sidebar.button("Wybierz"):
        st.session_state.current_agent = selected_role
        set_role(selected_role, st.session_state)
        conv_history = get_conversation(user_email, selected_role)
        if not conv_history:
            conv_history = [
                {"role": "system", "content": roles.get(selected_role, "")},
                {"role": "assistant", "content": welcome_messages.get(selected_role, "czesc jak sie masz")}
            ]
        st.session_state.conversation_history = conv_history
        st.success(f"Rozpoczęto rozmowę z: {selected_role}")

    # Dodatkowa weryfikacja – jeśli z jakiegoś powodu historia nie istnieje, ładujemy ją
    if "conversation_history" not in st.session_state or not st.session_state.conversation_history:
        current_agent = st.session_state.get("current_agent")
        if current_agent:
            conv_history = get_conversation(user_email, current_agent)
            if not conv_history:
                conv_history = [
                    {"role": "system", "content": roles.get(current_agent, "")},
                    {"role": "assistant", "content": welcome_messages.get(current_agent, "czesc jak sie masz")}
                ]
            st.session_state.conversation_history = conv_history
        else:
            st.session_state.conversation_history = []

    # Wyświetlanie historii rozmowy (pomijamy wiadomości systemowe)
    st.text("Historia rozmowy:")
    for message in st.session_state.conversation_history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Pole wejściowe wiadomości użytkownika – z unikalnym kluczem
    if user_input := st.chat_input("Twoja wiadomość", key="user_chat_input"):
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        current_agent = st.session_state.get("current_agent", "Nieustalony")
        save_message(user_email, current_agent, "user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)
        
        stream = get_chat_response(
            st.session_state.conversation_history,
            api_key=st.session_state.api_key
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        save_message(user_email, current_agent, "assistant", response)
