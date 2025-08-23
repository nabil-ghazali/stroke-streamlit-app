import streamlit as st
import requests
#from __future__ import annotations # resoud les problèmes d'annotations : sans cette directive, Python lèverait une erreur, et tu serais obligé d’écrire "A" au lieu de A
import os
from typing import Any, Dict, Optional
import pandas as pd

# === Charger la configuration ===

ENV = st.secrets["ENV"]
API_BASE = st.secrets[ENV]["API_URL"]

# API_BASE = st.secrets.get("API_BASE", os.getenv("API_BASE", "http://127.0.0.1:8000"))
PATIENTS_PATH = "/patients/"
STATS_PATH = "/patients/stats/"

def _build_url(path: str) -> str:
    return API_BASE.rstrip("/") + path

@st.cache_data(ttl=60)
def get_patients(gender: Optional[str]=None, stroke: Optional[int]=None, max_age: Optional[float]=None) -> pd.DataFrame:
    params: Dict[str, Any] = {}
    if gender:
        params["gender"] = gender
    if stroke is not None:
        params["stroke"] = stroke
    if max_age is not None:
        params["max_age"] = max_age

    url = _build_url(PATIENTS_PATH)
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()

    data = r.json()
    # L'API renvoie typiquement une liste de dicts → DataFrame
    df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
    return df

@st.cache_data(ttl=60)
def get_stats() -> Dict[str, Any]:
    url = _build_url(STATS_PATH)
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    stats = r.json()
    # On renvoie tel quel; la page "Statistiques" gère l'affichage
    return stats

# === Définition et navigation des pages ===

Accueil = st.Page("accueil.py", title="Accueil")
Donnees = st.Page("donnees.py", title="Données")
Visualisation = st.Page("visualisation.py", title="Visualisation")
Statistiques = st.Page("statistiques.py", title="Statistiques")

#  Configuration de la navigation
pg = st.navigation([Accueil, Donnees, Visualisation, Statistiques])

# Exécute les pages sélectionnéees
pg.run()


# === Charger la configuration test ===

# ENV = st.secrets["ENV"]
# API_URL = st.secrets[ENV]["API_URL"]


# st.title("Test connexion backend FastAPI")

# try:
#     response = requests.get(f"{API_URL}/patients")
#     response.raise_for_status()
#     data = response.json()
#     st.success("Connexion réussie ")
#     # st.write("Réponse du backend :", data[:5])  # afficher les 5 premiers patients
#     # st.table(data)

# except Exception as e:
#     st.error(f"Erreur de connexion au backend : {e}")