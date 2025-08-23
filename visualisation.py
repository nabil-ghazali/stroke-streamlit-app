import streamlit as st
import pandas as pd
import plotly.express as px
from app import get_patients

# Navbar
st.markdown("# Visualisation")
st.sidebar.markdown("# Visualisation")


st.title("Visualisations interactives")

# Récupération des données complètes (sans filtre pour une vue globale)
with st.spinner("Chargement…"):
    try:
        df = get_patients()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

if df.empty:
    st.warning("Données vides. Vérifie que l'API renvoie bien des patients.")
    st.stop()

# Vérifs colonnes courantes du dataset (Kaggle stroke)
needed = {"age", "stroke"}
missing = needed - set(df.columns)
if missing:
    st.error(f"Colonnes manquantes pour ces visuels : {missing}. Adapte les graphiques en fonction des champs disponibles.")
    st.stop()

# 1) Taux d’AVC par tranche d’âge (10 ans)
df_local = df.copy()
try:
    df_local["age_bin"] = pd.cut(df_local["age"], bins=list(range(0, 131, 10)), right=False)
    avc_by_age = df_local.groupby("age_bin", dropna=False)["stroke"].mean().reset_index()
    avc_by_age["stroke_rate_pct"] = avc_by_age["stroke"] * 100

    fig1 = px.bar(
        avc_by_age,
        x="age_bin",
        y="stroke_rate_pct",
        labels={"age_bin": "Tranche d'âge", "stroke_rate_pct": "Taux d'AVC (%)"},
        title="Taux d’AVC par tranche d’âge"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("On observe comment le taux d’AVC évolue avec l’âge. Les tranches plus âgées ont généralement un risque accru.")
except Exception:
    st.warning("Impossible de calculer le taux d’AVC par tranche d’âge (colonnes/valeurs manquantes).")

# 2) Relation glucose ↔ âge, colorée par AVC
if {"avg_glucose_level", "age", "stroke"}.issubset(df.columns):
    fig2 = px.scatter(
        df,
        x="age",
        y="avg_glucose_level",
        color=df["stroke"].map({0: "No stroke", 1: "Stroke"}),
        labels={"age": "Âge", "avg_glucose_level": "Glucose moyen"},
        title="Âge vs Glucose moyen (couleur = statut AVC)",
        hover_data=[c for c in ["gender", "bmi", "smoking_status"] if c in df.columns]
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Visualisation indicative : des niveaux de glucose élevés combinés à un âge avancé peuvent corréler avec un risque accru.")
else:
    st.info("Colonnes `avg_glucose_level` manquante(s). Adapte le second graphique selon les champs disponibles (ex. BMI, hypertension, etc.).")
