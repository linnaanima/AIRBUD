import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def app():

    def parse_pollen_value(value):
        if '-' in value:
            parts = value.split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        return float(value) if value != '0' else 0

    def pollen_level_label(value):
        if value <= 0.5:
            return "🟩 Gering"
        elif value <= 2:
            return "🟧 Mäßig"
        else:
            return "🟥 Stark"

    # Abruf DWD JSON
    def get_pollen_data(region_id, partregion_id):
        try:
            response = requests.get("https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json")
            if response.status_code != 200:
                st.error(f"❌ Fehler beim Abruf der DWD-Daten: {response.status_code}")
                return None
            data = response.json()
            for region in data.get("content", []):
                if str(region.get("region_id")) == region_id and str(region.get("partregion_id")) == partregion_id:
                    pollen_daten = region.get("Pollen", {})
                    pollen_vorhersage = []
                    for pollenart, werte in pollen_daten.items():
                        pollen_vorhersage.append({
                            "Pollenart": pollenart,
                            "Heute": werte.get("today", "-1"),
                            "Morgen": werte.get("tomorrow", "-1"),
                            "Übermorgen": werte.get("dayafter_to", "-1")
                        })
                    return pollen_vorhersage
            st.warning("⚠️ Keine Pollen-Daten für diese Region gefunden.")
            return None
        except Exception as e:
            st.error(f"❌ Fehler beim Verarbeiten der DWD-Daten: {e}")
            return None

    # Koordinaten (optional erweiterbar)
    coordinates = {
        "Inseln und Marschen": {"lat": 54.5, "lon": 8.9},
        "Geest,Schleswig-Holstein und Hamburg": {"lat": 54.3, "lon": 9.9},
        "Rhein-Main": {"lat": 50.1, "lon": 8.7},
        "Mainfranken": {"lat": 49.8, "lon": 9.9},
        "Mecklenburg-Vorpommern": {"lat": 53.6, "lon": 13.4},
        "Westl. Niedersachsen/Bremen": {"lat": 53.1, "lon": 8.6},
        "Östl. Niedersachsen": {"lat": 52.6, "lon": 10.3},
        "Rhein.-Westfäl. Tiefland": {"lat": 51.2, "lon": 6.8},
        "Ostwestfalen": {"lat": 52.0, "lon": 8.3},
        "Mittelgebirge NRW": {"lat": 51.5, "lon": 7.6},
        "Brandenburg und Berlin": {"lat": 52.5, "lon": 13.4},
        "Tiefland Sachsen-Anhalt": {"lat": 51.9, "lon": 11.6},
        "Harz": {"lat": 51.8, "lon": 10.8},
        "Tiefland Thüringen": {"lat": 50.9, "lon": 11.0},
        "Mittelgebirge Thüringen": {"lat": 50.7, "lon": 10.7},
        "Tiefland Sachsen": {"lat": 51.3, "lon": 13.0},
        "Mittelgebirge Sachsen": {"lat": 50.8, "lon": 12.8},
        "Nordhessen und hess. Mittelgebirge": {"lat": 51.3, "lon": 9.5},
        "Rhein-Main": {"lat": 50.1, "lon": 8.7},
        "Rhein, Pfalz, Nahe und Mosel": {"lat": 50.4, "lon": 7.5},
        "Mittelgebirgsbereich Rheinland-Pfalz": {"lat": 50.2, "lon": 7.2},
        "Saarland": {"lat": 49.4, "lon": 6.9},
        "Oberrhein und unteres Neckartal": {"lat": 48.9, "lon": 8.4},
        "Hohenlohe / mittlerer Neckar / Oberschwaben": {"lat": 49.1, "lon": 9.5},
        "Mittelgebirge Baden-Württemberg": {"lat": 48.4, "lon": 8.2},
        "Allgäu / Oberbayern / Bay. Wald": {"lat": 47.5, "lon": 10.0},
        "Donauniederungen": {"lat": 48.0, "lon": 12.8},
        "Bayern nördl. der Donau, o. Bayr. Wald, o. Mainfranken": {"lat": 48.6, "lon": 12.1},
        "Mainfranken": {"lat": 49.8, "lon": 9.9},
    }

    # Regionen
    regions = {
        "Schleswig-Holstein und Hamburg": {
            "Inseln und Marschen": ("10", "11"),
            "Geest,Schleswig-Holstein und Hamburg": ("10", "12"),
        },
        "Mecklenburg-Vorpommern": {
            "Mecklenburg-Vorpommern": ("20", "-1"),
        },
        "Niedersachsen und Bremen": {
            "Westl. Niedersachsen/Bremen": ("30", "31"),
            "Östl. Niedersachsen": ("30", "32"),
        },
        "Nordrhein-Westfalen": {
            "Rhein.-Westfäl. Tiefland": ("40", "41"),
            "Ostwestfalen": ("40", "42"),
            "Mittelgebirge NRW": ("40", "43"),
        },
        "Brandenburg und Berlin": {
            "Brandenburg und Berlin": ("50", "-1"),
        },
        "Sachsen-Anhalt": {
            "Tiefland Sachsen-Anhalt": ("60", "61"),
            "Harz": ("60", "62"),
        },
        "Thüringen": {
            "Tiefland Thüringen": ("70", "71"),
            "Mittelgebirge Thüringen": ("70", "72"),
        },
        "Sachsen": {
            "Tiefland Sachsen": ("80", "81"),
            "Mittelgebirge Sachsen": ("80", "82"),
        },
        "Hessen": {
            "Nordhessen und hess. Mittelgebirge": ("90", "91"),
            "Rhein-Main": ("90", "92"),
        },
        "Rheinland-Pfalz und Saarland": {
            "Rhein, Pfalz, Nahe und Mosel": ("100", "101"),
            "Mittelgebirgsbereich Rheinland-Pfalz": ("100", "102"),
            "Saarland": ("100", "103"),
        },
        "Baden-Württemberg": {
            "Oberrhein und unteres Neckartal": ("110", "111"),
            "Hohenlohe / mittlerer Neckar / Oberschwaben": ("110", "112"),
            "Mittelgebirge Baden-Württemberg": ("110", "113"),
        },
        "Bayern": {
            "Allgäu / Oberbayern / Bay. Wald": ("120", "121"),
            "Donauniederungen": ("120", "122"),
            "Bayern nördl. der Donau, o. Bayr. Wald, o. Mainfranken": ("120", "123"),
            "Mainfranken": ("120", "124"),
        },
    }

    # UI
    selected_region = st.selectbox("🌍 Wähle eine Region", list(regions.keys()))
    subregion_names = list(regions[selected_region].keys())
    selected_subregion = st.selectbox("📍 Wähle eine Unterregion", subregion_names)
    region_id, partregion_id = regions[selected_region][selected_subregion]

    pollen_info = get_pollen_data(region_id, partregion_id)

    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    st.success(f"Stand: {current_datetime}")

    # Interaktives Diagramm
    if not pollen_info:
        st.error("⚠️ Keine Pollen-Daten verfügbar für diese Region!")
    else:
        date_labels = ["Heute", "Morgen", "Übermorgen"]
        df = pd.DataFrame([
            {
                "Datum": label,
                "Wert": parse_pollen_value(pollen[day]),
                "Pollenart": pollen['Pollenart'],
                "Belastung": pollen_level_label(parse_pollen_value(pollen[day]))
            }
            for pollen in pollen_info
            for label, day in zip(date_labels, ['Heute', 'Morgen', 'Übermorgen'])
        ])

        farbskala = {
            "🟩 Gering": "green",
            "🟧 Mäßig": "orange",
            "🟥 Stark": "red"
        }
        df["Farbe"] = df["Belastung"].map(farbskala)

        fig = px.line(df, x="Datum", y="Wert", color="Pollenart", line_group="Pollenart",
                    hover_data={"Datum": False, "Wert": False, "Belastung": True, "Pollenart": True, "Farbe": False},
                    markers=True)

        for trace in fig.data:
            pollenart = trace.name
            farben = df[df["Pollenart"] == pollenart]["Farbe"].tolist()
            trace.line.color = None
            trace.marker.color = farben
            trace.line.color = farben[0] if farben else "gray"

        fig.update_traces(
            hovertemplate="<b>%{customdata[1]}</b><br>Stufe: %{customdata[2]}<extra></extra>",
            line_shape="linear"
        )

        fig.update_layout(
            title=f"Pollenbelastung – {selected_subregion}",
            yaxis_title="Belastung (0–3)",
            xaxis_title="Datum",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Aktive Pollenarten mit Rating
        st.markdown("### 🌿 Aktive Pollenarten heute")
        aktive = [
            f"{p['Pollenart']} ({pollen_level_label(parse_pollen_value(p['Heute']))})"
            for p in pollen_info if parse_pollen_value(p['Heute']) > 0
        ]
        if aktive:
            st.success("Aktuell aktiv: " + ", ".join(aktive))
        else:
            st.info("Heute keine Pollenbelastung.")

        # Tabelle ohne ID und mit Belastungsstufen
        st.markdown("### 📅 Belastungsvorhersage")
        df_without_id = pd.DataFrame(pollen_info).drop(columns=["ID"], errors='ignore')
        df_without_id["Belastung"] = df_without_id["Heute"].apply(lambda x: pollen_level_label(parse_pollen_value(x)))
        st.table(df_without_id)

        # Karte mit Regionen
        st.markdown("### 🗺️ Region auf Karte")
        if selected_subregion in coordinates:
            region_coords = coordinates[selected_subregion]
            region_lat = region_coords['lat']
            region_lon = region_coords['lon']
            
            # Erstellen eines Kreises als Platzhalter für die Region
            map_df = pd.DataFrame([{'latitude': region_lat, 'longitude': region_lon}])
            st.map(map_df)
        else:
            st.info("📍 Für diese Region sind keine Koordinaten hinterlegt.")
       # --- API Umweltbundesamt ---
        st.markdown("""
           
        > 🔍 Quelle: [DWD](https://opendata.dwd.de/climate_environment/health/alerts)
        """)