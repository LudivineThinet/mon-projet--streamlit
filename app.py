import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ============ PARTIE 1 : Authentification ============
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "dashboard_choice" not in st.session_state:
    st.session_state["dashboard_choice"] = "Flights"
if "go_to_dashboard" not in st.session_state:
    st.session_state["go_to_dashboard"] = False

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
    # ============ Sidebar : bienvenue + déconnexion ============
    with st.sidebar:
        st.write(f"Bienvenue, **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
        st.divider()

    # ============ Sidebar : menu de navigation ============
    main_menu_options = ["Accueil", "Dashboard", "Galerie Photos"]

    # Si un raccourci a été cliqué sur l'accueil, on force la sélection via manual_select
    manual_selection = None
    if st.session_state["go_to_dashboard"]:
        manual_selection = main_menu_options.index("Dashboard")
        st.session_state["go_to_dashboard"] = False

    with st.sidebar:
        selected_page = option_menu(
            menu_title="Menu principal",
            options=main_menu_options,
            icons=["house", "bar-chart-fill", "images"],
            default_index=0,
            manual_select=manual_selection,
            key="main_menu"
        )

    # ============ PAGE ACCUEIL ============
    if selected_page == "Accueil":
        st.title("Bienvenue sur l'Application Data")
        st.write("Accédez rapidement à vos projets d'analyse :")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🚕 Dashboard Taxis")
            st.write("Analyse des courses de taxis par quartier.")
            if st.button("Ouvrir le dashboard Taxis"):
                st.session_state["dashboard_choice"] = "Taxis"
                st.session_state["go_to_dashboard"] = True
                st.rerun()

        with col2:
            st.subheader("✈️ Dashboard Flights")
            st.write("Analyse du trafic aérien historique.")
            if st.button("Ouvrir le dashboard Flights"):
                st.session_state["dashboard_choice"] = "Flights"
                st.session_state["go_to_dashboard"] = True
                st.rerun()

    # ============ PAGE GALERIE PHOTOS ============
    elif selected_page == "Galerie Photos":
        st.title("Album Photos")

        tab_flights, tab_taxis = st.tabs(["✈️ Flights", "🚕 Taxis"])

        with tab_flights:
            st.write("Galerie sur le thème de l'aviation :")

            flight_images = [
                "https://images.unsplash.com/photo-1436491865332-7a61a109cc05",
                "https://images.unsplash.com/photo-1569154941061-e231b4725ef1",
                "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957"
            ]

            cols = st.columns(3)
            for index, url in enumerate(flight_images):
                with cols[index % 3]:
                    st.image(url, use_container_width=True, caption=f"Photo {index + 1}")

        with tab_taxis:
            st.write("Galerie sur le thème des taxis :")

            taxi_images = [
                "https://unsplash.com/photos/X-vNntrloZk/download",
                "https://unsplash.com/photos/zwEs8OvU_DE/download",
                "https://unsplash.com/photos/ck6TUc5T92E/download"
            ]

            cols = st.columns(3)
            for index, url in enumerate(taxi_images):
                with cols[index % 3]:
                    st.image(url, use_container_width=True, caption=f"Photo {index + 1}")

    # ============ PAGE DASHBOARD ============
    elif selected_page == "Dashboard":
        st.title("Dashboards d'Analyse")

        dashboard_options = ["Taxis", "Flights"]
        current_dashboard = st.session_state.get("dashboard_submenu", st.session_state["dashboard_choice"])

        if current_dashboard not in dashboard_options:
            current_dashboard = "Flights"

        dashboard_selection = option_menu(
            menu_title=None,
            options=dashboard_options,
            icons=["taxi-front-fill", "airplane-fill"],
            orientation="horizontal",
            default_index=dashboard_options.index(current_dashboard),
            key="dashboard_submenu"
        )
        st.session_state["dashboard_choice"] = dashboard_selection
        st.divider()

        # ---------- DASHBOARD TAXIS ----------
        if dashboard_selection == "Taxis":

            @st.cache_data
            def load_taxis():
                url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
                return pd.read_csv(url)

            df_taxis = load_taxis()

            quartiers = df_taxis["pickup_borough"].dropna().unique()
            quartier_choisi = st.selectbox("Choisissez un quartier de prise en charge :", quartiers)

            df_taxis_filtre = df_taxis[df_taxis["pickup_borough"] == quartier_choisi]

            st.divider()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Nombre de courses", value=df_taxis_filtre.shape[0])
            with col2:
                st.metric(label="Prix moyen", value=f"{df_taxis_filtre['total'].mean():.2f} $")
            with col3:
                st.metric(label="Distance moyenne", value=f"{df_taxis_filtre['distance'].mean():.2f} mi")
            with col4:
                st.metric(label="Pourboire moyen", value=f"{df_taxis_filtre['tip'].mean():.2f} $")

            st.divider()

            st.subheader(f"Aperçu des courses – {quartier_choisi}")
            st.dataframe(df_taxis_filtre.head())

            st.subheader("Distribution du prix des courses")
            fig_taxis = px.histogram(
                df_taxis_filtre,
                x="total",
                nbins=30,
                title=f"Distribution du prix des courses – {quartier_choisi}"
            )
            st.plotly_chart(fig_taxis, use_container_width=True)

            st.subheader("Relation distance / prix")
            fig_scatter = px.scatter(
                df_taxis_filtre,
                x="distance",
                y="total",
                color="payment",
                title=f"Distance vs Prix – {quartier_choisi}",
                labels={"distance": "Distance (mi)", "total": "Prix ($)", "payment": "Paiement"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.subheader("Nombre de courses par quartier")
            courses_par_quartier = df_taxis.dropna(subset=["pickup_borough"]).groupby("pickup_borough").size().reset_index(name="nombre_courses")
            fig_quartiers = px.bar(
                courses_par_quartier,
                x="pickup_borough",
                y="nombre_courses",
                title="Comparaison du nombre de courses par quartier (tous quartiers)"
            )
            st.plotly_chart(fig_quartiers, use_container_width=True)

        # ---------- DASHBOARD FLIGHTS ----------
        elif dashboard_selection == "Flights":

            @st.cache_data
            def load_flights():
                url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
                return pd.read_csv(url)

            df_flights = load_flights()

            annee_min = int(df_flights["year"].min())
            annee_max = int(df_flights["year"].max())

            plage_annees = st.slider(
                "Sélectionnez une plage d'années :",
                min_value=annee_min,
                max_value=annee_max,
                value=(annee_min, annee_max)
            )

            df_filtre = df_flights[
                (df_flights["year"] >= plage_annees[0]) &
                (df_flights["year"] <= plage_annees[1])
            ]

            mois_disponibles = ["Tous les mois"] + list(df_flights["month"].unique())
            mois_choisi = st.selectbox("Choisissez un mois :", mois_disponibles)

            if mois_choisi != "Tous les mois":
                df_filtre = df_filtre[df_filtre["month"] == mois_choisi]

            st.divider()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Total passagers", value=f"{df_filtre['passengers'].sum():,}")
            with col2:
                st.metric(label="Moyenne mensuelle", value=f"{df_filtre['passengers'].mean():,.0f}")
            with col3:
                annee_pic = df_filtre.groupby("year")["passengers"].sum().idxmax()
                st.metric(label="Année du pic de trafic", value=int(annee_pic))

            st.divider()

            st.subheader("Évolution du trafic")
            evolution = df_filtre.groupby("year")["passengers"].sum().reset_index()
            fig_evolution = px.line(
                evolution, x="year", y="passengers",
                markers=True, title="Passagers par année"
            )
            st.plotly_chart(fig_evolution, use_container_width=True)

            st.subheader("Saisonnalité")
            saisonnalite = df_filtre.groupby("month")["passengers"].sum().reset_index()
            fig_mois = px.bar(
                saisonnalite, x="month", y="passengers",
                title="Total par mois (toutes années)"
            )
            st.plotly_chart(fig_mois, use_container_width=True)

            if st.checkbox("Afficher la heatmap passagers par année/mois"):
                st.subheader("Répartition des passagers par année et par mois")
                pivot = df_filtre.pivot(index="month", columns="year", values="passengers")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
                st.pyplot(fig)