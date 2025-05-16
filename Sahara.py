import streamlit as st
import pandas as pd
import requests
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from PIL import Image
from io import BytesIO

# Caching für bessere Performance
@st.cache_data
def get_location(ort):
    geolocator = Nominatim(user_agent="sahara-app")
    return geolocator.geocode(f"{ort}, Deutschland")

def app():

    orte = [
        "Berlin", "Hamburg", "München", "Köln", "Frankfurt am Main",
        "Stuttgart", "Leipzig", "Dresden", "Bremen", "Hannover",
        "Nürnberg", "Dortmund", "Essen", "Kiel", "Rostock",
        "Freiburg", "Erfurt", "Regensburg"
    ]

    # Nutzer kann Schwellenwert selbst wählen
    aod_threshold = st.slider("AOD-Schwellenwert für Saharastaub", 0.1, 1.0, 0.39, step=0.01)

    heat_data = []
    warnungen = []
    df_liste = []
    saharastaub_orte = []

    st.info("Lade Saharastaubdaten …")

    for ort in orte:
        location = get_location(ort)
        if not location:
            continue
        lat = location.latitude
        lon = location.longitude

        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}&hourly=aerosol_optical_depth"
        )

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            data = response.json()
            aod_values = data.get("hourly", {}).get("aerosol_optical_depth", [])
            aod_values_cleaned = [v for v in aod_values if isinstance(v, (float, int))]

            if not aod_values_cleaned:
                continue

            max_aod = max(aod_values_cleaned)
            sahara_status = "🌫️ Ja" if max_aod > aod_threshold else "✅ Nein"

            if max_aod > aod_threshold:
                warnungen.append(f"⚠️ {ort}: AOD {max_aod:.2f} → Hohe Saharastaubbelastung!")
                saharastaub_orte.append(ort)

            df_liste.append({
                "Ort": ort,
                "Latitude": lat,
                "Longitude": lon,
                "AOD max": max_aod,
                "Saharastaub": sahara_status
            })

        except Exception as e:
            st.error(f"Fehler bei {ort}: {str(e)}")
            continue

    df = pd.DataFrame(df_liste)

    st.subheader("📊 Übersicht der Orte")
    if not df.empty:
        df_display = df[["Ort", "AOD max", "Saharastaub"]].copy()
        df_display["AOD max"] = df_display["AOD max"].apply(lambda x: f"{x:.2f}")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("Keine Daten verfügbar.")

    if saharastaub_orte:
        st.subheader("🌫️ Orte mit Saharastaub:")
        st.success(", ".join(saharastaub_orte))
    else:
        st.write(f"Es wurden keine Orte mit Saharastaub (AOD ≥ {aod_threshold}) gefunden.")

    # Heatmap vorbereiten
    df["AOD max"] = df["AOD max"].astype(float)
    df_heat = df[df["AOD max"] >= aod_threshold].copy()

    if not df_heat.empty:
        max_val = df_heat["AOD max"].max()
        min_val = df_heat["AOD max"].min()
        df_heat["AOD_norm"] = (df_heat["AOD max"] - min_val) / (max_val - min_val + 1e-5)

        heatmap_data = df_heat[["Latitude", "Longitude", "AOD_norm"]].values.tolist()

        m = folium.Map(location=[51.0, 10.0], zoom_start=6)
        HeatMap(
            heatmap_data,
            radius=25,
            blur=10,
            max_zoom=6,
            min_opacity=0.3
        ).add_to(m)

        # Optional: Marker mit AOD-Werten hinzufügen
        for _, row in df_heat.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"{row['Ort']}: AOD {row['AOD max']:.2f}"
            ).add_to(m)

        st.components.v1.html(m._repr_html_(), height=600)

    else:
        st.warning(f"Keine erhöhten Saharastaubwerte (AOD ≥ {aod_threshold}) für die Heatmap gefunden.")

    # --- OPENMETEO Einstufung anzeigen ---
    st.markdown("""
     > 🔍 Quelle: [OPEN-METEO](https://air-quality-api.open-meteo.com/v1/air-quality?)
    """)