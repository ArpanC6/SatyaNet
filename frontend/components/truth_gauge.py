"""Custom Truth Score gauge."""
import plotly.graph_objects as go
import streamlit as st


def render_truth_gauge(score, trust_level=""):
    if score >= 80:
        color = "#00E5A0"
        verdict = "VERIFIED"
    elif score >= 50:
        color = "#FFB547"
        verdict = "NEEDS REVIEW"
    else:
        color = "#FF4D6D"
        verdict = "LIKELY FAKE"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "<span style='font-size:14px; color:#8B95A9;'>TRUST SCORE</span><br>"
                    "<span style='font-size:12px; color:" + color + "; font-weight:600;'>" + verdict + "</span>",
            "font": {"size": 16},
        },
        number={
            "font": {"size": 44, "color": color, "family": "JetBrains Mono"},
            "suffix": "/100",
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#2A3447",
                "tickfont": {"color": "#8B95A9", "size": 10},
            },
            "bar": {"color": color, "thickness": 0.75},
            "bgcolor": "#141A2A",
            "borderwidth": 2,
            "bordercolor": "#2A3447",
            "steps": [
                {"range": [0, 50], "color": "rgba(255, 77, 109, 0.08)"},
                {"range": [50, 80], "color": "rgba(255, 181, 71, 0.08)"},
                {"range": [80, 100], "color": "rgba(0, 229, 160, 0.08)"},
            ],
        },
    ))

    fig.update_layout(
        height=280,
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        paper_bgcolor="#1C2336",
        font={"color": "#E8EDF5", "family": "Inter"},
    )

    st.plotly_chart(fig, use_container_width=True)
