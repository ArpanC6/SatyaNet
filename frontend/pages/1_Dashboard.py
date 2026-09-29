"""Dashboard page."""
import streamlit as st
import requests
from frontend.components.theme import apply_theme, render_header, render_metric

st.set_page_config(page_title="Dashboard - SatyaNet", layout="wide")
apply_theme()
render_header()

st.markdown("## Project Dashboard")
st.markdown("Aggregate view of evidence corpora across all active projects.")

API_URL = "http://127.0.0.1:8000/api/v1"

if st.button("Refresh Data", type="primary"):
    st.rerun()

try:
    response = requests.get(API_URL + "/projects", timeout=3)
    if response.status_code == 200:
        data = response.json()
        projects = data.get("projects", [])
        total = data.get("total", 0)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric("Active Projects", str(total), "primary")
        with col2:
            total_evidence = sum(p.get("total_evidence", 0) for p in projects)
            render_metric("Total Evidence", str(total_evidence), "primary")
        with col3:
            total_verified = sum(p.get("verified_count", 0) for p in projects)
            render_metric("Verified", str(total_verified), "success")
        with col4:
            total_fake = sum(p.get("likely_fake_count", 0) for p in projects)
            render_metric("Likely Fake", str(total_fake), "danger")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Projects")

        if projects:
            for p in projects:
                with st.expander(p.get("project", "Unknown"), expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total", p.get("total_evidence", 0))
                    c2.metric("Verified", p.get("verified_count", 0))
                    c3.metric("Review", p.get("needs_review_count", 0))
                    c4.metric("Fake", p.get("likely_fake_count", 0))
        else:
            st.info("No projects yet. Go to Verify page to upload evidence.")
    else:
        st.warning("Backend returned status: " + str(response.status_code))
except Exception as e:
    st.info("Backend not reachable. Start backend with: uvicorn backend.main:app --reload")
    st.caption("Error: " + str(e))
