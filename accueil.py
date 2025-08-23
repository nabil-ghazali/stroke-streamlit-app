import streamlit as st

# Navbar
st.markdown("# Accueil")
st.sidebar.markdown("# Accueil")

st.title("Stroke Prediction — Tableau de bord")
st.markdown("""
Bienvenue ! Cette application permet d’explorer les données patients relatives à l’AVC (stroke) :
- **Données** : filtrer et visualiser le jeu de données via l’API
- **Visualisations** : graphiques interactifs (Plotly)
- **Statistiques** : indicateurs clés calculés côté API
""")
