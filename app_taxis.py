import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
    return pd.read_csv(url)

st.title("Dashboard Analyse Taxis - Ludivine")

df = load_data()


# Liste des quartiers disponibles
quartiers = df["pickup_borough"].unique()

quartier_choisi = st.selectbox(
    "Choisissez un quartier de prise en charge :",
    quartiers
)

# Filtrage du dataframe
df_filtre = df[df["pickup_borough"] == quartier_choisi]

st.dataframe(df_filtre.head())

st.metric(label="Nombre total de courses", value=df_filtre.shape[0])