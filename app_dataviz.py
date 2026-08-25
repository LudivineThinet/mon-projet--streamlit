import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement direct du dataset "flights" depuis GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    return pd.read_csv(url)

df_flights = load_data()

annee_min = int(df_flights["year"].min())
annee_max = int(df_flights["year"].max())

plage_annees = st.slider(
    "Sélectionnez une plage d'années :",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max)
)

# Filtrage sur la plage choisie
df_filtre = df_flights[
    (df_flights["year"] >= plage_annees[0]) &
    (df_flights["year"] <= plage_annees[1])
]

mois_disponibles = ["Tous les mois"] + list(df_flights["month"].unique())

mois_choisi = st.selectbox(
    "Choisissez un mois :",
    mois_disponibles
)

if mois_choisi != "Tous les mois":
    df_filtre = df_filtre[df_filtre["month"] == mois_choisi]

total_passagers = df_filtre["passengers"].sum()
st.metric(label="Nombre total de passagers", value=f"{total_passagers:,}")

st.subheader("Évolution du nombre de passagers")
evolution = df_filtre.groupby("year")["passengers"].sum()
st.line_chart(evolution)

if st.checkbox("Afficher la heatmap passagers par année/mois"):
    st.subheader("Répartition des passagers par année et par mois")
    
    pivot = df_filtre.pivot(index="month", columns="year", values="passengers")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
    
    st.pyplot(fig)