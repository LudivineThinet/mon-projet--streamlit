import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Initialisation de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Chargement des comptes
@st.cache_data
def load_accounts():
    return pd.read_csv("accounts.csv")

def authenticate(username_input, password_input):
    accounts_df = load_accounts()
    user_match = accounts_df[
        (accounts_df["name"] == username_input) &
        (accounts_df["password"] == password_input)
    ]
    return not user_match.empty

if not st.session_state["logged_in"]:
    st.title("Connexion à l'Application Data")
    st.subheader("Veuillez vous identifier pour accéder au contenu")

    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(username_input, password_input):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.success(f"Bienvenue {username_input} !")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    # Sidebar : bienvenue + déconnexion
    with st.sidebar:
        st.write(f"Bienvenue, **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
        st.divider()

    # Sidebar : menu de navigation
    with st.sidebar:
        selected_page = option_menu(
            menu_title="Menu principal",
            options=["Accueil", "Galerie Photos"],
            icons=["house", "images"],
            default_index=0
        )

    # Contenu principal selon la page choisie
    if selected_page == "Accueil":
        st.title("Page d'Accueil Réservée")
        st.write("Ce contenu est uniquement accessible aux utilisateurs authentifiés.")


    elif selected_page == "Galerie Photos":
        st.title("Album Photos")
        st.write("Galerie de chats sur 3 colonnes :")

        image_urls = [
            "https://static.streamlit.io/examples/cat.jpg",
            "https://static.streamlit.io/examples/dog.jpg",
            "https://static.streamlit.io/examples/owl.jpg"
        ]

        cols = st.columns(3)
        for index, url in enumerate(image_urls):
            with cols[index % 3]:
                st.image(url, use_container_width=True, caption=f"Photo {index + 1}")