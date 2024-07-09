import streamlit as st


def display_inputs():
    """
    Displays the input fields for gold recovery rate calculation.

    This function creates input fields using Streamlit's sidebar components
    to allow the user to input values for gold head grade, particle size distribution,
    throughput, reagents, and ore mineralogy.

    Returns:
        None
    """
    st.sidebar.number_input("Gold Head Grade", key="gold_head_grade", step=1)
    st.sidebar.subheader("", divider="blue")

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
    st.sidebar.subheader("", divider="blue")

    st.sidebar.number_input("Throughput", key="throughput")
    st.sidebar.subheader("", divider="blue")

    st.sidebar.selectbox(
        "Reagents",
        options=[
            "Choose Reagent",
            "CN (kg/t)",
            "Lime (kg/t)",
            "Lime (kg/t)",
            "Collector A (g/t)",
            "Collector B (g/t)",
            "Frother (mL/t)",
        ],
        key="reagents",
    )
    st.sidebar.subheader("", divider="blue")

    minerals = [
        "Pyrite",
        "Arsenopyrite",
        "Chalcopyrite",
        "Sphalerite",
        "Galena",
        "Calcite",
        "Siderite",
        "Quartz",
        "Feldspars",
        "Montmorillonite",
        "Kaolinite",
    ]
    with st.sidebar.expander("Ore Mineralogy (%)"):
        for mineral in minerals:
            st.number_input(f"{mineral}", key=f"{mineral}_mineralogy")

    st.sidebar.button("See Identification", key="see_identification", type="primary")
