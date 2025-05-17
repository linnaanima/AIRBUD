import streamlit as st
import streamlit as st
import pandas as pd


def app():
    st.subheader("Luftqualität im Blick für Atemwegserkrankte")
    st.write("""
        Diese App liefert dir in Echtzeit verlässliche Informationen zur aktuellen Luftqualität an deinem Standort. Basierend auf Messwerten wie Feinstaub (PM2.5/PM10), Ozon, Stickstoffdioxid und weiteren Schadstoffen bewertet die App die Luftqualität tagesaktuell.

        Besonders hilfreich für Menschen mit Atemwegserkrankungen: Die App gibt eine individuelle Empfehlung, ob du dich im Freien aufhalten solltest, körperliche Aktivitäten besser vermeidest oder zusätzliche Schutzmaßnahmen (z. B. Maske) sinnvoll sind. So behältst du nicht nur den Überblick über deine Umgebung – sondern kannst auch gezielt auf deine Gesundheit achten.
    """)
    st.image("picture.png", caption="AirBUDDY")


    st.title("Das Problem")

    st.markdown("""
    Smogwelle & fehlende Transparenz:
    Anfang des Jahres kam es in Deutschland zu einer markanten Smogwelle, die das öffentliche Bewusstsein für Luftqualität erneut in den Fokus rückte. In meinem persönlichen Umfeld und durch eigene Recherchen wurde mir deutlich, wie wenig transparente und zugängliche Transparenz zur Luftqualität, insbesondere für Menschen mit Atemwegserkrankungen, verfügbar sind.
    </p>

    <p>
    <strong>🧠 Der Impuls:</strong>  
    Dies weckte in mir den Wunsch, besser zu verstehen, welche Schadstoffe und Partikel tatsächlich in der Luft vorhanden sind und wie diese mit Wetterphänomenen wie Saharastaub oder dem sogenannten <em>„Gewitterasthma“</em> zusammenhängen.
    </p>
    </div>

    <br>

    ### 🔍 Datengrundlage

    Um belastbare Aussagen treffen zu können wurden folgende Datenquellen kombiniert:

    - **Luftqualitätsdaten** Umweltbundesamt  
    - **Pollendaten** Deutscher Wetterdienst (DWD)
    - **Wetter- und Saharastaubdaten** Open-Meteo    
    - **Richtwerte der WHO** Luftqualität Weltweit 
    - **Sterberate durch Feinstaubbelastung** in Deutschland Europäische Umweltagentur (EEA)

    ---

    ### Entwicklung des Buddy

    Auf Basis dieser Daten wurde ein interaktives Dashboard, der **Buddy** entwickelt.

    Der Buddy:

    - verknüpft Luftqualität, Wetter und Gesundheitsfaktoren   
    - erkennt relevante Umweltphänomene  
    - bietet **konkrete Empfehlungen** für Menschen mit Atemwegserkrankungen  
    - visualisiert Daten leicht verständlich

    >  **Ziel:** Luftqualität als Zusammenspiel von Umwelt, Wetter und menschlicher Gesundheit verständlich machen, nicht nur als reinen Feinstaubwert.

    ---

    ###  Relevanz

    Phänomene wie **Saharastaub**, **Smog** oder **Gewitterasthma** sind in bestehenden Apps kaum berücksichtigt, obwohl sie nachweislich starke Auswirkungen auf die Gesundheit haben können.

    Mit meinem Buddy versuche ich diese Lücke zu schließen.
    """, unsafe_allow_html=True)
