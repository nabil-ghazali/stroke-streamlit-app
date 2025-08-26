import streamlit as st
import pandas as pd
import plotly.express as px
from app import get_patients
from app import get_stats
# Navbar
st.markdown("# Visualisation")
st.sidebar.markdown("# Visualisation")


# st.title("Visualisations interactives")

# Récupération des données complètes (à partir de la route get_patients)
with st.spinner("Chargement…"): # encapsulation : affiche chargement pendant l'exécution du code
    try:
        df = get_patients() 
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

if df.empty:
    st.warning("Données vides. Vérifie que l'API renvoie bien des patients.")
    st.stop()

# Vérifs colonnes courantes du dataset 
needed = {"age", "stroke"}
missing = needed - set(df.columns)
if missing:
    st.error(f"Colonnes manquantes pour ces visuels : {missing}. Adapte les graphiques en fonction des champs disponibles.")
    st.stop()

# 1) Taux d’AVC par tranche d’âge 
df_local = df.copy()
try:
# regroupement des ages
    avc_by_age = df_local.groupby("age_grouped", dropna=False, observed= False)["stroke"].mean().reset_index()
    avc_by_age["stroke_rate_pct"] = avc_by_age["stroke"] * 100

    fig1 = px.bar(
        avc_by_age,
        x="age_grouped",
        y="stroke_rate_pct",
        labels={"age_grouped": "Tranche d'âge", "stroke_rate_pct": "Taux d'AVC (%)"},
        title="Taux d’AVC par tranche d’âge"
    )
    st.plotly_chart(fig1, width="stretch")
    st.caption("On observe comment le taux d’AVC évolue avec l’âge. Les tranches plus âgées ont généralement un risque accru.")
except Exception as e:
    st.warning(f"Impossible de calculer le taux d’AVC par tranche d’âge (colonnes/valeurs manquantes): {e}")

# 2) Relation glucose <> âge, colorée par AVC
if {"avg_glucose_level", "age", "stroke"}.issubset(df_local.columns):
    fig2 = px.scatter(
        df_local,
        x="age",
        y="avg_glucose_level",
        color=df_local["stroke"].map({0: "No stroke", 1: "Stroke"}),
        labels={"age": "Âge", "avg_glucose_level": "Glucose moyen"},
        title="Âge vs Glucose moyen (couleur = statut AVC)",
        hover_data=[c for c in ["gender", "bmi", "smoking_status"] if c in df.columns]
    )
    st.plotly_chart(fig2, width="stretch")
    st.caption("Visualisation indicative : des niveaux de glucose élevés combinés à un âge avancé peuvent corréler avec un risque accru.")
else:
    st.info("Colonnes `avg_glucose_level` manquante(s). Adapte le second graphique selon les champs disponibles (ex. BMI, hypertension, etc.).")


# Récupération des données complètes (à partir de la route get_stats())
with st.spinner("Chargement…"): # encapsulation : affiche chargement pendant l'exécution du code
    try:
        stats = get_stats() 
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

if df.empty:
    st.warning("Données vides. Vérifie que l'API renvoie bien des patients.")
    st.stop()

# 3) Relation BMI <> AVC

if "stroke_by_bmi" in stats:
    st.subheader("Relation entre BMI et taux d’AVC")

    bmi_df = pd.DataFrame(stats["stroke_by_bmi"])

    fig = px.line(
        bmi_df,
        x="bmi_category",
        y="stroke",
        markers=True,
        title="Évolution du taux d’AVC selon la catégorie de BMI"
    )

    st.plotly_chart(fig, use_container_width=True)
