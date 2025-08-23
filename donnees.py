import streamlit as st
import requests
import pandas as pd
from app import get_patients


# Navbar
st.markdown("# Données")
st.sidebar.markdown("# Données")

st.title(" Données")

# --- Filtres
col1, col2, col3 = st.columns([1,1,2])
with col1:
    gender = st.selectbox(
        "Genre",
        options=["Tous", "male", "female", "other"],
        index=0
    )
with col2:
    stroke_label = st.selectbox(
        "AVC",
        options=["Tous", "0 - Pas d'AVC", "1 - AVC"],
        index=0
    )
with col3:
    use_max_age = st.checkbox("Filtrer par âge maximum", value=False)
    max_age = st.slider("Âge max", min_value=1, max_value=120, value=80, disabled=not use_max_age)

# Mapping des filtres → paramètres API
gender_param = None if gender == "Tous" else gender
if stroke_label == "Tous":
    stroke_param = None
elif stroke_label.startswith("0"):
    stroke_param = 0
else:
    stroke_param = 1

max_age_param = max_age if use_max_age else None

# --- Appel API
with st.spinner("Chargement des données…"):
    try:
        df = get_patients(gender=gender_param, stroke=stroke_param, max_age=max_age_param)
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")
        st.stop()

if df.empty:
    st.warning("Aucune donnée trouvée pour ces filtres.")
else:
    st.success(f"{len(df):,} enregistrements chargés.")
    st.dataframe(df, use_container_width=True)

    # Bouton de téléchargement
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger CSV", data=csv, file_name="patients.csv", mime="text/csv")


