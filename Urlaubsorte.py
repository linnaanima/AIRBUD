import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    def load_data():
        df = pd.read_excel("who_aap_2021_v9_11august2022.xlsx",
            sheet_name='AAP_2022_city_v9'
        )
        df = df[['ISO3', 'WHO Country Name', 'City or Locality', 'PM2.5 (μg/m3)', 'Measurement Year']].dropna()
        # Originalcode beibehalten
        df_country = df.groupby(['ISO3', 'WHO Country Name']).mean(numeric_only=True).reset_index()
        return df, df_country

    df_raw, df_country = load_data()

    def classify_pm25(value):
        if value <= 5:
            return "Sehr gut (0–5)"
        elif value <= 10:
            return "Gut (5–10)"
        elif value <= 15:
            return "Mäßig (10–15)"
        elif value <= 25:
            return "Ungesund für empfindliche Gruppen (15–25)"
        else:
            return "Gesundheitlich bedenklich (25+)"

    # --- Länder mit bester Luftqualität ---
    st.subheader("Länder mit der besten Luftqualität nach WHO.")
    top_countries = df_country.sort_values('PM2.5 (μg/m3)').head(30)
    
    # Erste Grafik unverändert lassen, wie vom Benutzer gewünscht
    fig_country = px.bar(
        top_countries,
        x='WHO Country Name',
        y='PM2.5 (μg/m3)',
        title='Top 30 Länder mit bester Luftqualität (PM2.5)',
        labels={'PM2.5 (μg/m3)': 'PM2.5 (μg/m³)', 'WHO Country Name': 'Land'},
        color='PM2.5 (μg/m3)',
        color_continuous_scale='Blues',
    )
    
    st.plotly_chart(fig_country)

    # --- Städte mit bester Luftqualität ---
    st.header("Städte mit der besten Luftqualität")
    # Filter auf Städte mit PM2.5 <= 15 (Sehr gut bis mäßig)
    clean_cities = df_raw[df_raw["PM2.5 (μg/m3)"] <= 15].copy()
    clean_cities = clean_cities.sort_values("PM2.5 (μg/m3)").reset_index(drop=True)

    # Slider: Anzahl angezeigter Städte
    num_cities = st.slider("Anzahl Städte anzeigen", min_value=5, max_value=50, value=30, step=5)
    selected_cities = clean_cities.head(num_cities)

    # WHO-Klassifikation hinzufügen
    selected_cities["Luftqualitätsstufe"] = selected_cities["PM2.5 (μg/m3)"].apply(classify_pm25)

    # Balkendiagramm
    fig_cities = px.bar(
        selected_cities,
        x='City or Locality',
        y='PM2.5 (μg/m3)',
        color='WHO Country Name',
        title=f'Top {num_cities} sauberste Städte weltweit (PM2.5 ≤ 15 μg/m³)',
        labels={
            'City or Locality': 'Stadt',
            'PM2.5 (μg/m3)': 'PM2.5 (μg/m³)',
            'WHO Country Name': 'Land'
        },
        hover_data=['WHO Country Name', 'PM2.5 (μg/m3)', 'Luftqualitätsstufe'],
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # für das zweite Diagramm, aber den Rest des Layouts beibehalten
    fig_cities.update_layout(
        xaxis_tickangle=45,
        yaxis=dict(
            range=[0, 15],  # Festlegung des Bereichs auf 0-15 μg/m³
        )
    )
    
    st.plotly_chart(fig_cities)
# --- Weltkarte als Choropleth ---
    st.header("Weltkarte der Luftqualität (nach Ländern)")
    
    df_country["Luftqualitätsstufe"] = df_country["PM2.5 (μg/m3)"].apply(classify_pm25)
    
    color_map = {
        "Sehr gut (0–5)": "#2ECC71",
        "Gut (5–10)": "#A9DFBF",
        "Mäßig (10–15)": "#F7DC6F",
        "Ungesund für empfindliche Gruppen (15–25)": "#F5B041",
        "Gesundheitlich bedenklich (25+)": "#E74C3C"
    }
    
    fig_choropleth = px.choropleth(
        df_country,
        locations="ISO3",
        color="Luftqualitätsstufe",
        hover_name="WHO Country Name",
        title="PM2.5-Luftqualität weltweit nach WHO-Klassifikation",
        color_discrete_map=color_map,
        projection="natural earth"
    )
    
    fig_choropleth.update_geos(showcoastlines=True, coastlinecolor="LightGray")
    
    # Legende unter die Karte legen
    fig_choropleth.update_layout(
        legend=dict(
            orientation="h",      # horizontal
            yanchor="bottom",     # vertikale Ausrichtung
            y=-0.2,               # Position unter der Karte
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig_choropleth, use_container_width=True)


    # --- WHO Einstufung anzeigen ---
    st.markdown("""
     > 🔍 Quelle: [WHO Global Air Quality Guidelines (2021)](https://www.who.int/news/item/22-09-2021-who-global-air-quality-guidelines)
    """)
