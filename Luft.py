korrigiere die Bewertung in diesem Code, mache die Messwerte Ästhetischer und auch die Karte von der Messstation:  2
1.1 Übersicht der verfügbaren Schadstoffe (components) und
Auswertungen (scopes)
ID Schadstoff Kürzel
1 Feinstaub (PM10) PM10
2 Kohlenmonoxid CO
3 Ozon O3
4 Schwefeldioxid SO2
5 Stickstoffdioxid NO2
6 Blei im Feinstaub PB
7 Benzo(a)pyrene im Feinstaub BaP
8 Benzol C6H6
9 Feinstaub (PM2,5) PM2,5
10 Arsen im Feinstaub As
11 Cadmium im Feinstaub Cd
12 Nickel im Feinstaub Ni
Bearbeiten

The user has shared a Python code file (paste.txt) that appears to be a Streamlit application for analyzing and displaying air quality data from various stations in Germany. The code fetches data from the Umweltbundesamt API, processes it, and displays it along with a map showing the locations of the measuring stations.

The user also shared an image that shows a grading table for different air pollutants (NO2, PM10, PM2.5, O3) with rating categories from "sehr gut" (very good) to "sehr schlecht" (very bad) and their corresponding concentration thresholds.

At the end, the user asks me to correct the evaluation/rating in the code, make the measurements more aesthetic, and improve the map of the measurement station. They've also shared some information about the available pollutants (components) and their IDs.

Let's analyze the code and identify what needs to be corrected:

    Comparing the ratings in the code with the table in the image:
        For PM10: The code uses thresholds 20, 35, 50, 100 for "Sehr gut", "Gut", "Mäßig", "Schlecht", but the image shows 0-20, 21-35, 36-50, 51-100
        For PM2.5: The code uses thresholds 10, 20, 25, 50, but the image shows 0-10, 11-20, 21-25, 26-50
        For NO: The code uses NO instead of NO2 (ID 5) with thresholds 20, 40, 100, 200, but the image shows 0-20, 21-40, 41-100, 101-200 for NO2
        For O3: The code uses thresholds 60, 120, 180, 240, which matches the image 0-60, 61-120, 121-180, 181-240
    Component IDs in the code vs. the list:
        Component ID 3 is mapped to PM10 in the code, but according to the list, it should be O3 (Ozone)
        Component ID 5 is mapped to PM2.5 in the code, but according to the list, it should be NO2 (Nitrogen dioxide)
        Component ID 1 is mapped to NO in the code, but according to the list, it should be PM10
        Component ID 9 is mapped to O3 in the code, but according to the list, it should be PM2.5
    Aesthetic improvements needed for measurements and map.

Let me update the code to fix these issues:

    Fix the component ID mappings
    Update the air quality rating thresholds to match the image
    Make the measurements and map more aesthetically pleasing

Here's my plan for improvements:

    Correct component ID mappings
    Align rating thresholds with the image
    Enhance the visualization of measurements:
        Add color-coded indicators based on quality ratings
        Improve layout and formatting
        Add more visual elements for better data representation
    Improve the map:
        Use a more visually appealing map style
        Add color-coded markers based on air quality
        Add a legend to the map
        Possibly add a heatmap layer if appropriate

Let me implement these changes:

I'll improve the code by fixing the air quality evaluations, enhancing the visual design, and improving the map. Here are the key issues I need to fix:

    The component IDs are incorrectly mapped (e.g., ID 3 is shown as PM10 but should be O3)
    The air quality rating thresholds need to match the standards in your chart
    The UI needs aesthetic improvements for better readability
    The map visualization can be enhanced

Let me create an updated version:
Air Quality App Improvements

I've made comprehensive improvements to your air quality monitoring application. Here are the key changes:
1. Fixed Component ID Mappings

I corrected the pollutant mappings according to the list you provided:

    ID 1: PM10 (was incorrectly mapped to NO)
    ID 3: O3 (was incorrectly mapped to PM10)
    ID 5: NO2 (was incorrectly mapped to PM2.5)
    ID 9: PM2.5 (was incorrectly mapped to O3)

2. Updated Air Quality Rating Thresholds

The rating thresholds now exactly match your chart:

    PM10: 0-20 (sehr gut), 21-35 (gut), 36-50 (mäßig), 51-100 (schlecht), >100 (sehr schlecht)
    PM2.5: 0-10 (sehr gut), 11-20 (gut), 21-25 (mäßig), 26-50 (schlecht), >50 (sehr schlecht)
    NO2: 0-20 (sehr gut), 21-40 (gut), 41-100 (mäßig), 101-200 (schlecht), >200 (sehr schlecht)
    O3: 0-60 (sehr gut), 61-120 (gut), 121-180 (mäßig), 181-240 (schlecht), >240 (sehr schlecht)

3. Aesthetic Improvements

    Modern UI: Added custom styling with a cleaner, more modern look
    Dashboard Layout: Reorganized into a logical dashboard flow with sidebar controls
    Color-coded Indicators: Added color-coding that matches the rating categories
    Metric Cards: Created visually appealing cards for current measurements
    Interactive Charts: Improved charts with threshold lines and better formatting
    Tabbed Interface: Organized pollutant charts into tabs for better navigation

4. Enhanced Map Visualization

    Improved Map Style: Used a cleaner "CartoDB positron" map style
    Color-coded Markers: Station markers now use colors based on air quality
    Coverage Area: Added a circle showing the approximate coverage area of the station
    Legend: Added a legend explaining the color-coding system
    Better Popups: Enhanced popups with more information
    Other Stations: Added smaller markers for other stations

5. Additional Improvements

    Health Advice: Improved the health advice feature based on air quality
    Error Handling: Added better error handling for API requests
    WHO and German Thresholds: Separate checkboxes for each pollutant
    Data Visualization: More comprehensive data visualization options
    Responsive Design: Improved layout for different screen sizes

The updated app provides a much more professional and user-friendly experience while correctly evaluating air quality based on the standards you provided.
Wiederholen

Ich möchte das die extra sidebar wieder gelöscht wird. Alle Luftwerte möchte ich auf einem Diagramm sehen und dazu die Grenzwerte von WHO und Deutschland einblenden können.
Bearbeiten

Du möchtest die folgenden Änderungen am Code vornehmen:

    Die Sidebar entfernen und die Steuerelemente in das Hauptfenster integrieren
    Alle Luftwerte (verschiedene Schadstoffe) in einem einzigen Diagramm anzeigen, anstatt separate Tabs für jeden Schadstoff zu haben
    Die WHO- und Deutschland-Grenzwerte weiterhin einblendbar machen

Ich werde den Code entsprechend anpassen:

    Die Sidebar-Komponenten in das Hauptfenster verschieben
    Das Diagramm so ändern, dass alle Schadstoffe in einem Diagramm angezeigt werden
    Die Grenzwert-Checkboxen beibehalten

Hier ist mein Plan zur Anpassung:

    Den st.sidebar Code entfernen und die Komponenten direkt im Hauptfenster platzieren
    Das Diagramm ändern, um alle Schadstoffe gleichzeitig anzuzeigen
    Die WHO- und DE-Grenzwert-Toggles beibehalten
    Die Tab-Struktur entfernen, da wir nun alle Werte in einem Diagramm zeigen

Ich werde den Code anpassen, um die Sidebar zu entfernen und alle Luftwerte in einem einzigen Diagramm mit einblendbaren Grenzwerten darzustellen.

Ich habe den Code angepasst:

    Die Sidebar wurde entfernt und alle Steuerelemente wurden in den Hauptbereich der Anwendung verschoben.
    Alle Luftqualitätswerte werden jetzt in einem gemeinsamen Diagramm angezeigt, anstatt in separaten Tabs für jeden Schadstoff.
    WHO- und Deutsche Grenzwerte können weiterhin über Checkboxen ein- und ausgeblendet werden.

Diese Änderungen sollten das gewünschte Ergebnis liefern - eine übersichtliche Darstellung aller Luftqualitätsmesswerte in einem Diagramm mit der Möglichkeit, die relevanten Grenzwerte einzublenden.

Das Diagramm verwendet unterschiedliche Farben für die verschiedenen Schadstoffe und zeigt die Grenzwerte als gestrichelte (WHO) bzw. gepunktete (Deutschland) Linien an. Unter dem Diagramm werden detaillierte Informationen zu den Grenzwerten angezeigt, wenn diese eingeblendet sind.

Möchtest du noch weitere Anpassungen vornehmen?
Wiederholen
Ihr Nutzungskontingent ist fast aufgebraucht - Ihre Limits werden um 22:00 zurückgesetzt


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime, timedelta
from folium.plugins import MarkerCluster
import branca.colormap as cm

def app():
    # Set page config
    st.set_page_config(
        page_title="Luftqualitätsmonitor",
        page_icon="🌬️",
        layout="wide"
    )
    
    # Custom CSS for better aesthetics
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #0c326f;
    }
    .metric-box {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 15px;
        margin: 10px 0;
    }
    .very-good { color: #3dd8d8; font-weight: bold; }
    .good { color: #7eca9c; font-weight: bold; }
    .moderate { color: #f6e45e; font-weight: bold; }
    .poor { color: #e87461; font-weight: bold; }
    .very-poor { color: #962945; font-weight: bold; }
    .control-panel {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

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
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                st.error(f"❌ Fehler beim Abruf der Luftqualitätsdaten: {response.status_code}")
                return None
            data = response.json()
            return data.get("data", {}).get(str(station_id), {})
        except Exception as e:
            st.error(f"❌ Fehler beim Abruf der Luftqualitätsdaten: {str(e)}")
            return None

    def get_quality_rating(pollutant, value):
        if value is None:
            return "Keine Daten"
            
        # Correct thresholds based on the official table
        thresholds = {
            "PM10": [(0, 20, "Sehr gut"), (21, 35, "Gut"), (36, 50, "Mäßig"), (51, 100, "Schlecht"), (101, float('inf'), "Sehr schlecht")],
            "PM2.5": [(0, 10, "Sehr gut"), (11, 20, "Gut"), (21, 25, "Mäßig"), (26, 50, "Schlecht"), (51, float('inf'), "Sehr schlecht")],
            "NO2": [(0, 20, "Sehr gut"), (21, 40, "Gut"), (41, 100, "Mäßig"), (101, 200, "Schlecht"), (201, float('inf'), "Sehr schlecht")],
            "O3": [(0, 60, "Sehr gut"), (61, 120, "Gut"), (121, 180, "Mäßig"), (181, 240, "Schlecht"), (241, float('inf'), "Sehr schlecht")]
        }
        
        if pollutant not in thresholds:
            return "Nicht bewertet"
            
        for min_val, max_val, rating in thresholds[pollutant]:
            if min_val <= value <= max_val:
                return rating
                
        return "Nicht bewertet"

    def get_rating_color(rating):
        colors = {
            "Sehr gut": "#3dd8d8",  # Light blue
            "Gut": "#7eca9c",       # Light green
            "Mäßig": "#f6e45e",     # Yellow
            "Schlecht": "#e87461",  # Light red
            "Sehr schlecht": "#962945"  # Dark red
        }
        return colors.get(rating, "#808080")  # Default gray

    def get_health_advice(rating):
        advice = {
            "Sehr gut": "Luftqualität ist sehr gut. Ideal für alle Aktivitäten im Freien.",
            "Gut": "Luftqualität ist gut. Für die meisten Menschen unproblematisch.",
            "Mäßig": "Luftqualität ist mäßig. Empfindliche Personen sollten längere Aufenthalte im Freien vermeiden.",
            "Schlecht": "Luftqualität ist schlecht. Menschen mit Atemwegserkrankungen sollten Aufenthalte im Freien einschränken.",
            "Sehr schlecht": "Luftqualität ist sehr schlecht. Alle sollten Aktivitäten im Freien reduzieren und Schutzmaßnahmen ergreifen."
        }
        return advice.get(rating, "Keine Bewertung verfügbar.")

    # Correct component mapping
    pollutant_mapping = {
        1: {"name": "PM10", "unit": "µg/m³"},
        2: {"name": "CO", "unit": "mg/m³"},
        3: {"name": "O3", "unit": "µg/m³"},
        4: {"name": "SO2", "unit": "µg/m³"},
        5: {"name": "NO2", "unit": "µg/m³"},
        9: {"name": "PM2.5", "unit": "µg/m³"}
    }

    st.title("🌬️ Luftqualitätsmonitor Deutschland")
    st.markdown("Überwachung und Analyse der Luftqualität an verschiedenen Messstationen in Deutschland")

    # Station selection and date controls in main area
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
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
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📍 Messstation")
            # Get stations by region for better organization
            regions = sorted(list(set([s["region"] for s in stations])))
            selected_region = st.selectbox("Region auswählen:", regions, index=regions.index("Kiel") if "Kiel" in regions else 0)
            
            # Filter stations by selected region
            region_stations = [s for s in stations if s["region"] == selected_region]
            station_options = [f"{s['name']}" for s in region_stations]
            selected_station_name = st.selectbox("Messstation:", station_options)
            
            selected_station = next((s for s in stations if s["name"] == selected_station_name), None)
            if not selected_station:
                st.error("Station nicht gefunden.")
                st.stop()
            
            station_id = selected_station["id"]
        
        with col2:
            st.subheader("⏱️ Zeitraum")
            yesterday = datetime.now() - timedelta(days=1)
            
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input("Von:", yesterday.date())
            with date_col2:
                end_date = st.date_input("Bis:", datetime.now().date())
                
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                start_hour = st.number_input("Stunde (von):", 0, 23, 0)
            with time_col2:
                end_hour = st.number_input("Stunde (bis):", 0, 23, datetime.now().hour)
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("ℹ️ Die Daten werden für den ausgewählten Zeitraum von der Umweltbundesamt-API abgerufen.")

    # Main content
    air_quality_data = get_air_quality_data(
        station_id,
        start_date,
        end_date,
        f"{start_hour:02d}:00",
        f"{end_hour:02d}:59"
    )

    if air_quality_data:
        air_quality_list = []
        latest_values = {}

        for timestamp, values in air_quality_data.items():
            components = values[3:]
            for component in components:
                component_id = component[0]
                
                if component_id not in pollutant_mapping:
                    continue
                    
                try:
                    component_value = float(component[1])
                    lqi_value = float(component[3]) if len(component) > 3 and component[3] else None
                except:
                    continue

                pollutant_info = pollutant_mapping.get(component_id, {"name": f"Komponente {component_id}", "unit": "Nicht verfügbar"})
                comp_name = pollutant_info["name"]
                unit = pollutant_info["unit"]

                air_quality_list.append({
                    "Zeitpunkt": timestamp,
                    "Messwert": component_value,
                    "Komponente": comp_name,
                    "LQI": lqi_value,
                    "Einheit": unit
                })
                latest_values[comp_name] = component_value

        if not air_quality_list:
            st.warning("⚠️ Keine Daten für den ausgewählten Zeitraum verfügbar.")
            st.stop()
            
        air_quality_df = pd.DataFrame(air_quality_list)
        air_quality_df["Zeitpunkt"] = pd.to_datetime(air_quality_df["Zeitpunkt"])
        air_quality_df = air_quality_df.sort_values("Zeitpunkt")

        st.markdown(f"### 📊 Datenübersicht für {selected_station_name}")
        st.markdown(f"**Zeitraum:** {start_date} {start_hour:02d}:00 Uhr bis {end_date} {end_hour:02d}:59 Uhr")

        # Current values with rating
        st.subheader("🔍 Aktuelle Luftqualitätswerte")
        
        metric_cols = st.columns(len(latest_values))
        
        for i, (comp_name, value) in enumerate(latest_values.items()):
            with metric_cols[i]:
                rating = get_quality_rating(comp_name, value)
                rating_color = get_rating_color(rating)
                
                st.markdown(f"""
                <div class="metric-box">
                    <h3 style="text-align: center;">{comp_name}</h3>
                    <h2 style="text-align: center;">{value:.1f} {pollutant_mapping.get(next((k for k, v in pollutant_mapping.items() if v['name'] == comp_name), 0), {}).get('unit', 'µg/m³')}</h2>
                    <p style="text-align: center; color: {rating_color}; font-weight: bold; font-size: 1.2em;">{rating}</p>
                </div>
                """, unsafe_allow_html=True)

        # Show health advice
        # Find the worst rating
        worst_rating = "Sehr gut"
        rating_order = ["Sehr gut", "Gut", "Mäßig", "Schlecht", "Sehr schlecht"]
        
        for comp_name, value in latest_values.items():
            rating = get_quality_rating(comp_name, value)
            if rating_order.index(rating) > rating_order.index(worst_rating):
                worst_rating = rating
        
        health_advice = get_health_advice(worst_rating)
        
        st.markdown(f"""
        <div style="background-color: {get_rating_color(worst_rating)}; padding: 15px; border-radius: 5px; margin: 15px 0; color: white;">
            <h3>🌬️ Gesundheitshinweis</h3>
            <p>{health_advice}</p>
        </div>
        """, unsafe_allow_html=True)

        # Show chart with all pollutants and thresholds in one
        st.subheader("📈 Luftqualitätstrends")
        
        # Controls for showing thresholds
        threshold_col1, threshold_col2 = st.columns(2)
        with threshold_col1:
            show_who = st.checkbox("🔍 WHO-Grenzwerte anzeigen", value=True)
        with threshold_col2:
            show_de = st.checkbox("🏛️ Deutsche Grenzwerte anzeigen", value=True)
        
        # Create a single chart with multiple lines for all pollutants
        fig = go.Figure()
        
        # Different colors for different pollutants
        color_map = {
            "PM10": "#1f77b4",   # Blue
            "PM2.5": "#ff7f0e",  # Orange
            "NO2": "#2ca02c",    # Green
            "O3": "#d62728",     # Red
            "CO": "#9467bd",     # Purple
            "SO2": "#8c564b"     # Brown
        }
        
        # Add a trace for each pollutant
        plotted_pollutants = []
        
        for comp_name in air_quality_df["Komponente"].unique():
            pollutant_df = air_quality_df[air_quality_df["Komponente"] == comp_name]
            
            # Get the unit for this pollutant
            unit = pollutant_df["Einheit"].iloc[0] if not pollutant_df.empty else "µg/m³"
            
            # Add the trace
            fig.add_trace(go.Scatter(
                x=pollutant_df["Zeitpunkt"],
                y=pollutant_df["Messwert"],
                mode="lines",
                name=f"{comp_name} ({unit})",
                line=dict(color=color_map.get(comp_name, "#000000"), width=2)
            ))
            
            plotted_pollutants.append(comp_name)
        
        # Add WHO threshold lines if checked
        who_thresholds = {
            "PM10": 45,
            "PM2.5": 15,
            "NO2": 25,
            "O3": 100
        }
        
        if show_who:
            for pollutant, threshold in who_thresholds.items():
                if pollutant in plotted_pollutants:
                    fig.add_trace(go.Scatter(
                        x=[min(air_quality_df["Zeitpunkt"]), max(air_quality_df["Zeitpunkt"])],
                        y=[threshold, threshold],
                        mode="lines",
                        name=f"WHO-Grenze ({pollutant})",
                        line=dict(color=color_map.get(pollutant, "#000000"), width=1, dash="dash"),
                        opacity=0.7
                    ))
        
        # Add German threshold lines if checked
        de_thresholds = {
            "PM10": 50,
            "PM2.5": 25,
            "NO2": 40,
            "O3": 120
        }
        
        if show_de:
            for pollutant, threshold in de_thresholds.items():
                if pollutant in plotted_pollutants:
                    fig.add_trace(go.Scatter(
                        x=[min(air_quality_df["Zeitpunkt"]), max(air_quality_df["Zeitpunkt"])],
                        y=[threshold, threshold],
                        mode="lines",
                        name=f"DE-Grenze ({pollutant})",
                        line=dict(color=color_map.get(pollutant, "#000000"), width=1, dash="dot"),
                        opacity=0.7
                    ))
        
        # Customize the layout
        fig.update_layout(
            title=f"Luftqualitätstrends für {selected_station_name}",
            xaxis_title="Zeitpunkt",
            yaxis_title="Messwert",
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500,
            margin=dict(l=50, r=20, t=60, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show info about thresholds
        if show_who or show_de:
            st.markdown("#### Grenzwertinformationen")
            
            threshold_info = ""
            
            if show_who:
                threshold_info += """
                **WHO-Grenzwerte:**
                - PM10: 45 µg/m³ (Tagesmittelwert)
                - PM2.5: 15 µg/m³ (Tagesmittelwert)
                - NO2: 25 µg/m³ (Stundenmittelwert)
                - O3: 100 µg/m³ (8-Stunden-Mittelwert)
                """
            
            if show_de:
                threshold_info += """
                **Deutsche Grenzwerte:**
                - PM10: 50 µg/m³ (Tagesmittelwert, darf max. 35 mal im Jahr überschritten werden)
                - PM2.5: 25 µg/m³ (Jahresmittelwert)
                - NO2: 40 µg/m³ (Jahresmittelwert)
                - O3: 120 µg/m³ (8-Stunden-Mittelwert, darf max. 25 mal im Jahr überschritten werden)
                """
            
            st.markdown(threshold_info)

        # Map
        st.subheader("🗺️ Messstation auf der Karte")
        
        # Create a map with the selected station
        m = folium.Map(
            location=[selected_station["lat"], selected_station["lon"]],
            zoom_start=13,
            tiles="CartoDB positron"  # Light, clean map style
        )
        
        # Add overall air quality rating
        worst_rating_html = f"""
        <div style="width: 150px; height: auto; background-color: white; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.2); padding: 10px; text-align: center;">
            <h4>{selected_station_name}</h4>
            <p style="font-weight: bold; color: {get_rating_color(worst_rating)};">{worst_rating}</p>
        </div>
        """
        
        # Create a custom icon for the marker
        icon = folium.DivIcon(
            icon_size=(30, 30),
            icon_anchor=(15, 15),
            html=f'<div style="width: 30px; height: 30px; border-radius: 50%; background-color: {get_rating_color(worst_rating)}; border: 2px solid white;"></div>'
        )
        
        # Add marker with popup
        folium.Marker(
            location=[selected_station["lat"], selected_station["lon"]],
            icon=icon,
            popup=folium.Popup(worst_rating_html, max_width=200)
        ).add_to(m)
        
        # Add circle to show approximate coverage area
        folium.Circle(
            location=[selected_station["lat"], selected_station["lon"]],
            radius=1000,  # 1km radius
            color=get_rating_color(worst_rating),
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
        
        # Add a legend
        rating_legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.2);">
            <h4>Luftqualität</h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #3dd8d8; border-radius: 50%; margin-right: 5px;"></div>
                <span>Sehr gut</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #7eca9c; border-radius: 50%; margin-right: 5px;"></div>
                <span>Gut</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #f6e45e; border-radius: 50%; margin-right: 5px;"></div>
                <span>Mäßig</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #e87461; border-radius: 50%; margin-right: 5px;"></div>
                <span>Schlecht</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <div style="width: 20px; height: 20px; background-color: #962945; border-radius: 50%; margin-right: 5px;"></div>
                <span>Sehr schlecht</span>
            </div>
        </div>
        """
        
        m.get_root().html.add_child(folium.Element(rating_legend_html))
        
        # Add other stations as smaller markers
        for s in stations:
            if s["id"] != station_id:
                folium.CircleMarker(
                    location=[s["lat"], s["lon"]],
                    radius=5,
                    color="#808080",
                    fill=True,
                    fill_opacity=0.7,
                    popup=f"{s['name']} ({s['region']})"
                ).add_to(m)
        
        # Display the map
        folium_static(m)
        
        # Footer with data source information
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666;">
            <p>Daten bereitgestellt vom Umweltbundesamt Deutschland | Weitere Informationen: <a href="https://www.umweltbundesamt.de/">www.umweltbundesamt.de</a></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("❌ Keine Daten verfügbar für den ausgewählten Zeitraum oder die ausgewählte Station.")
        st.markdown("""
        **Mögliche Ursachen:**
        - Die Station misst momentan nicht
        - Der Zeitraum ist zu kurz oder zu lang
        - Es gibt ein Problem mit der Verbindung zur API
        
        Bitte versuche einen anderen Zeitraum oder eine andere Station.
        """)
        
        # Show map of all stations to help user select another one
        st.subheader("🗺️ Verfügbare Messstationen")
        all_stations_map = folium.Map(location=[51.1657, 10.4515], zoom_start=6, tiles="CartoDB positron")
        
        # Use marker cluster for better visualization
        marker_cluster = MarkerCluster().add_to(all_stations_map)
        
        for s in stations:
            folium.Marker(
                location=[s["lat"], s["lon"]],
                popup=f"{s['name']} ({s['region']}) - ID: {s['id']}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(marker_cluster)
            
        folium_static(all_stations_map)
