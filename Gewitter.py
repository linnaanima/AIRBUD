import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
from datetime import datetime, timedelta

def app():
    st.subheader("🌩️ Gewittervorhersage in Deutschland (5 Tage)")

    orte = {
        "Berlin": (52.52, 13.405),
        "Hamburg": (53.55, 10.0),
        "München": (48.14, 11.58),
        "Kiel": (54.32, 10.13),
        "Stuttgart": (48.78, 9.18),
        "Köln": (50.94, 6.96),
        "Dresden": (51.05, 13.74),
        "Leipzig": (51.34, 12.37),
        "Frankfurt am Main": (50.11, 8.68),
        "Nürnberg": (49.45, 11.08),
        "Bremen": (53.08, 8.80),
        "Hannover": (52.38, 9.73),
        "Dortmund": (51.51, 7.46)
    }

    auswahl = st.selectbox("📍 Wähle eine Stadt", list(orte.keys()))
    lat, lon = orte[auswahl]

    heute = datetime.now()
    in_5_tagen = heute + timedelta(days=5)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weathercode,windspeed_10m,precipitation_probability&timezone=Europe/Berlin"
    response = requests.get(url).json()

    try:
        times = pd.to_datetime(response["hourly"]["time"])
        df = pd.DataFrame({
            "Zeit": times,
            "Temperatur (°C)": response["hourly"]["temperature_2m"],
            "Wettercode": response["hourly"]["weathercode"],
            "Wind (km/h)": response["hourly"]["windspeed_10m"],
            "Regenwahrscheinlichkeit (%)": response["hourly"]["precipitation_probability"]
        })
    except Exception as e:
        st.error(f"❌ Fehler beim Abrufen der Wetterdaten: {e}")
        return

    df = df[(df["Zeit"] >= heute) & (df["Zeit"] <= in_5_tagen)]
    df["Datum"] = df["Zeit"].dt.date
    df["Stunde"] = df["Zeit"].dt.hour
    df["Gewitter"] = df["Wettercode"].isin([95, 96, 99])

    # ⚠️ Hinweis bei Gewitter
    gewitterzeiten = df[df["Gewitter"]]["Zeit"].dt.strftime("%Y-%m-%d %H:%M").tolist()
    if gewitterzeiten:
        st.warning("⚡ In {0} wird Gewitter erwartet zu folgenden Zeiten:\n\n{1}".format(
            auswahl, "\n".join(gewitterzeiten)))
    else:
        st.success(f"✅ Kein Gewitter in {auswahl} in den nächsten 5 Tagen vorhergesagt.")

    # 🗓️ Wetter-Tabelle mit Tageszeiten
    st.subheader("📋 Wetterübersicht für die nächsten 5 Tage (Tageszeiten)")

    df_morgens = df[df["Stunde"].between(6, 9)].groupby("Datum")["Temperatur (°C)"].mean().rename("Morgens")
    df_mittags = df[df["Stunde"].between(11, 14)].groupby("Datum")["Temperatur (°C)"].mean().rename("Mittags")
    df_abends = df[df["Stunde"].between(17, 20)].groupby("Datum")["Temperatur (°C)"].mean().rename("Abends")
    df_nachts = df[df["Stunde"].between(0, 3)].groupby("Datum")["Temperatur (°C)"].mean().rename("Nachts")

    df_tagesübersicht = df.groupby("Datum").agg({
        "Wind (km/h)": "mean",
        "Regenwahrscheinlichkeit (%)": "max",
        "Gewitter": "max"
    })

    # Zusammenführen der Tageszeitdaten
    df_tagesübersicht = pd.concat([
        df_tagesübersicht, df_morgens, df_mittags, df_abends, df_nachts
    ], axis=1).reset_index()

    df_tagesübersicht["Gewitter"] = df_tagesübersicht["Gewitter"].replace({True: "⚡ möglich", False: "–"})

    # Spaltenreihenfolge
    df_tagesübersicht = df_tagesübersicht[[
        "Datum", "Morgens", "Mittags", "Abends", "Nachts", "Wind (km/h)", "Regenwahrscheinlichkeit (%)", "Gewitter"
    ]]

    st.dataframe(df_tagesübersicht.style.format({
        "Morgens": "{:.1f} °C",
        "Mittags": "{:.1f} °C",
        "Abends": "{:.1f} °C",
        "Nachts": "{:.1f} °C",
        "Wind (km/h)": "{:.0f}",
        "Regenwahrscheinlichkeit (%)": "{:.0f} %"
    }), use_container_width=True, hide_index=True)

    # 🌍 Heatmap mit allen Orten
    st.subheader("🌍 Mögliche Gewitterregionen in Deutschland")
    heat_data = []
    tooltip_infos = []

    for ort, (lat, lon) in orte.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=weathercode&timezone=Europe/Berlin"
        try:
            r = requests.get(url).json()
            times = pd.to_datetime(r["hourly"]["time"])
            codes = r["hourly"]["weathercode"]
            df_ort = pd.DataFrame({"Zeit": times, "Wettercode": codes})
            df_ort = df_ort[(df_ort["Zeit"] >= heute) & (df_ort["Zeit"] <= in_5_tagen)]
            hat_gewitter = df_ort["Wettercode"].isin([95, 96, 99]).any()
            wert = 1 if hat_gewitter else 0
            heat_data.append([lat, lon, wert])
            tooltip_infos.append((lat, lon, ort, "⚡ Gewitter möglich" if wert else "☀️ Kein Gewitter"))
        except Exception as e:
            st.error(f"Fehler bei Ort {ort}: {e}")

    m = folium.Map(location=[51.0, 10.0], zoom_start=6)
    HeatMap(heat_data, radius=15, max_zoom=9).add_to(m)
    for lat, lon, ort, info in tooltip_infos:
        folium.Marker([lat, lon], tooltip=info).add_to(m)

    folium_static(m, height=600)

    st.markdown("""
           
    > 🔍 Quelle: [OPEN-METEO](https://api.open-meteo.com)
        """
                    )