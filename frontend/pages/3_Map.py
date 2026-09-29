"""Map page."""
import streamlit as st
from frontend.components.theme import apply_theme, render_header

st.set_page_config(page_title="Map - SatyaNet", layout="wide")
apply_theme()
render_header()

st.markdown("## Geospatial Evidence View")
st.markdown("Verified field evidence mapped by location.")

try:
    import folium
    from streamlit_folium import st_folium

    m = folium.Map(
        location=[22.5, 78.9],
        zoom_start=5,
        tiles="CartoDB dark_matter",
    )

    sample_locations = [
        {"name": "Siliguri Flood Zone", "lat": 26.7271, "lon": 88.3953, "score": 92, "color": "green"},
        {"name": "Guwahati Relief Camp", "lat": 26.1445, "lon": 91.7362, "score": 78, "color": "orange"},
        {"name": "Patna Inundation", "lat": 25.5941, "lon": 85.1376, "score": 45, "color": "red"},
    ]

    for loc in sample_locations:
        folium.CircleMarker(
            location=[loc["lat"], loc["lon"]],
            radius=12,
            color=loc["color"],
            fill=True,
            fill_color=loc["color"],
            fill_opacity=0.7,
            popup=loc["name"] + " - Trust: " + str(loc["score"]) + "/100",
        ).add_to(m)

    st_folium(m, width=None, height=600, returned_objects=[])

    st.markdown("### Legend")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px;">'
            '<span style="width:12px; height:12px; background:#00E5A0; border-radius:50%;"></span>'
            '<span style="color:#E8EDF5;">Verified (80+)</span></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px;">'
            '<span style="width:12px; height:12px; background:#FFB547; border-radius:50%;"></span>'
            '<span style="color:#E8EDF5;">Needs Review (50-79)</span></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px;">'
            '<span style="width:12px; height:12px; background:#FF4D6D; border-radius:50%;"></span>'
            '<span style="color:#E8EDF5;">Likely Fake (&lt;50)</span></div>',
            unsafe_allow_html=True,
        )
except Exception as e:
    st.error("Map rendering failed: " + str(e))
