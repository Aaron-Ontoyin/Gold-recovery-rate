import streamlit as st

from constants import Ore


def display_inputs():
    """
    Displays the input fields for gold recovery rate calculation.

    This function creates input fields using Streamlit's sidebar components
    to allow the user to input values for gold head grade, particle size distribution,
    throughput, reagents, and ore mineralogy.

    Returns:
        None
    """
    st.sidebar.title("Sample Inputs")

    st.sidebar.text_input("Sample ID", placeholder="Enter sample ID here")

    with st.sidebar.expander("Ore Mineralogy (%)"):
        for mineral in Ore.minerals:
            st.number_input(
                f"{mineral}", key=f"{mineral}_mineralogy", min_value=0.0, step=0.01
            )

    st.sidebar.number_input(
        "Gold Head Grade", key="gold_head_grade", min_value=0.0, step=0.01
    )
    st.sidebar.subheader("", divider="blue")

    if st.sidebar.checkbox("Particle Size as range", True):
        st.sidebar.selectbox(
            "Particle Size Distribution",
            options=[
                "Choose Particle Size",
                "P10 (microns)",
                "P50 (microns)",
                "P80 (microns)",
            ],
            key="particle_size_distribution",
        )
    else:
        st.sidebar.number_input(
            "Particle Size Distribution",
            min_value=0.0,
            step=0.01,
            key="particle_size_distribution",
        )
    st.sidebar.subheader("", divider="blue")

    st.sidebar.number_input("Throughput", key="throughput", min_value=0.0, step=0.01)
    st.sidebar.subheader("", divider="blue")

    with st.sidebar.expander("Reagents"):
        for reagent in Ore.reagents:
            st.number_input(
                f"{reagent}", key=f"{reagent}_reagent", min_value=0.0, step=0.01
            )

    st.sidebar.subheader("", divider="blue")

    st.sidebar.button("Get Identification", key="see_identification", type="primary")
