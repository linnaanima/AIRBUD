import streamlit as st
import pandas as pd
import requests
import altair as alt
import pydeck as pdk

def app():
    components = {
        "NO₂ (Stickstoffdioxid)": 5,
        "PM10 (Feinstaub)": 1
    }

    st.subheader("Luftqualitätsanalyse – Umweltbundesamt")
    component_name = st.selectbox("Wähle Schadstoff", list(components.keys()))
    year = st.selectbox("Wähle Jahr", list(range(2000, 2025))[::-1])
    component = components[component_name]

    stations_url = "https://www.umweltbundesamt.de/api/air_data/v3/stations/json"
    jahresbilanz_url = f"https://www.umweltbundesamt.de/api/air_data/v3/annualbalances/json?component={component}&year={year}&lang=de"

    try:

        station_response = requests.get(stations_url)
        station_data = station_response.json()["data"]

        station_list = []
        for station_id, values in station_data.items():
            station_list.append({
                "station_id": values[0],
                "station_code": values[1],
                "name": values[2],
                "city": values[3],
                "latitude": float(values[8]),
                "longitude": float(values[7])
            })
        station_df = pd.DataFrame(station_list)

        # Lade Jahresbilanzdaten
        st.subheader("📊 Jahresbilanz")
        bilanz_response = requests.get(jahresbilanz_url)
        bilanz_json = bilanz_response.json()
        headers = bilanz_json["headers"]
        bilanz_raw = bilanz_json["data"]

        bilanz_list = []
        for row in bilanz_raw:
            station_id = row[0]
            eintrag = {"station_id": station_id}
            for i, key in enumerate(headers.keys()):
                if i == 0:
                    continue
                try:
                    eintrag[headers[str(i)]] = float(row[i])
                except:
                    eintrag[headers[str(i)]] = None
            bilanz_list.append(eintrag)

        bilanz_df = pd.DataFrame(bilanz_list)
        merged_df = pd.merge(bilanz_df, station_df, on="station_id", how="left")


        search_city = st.text_input("Gib (Teil-)Namen der Stadt ein (leer = alle)")

        if search_city:
            filtered_df = merged_df[merged_df["city"].str.contains(search_city, case=False, na=False)]
        else:
            filtered_df = merged_df

        max_stations = len(filtered_df)
        num_stations = st.slider("Anzahl der Städte im Diagramm anzeigen", min_value=5, max_value=min(100, max_stations), value=20)

        metric = list(headers.values())[0]
        if metric in filtered_df.columns and not filtered_df.empty:
            display_df = filtered_df.sort_values(by=metric, ascending=False).head(num_stations)

            chart = alt.Chart(display_df).mark_bar().encode(
                x=alt.X('name:N', sort='-y', title="Station"),
                y=alt.Y(f"{metric}:Q", title=metric),
                tooltip=["name", metric, "city"]
            ).properties(width=800, height=400)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Keine Daten für die gewählte Stadt/Filter gefunden.")

        # Vergleich aller Schadstoffe über die Jahre
        st.subheader("📉 Entwicklung aller Schadstoffe im Vergleich")
        jahre = list(range(2010, 2025))
        alle_werte = []

        for comp_name, comp_id in components.items():
            for y in jahre:
                url = f"https://www.umweltbundesamt.de/api/air_data/v3/annualbalances/json?component={comp_id}&year={y}&lang=de"
                try:
                    r = requests.get(url).json()
                    headers_comp = r["headers"]
                    data = r["data"]
                    metric_label = list(headers_comp.values())[0]
                    werte = [
                        float(row[1]) for row in data
                        if isinstance(row[1], (int, float, str)) and str(row[1]).replace('.', '', 1).isdigit()
                    ]
                    if werte:
                        alle_werte.append({
                            "Jahr": y,
                            "Wert": sum(werte) / len(werte),
                            "Komponente": comp_name
                        })
                except:
                    continue

        alle_df = pd.DataFrame(alle_werte)

        if not alle_df.empty:
            chart_all = alt.Chart(alle_df).mark_line(point=True).encode(
                x=alt.X("Jahr:O", title="Jahr"),
                y=alt.Y("Wert:Q", title="Durchschnittlicher Jahreswert"),
                color=alt.Color("Komponente:N", title="Schadstoff"),
                tooltip=["Jahr", "Komponente", "Wert"]
            ).properties(width=800, height=400)
            st.altair_chart(chart_all, use_container_width=True)

        # Top 40 Orte mit bester Luftqualität
        st.subheader(f"🏆 Orte mit der besten Luftqualität ({metric}) {year}")
        if metric in merged_df.columns:
            best_df = merged_df.sort_values(by=metric).head(40)

            # Hellblaues Balkendiagramm
            best_chart = alt.Chart(best_df).mark_bar(color='#ADD8E6').encode(
                x=alt.X('name:N', sort='y', title="Station"),
                y=alt.Y(f"{metric}:Q", title=metric),
                tooltip=["name", metric, "city"]
            ).properties(width=1000, height=400)
            st.altair_chart(best_chart, use_container_width=True)

            # 📍 Interaktive Karte
            st.subheader(f"📍 Geografische Verteilung – Beste Luftqualität ({metric}) {year}")
            best_map_df = best_df[["name", "city", metric, "latitude", "longitude"]].copy()
            best_map_df.rename(columns={"latitude": "lat", "longitude": "lon"}, inplace=True)

            initial_lat = best_map_df.iloc[0]["lat"]
            initial_lon = best_map_df.iloc[0]["lon"]

            min_val = best_map_df[metric].min()
            max_val = best_map_df[metric].max()

            def color_scale(value):
                ratio = (value - min_val) / (max_val - min_val) if max_val != min_val else 0
                r = int(255 * ratio)
                g = int(255 * (1 - ratio))
                return [r, g, 0, 160]

            best_map_df["color"] = best_map_df[metric].apply(color_scale)

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=best_map_df,
                get_position='[lon, lat]',
                get_color='color',
                get_radius=5000,
                pickable=True,
            )

            tooltip = {
                "html": "<b>{name}</b><br/>Ort: {city}<br/>Wert: {" + metric + "}",
                "style": {"backgroundColor": "white", "color": "black"}
            }

            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=pdk.ViewState(
                    latitude=initial_lat,
                    longitude=initial_lon,
                    zoom=9,
                    pitch=40,
                ),
                layers=[layer],
                tooltip=tooltip
            ))

        else:
            st.warning("Metrik für Bewertung der Luftqualität nicht gefunden.")

    except Exception as e:
        st.error("❌ Fehler beim Laden oder Verarbeiten der Daten.")
        st.exception(e)
        st.markdown("""
           
        > 🔍 Quelle: [Umweltbundesamt](https://www.umweltbundesamt.de/api/air_data/v3/)
        """
                    )
