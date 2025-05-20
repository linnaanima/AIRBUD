import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import json

# Air quality component definitions as JSON
AIR_QUALITY_COMPONENTS = {
    "1": {"code": "PM10", "symbol": "PM₁₀", "unit": "µg/m³", "name": "Particulate matter"},
    "2": {"code": "CO", "symbol": "CO", "unit": "mg/m³", "name": "Carbon monoxide"},
    "3": {"code": "O3", "symbol": "O₃", "unit": "µg/m³", "name": "Ozone"},
    "4": {"code": "SO2", "symbol": "SO₂", "unit": "µg/m³", "name": "Sulphur dioxide"},
    "5": {"code": "NO2", "symbol": "NO₂", "unit": "µg/m³", "name": "Nitrogen dioxide"},
    "6": {"code": "PM10PB", "symbol": "Pb", "unit": "µg/m³", "name": "Lead in particulate matter"},
    "7": {"code": "PM10BAP", "symbol": "BaP", "unit": "ng/m³", "name": "Benzo(a)pyrene in particulate matter"},
    "8": {"code": "CHB", "symbol": "C₆H₆", "unit": "µg/m³", "name": "Benzene"},
    "9": {"code": "PM2", "symbol": "PM₂,₅", "unit": "µg/m³", "name": "Particulate matter"},
    "10": {"code": "PM10AS", "symbol": "As", "unit": "ng/m³", "name": "Arsenic in particulate matter"},
    "11": {"code": "PM10CD", "symbol": "Cd", "unit": "ng/m³", "name": "Cadmium in particulate matter"},
    "12": {"code": "PM10NI", "symbol": "Ni", "unit": "ng/m³", "name": "Nickel in particulate matter"}
}


def app():
    
    # Stile für das Dashboard
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
        border-bottom: 2px solid #4b84ff;
    }
    div.stTitle {
        font-weight: bold;
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

    
    # Zentrale Datenstruktur für Städte und Regionen
    locations = {
        "Berlin": {
            "lat": 52.52, 
            "lon": 13.405,
            "stations": [
                {"id": "121", "name": "Berlin Wedding"},
                {"id": "143", "name": "Berlin Grunewald"},
                {"id": "145", "name": "Berlin Neukölln"},
                {"id": "158", "name": "Berlin Buch"},
                {"id": "172", "name": "Berlin Frankfurter Allee"}
            ],
            "pollen_region": "Brandenburg und Berlin",
            "pollen_subregion": "Brandenburg und Berlin",
            "region_id": "40", 
            "partregion_id": "-1"
        },
        "Hamburg": {
            "lat": 53.55, 
            "lon": 10.0,
            "stations": [
                {"id": "784", "name": "Hamburg Sternschanze"},
                {"id": "809", "name": "Hamburg Flughafen Nord"},
                {"id": "823", "name": "Hamburg Bramfeld"},
                {"id": "826", "name": "Hamburg Neugraben"}
            ],
            "pollen_region": "Schleswig-Holstein und Hamburg",
            "pollen_subregion": "Geest,Schleswig-Holstein und Hamburg",
            "region_id": "10", 
            "partregion_id": "12"
        },
        "München": {
            "lat": 48.14, 
            "lon": 11.58,
            "stations": [
                {"id": "471", "name": "München/Stachus"},
                {"id": "473", "name": "München/Lothstraße"},
                {"id": "609", "name": "München/Allach"}
            ],
            "pollen_region": "Bayern",
            "pollen_subregion": "Bayern (Südost)",
            "region_id": "70", 
            "partregion_id": "72"
        },
        "Bremen": {
            "lat": 53.08, 
            "lon": 8.80,
            "stations": [
                {"id": "616", "name": "Bremen-Mitte"},
                {"id": "619", "name": "Bremen-Nord"},
                {"id": "628", "name": "Bremen-Hasenbüren"}
            ],
            "pollen_region": "Niedersachsen und Bremen",
            "pollen_subregion": "Westl. Niedersachsen/Bremen",
            "region_id": "30", 
            "partregion_id": "31"
        },
        "Frankfurt": {
            "lat": 50.11, 
            "lon": 8.68,
            "stations": [
                {"id": "633", "name": "Frankfurt-Höchst"},
                {"id": "636", "name": "Frankfurt Ost"},
                {"id": "763", "name": "Frankfurt-Schwanheim"}
            ],
            "pollen_region": "Hessen",
            "pollen_subregion": "Hessen",
            "region_id": "60", 
            "partregion_id": "-1"
        },
        "Stuttgart": {
            "lat": 48.78, 
            "lon": 9.18,
            "stations": [
                {"id": "224", "name": "Stuttgart-Bad Cannstatt"}
            ],
            "pollen_region": "Baden-Württemberg",
            "pollen_subregion": "Baden-Württemberg (ohne Oberrhein)",
            "region_id": "50", 
            "partregion_id": "51"
        },
        "Kiel": {
            "lat": 54.32, 
            "lon": 10.13,
            "stations": [
                {"id": "1584", "name": "Kiel-Bremerskamp"}
            ],
            "pollen_region": "Schleswig-Holstein und Hamburg",
            "pollen_subregion": "Inseln und Marschen",
            "region_id": "10", 
            "partregion_id": "11"
        },
        "Köln": {
            "lat": 50.94, 
            "lon": 6.96,
            "stations": [
                {"id": "583", "name": "Köln-Chorweiler"},
                {"id": "592", "name": "Köln-Rodenkirchen"}
            ],
            "pollen_region": "Nordrhein-Westfalen",
            "pollen_subregion": "Rheinland",
            "region_id": "20", 
            "partregion_id": "21"
        },
        "Düsseldorf": {
            "lat": 51.23, 
            "lon": 6.78,
            "stations": [
                {"id": "550", "name": "Düsseldorf-Lörick"}
            ],
            "pollen_region": "Nordrhein-Westfalen",
            "pollen_subregion": "Rheinland",
            "region_id": "20", 
            "partregion_id": "21"
        },
        "Leipzig": {
            "lat": 51.34, 
            "lon": 12.38,
            "stations": [
                {"id": "313", "name": "Leipzig-Mitte"},
                {"id": "314", "name": "Leipzig-West"}
            ],
            "pollen_region": "Sachsen",
            "pollen_subregion": "Sachsen",
            "region_id": "80", 
            "partregion_id": "-1"
        },
        "Dresden": {
            "lat": 51.05, 
            "lon": 13.74,
            "stations": [
                {"id": "298", "name": "Dresden-Nord"},
                {"id": "311", "name": "Dresden-Winckelmannstr."}
            ],
            "pollen_region": "Sachsen",
            "pollen_subregion": "Sachsen",
            "region_id": "80", 
            "partregion_id": "-1"
        },
        "Hannover": {
            "lat": 52.37, 
            "lon": 9.73,
            "stations": [
                {"id": "602", "name": "Hannover"}
            ],
            "pollen_region": "Niedersachsen und Bremen",
            "pollen_subregion": "Östl. Niedersachsen",
            "region_id": "30", 
            "partregion_id": "32"
        },
        "Nürnberg": {
            "lat": 49.45, 
            "lon": 11.08,
            "stations": [
                {"id": "477", "name": "Nürnberg/Bahnhof"}
            ],
            "pollen_region": "Bayern",
            "pollen_subregion": "Bayern (Nord)",
            "region_id": "70", 
            "partregion_id": "71"
        }
    }
    
    # Liste der Allergenen für allergisches Asthma
    asthma_allergene = ["Graeser", "Hasel", "Birke", "Erle", "Ambrosia", "Beifuß", "Roggen"]
    
    # Stadt-Auswahl mit Standortfunktion
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_city = st.selectbox("🌍 Stadt auswählen:", list(locations.keys()))
    
    with col2:
        # Standortbutton hinzufügen
        if st.button("📍 Meinen Standort verwenden"):

            
            # JavaScript-Code für Geolokalisierung einbinden
            st.markdown("""
            <script>
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // In einer realen Implementierung würden die Koordinaten an den Server gesendet
                    console.log("Standort: " + position.coords.latitude + ", " + position.coords.longitude);
                    // Da Streamlit kein direktes JavaScript-Callback unterstützt, müssten wir hier 
                    // einen Workaround mit einer API-Anfrage implementieren
                },
                function(error) {
                    console.error("Fehler bei der Standortbestimmung: " + error.message);
                }
            );
            </script>
            """, unsafe_allow_html=True)
            
            # Für Demozwecke nehmen wir an, dass der Benutzer in Kiel ist
            selected_city = "Kiel"
            st.success(f"Standort erkannt: {selected_city}")
    
    # Ausgewählte Stadt-Daten
    location_data = locations[selected_city]
    
    # Stationsauswahl in die Hauptansicht verschieben
    stations = location_data["stations"]
    if len(stations) > 1:
        selected_station = st.selectbox(
            "📍 Messstation auswählen:", 
            [s["name"] for s in stations]
        )
        station_id = next(s["id"] for s in stations if s["name"] == selected_station)
    else:
        selected_station = stations[0]["name"]
        station_id = stations[0]["id"]
        st.info(f"Verfügbare Messstation: {selected_station}")
    
    
    # Übersichts-Dashboard
    st.subheader(f"Umwelt-Übersicht für {selected_city}")
    
    # Fortschrittsbalken für Datenladung
    progress_bar = st.progress(0)
    
    # Daten abrufen
    with st.spinner("Lade alle Umweltdaten..."):
        # Luftqualitätsdaten - fest auf 24 Stunden eingestellt
        progress_bar.progress(10)
        
        # Feste Einstellung auf einen Tag (keine Auswahlmöglichkeit)
        data_days = 1
        
        air_quality_data = get_air_quality_data(
            station_id, 
            (datetime.now() - timedelta(days=data_days)).date(), 
            datetime.now().date(), 
            "00:00", 
            "23:59"
        )
        
        # Pollendaten
        progress_bar.progress(40)
        pollen_info = get_pollen_data(
            location_data["region_id"], 
            location_data["partregion_id"]
        )
        
        # Gewitterdaten
        progress_bar.progress(70)
        thunder_forecast = get_thunder_forecast(
            location_data["lat"], 
            location_data["lon"]
        )
        
        # Saharastaubdaten
        progress_bar.progress(90)
        sahara_status = get_sahara_dust_status(
            selected_city,
            location_data["lat"], 
            location_data["lon"]
        )
        
        # Smog-Daten berechnen (basierend auf Luftqualitätsdaten)
        smog_status = calculate_smog_status(air_quality_data)
        
        progress_bar.progress(100)
    
    # Progress Bar ausblenden nach dem Laden
    progress_bar.empty()

    
    # Obere Informationskarten
    col1, col2, col3, col4 = st.columns(4)
    
    # Luftqualitäts-Karte
    with col1:
        st.subheader("📊 Luft")
        
        if air_quality_data:
            # Berechnung des offiziellen LQI basierend auf dem schlechtesten Einzelwert
            rating = calculate_air_quality_rating(air_quality_data)
            
            # Farbcodierte LQI-Anzeige entsprechend der UBA-Bewertung
            if rating == "Sehr gut":
                st.success(f"🟦 Luftqualität: {rating}")
                st.markdown("✅ **Beste Voraussetzungen, um sich ausgiebig im Freien aufzuhalten.**")
            elif rating == "Gut":
                st.info(f"🟩 Luftqualität: {rating}")
                st.markdown("✅ **Genießen Sie Ihre Aktivitäten im Freien, gesundheitlich nachteilige Wirkungen sind nicht zu erwarten.**")
            elif rating == "Mäßig":
                st.warning(f"🟨 Luftqualität: {rating}")
                st.markdown("⚠️ **Kurzfristige nachteilige Auswirkungen auf die Gesundheit sind unwahrscheinlich. Empfindliche Personen sollten vorsichtig sein.**")
            elif rating == "Schlecht":
                st.error(f"🟧 Luftqualität: {rating}")
                st.markdown("⚠️ **Bei empfindlichen Menschen können nachteilige gesundheitliche Wirkungen auftreten. Körperlich anstrengende Tätigkeiten im Freien vermeiden.**")
            elif rating == "Sehr schlecht":
                st.error(f"🟥 Luftqualität: {rating}")
                st.markdown("❌ **Negative gesundheitliche Auswirkungen können auftreten. Empfindliche Personen sollten körperliche Anstrengungen im Freien vermeiden.**")
            else:
                st.warning("Keine ausreichenden LQI-Daten verfügbar")
        else:
            st.error("Keine Luftqualitätsdaten verfügbar")
    
    # Pollen-Karte
    with col2:
        st.subheader("🌿 Pollen")
        
        if pollen_info:
            aktive = []
            asthma_pollen = []
            
            for p in pollen_info:
                today_val = parse_pollen_value(p['Heute'])
                if today_val > 0:
                    level = pollen_level_label(today_val)
                    aktive.append(f"{p['Pollenart']} ({level})")
                    # Prüfen, ob es sich um ein Allergen für allergisches Asthma handelt
                    if p['Pollenart'] in asthma_allergene and today_val > 1:
                        asthma_pollen.append(p['Pollenart'])
            
            if aktive:
                if any("🟥" in item for item in aktive):
                    st.error(f"Starke Belastung durch {', '.join(aktive)}")
                elif any("🟧" in item for item in aktive):
                    st.warning(f"Mäßige Belastung durch {', '.join(aktive)}")
                else:
                    st.info(f"Geringe Belastung durch {', '.join(aktive)}")
                    
                # Warnung für allergisches Asthma
                if asthma_pollen:
                    st.warning(f"⚠️ **Asthma-Achtung:** Erhöhtes Risiko für allergisches Asthma durch {', '.join(asthma_pollen)}.")
            else:
                st.success("Heute keine Pollenbelastung")
        else:
            st.error("Keine Pollendaten verfügbar")
    
    # Gewitter-Karte
    with col3:
        st.subheader("⚡ Gewitter")
        
        if thunder_forecast is not None:
            if thunder_forecast:
                st.warning(f"Gewitter erwartet in den nächsten 5 Tagen")
                st.markdown(f"Nächstes Gewitter: {thunder_forecast[0]['zeit']}")
                
                # Warnung für Gewitterasthma hinzufügen
                st.error("⚠️ **Gewitterasthma-Warnung:** Bei Gewitter erhöhtes Risiko für Asthmaanfälle. Asthmapatienten sollten Fenster schließen und sich im Inneren aufhalten.")
            else:
                st.success("Keine Gewitter vorhergesagt")
        else:
            st.error("Keine Gewitterdaten verfügbar")
    
    # Saharastaub-Karte
    with col4:
        st.subheader("🌫️ Sahara")
        
        if sahara_status and sahara_status["status"] != "Keine Daten":
            if sahara_status["status"] == "Ja":
                st.warning(f"Saharastaub aktiv (AOD: {sahara_status['max_aod']:.2f})")
            else:
                st.success("Kein Saharastaub")
        else:
            st.error("Keine Saharastaubdaten verfügbar")
    
    # Neue Smog-Karte
    st.subheader("🏭 Smog-Status")
    
    if smog_status:
        if smog_status["status"] == "Gefahr":
            st.error(f"⚠️ Smog-Warnung: {smog_status['message']}")
        elif smog_status["status"] == "Erhöht":
            st.warning(f"⚠️ Erhöhtes Smog-Risiko: {smog_status['message']}")
        else:
            st.success(f"✅ Kein Smog: {smog_status['message']}")
    else:
        st.error("Keine Daten für Smog-Berechnung verfügbar")
    
    # Detaillierte Tabs für weitere Informationen
    tab1, tab2, tab3, tab4 = st.tabs(["_Luftqualität Details_", "_Pollen Details_", "_Gewitter Details_", "_Saharastaub Details_"])
    
    with tab1:
        if air_quality_data:
            display_air_quality_details(air_quality_data)
        else:
            st.error("Keine Luftqualitätsdaten verfügbar.")
    
    with tab2:
        if pollen_info:
            display_pollen_details(pollen_info, asthma_allergene)
        else:
            st.error("Keine Pollendaten verfügbar.")
    
    with tab3:
        if thunder_forecast is not None:
            display_thunder_details(thunder_forecast, selected_city)
        else:
            st.error("Keine Gewitterdaten verfügbar.")
    
    with tab4:
        if sahara_status:
            display_sahara_details(sahara_status)
        else:
            st.error("Keine Saharastaubdaten verfügbar.")
    
    # Fußzeile mit Zeitstempel
    st.markdown("---")
    current_datetime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    st.caption(f"Stand: {current_datetime}")

def get_air_quality_data(station_id, start_date, end_date, start_time, end_time):
    """Luftqualitätsdaten vom Umweltbundesamt abrufen"""
    try:
        url = "https://www.umweltbundesamt.de/api/air_data/v3/airquality/json"
        params = {
            "station": station_id,
            "date_from": str(start_date),
            "date_to": str(end_date),
            "time_from": start_time,
            "time_to": end_time,
            "lang": "de"
        }
        
        st.info(f"Rufe Luftqualitätsdaten ab für Station {station_id} vom {start_date} bis {end_date}")
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            st.error(f"❌ Fehler beim Abruf der Luftqualitätsdaten: {response.status_code}")
            return None
        
        data = response.json()
        station_data = data.get("data", {}).get(str(station_id), {})
        
        # Prüfe, ob Daten vorhanden sind
        if not station_data:
            st.warning(f"Keine Daten für Station {station_id} im angegebenen Zeitraum verfügbar.")
            
            # Versuche, einen größeren Zeitraum abzurufen (bis zu 7 Tage zurück)
            for days_back in [3, 5, 7]:
                earlier_start = (datetime.now() - timedelta(days=days_back)).date()
                st.info(f"Versuche, Daten vom {earlier_start} bis {end_date} abzurufen...")
                
                params["date_from"] = str(earlier_start)
                backup_response = requests.get(url, params=params)
                
                if backup_response.status_code == 200:
                    backup_data = backup_response.json()
                    backup_station_data = backup_data.get("data", {}).get(str(station_id), {})
                    
                    if backup_station_data:
                        st.success(f"Daten erfolgreich für einen erweiterten Zeitraum abgerufen: {earlier_start} bis {end_date}")
                        return backup_station_data
            
            st.error("Keine Daten auch nach erweiterter Suche verfügbar.")
            return None
            
        # Wenn Daten gefunden wurden, prüfe das neueste Datum
        timestamps = list(station_data.keys())
        if timestamps:
            latest_timestamp = max(timestamps)
            data_time = datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - data_time
            
            # Zeige Information über das Datums-Alter an
            hours_diff = time_diff.total_seconds() / 3600
            if hours_diff > 24:
                st.warning(f"⚠️ Die neuesten Daten sind {int(hours_diff)} Stunden alt (von {data_time.strftime('%d.%m.%Y %H:%M')})")
            else:
                st.success(f"Neueste Daten von {data_time.strftime('%d.%m.%Y %H:%M')} (vor {int(hours_diff)} Stunden)")
        
        return station_data
    except Exception as e:
        st.error(f"❌ Fehler bei der Verarbeitung der Luftqualitätsdaten: {str(e)}")
        return None

def display_air_quality_details(air_quality_data):
    """Aufbereitung und Anzeige der detaillierten Luftqualitätsdaten"""
    st.subheader("Luftqualitätsdetails")
    
    air_quality_list = []
    components_data = {}
    
    for timestamp, values in air_quality_data.items():
        components = values[3:]
        for component in components:
            component_id = component[0]
            try:
                component_value = float(component[1])
                lqi_value = float(component[3])
            except:
                continue

            # Verwende das JSON-Mapping für die Komponenten
            str_component_id = str(component_id)
            if str_component_id in AIR_QUALITY_COMPONENTS:
                component_info = AIR_QUALITY_COMPONENTS[str_component_id]
                comp_name = component_info["code"]
                unit = component_info["unit"]
                full_name = component_info["name"]
                symbol = component_info["symbol"]
            else:
                unit, comp_name = "Nicht verfügbar", f"Komponente {component_id}"
                full_name = "Unbekannte Komponente"
                symbol = ""

            # Für tabellarische Darstellung
            air_quality_list.append({
                "Zeitpunkt": timestamp,
                "Messwert": component_value,
                "Komponente": comp_name,
                "Symbol": symbol,
                "Vollständiger Name": full_name,
                "LQI": lqi_value,
                "Einheit": unit
            })
            
            # Für das kombinierte Diagramm
            if comp_name not in components_data:
                components_data[comp_name] = []
            
            components_data[comp_name].append({
                "Zeitpunkt": timestamp,
                "Messwert": component_value
            })

    # Aktuelle Messwerte anzeigen
    st.subheader("Aktuelle Messwerte & Gesundheitsbewertung")
    
    # Tabelle mit allen aktuellen Komponenten
    latest_values = {}
    for comp_name, data_list in components_data.items():
        sorted_data = sorted(data_list, key=lambda x: x["Zeitpunkt"], reverse=True)
        if sorted_data:
            latest_values[comp_name] = sorted_data[0]["Messwert"]
    
    if latest_values:
        # Tabelle für bessere Darstellung verwenden
        messwerte = []
        for comp, val in latest_values.items():
            qual = interpret_component(comp, val)
            # Finden der vollständigen Informationen für diese Komponente
            comp_info = next((AIR_QUALITY_COMPONENTS[cid] for cid, info in AIR_QUALITY_COMPONENTS.items() 
                             if info["code"] == comp), None)
            
            if comp_info:
                symbol = comp_info["symbol"]
                full_name = comp_info["name"]
                unit = comp_info["unit"]
            else:
                symbol = comp
                full_name = "Unbekannt"
                unit = "µg/m³"
                
            messwerte.append({
                "Symbol": symbol,
                "Name": full_name,
                f"Wert ({unit})": val,
                "Bewertung": qual
            })
        
        df_messwerte = pd.DataFrame(messwerte)
        st.dataframe(df_messwerte, hide_index=True, use_container_width=True)
    
    # Verhaltensempfehlungen nur anzeigen, wenn Luftqualität schlecht ist
    avg_rating = "Gut"  # Standardwert
    if latest_values:
        ratings = [interpret_component(comp, val) for comp, val in latest_values.items()]
        if "Schlecht" in ratings:
            avg_rating = "Schlecht"
    
    # Nur Verhaltensempfehlungen anzeigen, wenn Luftqualität schlecht ist (nicht bei mäßig)
    if avg_rating == "Schlecht":
        st.subheader("Verhaltensempfehlungen bei aktueller Luftqualität")
        
        # Erhöhte Feinstaubwerte identifizieren und anzeigen
        elevated_components = []
        for comp, val in latest_values.items():
            rating = interpret_component(comp, val)
            if rating == "Schlecht":
                # Finden der vollständigen Informationen für diese Komponente
                comp_info = next((AIR_QUALITY_COMPONENTS[cid] for cid, info in AIR_QUALITY_COMPONENTS.items() 
                                if info["code"] == comp), None)
                unit = comp_info["unit"] if comp_info else "µg/m³"
                elevated_components.append(f"{comp}: {val:.1f} {unit} ({rating})")
        
        if elevated_components:
            st.info(f"**Erhöhte Schadstoffwerte:** {', '.join(elevated_components)}")
        
        # Empfehlungen für schlechte Luftqualität
        st.error("""
        ❌ **Bei schlechter Luftqualität:**
        - Vermeiden Sie Aktivitäten im Freien, besonders an stark befahrenen Straßen
        - Halten Sie Fenster geschlossen, besonders zu Hauptverkehrszeiten
        - Asthmatiker und Personen mit Lungenerkrankungen: Notfallmedikamente griffbereit halten
        - Verwenden Sie ggf. einen Luftreiniger in Innenräumen
        - Bei Symptomen wie Atemnot, Husten oder Reizungen: Ärztlichen Rat einholen
        """)
    

    # Kombiniertes Diagramm für alle Komponenten
    st.subheader("Verlauf der letzten 24 Stunden (alle Komponenten)")
    
    if components_data:
        # Erstelle ein DataFrame für das kombinierte Diagramm
        combined_df = pd.DataFrame()
        
        for comp_name, data_list in components_data.items():
            if data_list:
                df_comp = pd.DataFrame(data_list)
                df_comp["Zeitpunkt"] = pd.to_datetime(df_comp["Zeitpunkt"])
                df_comp = df_comp.set_index("Zeitpunkt")
                combined_df[comp_name] = df_comp["Messwert"]
        
        if not combined_df.empty:
            st.line_chart(combined_df)
        else:
            st.warning("Keine Daten für das Diagramm verfügbar")
    else:
        st.warning("Keine Komponentendaten verfügbar")

def calculate_air_quality_rating(air_quality_data):
    """Berechnung der Luftqualitätsbewertung basierend auf dem offiziellen Umweltbundesamt LQI
    
    Der LQI richtet sich nach dem Schadstoff mit der schlechtesten Bewertung.
    """
    if not air_quality_data:
        return "Keine Daten"
        
    # Extrahiere die neuesten Werte für relevante Komponenten
    pollutant_values = {}
    
    for timestamp, values in air_quality_data.items():
        components = values[3:]
        for component in components:
            component_id = component[0]
            str_component_id = str(component_id)
            
            try:
                component_value = float(component[1])
                
                # Verwende JSON-Mapping für die Komponenten-Identifikation
                if str_component_id in AIR_QUALITY_COMPONENTS:
                    component_code = AIR_QUALITY_COMPONENTS[str_component_id]["code"]
                    if component_code in ["PM10", "PM2", "NO2", "O3"]:
                        if component_code not in pollutant_values:
                            pollutant_values[component_code] = []
                        pollutant_values[component_code].append(component_value)
            except:
                continue
    
    # Berechne den Durchschnitt für jeden Schadstoff
    avg_values = {}
    for comp, values in pollutant_values.items():
        if values:
            avg_values[comp] = np.mean(values)
    
    if not avg_values:
        return "Keine Daten"
    
    # Bewerte jeden Schadstoff und finde die schlechteste Bewertung
    ratings = []
    for comp, val in avg_values.items():
        rating = interpret_component(comp, val)
        ratings.append(rating)
    
    # Priorität: Sehr schlecht > Schlecht > Mäßig > Gut > Sehr gut
    if "Sehr schlecht" in ratings:
        return "Sehr schlecht"
    elif "Schlecht" in ratings:
        return "Schlecht"
    elif "Mäßig" in ratings:
        return "Mäßig"
    elif "Gut" in ratings:
        return "Gut"
    else:
        return "Sehr gut"

def interpret_component(comp, val):
    """Interpretiert den Messwert einer Komponente gemäß offizieller Umweltbundesamt-Luftqualitätsindex-Skala"""
    if comp == "PM10":
        if val <= 20: return "Sehr gut"
        elif val <= 35: return "Gut"
        elif val <= 50: return "Mäßig"
        elif val <= 100: return "Schlecht"
        else: return "Sehr schlecht"
    elif comp == "PM2":
        if val <= 10: return "Sehr gut"
        elif val <= 20: return "Gut"
        elif val <= 25: return "Mäßig"
        elif val <= 50: return "Schlecht"
        else: return "Sehr schlecht"
    elif comp == "NO2":
        if val <= 20: return "Sehr gut"
        elif val <= 40: return "Gut"
        elif val <= 100: return "Mäßig"
        elif val <= 200: return "Schlecht"
        else: return "Sehr schlecht"
    elif comp == "O3":
        if val <= 60: return "Sehr gut"
        elif val <= 120: return "Gut"
        elif val <= 180: return "Mäßig"
        elif val <= 240: return "Schlecht"
        else: return "Sehr schlecht"
    else:
        return "Nicht bewertet"

def calculate_smog_status(air_quality_data):
    """Berechnet den Smog-Status basierend auf Luftqualitätsdaten"""
    if not air_quality_data:
        return None
        
    # Extrahiere die neuesten Werte für relevante Komponenten
    latest_values = {"PM10": 0, "PM2": 0, "NO2": 0, "O3": 0}
    latest_timestamp = None
    
    for timestamp, values in air_quality_data.items():
        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_timestamp = timestamp
            
        components = values[3:]
        for component in components:
            component_id = component[0]
            str_component_id = str(component_id)
            
            try:
                component_value = float(component[1])
                
                # Verwende JSON-Mapping für die Komponenten-Identifikation
                if str_component_id in AIR_QUALITY_COMPONENTS:
                    component_code = AIR_QUALITY_COMPONENTS[str_component_id]["code"]
                    if component_code in latest_values:
                        latest_values[component_code] = max(latest_values[component_code], component_value)
            except:
                continue
    
    # Smog-Definition basierend auf UBA-Schwellenwerten
    # Smog-Definition: Kombination aus hohen Werten für PM10, PM2.5 und NO2 bei geringer Luftbewegung
    smog_score = 0
    
    # PM10 Bewertung (nach UBA-Skala)
    if latest_values["PM10"] > 100:  # sehr schlecht
        smog_score += 3
    elif latest_values["PM10"] > 50:  # schlecht
        smog_score += 2
    elif latest_values["PM10"] > 35:  # mäßig
        smog_score += 1
        
    # PM2.5 Bewertung (nach UBA-Skala)
    if latest_values["PM2"] > 50:  # sehr schlecht
        smog_score += 3
    elif latest_values["PM2"] > 25:  # schlecht
        smog_score += 2
    elif latest_values["PM2"] > 20:  # mäßig
        smog_score += 1
        
    # NO2 Bewertung (nach UBA-Skala)
    if latest_values["NO2"] > 200:  # sehr schlecht
        smog_score += 3
    elif latest_values["NO2"] > 100:  # schlecht
        smog_score += 2
    elif latest_values["NO2"] > 40:  # mäßig
        smog_score += 1
    
    # Smog-Status basierend auf Score
    if smog_score >= 6:
        return {
            "status": "Gefahr",
            "message": f"Hohe Smog-Belastung (PM10: {latest_values['PM10']:.1f}, PM2.5: {latest_values['PM2']:.1f}, NO2: {latest_values['NO2']:.1f})",
            "score": smog_score
        }
    elif smog_score >= 3:
        return {
            "status": "Erhöht",
            "message": f"Leicht erhöhte Smog-Werte (PM10: {latest_values['PM10']:.1f}, PM2.5: {latest_values['PM2']:.1f})",
            "score": smog_score
        }
    else:
        return {
            "status": "Normal",
            "message": "Keine Smog-Belastung festgestellt",
            "score": smog_score
        }

def get_pollen_data(region_id, partregion_id):
    """Pollendaten vom DWD abrufen"""
    try:
        response = requests.get("https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json")
        if response.status_code != 200:
            st.error(f"❌ Fehler beim Abruf der DWD-Daten: {response.status_code}")
            return None
        data = response.json()
        for region in data.get("content", []):
            if str(region.get("region_id")) == region_id:
                # Wenn partregion_id = -1, nehmen wir alle Daten für die Region
                if partregion_id == "-1" or str(region.get("partregion_id")) == partregion_id:
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

def parse_pollen_value(value):
    """Parst den Pollenwert und gibt einen numerischen Wert zurück"""
    if value == "-1":
        return 0
    if '-' in value:
        parts = value.split('-')
        return (float(parts[0]) + float(parts[1])) / 2
    return float(value) if value != '0' else 0

def pollen_level_label(value):
    """Gibt ein Label für den Pollenbelastungswert zurück"""
    if value <= 0.5:
        return "🟩 Gering"
    elif value <= 2:
        return "🟧 Mäßig"
    else:
        return "🟥 Stark"

def display_pollen_details(pollen_info, asthma_allergene):
    """Anzeige der detaillierten Pollendaten mit speziellem Fokus auf allergisches Asthma"""
    st.subheader("Pollendetails")
    
    # Pollenvorhersage für alle Tage als Tabelle
    pollen_data = []
    
    for p in pollen_info:
        today_val = parse_pollen_value(p['Heute'])
        tomorrow_val = parse_pollen_value(p['Morgen'])
        dayafter_val = parse_pollen_value(p['Übermorgen'])
        
        pollen_data.append({
            "Pollenart": p['Pollenart'],
            "Heute": pollen_level_label(today_val),
            "Morgen": pollen_level_label(tomorrow_val),
            "Übermorgen": pollen_level_label(dayafter_val)
        })
    
    df_pollen = pd.DataFrame(pollen_data)
    st.dataframe(df_pollen, hide_index=True, use_container_width=True)
    
    # Aktive Pollenarten heute
    st.subheader("Aktive Pollenarten heute")
    aktive = []
    for p in pollen_info:
        today_val = parse_pollen_value(p['Heute'])
        if today_val > 0:
            level = pollen_level_label(today_val)
            aktive.append(f"{p['Pollenart']} ({level})")
    
    if aktive:
        # Gruppiert nach Belastungsgrad
        stark = [p for p in aktive if "🟥" in p]
        maessig = [p for p in aktive if "🟧" in p]
        gering = [p for p in aktive if "🟩" in p]
        
        if stark:
            st.error("Starke Belastung: " + ", ".join(stark))
        if maessig:
            st.warning("Mäßige Belastung: " + ", ".join(maessig))
        if gering:
            st.info("Geringe Belastung: " + ", ".join(gering))
    else:
        st.success("Heute keine Pollenbelastung")
        
    # Spezielle Sektion für allergisches Asthma
    st.subheader("Allergisches Asthma - Risikobewertung")
    
    # Aktive Asthma-relevante Pollen identifizieren
    aktive_asthma_pollen = []
    for p in pollen_info:
        if p['Pollenart'] in asthma_allergene:
            today_val = parse_pollen_value(p['Heute'])
            if today_val > 1:  # Nur mäßige oder starke Belastung berücksichtigen
                aktive_asthma_pollen.append({
                    "Pollenart": p['Pollenart'],
                    "Belastung": pollen_level_label(today_val),
                    "Wert": today_val
                })
    
    if aktive_asthma_pollen:
        # Risikobewertung
        risk_level = 0
        for p in aktive_asthma_pollen:
            if "🟥" in p["Belastung"]:  # Starke Belastung
                risk_level += 2
            elif "🟧" in p["Belastung"]:  # Mäßige Belastung
                risk_level += 1
        
        # Gefärbte Box mit Risikobewertung
        if risk_level >= 3:
            st.error(f"""
            ⚠️ **Hohes Risiko für allergisches Asthma heute!**
            
            Aktive asthma-relevante Allergene:
            {', '.join([f"{p['Pollenart']} ({p['Belastung']})" for p in aktive_asthma_pollen])}
            
            **Empfehlungen:**
            - Halten Sie Ihre Notfallmedikation griffbereit
            - Vermeiden Sie Aufenthalte im Freien
            - Halten Sie Fenster geschlossen
            - Wechseln Sie Kleidung nach dem Aufenthalt im Freien
            - Bei Symptomen sofort Notfallmedikation anwenden und ggf. ärztliche Hilfe aufsuchen
            """)
        elif risk_level >= 1:
            st.warning(f"""
            ⚠️ **Erhöhtes Risiko für allergisches Asthma heute**
            
            Aktive asthma-relevante Allergene:
            {', '.join([f"{p['Pollenart']} ({p['Belastung']})" for p in aktive_asthma_pollen])}
            
            **Empfehlungen:**
            - Führen Sie Ihre Asthma-Medikation nach ärztlichem Plan fort
            - Reduzieren Sie Aktivitäten im Freien
            - Duschen Sie nach dem Aufenthalt im Freien und wechseln Sie die Kleidung
            - Lüften Sie früh morgens oder nach Regen
            """)
    else:
        st.success("""
        ✅ **Geringes Risiko für allergisches Asthma heute**
        
        Derzeit sind keine oder nur geringe Mengen asthma-relevanter Allergene aktiv.
        
        **Tipp:** Führen Sie Ihre Basis-Asthmamedikation nach ärztlichem Plan fort.
        """)
        
    # Gesundheitstipps bei Pollenbelastung
    st.subheader("Gesundheitstipps bei Pollenbelastung")
    st.info("""
    - Fenster in der Stadt morgens, auf dem Land abends schließen
    - Nach dem Aufenthalt im Freien Kleidung wechseln und Haare waschen
    - Pollenfilter in Auto und Wohnung regelmäßig wechseln
    - Wäsche nicht im Freien trocknen während der Pollensaison
    - Antihistaminika nach ärztlicher Empfehlung einnehmen
    - Bei bekanntem allergischem Asthma: Inhalator stets griffbereit halten
    """)

def get_thunder_forecast(lat, lon):
    """Gewittervorhersage abrufen"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=weathercode&timezone=Europe/Berlin"
        response = requests.get(url)
        
        if response.status_code != 200:
            st.error(f"❌ Fehler beim Abrufen der Wetterdaten: {response.status_code}")
            return None
            
        data = response.json()
        times = data["hourly"]["time"]
        codes = data["hourly"]["weathercode"]
        
        # Gewitterprüfung
        gewitterzeiten = []
        for time, code in zip(times, codes):
            # Wettercodes für Gewitter: 95 (leichtes Gewitter), 96, 99 (starkes Gewitter)
            if code in [95, 96, 99]:
                # Formatiere Zeit für Anzeige
                dt = datetime.fromisoformat(time)
                formatted_time = dt.strftime("%d.%m.%Y %H:%00 Uhr")
                intensitaet = "starkes" if code in [96, 99] else "leichtes"
                gewitterzeiten.append({"zeit": formatted_time, "intensitaet": intensitaet})
                
        return gewitterzeiten
    except Exception as e:
        st.error(f"❌ Fehler bei der Gewittervorhersage: {str(e)}")
        return None

def display_thunder_details(thunder_forecast, city_name):
    """Zeigt die detaillierten Gewitterdaten an, mit Fokus auf Gewitterasthma"""
    st.subheader("Gewitterdetails")
    
    if not thunder_forecast:
        st.success(f"✅ Kein Gewitter in {city_name} in den nächsten 5 Tagen vorhergesagt.")
        st.info("Bei Gewitterwarnung werden hier Details zu erwarteten Gewittern angezeigt.")
        return
        
    st.warning(f"⚡ In {city_name} werden in den nächsten 5 Tagen Gewitter erwartet!")
    
    # Zeige alle Gewitterzeiten tabellarisch an
    gewitter_data = []
    for gewitter in thunder_forecast:
        gewitter_data.append({
            "Zeitpunkt": gewitter["zeit"],
            "Intensität": gewitter["intensitaet"]
        })
    
    df_gewitter = pd.DataFrame(gewitter_data)
    st.dataframe(df_gewitter, hide_index=True, use_container_width=True)
    
    # Spezielle Warnung für Gewitterasthma
    st.subheader("Gewitterasthma-Warnung ⚠️")
    st.error("""
    **Was ist Gewitterasthma?**
    Gewitterasthma ist eine plötzliche Verschlechterung asthmatischer Symptome, die durch Gewitter ausgelöst wird. 
    Bei Gewittern werden Pollen durch Feuchtigkeit aufgebrochen und können als kleinere Partikel tiefer in die Atemwege eindringen.
    
    **Wer ist gefährdet?**
    - Personen mit bekanntem Asthma
    - Personen mit Heuschnupfen oder Pollenallergien
    - Auch Personen ohne diagnostiziertes Asthma können betroffen sein
    
    **Vorsichtsmaßnahmen bei Gewittervorhersage:**
    - Bleiben Sie während des Gewitters in Innenräumen
    - Halten Sie Fenster und Türen geschlossen
    - Halten Sie Ihre Asthma-Medikamente bereit
    - Bei Atemnot sofort den Notarzt rufen (112)
    """)
    
    # Sicherheitstipps für Gewitter
    st.subheader("Allgemeine Sicherheitstipps bei Gewitter")
    st.info("""
    - Suchen Sie Schutz in Gebäuden oder Fahrzeugen
    - Meiden Sie offene Flächen, Wasser und einzeln stehende Bäume
    - Elektronische Geräte vom Stromnetz trennen
    - Fenster schließen
    - Bei Starkregen auf mögliche Überschwemmungen achten
    """)

def get_sahara_dust_status(city_name, lat, lon):
    """Saharastaubdaten abrufen"""
    try:
        aod_threshold = 0.39
        
        url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}&hourly=aerosol_optical_depth"
        )
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            st.error(f"❌ Fehler beim Abrufen der Saharastaubdaten: {response.status_code}")
            return None
            
        data = response.json()
        times = data.get("hourly", {}).get("time", [])
        aod_values = data.get("hourly", {}).get("aerosol_optical_depth", [])
        
        if not times or not aod_values:
            return {"status": "Keine Daten", "max_aod": None, "aod_values": None, "times": None}
            
        # Filtere und bereinige AOD-Werte
        aod_data = []
        for t, v in zip(times, aod_values):
            if isinstance(v, (int, float)):
                dt = datetime.fromisoformat(t)
                aod_data.append({"time": dt, "aod": v})
        
        if not aod_data:
            return {"status": "Keine Daten", "max_aod": None, "aod_values": None, "times": None}
            
        # Finde den maximalen AOD-Wert
        max_aod_item = max(aod_data, key=lambda x: x["aod"])
        max_aod = max_aod_item["aod"]
        
        # Erstelle Zeitreihen für Diagramm
        times_clean = [item["time"] for item in aod_data]
        aod_values_clean = [item["aod"] for item in aod_data]
        
        sahara_status = "Ja" if max_aod > aod_threshold else "Nein"

        return {
            "status": sahara_status,
            "max_aod": max_aod,
            "aod_values": aod_values_clean,
            "times": times_clean
        }
    except Exception as e:
        st.error(f"❌ Fehler bei den Saharastaubdaten: {str(e)}")
        return None

def display_sahara_details(sahara_data):
    """Zeigt die detaillierten Saharastaubdaten an"""
    st.subheader("Saharastaub-Details")
    
    if sahara_data["status"] == "Keine Daten":
        st.warning("⚠️ Keine Messwerte für Saharastaub verfügbar.")
        return
        
    # Zeige AOD-Wert und Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("AOD-Maximalwert", f"{sahara_data['max_aod']:.2f}")
    
    with col2:
        if sahara_data["status"] == "Ja":
            st.warning("🌫️ **Hohe Saharastaubbelastung!**")
        else:
            st.success("✅ **Kein Saharastaub**")
    
    # Zeige Diagramm, wenn Daten verfügbar sind
    if sahara_data["aod_values"] and sahara_data["times"]:
        # Erstelle DataFrame für das Diagramm
        df_sahara = pd.DataFrame({
            "Zeitpunkt": sahara_data["times"],
            "AOD-Wert": sahara_data["aod_values"]
        })
        
        df_sahara = df_sahara.set_index("Zeitpunkt")
        
        # Zeige das Diagramm
        st.subheader("AOD-Werte im Zeitverlauf")
        st.line_chart(df_sahara)
        
        # Zeige horizontale Linie für den Schwellenwert
        st.markdown(f"Die rote Linie würde den Schwellenwert von 0.39 darstellen, ab dem Saharastaub erkannt wird.")
    
    # Gesundheitsinformationen
    st.subheader("Gesundheitsinformationen bei Saharastaub")
    
    if sahara_data["status"] == "Ja":
        st.warning("""
        Bei erhöhter Saharastaubkonzentration:
        - Körperliche Anstrengung im Freien reduzieren
        - Menschen mit Atemwegserkrankungen sollten besonders vorsichtig sein
        - Bei Bedarf Fenster geschlossen halten
        - Mehr trinken als üblich
        - Bei Atembeschwerden ärztlichen Rat einholen
        - Asthmapatienten: Beobachten Sie Ihre Symptome sorgfältig und passen Sie ggf. Ihre Medikation nach Rücksprache mit dem Arzt an
        """)
    else:
        st.info("Aktuell keine besonderen Maßnahmen erforderlich.")

def check_geolocation(lat, lon):
    """Überprüft die nächstgelegene Stadt basierend auf Geokoordinaten"""
    try:
        # Verwenden des Nominatim Geocoders aus geopy
        geolocator = Nominatim(user_agent="umwelt-dashboard-app")
        location = geolocator.reverse(f"{lat}, {lon}", language="de")
        
        if not location:
            return None
            
        address = location.raw.get("address", {})
        
        # Verschiedene Adresselemente prüfen
        city = address.get("city")
        town = address.get("town")
        village = address.get("village")
        suburb = address.get("suburb")
        
        # Erste nicht-leere Stadt/Siedlung zurückgeben
        for place in [city, town, village, suburb]:
            if place:
                return place
                
        return None
    except Exception as e:
        st.error(f"Fehler bei der Standortbestimmung: {str(e)}")
        return None

def find_nearest_city(lat, lon, locations):
    """Findet die nächstgelegene Stadt in der locations-Liste basierend auf Koordinaten"""
    min_distance = float('inf')
    nearest_city = None
    
    for city, data in locations.items():
        city_lat = data["lat"]
        city_lon = data["lon"]
        
        # Einfache Entfernungsberechnung (Luftlinie)
        distance = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5
        
        if distance < min_distance:
            min_distance = distance
            nearest_city = city
    
    return nearest_city
