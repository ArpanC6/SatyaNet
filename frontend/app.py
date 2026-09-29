"""SatyaNet - Main Frontend App (Premium)."""
import streamlit as st
from frontend.components.theme import (
    apply_theme,
    render_header,
    render_hero,
    render_metric,
    render_info_panel,
    render_sidebar_brand,
    render_sidebar_status,
)

st.set_page_config(
    page_title="SatyaNet - Command Center",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_header()

with st.sidebar:
    render_sidebar_brand()
    render_sidebar_status()

render_hero()

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric("Total Evidence", "0", "primary", "Awaiting ingest")

with col2:
    render_metric("Verified", "0", "success", "Trust >= 80")

with col3:
    render_metric("Needs Review", "0", "warning", "Trust 50-79")

with col4:
    render_metric("Likely Fake", "0", "danger", "Trust < 50")

st.markdown("<br>", unsafe_allow_html=True)

render_info_panel(
    "Quick Start",
    "Navigate using the sidebar: <b>Verify</b> uploads and scores field evidence, "
    "<b>Dashboard</b> aggregates project intelligence, <b>Map</b> plots geospatial "
    "evidence, and <b>Reports</b> generates PDF situation reports for incident commanders.",
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### System Architecture")

arch_col1, arch_col2, arch_col3, arch_col4 = st.columns(4)

with arch_col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Media Layer</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: #00E5FF; margin-bottom: 8px;">Cloudinary</div>
            <div style="font-size: 13px; color: #7A85A8; line-height: 1.6;">
                Upload, auto-tag, AI metadata extraction, folder organization
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with arch_col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Intelligence Layer</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: #7C5CFF; margin-bottom: 8px;">Bayesian UQ</div>
            <div style="font-size: 13px; color: #7A85A8; line-height: 1.6;">
                5-signal weighted fusion: EXIF, temporal, satellite, duplicate, quality
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with arch_col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Search Layer</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: #00FFB2; margin-bottom: 8px;">Qdrant</div>
            <div style="font-size: 13px; color: #7A85A8; line-height: 1.6;">
                Semantic vector search across evidence corpus
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with arch_col4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Output Layer</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: #FFB84D; margin-bottom: 8px;">Reports</div>
            <div style="font-size: 13px; color: #7A85A8; line-height: 1.6;">
                PDF situation reports for incident commanders
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
