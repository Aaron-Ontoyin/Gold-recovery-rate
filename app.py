import streamlit as st
import hydralit_components as hc

from inputs import display_inputs
from utils import identify


st.set_page_config(layout="wide")

menu_data = [{"icon": "fas fa-info-circle", "label": "About"}]
over_theme = {"txc_inactive": "#FFFFFF", "menu_background": "#528aff"}
st.markdown("<style>.css-1l02zno{margin-top: 20px;}</style>", unsafe_allow_html=True)
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Home",
    hide_streamlit_markers=True,
    sticky_nav=True,
    sticky_mode="pinned",
)

display_inputs()

if st.session_state.get("see_identification"):
    with hc.HyLoader(
        "Identifying ore and appropriate flowsheet",
        hc.Loaders.standard_loaders,
        index=1,
    ):
        ore_id = identify()

    identification_tab, simulation_tab = st.tabs(["Identification", "Simulation"])
    with identification_tab:
        hc.info_card(
            title=ore_id["ore_type"],
            content=ore_id["ore_type_reason"],
            sentiment="good",
            bar_value=90,
        )
        hc.info_card(
            title=ore_id["flowsheet"],
            content=ore_id["flowsheet_reason"],
            sentiment="good",
            bar_value=85,
        )

    with simulation_tab:
        st.button("Run Simulation", key="run_simulation")
