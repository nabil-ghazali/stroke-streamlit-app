import streamlit as st
import pandas as pd
from app import get_stats

st.markdown("# Statistiques")
st.sidebar.markdown("# Statistiques")

with st.spinner("Chargement des statistiques…"):
    try:
        stats = get_stats()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

if not isinstance(stats, dict) or len(stats) == 0:
    st.warning("Le format des statistiques n'est pas un dictionnaire. Affichage brut ci-dessous :")
    st.json(stats)
else:
    st.subheader("Métriques principales")
    cols = st.columns(3)
    if "total_patients" in stats:
        cols[0].metric("Nombre de patients", f"{stats['total_patients']:,}")
    if "avg_age" in stats:
        cols[1].metric("Âge moyen", f"{stats['avg_age']:.1f}")
    if "stroke_rate" in stats:
        cols[2].metric("Taux d'AVC (%)", f"{stats['stroke_rate']:.1f}%")

    if "age_min" in stats and "age_max" in stats and "age_std" in stats:
        cols2 = st.columns(3)
        cols2[0].metric("Âge minimum", f"{stats['age_min']:.1f}")
        cols2[1].metric("Âge maximum", f"{stats['age_max']:.1f}")
        cols2[2].metric("Écart-type âge", f"{stats['age_std']:.1f}")

    # --- Répartition AVC global ---
    if "stroke_counts" in stats:
        st.subheader("Répartition AVC global")
        stroke_df = pd.DataFrame(list(stats["stroke_counts"].items()), columns=["Statut", "Nombre"])
        st.dataframe(stroke_df)

    # --- Répartition par genre ---
    if "gender_distribution" in stats:
        st.subheader("Répartition par genre")
        gender_df = pd.DataFrame(list(stats["gender_distribution"].items()), columns=["Genre", "Nombre"])
        st.dataframe(gender_df)

    # --- AVC par genre avec pourcentage ---
    if "gender_stroke" in stats:
        st.subheader("AVC par genre")
        gender_stroke_df = pd.DataFrame(stats["gender_stroke"])
        gender_stroke_df["stroke"] = gender_stroke_df["stroke"].map({0: "Pas d'AVC", 1: "AVC"})
        st.dataframe(gender_stroke_df[["gender", "stroke", "count", "percent"]])

    # --- AVC par statut tabac avec pourcentage ---
    if "smoking_stroke" in stats:
        st.subheader("AVC par statut tabac")
        smoking_df = pd.DataFrame(stats["smoking_stroke"])
        smoking_df["stroke"] = smoking_df["stroke"].map({0: "Pas d'AVC", 1: "AVC"})
        st.dataframe(smoking_df[["smoking_status", "stroke", "count", "percent"]])

    # --- AVC par BMI
    if "stroke_by_bmi" in stats:
        st.subheader("AVC par BMI")
        stroke_by_bmi_df = pd.DataFrame(list(stats["stroke_by_bmi"].items()), columns=["bmi", "stroke"])
        st.dataframe(stroke_by_bmi_df[["bmi", "stroke"]])

    # # --- Détails bruts ---
    # st.subheader("Détails bruts")
    # st.json(stats)
