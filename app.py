import streamlit as st
from streamlit import session_state as ss
import hydralit_components as hc

from inputs import display_inputs
from constants import Ore


if ss.get("ore_type") is None:
    ss["ore_type"] = "Yet to Identify"
if ss.get("ore_type_reason") is None:
    ss["ore_type_reason"] = "Enter Inputs and click on `Get Identification`"

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

if menu_id == "Home":
    if ss.get("see_identification"):
        with hc.HyLoader(
            "Identifying ore and appropriate flowsheet",
            hc.Loaders.standard_loaders,
            index=1,
        ):
            Ore.identify()

    action = st.radio(
        "Action",
        ["Ore Identification", "Simulation"],
        horizontal=True,
        label_visibility="hidden",
    )
    if action == "Ore Identification":
        hc.info_card(
            title=ss.ore_type,
            content=ss.ore_type_reason,
            sentiment="bad" if ss.ore_type == "Unknown" else "good",
            bar_value=90,
        )
    else:
        if ss.ore_type == "Yet to Identify":
            st.info(
                "Enter the inputs and click on `Get Identification` to Identify a valid ore or first!"
            )
        else:
            if ss.ore_type == "Unknown":
                st.warning(
                    "The ore type is unknown. Please check the inputs and try again"
                )
            else:
                c1, c2, c3, c4, c5 = st.columns(5)
                with c3:
                    sim_btn = st.button("Run Simulation")

                if sim_btn:
                    with hc.HyLoader(
                        "Optimizing for the best params...",
                        hc.Loaders.standard_loaders,
                        index=2,
                    ):
                        st.write(Ore.overall_recovery())

if menu_id == "About":
    st.markdown(
        """
        This app is designed to help in identifying the ore type based on the mineralogy values.
        """
    )
    st.markdown(
        """
        The app is divided into two sections:
        - Identification: This section displays the identified ore type and the reason for identification.
        - Simulation: This section allows you to run a simulation to get the best parameters for high ore recovery.
        """
    )
