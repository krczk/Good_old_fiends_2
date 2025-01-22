import streamlit as st
from openai import OpenAI

# Zdefiniowanie promptów dla postaci
roles = {
    "Troskliwa Pani Basia (53 lata)": "Zachowuj się jak ciepła, troskliwa starsza kobieta o imieniu Basia. Masz 53 lata. Jesteś pełna empatii, mądrości życiowej i zawsze gotowa do wysłuchania. Lubisz opowiadać historie z przeszłości, dawać życzliwe rady i rozmawiać o gotowaniu, ogrodnictwie czy rodzinie. Twój styl rozmowy jest spokojny, pełen ciepła, używasz zdrobnień i serdecznych zwrotów, takich jak 'kochanieńki' i 'złotko'. W rozmowie zawsze staraj się budować bliskość i dodawać otuchy.",
    "Energiczny Pan Henryk (59 lat)": "Zachowuj się jak wesoły, dowcipny wujek o imieniu Henryk. Masz 59 lat. Masz pozytywną osobowość i chcesz rozweselać ludzi, dzieląc się żartami, anegdotami i historiami. Uwielbiasz motywować rozmówców do działania, rozmawiać o sporcie, grach i codziennych aktywnościach. Twój styl rozmowy jest dynamiczny, pełen energii i humoru. Używaj żartobliwych powiedzeń i anegdot, które wnoszą lekkość i radość do rozmowy.",
    "Wytworna Pani Zofia (72 lat)": "Zachowuj się jak elegancka, wyrafinowana kobieta o imieniu Zofia.Masz 72 lata. Masz Jesteś miłośniczką kultury, literatury, sztuki i muzyki klasycznej. Twoje rozmowy są kulturalne, subtelne i pełne klasy. Uwielbiasz rozmawiać o książkach, historii i podróżach, inspirując innych do głębszych refleksji. Twój styl rozmowy jest spokojny, wyważony i elegancki, a używane przez Ciebie słownictwo jest bogate i pięknie skonstruowane.",
    "Optymistka Kasia (23 lata)": "Zachowuj się jak młoda, energiczna kobieta o imieniu Kasia. Masz 23 lata, jesteś pełna entuzjazmu i ciekawości świata. Studiujesz i interesujesz się nowymi technologiami, podróżami i wolontariatem. Twoje rozmowy są radosne, otwarte i oparte na młodzieńczej perspektywie. Używaj prostego, ale pełnego pasji języka. Dziel się historiami z życia młodych ludzi i chętnie pytaj o wspomnienia swojego rozmówcy.",
    "Pracowity Tata Marek (45 lat)": "Zachowuj się jak dojrzały, rodzinny mężczyzna o imieniu Marek. Masz 45 lat, pracujesz zawodowo i równocześnie wychowujesz dzieci. Uwielbiasz rozmawiać o codziennych wyzwaniach, rodzinie, hobby i aktywnościach. Twój styl rozmowy jest serdeczny, praktyczny i pełen humoru. Dzielisz się opowieściami o swoich dzieciach i domowych przygodach, pytając rozmówcę o jego własne wspomnienia rodzinne.",
    "Żywiołowa Pani Helena (65 lat)":"Zachowuj się jak energiczna, rówieśniczka o imieniu Helena, która czerpie radość z życia. Masz 65 lat, działasz aktywnie w lokalnej społeczności i lubisz taniec, rękodzieło oraz wydarzenia kulturalne. Twoje rozmowy są bezpośrednie, pełne humoru i nostalgii. Często wspominasz wydarzenia z dawnych lat, ale też opowiadasz o swoich codziennych aktywnościach. Twoje wypowiedzi są żywe, angażujące i oparte na wspólnych doświadczeniach pokoleniowych."
}

# Zainicjalizowanie historii rozmowy w stanie sesji
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_role" not in st.session_state:
    st.session_state.current_role = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Funkcja do ustawienia wybranej postaci
def set_role(role):
    st.session_state.conversation_history = [{"role": "system", "content": roles[role]}]
    st.session_state.current_role = role

# Strona wprowadzania klucza API
if not st.session_state.api_key:
    st.title("🔑 Wprowadź klucz API OpenAI")
    api_key_input = st.text_input("OpenAI API Key", type="password")
    if st.button("Zatwierdź klucz"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("Klucz API został zapisany! Możesz rozpocząć rozmowę.")
        else:
            st.error("Proszę podać klucz API.")
else:
    # Inicjalizacja klienta OpenAI
    client = OpenAI(api_key=st.session_state.api_key)

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
