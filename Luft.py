import streamlit as st
import requests
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime, timedelta

def app():
    def get_air_quality_data(station_id, start_date, end_date, start_time, end_time):
        url = "https://www.umweltbundesamt.de/api/air_data/v3/airquality/json"
        params = {
            "station": station_id,
            "date_from": str(start_date),
            "date_to": str(end_date),
            "time_from": start_time,
            "time_to": end_time,
            "lang": "de"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            st.error("❌ Fehler beim Abruf der Luftqualitätsdaten.")
            return None
        data = response.json()
        return data.get("data", {}).get(str(station_id), {})

    def calculate_air_quality_rating(lqi_values):
        average_lqi = np.mean(lqi_values)
        if average_lqi <= 50:
            return "Sehr gut"
        elif average_lqi <= 100:
            return "Gut"
        elif average_lqi <= 150:
            return "Mäßig"
        elif average_lqi <= 200:
            return "Schlecht"
        else:
            return "Sehr Schlecht"

    def get_health_advice(average_lqi):
        if average_lqi <= 50:
            return "Luftqualität ist sehr gut. Für Menschen mit Atemwegserkrankungen sind keine Bedenken zu erwarten."
        elif average_lqi <= 100:
            return "Luftqualität ist gut. Menschen mit Atemwegserkrankungen sollten sich weiterhin im Freien aufhalten, aber bei Bedarf Vorsichtsmaßnahmen treffen."
        elif average_lqi <= 150:
            return "Luftqualität ist mäßig. Menschen mit Atemwegserkrankungen sollten den Aufenthalt im Freien ggf. einschränken."
        else:
            return "Luftqualität ist schlecht. Personen mit Atemwegserkrankungen sollten den Aufenthalt im Freien vermeiden oder Schutzmaßnahmen treffen."


    stations = [
        {"id": "1584", "name": "Kiel-Bremerskamp", "region": "Kiel", "lat": 54.3439, "lon": 10.1185},
        {"id": "121", "name": "Berlin Wedding", "region": "Berlin", "lat": 52.543, "lon": 13.3493},
        {"id": "143", "name": "Berlin Grunewald", "region": "Berlin", "lat": 52.4732, "lon": 13.2251},
        {"id": "145", "name": "Berlin Neukölln", "region": "Berlin", "lat": 52.4895, "lon": 13.4308},
        {"id": "158", "name": "Berlin Buch", "region": "Berlin", "lat": 52.6442, "lon": 13.4831},
        {"id": "172", "name": "Berlin Frankfurter Allee", "region": "Berlin", "lat": 52.5141, "lon": 13.4699},
        {"id": "471", "name": "München/Stachus", "region": "München", "lat": 48.1373, "lon": 11.5649},
        {"id": "473", "name": "München/Lothstraße", "region": "München", "lat": 48.1545, "lon": 11.5547},
        {"id": "609", "name": "München/Allach", "region": "München", "lat": 48.1817, "lon": 11.4645},
        {"id": "616", "name": "Bremen-Mitte", "region": "Bremen", "lat": 53.0772, "lon": 8.8158},
        {"id": "619", "name": "Bremen-Nord", "region": "Bremen", "lat": 53.1809, "lon": 8.6255},
        {"id": "628", "name": "Bremen-Hasenbüren", "region": "Bremen", "lat": 53.1177, "lon": 8.6951},
        {"id": "633", "name": "Frankfurt-Höchst", "region": "Frankfurt", "lat": 50.1018, "lon": 8.5425},
        {"id": "636", "name": "Frankfurt Ost", "region": "Frankfurt", "lat": 50.1253, "lon": 8.7463},
        {"id": "763", "name": "Frankfurt-Schwanheim", "region": "Frankfurt", "lat": 50.0755, "lon": 8.5763},
        {"id": "784", "name": "Hamburg Sternschanze", "region": "Hamburg", "lat": 53.5641, "lon": 9.9679},
        {"id": "809", "name": "Hamburg Flughafen Nord", "region": "Hamburg", "lat": 53.6383, "lon": 9.998},
        {"id": "823", "name": "Hamburg Bramfeld", "region": "Hamburg", "lat": 53.6307, "lon": 10.1106},
        {"id": "826", "name": "Hamburg Neugraben", "region": "Hamburg", "lat": 53.4809, "lon": 9.8572},
        {"id": "224", "name": "Stuttgart-Bad Cannstatt", "region": "Stuttgart", "lat": 48.8088, "lon": 9.2297}
    ]
    station_names = {s["name"]: s["id"] for s in stations}
    selected_station_name = st.selectbox("📍 Wähle eine Messstation:", [f"{s['name']} ({s['region']})" for s in stations])
    selected_station_name = selected_station_name.split(" (")[0]
    station_id = station_names[selected_station_name]

    yesterday = datetime.now() - timedelta(days=1)
    start_date = yesterday.date()
    start_hour = 0
    end_date = datetime.now().date()
    end_hour = datetime.now().hour

    col1, col2 = st.columns(2)
    with col1:
        start_date_input = st.date_input("Startdatum", start_date)
    with col2:
        end_date_input = st.date_input("Enddatum", end_date)

    col3, col4 = st.columns(2)
    with col3:
        start_time_input = st.selectbox("Startzeit (Stunde)", list(range(0, 24)), index=start_hour)
    with col4:
        end_time_input = st.selectbox("Endzeit (Stunde)", list(range(0, 24)), index=end_hour)

    air_quality_data = get_air_quality_data(
        station_id,
        start_date_input,
        end_date_input,
        f"{start_time_input}:00",
        f"{end_time_input}:59"
    )

    if air_quality_data:
        air_quality_list = []
        lqi_values = []
        latest_values = {}

        for timestamp, values in air_quality_data.items():
            components = values[3:]
            for component in components:
                component_id = component[0]
                try:
                    component_value = float(component[1])
                    lqi_value = float(component[3])
                    lqi_values.append(lqi_value)
                except:
                    continue

                if component_id == 3:
                    unit, comp_name = "µg/m³", "PM10"
                elif component_id == 5:
                    unit, comp_name = "µg/m³", "PM2.5"
                elif component_id == 1:
                    unit, comp_name = "µg/m³", "NO"
                elif component_id == 9:
                    unit, comp_name = "µg/m³", "O3"
                else:
                    unit, comp_name = "Nicht verfügbar", f"Komponente {component_id}"

                air_quality_list.append({
                    "Zeitpunkt": timestamp,
                    "Messwert": component_value,
                    "Komponente": comp_name,
                    "LQI": lqi_value,
                    "Einheit": unit
                })
                latest_values[comp_name] = component_value

        air_quality_df = pd.DataFrame(air_quality_list)

        st.markdown(f"**Zeitraum der angezeigten Daten:** {start_date_input} {start_time_input}:00 Uhr bis {end_date_input} {end_time_input}:59 Uhr")

        average_lqi = np.mean(lqi_values)
        rating = calculate_air_quality_rating(lqi_values)
        health_advice = get_health_advice(average_lqi)


        # Checkboxen zur Anzeige von Grenzwerten
        show_who = st.checkbox("🔍 WHO-Grenzwerte anzeigen", value=True)
        show_de = st.checkbox("🏛️ Deutsche Grenzwerte anzeigen", value=True)

        # Diagramm mit Grenzwerten
        fig_air = px.line(air_quality_df, x="Zeitpunkt", y="Messwert", color="Komponente", title="📉 Luftqualitätstrends")

        # Farben der Komponenten aus der Figur extrahieren
        component_colors = {}
        for trace in fig_air.data:
            component_name = trace.name
            component_colors[component_name] = trace.line.color

        components_in_df = air_quality_df["Komponente"].unique()
        thresholds = {
            "PM10": {"WHO": 45, "DE": 50},
            "PM2.5": {"WHO": 15, "DE": 25},
            "NO": {"WHO": 25, "DE": 40},
            "O3": {"WHO": 100, "DE": 120}
        }

        for comp in components_in_df:
            if comp in thresholds:
                if show_who and comp in component_colors:
                    fig_air.add_hline(y=thresholds[comp]["WHO"], line_dash="dash", line_color=component_colors[comp],
                                     annotation_text=f"WHO-Grenze ({comp})", annotation_position="top left")
                if show_de and comp in component_colors:
                    fig_air.add_hline(y=thresholds[comp]["DE"], line_dash="dot", line_color=component_colors[comp],
                                     annotation_text=f"DE-Grenze ({comp})", annotation_position="top right")

        st.plotly_chart(fig_air, use_container_width=True)

        st.subheader("Aktuelle Messwerte")
        for comp_name, value in latest_values.items():
            st.write(f"{comp_name}: {value} µg/m³")
            if comp_name == "PM10":
                if value <= 20:
                    quality = "Sehr gut"
                elif value <= 35:
                    quality = "Gut"
                elif value <= 50:
                    quality = "Mäßig"
                elif value <= 100:
                    quality = "Schlecht"
                else:
                    quality = "Sehr Schlecht"
            elif comp_name == "PM2.5":
                if value <= 10:
                    quality = "Sehr gut"
                elif value <= 20:
                    quality = "Gut"
                elif value <= 25:
                    quality = "Mäßig"
                elif value <= 50:
                    quality = "Schlecht"
                else:
                    quality = "Sehr Schlecht"
            elif comp_name == "NO":
                if value <= 20:
                    quality = "Sehr gut"
                elif value <= 40:
                    quality = "Gut"
                elif value <= 100:
                    quality = "Mäßig"
                elif value <= 200:
                    quality = "Schlecht"
                else:
                    quality = "Sehr Schlecht"
            elif comp_name == "O3":
                if value <= 60:
                    quality = "Sehr gut"
                elif value <= 120:
                    quality = "Gut"
                elif value <= 180:
                    quality = "Mäßig"
                elif value <= 240:
                    quality = "Schlecht"
                else:
                    quality = "Sehr schlecht"
            else:
                quality = "Nicht verfügbar"
            st.write(f"Bewertung für {comp_name}: {quality}")
    else:
        st.write("Keine Daten verfügbar.")

    # Karte anzeigen
    m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
    for s in stations:
        folium.Marker(
            location=[s["lat"], s["lon"]],
            tooltip=s["name"],
            popup=f"{s['name']} ({s['region']}) - ID: {s['id']}"
        ).add_to(m)

    selected_station = next(s for s in stations if s["name"] == selected_station_name)
    selected_lat = selected_station["lat"]
    selected_lon = selected_station["lon"]
    dark_tiles = "CartoDB dark_matter"
    m = folium.Map(location=[selected_lat, selected_lon], zoom_start=12)

    folium.Marker(
        location=[selected_lat, selected_lon],
        tooltip=selected_station_name,
        popup=f"{selected_station_name} ({selected_station['region']}) - ID: {station_id}"
    ).add_to(m)

    folium_static(m)

       # --- API Umweltbundesamt ---
    st.markdown("""
     > 🔍 Quelle: [Umweltbundesamt](https://www.umweltbundesamt.de/api/air_data/v3/airquality/)
    """)
