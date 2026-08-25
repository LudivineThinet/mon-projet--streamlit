# Dashboard Analyse Data - Streamlit

Projet réalisé dans le cadre de ma formation Data Analyst chez Simplon. Il s'agit d'un projet fil rouge simulant la demande d'une entreprise fictive, **DataInsight Solutions**, qui souhaite moderniser la restitution de ses travaux d'analyse via une application web interactive.

## Contexte du projet

L'objectif était de développer une interface web sous Streamlit, versionnée avec Git et hébergée dans le cloud, en couvrant l'ensemble de la chaîne : environnement Python, bases du web (HTML/CSS), création d'une application interactive, sécurisation par authentification, et déploiement public.

## Démo en ligne

🔗 **URL de l'application** : https://mon-projet--app-twholnqb8vkfoqcaukgriu.streamlit.app/

### Identifiants de démonstration

Ce projet est un projet témoin à visée pédagogique, sans donnée sensible. Deux comptes de test sont disponibles :

| Rôle | Nom d'utilisateur | Mot de passe |
|------|-------------------|---------------|
| Utilisateur | `utilisateur` | `mdp123` |
| Administrateur | `admin` | `admin123` |

## Fonctionnalités

- **Authentification** : connexion sécurisée via lecture d'un fichier CSV (`accounts.csv`) et gestion de session (`st.session_state`)
- **Page d'accueil** : raccourcis directs vers les différents dashboards d'analyse
- **Menu de navigation latéral** (`streamlit-option-menu`) : Accueil / Dashboard / Galerie Photos
- **Dashboard Taxis** (dataset `taxis.csv` - Seaborn Data)
  - Filtrage par quartier de prise en charge
  - Indicateurs clés : nombre de courses, prix moyen, distance moyenne, pourboire moyen
  - Distribution des prix, relation distance/prix, comparaison entre quartiers
- **Dashboard Flights** (dataset `flights.csv` - Seaborn Data)
  - Filtrage par plage d'années et par mois
  - Indicateurs clés : total de passagers, moyenne mensuelle, année de pic de trafic
  - Évolution du trafic, saisonnalité, heatmap passagers par année/mois
- **Galerie Photos** : organisée par onglets thématiques (Flights / Taxis), affichage en 3 colonnes

## Stack technique

- **Python** (3.14)
- **Streamlit** - framework web
- **Pandas** - manipulation de données
- **Plotly Express** - graphiques interactifs
- **Matplotlib / Seaborn** - visualisation (heatmap)
- **streamlit-option-menu** - navigation avancée

## Déroulé du projet (activités réalisées)

1. **Environnement Python, Git & HTML/CSS** : mise en place du venv, `.gitignore`, création d'une page portfolio HTML/CSS publiée sur GitHub Pages
2. **Prise en main de Streamlit & Data Visualisation** : premiers dashboards interactifs (widgets, graphiques natifs, Matplotlib/Seaborn, Plotly)
3. **Fonctionnalités avancées & Sécurisation** : mise en page en colonnes, menu de navigation, authentification par CSV
4. **Déploiement** : génération du `requirements.txt`, publication sur Streamlit Cloud

## Installation en local

```bash
# Cloner le dépôt
git clone https://github.com/LudivineThinet/mon-projet--streamlit.git

# Créer et activer l'environnement virtuel
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## Auteure

Ludivine - Formation Data Analyst, Simplon