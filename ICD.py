import streamlit as st
import pandas as pd
import requests
import altair as alt

def app():
    st.subheader("Krankheiten und Luftschadstoffe im Vergleich")
    st.markdown("Analyse von Krankenhausfällen, Todesfällen und Luftschadstoffen.")

    # Lokales CSV einlesen
    try:
        df_kr = pd.read_csv("krankenhausdaten_long.csv")
        df_kr.columns = df_kr.columns.str.strip()
        df_kr["Jahr"] = pd.to_numeric(df_kr["Jahr"], errors="coerce")
        df_kr["Fälle"] = pd.to_numeric(df_kr["Fälle"], errors="coerce")
        df_kr = df_kr.dropna(subset=["Jahr", "Fälle", "Bezeichnung"])
    except Exception as e:
        st.error("❌ Fehler beim Einlesen der Krankenhausdaten:")
        st.exception(e) 
        st.stop()

    # Diagnoseauswahl
    diagnosen = sorted(df_kr["Bezeichnung"].unique().tolist())
    selected_diagnosen = st.multiselect("🏥 Wähle Diagnosegruppen", diagnosen, default=diagnosen[:5])
    df_diag = df_kr[df_kr["Bezeichnung"].isin(selected_diagnosen)]

    # Krankenhausfälle Diagramm
    st.subheader("📈 Krankenhausfälle pro Jahr")
    chart_krankheiten = alt.Chart(df_diag).mark_line(point=True).encode(
        x=alt.X("Jahr:O", title="Jahr"),
        y=alt.Y("Fälle:Q", title="Fallzahlen"),
        color=alt.Color("Bezeichnung:N", title="Diagnosegruppe"),
        tooltip=["Jahr", "Bezeichnung", "Fälle"]
    ).properties(width=1000, height=400)

    st.altair_chart(chart_krankheiten, use_container_width=True)

    # Todesfälle durch Luftschadstoffe (Excel-Dateien)
    st.subheader("Todesfälle durch Luftschadstoffe 2022 (EEA-Auswertung)")

    try:
        df_no2 = pd.read_excel("https://www.duh.de/fileadmin/user_upload/download/Projektinformation/Verkehr/Luftreinhaltung/DUH-Auswertung_EEA_Todesf%C3%A4lle_NO2.xlsx", skiprows=2)
        df_pm25 = pd.read_excel("DUH-Auswertung_EEA_Todesfälle_PM2_5.xlsx", skiprows=2)

        df_no2.columns = df_no2.columns.str.strip()
        df_pm25.columns = df_pm25.columns.str.strip()

        df_no2 = df_no2.rename(columns={
            "Landkreis/ Kreisfreie Städte \n(NUTS** Name - NUTS3-Level )": "Region",
            "Todesfälle (Total)": "Todesfälle"
        })[["Region", "Todesfälle"]]
        df_no2["Jahr"] = 2022
        df_no2["Schadstoff"] = "NO₂"

        df_pm25 = df_pm25.rename(columns={
            "Landkreis/ Kreisfreie Städte \n(NUTS** Name - NUTS3-Level )": "Region",
            "Todesfälle (Total)": "Todesfälle"
        })[["Region", "Todesfälle"]]
        df_pm25["Jahr"] = 2022
        df_pm25["Schadstoff"] = "PM2.5"

        df_todesfaelle = pd.concat([df_no2, df_pm25])
        df_todesfaelle["Todesfälle"] = pd.to_numeric(df_todesfaelle["Todesfälle"], errors="coerce")
        df_todesfaelle = df_todesfaelle.dropna(subset=["Todesfälle"])

        # Neue Stadt-Suchfunktion
        st.markdown("### 🔍 Suche nach Region")
        suchbegriff = st.text_input("Gib den Namen einer Region ein (z. B. Berlin, München):").strip()

        if suchbegriff:
            df_gefunden = df_todesfaelle[df_todesfaelle["Region"].str.contains(suchbegriff, case=False, na=False)]
            if df_gefunden.empty:
                st.warning("⚠️ Keine passende Region gefunden.")
            else:
                st.markdown("#### Ergebnis für Suchbegriff:")
                st.dataframe(df_gefunden)
                chart_suche = alt.Chart(df_gefunden).mark_bar().encode(
                    x=alt.X("Region:N", sort="-y", title="Region"),
                    y=alt.Y("Todesfälle:Q", title="Todesfälle"),
                    color=alt.Color("Schadstoff:N"),
                    tooltip=["Region", "Todesfälle", "Schadstoff"]
                ).properties(width=1000, height=400)
                st.altair_chart(chart_suche, use_container_width=True)

        # Anzeige der Top-Regionen
        max_zeilen = st.slider("Anzahl der angezeigten Regionen", min_value=10, max_value=100, value=20)

        df_todesfaelle_sorted = df_todesfaelle.sort_values(by="Todesfälle", ascending=False).head(max_zeilen)

        chart_todesfaelle = alt.Chart(df_todesfaelle_sorted).mark_bar().encode(
            x=alt.X("Region:N", sort="-y", title="Region"),
            y=alt.Y("Todesfälle:Q", title="Todesfälle"),
            color=alt.Color("Schadstoff:N"),
            tooltip=["Region", "Todesfälle", "Schadstoff"]
        ).properties(width=1000, height=500)

        st.markdown("### 📊 Top-Regionen nach Todesfällen")
        st.altair_chart(chart_todesfaelle, use_container_width=True)

    except Exception as e:
        st.error("❌ Fehler beim Einlesen der Excel-Dateien:")
        st.exception(e)

    # Vergleich aller Schadstoffe über die Jahre
    st.subheader("📉 Entwicklung aller Schadstoffe im Vergleich")
    jahre = list(range(2010, 2025))
    components = {
        "NO₂": "5",
        "PM10": "1",
        "PM2.5": "6001"
    }
    alle_werte = []

    for comp_name, comp_id in components.items():
        for y in jahre:
            url = f"https://www.umweltbundesamt.de/api/air_data/v3/annualbalances/json?component={comp_id}&year={y}&lang=de"
            try:
                r = requests.get(url).json()
                headers_comp = r["headers"]
                data = r["data"]
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

        st.markdown("""
           
        > 🔍 Quelle: [Statistisches Bundesamt](https://www-genesis.destatis.de)
                    [Deutsche Umwelthilfe e.V.](https://www.duh.de)
        """
                    )
