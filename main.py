import streamlit as st
import page_start
import Luft
import Gewitter
import Sahara
import Jahresbilanz
import Luft_Pollen
import Urlaubsorte
import ICD
import Dash

st.title("AIRBUDDY - Deine Luftqualität.")

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 50px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
pages = {
    "Start"                 : page_start,
    "BUDDY"                 : Dash,
    "Luft"                  : Luft,
    "Pollen"                : Luft_Pollen,
    "Gewitter"             : Gewitter,
    "Sahara"                : Sahara,
    "Bilanz"                : Jahresbilanz,
    "Urlaub"                : Urlaubsorte,
    "ICD"                   : ICD
}



select = st.sidebar.radio("",list(pages.keys()))

pages[select].app()


st.sidebar.markdown("---")
st.sidebar.write("🧠 Linda powered by :coffee:  ");  
