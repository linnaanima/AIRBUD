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

    
    # Custom CSS for better aesthetics
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }

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

    st.subheader("Luftqualitätsmonitor Deutschland")
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
            title=f"",
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

