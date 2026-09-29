"""Signal radar chart."""
import plotly.graph_objects as go
import streamlit as st


def render_signal_radar(signals):
    if not signals:
        st.info("No signal data available.")
        return

    labels = [s.get("signal", "").replace("_", " ").title() for s in signals]
    scores = [s.get("score", 0) * 100 for s in signals]

    labels_closed = labels + [labels[0]]
    scores_closed = scores + [scores[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(0, 212, 255, 0.15)",
        line={"color": "#00D4FF", "width": 2},
        name="Signal Score",
    ))

    fig.update_layout(
        polar={
            "bgcolor": "#141A2A",
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "gridcolor": "#2A3447",
                "tickfont": {"color": "#8B95A9", "size": 9},
                "tickvals": [20, 40, 60, 80, 100],
            },
            "angularaxis": {
                "gridcolor": "#2A3447",
                "tickfont": {"color": "#E8EDF5", "size": 11},
            },
        },
        showlegend=False,
        height=380,
        margin={"l": 60, "r": 60, "t": 40, "b": 40},
        paper_bgcolor="#1C2336",
        font={"color": "#E8EDF5", "family": "Inter"},
    )

    st.plotly_chart(fig, use_container_width=True)
