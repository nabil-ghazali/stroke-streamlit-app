import streamlit as st
from app import get_stats
import pandas as pd

# Navbar
st.markdown("# Statistiques")
st.sidebar.markdown("# Statistiques")


st.title(" Statistiques (API)")

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
    # On essaye d'afficher des métriques si certaines clés existent
    col_keys = {
        "total_patients": "Nombre de patients",
        "avg_age": "Âge moyen",
        "stroke_rate": "Taux d'AVC (%)",
        "stroke_percentage": "Taux d'AVC (%)"
    }

    cols = st.columns(3)
    i = 0
    # Afficher quelques métriques connues si présentes
    if "total_patients" in stats:
        cols[i % 3].metric(col_keys["total_patients"], f"{stats['total_patients']:,}")
        i += 1
    if "avg_age" in stats:
        cols[i % 3].metric(col_keys["avg_age"], f"{stats['avg_age']:.1f}")
        i += 1
    # Accepte stroke_rate (0..1) ou stroke_percentage (0..100)
    if "stroke_rate" in stats:
        cols[i % 3].metric(col_keys["stroke_rate"], f"{stats['stroke_rate']*100:.1f}%")
        i += 1
    elif "stroke_percentage" in stats:
        cols[i % 3].metric(col_keys["stroke_percentage"], f"{stats['stroke_percentage']:.1f}%")
        i += 1

    st.subheader("Détails bruts")
    # On normalise pour un affichage tabulaire lisible
    try:
        df_stats = pd.json_normalize(stats)
        st.dataframe(df_stats, use_container_width=True)
    except Exception:
        st.json(stats)
