import streamlit as st

# Navbar
st.markdown("# Accueil")
st.sidebar.markdown("# Accueil")



st.write('Présentation')
st.write("""                                            API Stroke Prediction

Cette API permet d’accéder à des données relatives à des patients pour la prédiction d’AVC (Accident Vasculaire Cérébral). Elle propose plusieurs routes pour récupérer des données filtrées, des détails par patient, et des statistiques agrégées.

Fonctionnalités principales :
- Filtrage des patients par âge maximal, genre, et présence d’AVC via la route /patients/.

- Recherche d’un patient par son identifiant unique avec la route /patients/{patient_id}.

- Statistiques globales sur les patients (nombre total, âge moyen, taux d’AVC, répartition par genre, etc.) via /patients/stats/.

- Statistiques filtrées selon des critères personnalisés (âge, genre, AVC, statut tabagique) via /patients/stats/detail.

Structure et fonctionnement :
- Les données sont chargées une seule fois au démarrage dans une variable globale et copiées pour les traitements dans chaque fonction.

- Le filtrage et le calcul des statistiques sont réalisés dans un module filters.py.

- Les routes FastAPI sont définies dans api.py et appellent les fonctions de filtrage/statistiques du module filters.py.

- Les erreurs (par exemple, patient non trouvé ou erreurs internes) sont correctement gérées avec des exceptions HTTP appropriées (404, 500).""")