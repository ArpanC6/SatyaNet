"""Reports page."""
import streamlit as st
from datetime import datetime
from frontend.components.theme import apply_theme, render_header

st.set_page_config(page_title="Reports - SatyaNet", layout="wide")
apply_theme()
render_header()

st.markdown("## Situation Reports")
st.markdown("Generate PDF situation reports from verified evidence.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Report Configuration")
    project_name = st.text_input("Project Name", value="Siliguri Flood 2026")
    report_date = st.date_input("Report Date", value=datetime.now())
    include_fake = st.checkbox("Include likely-fake evidence", value=False)
    generate = st.button("Generate PDF Report", type="primary")

with col2:
    st.markdown("### Report Preview")
    if generate:
        st.success("Report generated: SatyaNet_" + project_name.replace(" ", "_") + ".pdf")
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Report Summary</div>
                <div style="font-size: 13px; color: #8B95A9; line-height: 1.8; margin-top: 8px;">
                    <b style="color: #E8EDF5;">Project:</b> """ + project_name + """<br>
                    <b style="color: #E8EDF5;">Generated:</b> """ + str(report_date) + """<br>
                    <b style="color: #E8EDF5;">Total Evidence:</b> 0<br>
                    <b style="color: #E8EDF5;">Verified:</b> 0<br>
                    <b style="color: #E8EDF5;">Flagged:</b> 0
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Configure and generate a report.")
