"""SatyaNet - Clean Professional Light Theme."""
import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .stApp {
            background: #FFFFFF;
            color: #111827;
        }

        html, body, [class*="css"] {
            font-size: 16px;
        }

        section[data-testid="stSidebar"] {
            background: #F7F8FA;
            border-right: 1px solid #E5E7EB;
        }

        section[data-testid="stSidebar"] * {
            color: #374151 !important;
        }

        .main .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        .satyanet-header {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 20px 0 24px 0;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 40px;
        }

        .satyanet-logo {
            font-family: 'Inter', sans-serif;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.6px;
            color: #111827;
        }

        .satyanet-subtitle {
            font-size: 14px;
            color: #6B7280;
            font-weight: 500;
        }

        h1, h2, h3, h4 {
            font-family: 'Inter', sans-serif !important;
            color: #111827 !important;
            letter-spacing: -0.8px !important;
            font-weight: 700 !important;
        }

        h1 { font-size: 44px !important; line-height: 1.15 !important; margin-bottom: 16px !important; }
        h2 { font-size: 28px !important; line-height: 1.25 !important; margin-top: 32px !important; margin-bottom: 16px !important; }
        h3 { font-size: 20px !important; line-height: 1.3 !important; margin-top: 24px !important; margin-bottom: 12px !important; }

        p, .stMarkdown p {
            font-size: 16px !important;
            line-height: 1.7 !important;
            color: #4B5563 !important;
        }

        .hero-title {
            font-family: 'Inter', sans-serif;
            font-size: 52px;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -1.5px;
            color: #111827;
            margin-bottom: 20px;
        }

        .hero-subtitle {
            font-size: 18px;
            line-height: 1.7;
            color: #6B7280;
            max-width: 780px;
            margin-bottom: 40px;
            font-weight: 400;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 16px;
            transition: all 0.15s ease;
        }

        .metric-card:hover {
            border-color: #D1D5DB;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }

        .metric-label {
            font-size: 13px;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .metric-value {
            font-family: 'Inter', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #111827;
            line-height: 1;
            letter-spacing: -1px;
        }

        .metric-value.primary { color: #4F46E5; }
        .metric-value.success { color: #10B981; }
        .metric-value.warning { color: #F59E0B; }
        .metric-value.danger  { color: #EF4444; }

        .metric-delta {
            font-size: 13px;
            color: #9CA3AF;
            margin-top: 10px;
            font-weight: 400;
        }

        .info-panel {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 28px 32px;
            margin-top: 24px;
        }

        .info-panel-title {
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #4F46E5;
            margin-bottom: 14px;
        }

        .info-panel-body {
            font-size: 15px;
            line-height: 1.75;
            color: #4B5563;
        }

        .info-panel-body b {
            color: #111827;
            font-weight: 600;
        }

        .stButton > button {
            background: #111827;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 15px;
            font-family: 'Inter', sans-serif;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            background: #1F2937;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background: #FFFFFF !important;
            border: 1px solid #D1D5DB !important;
            color: #111827 !important;
            border-radius: 8px !important;
            font-size: 15px !important;
            padding: 10px 14px !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }

        .stTextInput label, .stTextArea label, .stSelectbox label,
        .stFileUploader label, .stDateInput label {
            color: #374151 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }

        .stFileUploader > div {
            background: #F9FAFB;
            border: 2px dashed #D1D5DB;
            border-radius: 12px;
            transition: all 0.15s ease;
        }

        .stFileUploader > div:hover {
            border-color: #4F46E5;
            background: #F3F4F6;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: #F3F4F6;
            border-radius: 10px;
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #6B7280;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
        }

        .stTabs [aria-selected="true"] {
            background: #FFFFFF !important;
            color: #111827 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }

        .stAlert {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 16px 20px;
        }

        .stProgress > div > div > div > div {
            background: #4F46E5;
            border-radius: 4px;
        }

        .stProgress > div > div > div {
            background: #F3F4F6;
            border-radius: 4px;
            height: 8px;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 6px 0;
            font-size: 13px;
            color: #4B5563;
        }

        .status-dot-online {
            width: 8px;
            height: 8px;
            background: #10B981;
            border-radius: 50%;
        }

        .status-dot-offline {
            width: 8px;
            height: 8px;
            background: #F59E0B;
            border-radius: 50%;
        }

        .sidebar-brand {
            padding: 16px 0 24px 0;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 20px;
        }

        .sidebar-brand-logo {
            font-family: 'Inter', sans-serif;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #111827;
        }

        .sidebar-brand-meta {
            font-size: 11px;
            color: #9CA3AF;
            margin-top: 6px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            font-weight: 600;
        }

        .sidebar-section-label {
            font-size: 11px;
            color: #9CA3AF;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin: 20px 0 10px 0;
        }

        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: #F9FAFB; }
        ::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #9CA3AF; }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: transparent;}

        div[data-testid="stMetricValue"] {
            font-family: 'Inter', sans-serif;
            color: #111827;
            font-size: 28px;
            font-weight: 700;
        }

        div[data-testid="stMetricLabel"] {
            color: #6B7280;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="satyanet-header">
            <div class="satyanet-logo">SatyaNet</div>
            <div class="satyanet-subtitle">Trust-Aware Field Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div style="padding: 32px 0 40px 0;">
            <div class="hero-title">Verify field evidence<br/>before it drives decisions.</div>
            <div class="hero-subtitle">
                SatyaNet ingests field media, cross-checks it against satellite data,
                EXIF metadata, and perceptual duplicates, and assigns a Bayesian trust
                score so responders know exactly how much to rely on each piece of evidence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value, variant="primary", delta=None):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {variant}">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_panel(title, body):
    st.markdown(
        f"""
        <div class="info-panel">
            <div class="info-panel-title">{title}</div>
            <div class="info-panel-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-logo">SatyaNet</div>
            <div class="sidebar-brand-meta">Mission Control v1.0.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_status():
    st.markdown(
        """
        <div class="sidebar-section-label">System Status</div>
        <div class="status-item">
            <span class="status-dot-online"></span>
            <span>API · localhost:8000</span>
        </div>
        <div class="status-item">
            <span class="status-dot-offline"></span>
            <span>Qdrant · offline</span>
        </div>
        <div class="status-item">
            <span class="status-dot-offline"></span>
            <span>Cloudinary · not set</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
