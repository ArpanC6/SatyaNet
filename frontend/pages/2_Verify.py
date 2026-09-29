"""Verify page."""
import streamlit as st
import requests
from datetime import datetime
from frontend.components.theme import apply_theme, render_header
from frontend.components.truth_gauge import render_truth_gauge
from frontend.components.signal_chart import render_signal_radar

st.set_page_config(page_title="Verify - SatyaNet", layout="wide")
apply_theme()
render_header()

st.markdown("## Verify Field Evidence")
st.markdown("Upload a photo or video to run Bayesian trust verification.")

API_URL = "http://127.0.0.1:8000/api/v1"

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### Evidence Input")

    uploaded_file = st.file_uploader(
        "Upload evidence",
        type=["jpg", "jpeg", "png", "webp", "mp4", "mov"],
    )

    project = st.text_input("Project", value="Siliguri Flood 2026")
    location_label = st.text_input("Location", value="Siliguri, WB")
    claimed_date = st.date_input("Claimed Date", value=datetime.now())

    lat = st.number_input("Latitude (optional)", value=26.7271, format="%.4f")
    lon = st.number_input("Longitude (optional)", value=88.3953, format="%.4f")

    verify_button = st.button("Verify Evidence", type="primary")

with col_right:
    st.markdown("### Verification Result")

    if verify_button and uploaded_file is not None:
        with st.spinner("Running Bayesian trust scoring..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                data = {
                    "project": project,
                    "location_label": location_label,
                    "claimed_date": claimed_date.isoformat(),
                    "latitude": str(lat),
                    "longitude": str(lon),
                }
                response = requests.post(
                    API_URL + "/verify",
                    files=files,
                    data=data,
                    timeout=30,
                )

                if response.status_code == 201:
                    result = response.json()
                    verification = result.get("verification", {})
                    score = verification.get("trust_score", 0)

                    render_truth_gauge(score, verification.get("trust_level", ""))

                    st.markdown("#### Signal Breakdown")
                    render_signal_radar(verification.get("signals", []))

                    st.markdown("#### Reasons")
                    for reason in verification.get("reasons", []):
                        st.markdown("- " + reason)

                    flags = verification.get("flags", [])
                    if flags:
                        st.markdown("#### Flags")
                        for flag in flags:
                            st.warning(flag)
                else:
                    st.error("Verification failed: " + str(response.status_code))
                    st.caption(response.text[:500])
            except Exception as e:
                st.error("Error: " + str(e))
    else:
        st.info("Upload a file and click Verify Evidence.")
