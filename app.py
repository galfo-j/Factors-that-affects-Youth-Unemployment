"""
SDG 8 – Youth Unemployment Dashboard  (Premium UI v3)
=====================================================
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SDG 8 – Youth Unemployment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 2. Load & Prepare Data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    numeric_cols = ['access_to_electricity_pct', 'gdp_growth_pct',
                    'labor_force_participation_pct', 'youth_unemployment_pct']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()
df = df.rename(columns={
    'access_to_electricity_pct':      'Electricity_Access',
    'gdp_growth_pct':                 'GDP_Growth',
    'labor_force_participation_pct':  'Labor_Force_Participation',
    'youth_unemployment_pct':         'Youth_Unemployment_Rate',
    'year':                           'Year'
})

# ─────────────────────────────────────────────
# 3. Global CSS / Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@300;400;500&family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600&display=swap');

/* ════════════════════════════════════════
   RESET & BASE
════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #dde3ee;
    font-size: 15px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
}

/* ════════════════════════════════════════
   APP SHELL — deep navy cosmos
════════════════════════════════════════ */
.stApp {
    background-color: #060b14;
    background-image:
        radial-gradient(ellipse 110% 55% at 5%  0%,   rgba(14,165,233,0.13)  0%, transparent 55%),
        radial-gradient(ellipse  70% 45% at 95% 5%,   rgba(99, 102,241,0.11) 0%, transparent 50%),
        radial-gradient(ellipse  60% 70% at 50% 100%, rgba(20,184,166,0.09)  0%, transparent 55%),
        radial-gradient(ellipse  40% 35% at 80% 55%,  rgba(244,63,94,0.06)   0%, transparent 50%);
    min-height: 100vh;
}

/* ════════════════════════════════════════
   MAIN CONTAINER
════════════════════════════════════════ */
.main .block-container {
    padding: 0 2.4rem 3.5rem;
    max-width: 98%;
}

/* ════════════════════════════════════════
   SIDEBAR
════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101f 0%, #060d1a 100%) !important;
    border-right: 1px solid rgba(14,165,233,0.12) !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

/* ── Sidebar brand block ── */
.sidebar-brand {
    padding: 0.5rem 0.8rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.8rem;
}
.sidebar-brand-title {
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #f0f6ff;
    letter-spacing: -0.01em;
    line-height: 1.2;
    margin-bottom: 2px;
}
.sidebar-brand-sub {
    font-size: 0.68rem;
    color: #4a6080;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    font-weight: 600;
}
.sidebar-sdg-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 8px;
    background: linear-gradient(135deg, rgba(20,184,166,0.18), rgba(14,165,233,0.12));
    border: 1px solid rgba(20,184,166,0.28);
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #2dd4bf;
}

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] button {
    width: 100% !important;
    padding: 0.72rem 1rem !important;
    margin-bottom: 3px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    border-radius: 9px !important;
    border: 1px solid rgba(255,255,255,0.045) !important;
    background: rgba(255,255,255,0.03) !important;
    color: #7a90a8 !important;
    transition: all 0.18s cubic-bezier(0.4,0,0.2,1) !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(14,165,233,0.09) !important;
    border-color: rgba(14,165,233,0.22) !important;
    color: #e2eaf4 !important;
    transform: translateX(4px) !important;
    box-shadow: 0 0 14px rgba(14,165,233,0.08) !important;
}

/* ── Sidebar info badges ── */
.info-badge {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 9px;
    padding: 0.52rem 0.85rem;
    font-size: 0.78rem;
    color: #7a90a8;
    line-height: 1.55;
    margin-top: 5px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.info-badge strong { color: #b8cce0; font-weight: 600; }

/* ════════════════════════════════════════
   HERO BANNER  (image + overlay)
════════════════════════════════════════ */
.hero-wrapper {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 1.8rem;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 24px 64px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.07);
    min-height: 200px;
}
.hero-image {
    position: absolute;
    inset: 0;
    background-image: url('https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=1600&q=80&auto=format&fit=crop');
    background-size: cover;
    background-position: center 35%;
    filter: brightness(0.32) saturate(0.6);
    z-index: 0;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(105deg, rgba(6,11,20,0.75) 0%, rgba(6,11,20,0.30) 55%, rgba(6,11,20,0.55) 100%),
        linear-gradient(0deg, rgba(6,11,20,0.85) 0%, transparent 60%);
    z-index: 1;
}
.hero-content {
    position: relative;
    z-index: 2;
    padding: 2.2rem 2.4rem 2rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(20,184,166,0.14);
    border: 1px solid rgba(20,184,166,0.30);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #2dd4bf;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #f0f6ff;
    line-height: 1.18;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 20px rgba(0,0,0,0.6);
}
.hero-title span {
    color: #38bdf8;
}
.hero-sub {
    font-size: 0.875rem;
    color: #8da4be;
    max-width: 580px;
    line-height: 1.6;
}
.hero-divider {
    width: 48px;
    height: 3px;
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    border-radius: 2px;
    margin: 0.85rem 0;
}

/* ── Alternate hero for inner pages (no photo) ── */
.page-hero {
    background:
        linear-gradient(135deg, rgba(14,165,233,0.09) 0%, rgba(99,102,241,0.08) 50%, rgba(20,184,166,0.06) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.page-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(14,165,233,0.4), rgba(99,102,241,0.4), transparent);
}
.page-hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(14,165,233,0.10) 0%, transparent 65%);
    pointer-events: none;
}
.page-hero h1 {
    font-family: 'Fraunces', serif !important;
    font-size: 1.65rem !important;
    font-weight: 600 !important;
    color: #f0f6ff !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.3rem !important;
    -webkit-text-fill-color: #f0f6ff !important;
}
.page-hero p {
    color: #7a90a8;
    font-size: 0.875rem;
    margin: 0;
    line-height: 1.55;
}

/* ════════════════════════════════════════
   SECTION LABELS
════════════════════════════════════════ */
.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(14,165,233,0.09);
    border: 1px solid rgba(14,165,233,0.20);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.9rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ════════════════════════════════════════
   METRIC CARDS
════════════════════════════════════════ */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.052) 0%,
        rgba(255,255,255,0.022) 100%) !important;
    border: 1px solid rgba(255,255,255,0.075) !important;
    border-radius: 16px !important;
    padding: 1.15rem 1.35rem !important;
    backdrop-filter: blur(24px) saturate(1.4);
    -webkit-backdrop-filter: blur(24px) saturate(1.4);
    transition: transform 0.22s cubic-bezier(0.4,0,0.2,1),
                box-shadow 0.22s cubic-bezier(0.4,0,0.2,1),
                border-color 0.22s ease;
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0ea5e9, #6366f1, #14b8a6);
    opacity: 0.65;
    border-radius: 2px 2px 0 0;
}
div[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 90px; height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(14,165,233,0.07) 0%, transparent 70%);
    pointer-events: none;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow:
        0 20px 48px rgba(0,0,0,0.5),
        0 0 0 1px rgba(14,165,233,0.20),
        0 0 28px rgba(14,165,233,0.08);
    border-color: rgba(14,165,233,0.22) !important;
}
div[data-testid="stMetric"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #546a82 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.62rem !important;
    font-weight: 400 !important;
    color: #eaf1fb !important;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
}

/* ════════════════════════════════════════
   CHARTS
════════════════════════════════════════ */
.stPlotlyChart {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.065);
    border-radius: 18px;
    padding: 12px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.28);
    transition: box-shadow 0.2s ease;
}
.stPlotlyChart:hover {
    box-shadow: 0 12px 44px rgba(0,0,0,0.4), 0 0 0 1px rgba(14,165,233,0.10);
}

/* ════════════════════════════════════════
   DATAFRAMES
════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.065);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.22);
}

/* ════════════════════════════════════════
   FORM CONTROLS
════════════════════════════════════════ */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.045) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.095) !important;
}
div[data-testid="stSlider"] { padding: 0.5rem 0; }
label[data-testid="stCheckbox"] {
    font-size: 0.875rem !important;
    color: #b0c0d4 !important;
}

/* ════════════════════════════════════════
   ALERTS
════════════════════════════════════════ */
.stAlert {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    backdrop-filter: blur(12px);
}

/* ════════════════════════════════════════
   HEADINGS
════════════════════════════════════════ */
h1 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    font-size: 1.85rem !important;
    letter-spacing: -0.025em !important;
    color: #f0f6ff !important;
    margin-bottom: 0.15rem !important;
    line-height: 1.2 !important;
}
h2 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    color: #c8d8ea !important;
    letter-spacing: -0.01em !important;
}
h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: #7a90a8 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   DIVIDERS & MISC
════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.065) !important;
    margin: 1.3rem 0 !important;
}

/* ════════════════════════════════════════
   SCROLLBAR
════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.025); }
::-webkit-scrollbar-thumb {
    background: rgba(14,165,233,0.28);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(14,165,233,0.50); }

/* ════════════════════════════════════════
   STAT BADGE  (sidebar)
════════════════════════════════════════ */
.stat-badge {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.065);
    border-radius: 9px;
    padding: 0.52rem 0.85rem;
    font-size: 0.78rem;
    color: #7a90a8;
    line-height: 1.55;
    margin-top: 5px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stat-badge span { color: #b8cce0; font-weight: 700; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. Sidebar Navigation
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">SDG 8 Dashboard</div>
        <div class="sidebar-brand-sub">Youth Unemployment Analysis</div>
        <div class="sidebar-sdg-badge">⚡ Decent Work &amp; Growth</div>
    </div>
    """, unsafe_allow_html=True)

    nav_options = {
        "dashboard":           "📈  Dashboard Overview",
        "comparison":          "🌏  Country Comparison",
        "trends":              "📉  Trend Analysis",
        "forecasting":         "🔮  Unemployment Forecasting",
        "regression_insights": "📐  Regression Insights",
    }

    if 'navigation' not in st.session_state:
        st.session_state.navigation = "dashboard"

    for nav_key, nav_label in nav_options.items():
        if st.sidebar.button(nav_label, key=nav_key, use_container_width=True):
            st.session_state.navigation = nav_key

    st.markdown("---")
    st.markdown("""
    <div class="stat-badge"><span>Data Source</span><br>World Bank WDI</div>
    <div class="stat-badge" style="margin-top:5px;"><span>Region</span><br>East Asia &amp; Pacific</div>
    <div class="stat-badge" style="margin-top:5px;"><span>Period</span><br>2014 – 2024</div>
    <div class="stat-badge" style="margin-top:5px;"><span>Goal</span><br>SDG 8 · Decent Work &amp; Growth</div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. Shared Plotly template
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#7a90a8', size=12),
    margin=dict(l=52, r=28, t=52, b=48),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.045)', zeroline=False,
        title_font=dict(size=11, color='#546a82'),
        tickfont=dict(size=10, color='#546a82'),
        linecolor='rgba(255,255,255,0.07)',
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.045)', zeroline=False,
        title_font=dict(size=11, color='#546a82'),
        tickfont=dict(size=10, color='#546a82'),
        linecolor='rgba(255,255,255,0.07)',
    ),
    legend=dict(
        bgcolor='rgba(6,11,20,0.7)',
        bordercolor='rgba(255,255,255,0.07)',
        borderwidth=1,
        font=dict(size=11, color='#94a3b8'),
    ),
    hoverlabel=dict(
        bgcolor='#0b1628',
        font_family='JetBrains Mono, monospace',
        font_size=12,
        bordercolor='rgba(14,165,233,0.3)',
        font_color='#dde3ee',
    ),
)

COLOR_MAP = {
    'Youth_Unemployment_Rate':  '#f87171',
    'GDP_Growth':               '#34d399',
    'Labor_Force_Participation':'#38bdf8',
    'Electricity_Access':       '#fb923c',
}

# ─────────────────────────────────────────────
# 6. Regression (cached)
# ─────────────────────────────────────────────
@st.cache_data
def run_regression():
    df_reg = df[['Youth_Unemployment_Rate', 'GDP_Growth',
                 'Labor_Force_Participation', 'Electricity_Access']].dropna().copy()
    y = df_reg['Youth_Unemployment_Rate']
    X = sm.add_constant(df_reg[['GDP_Growth', 'Labor_Force_Participation', 'Electricity_Access']])
    return sm.OLS(y, X).fit()

ols_model = run_regression()

# ─────────────────────────────────────────────
# 7. Shared data
# ─────────────────────────────────────────────
all_countries   = sorted(df["Country Name"].dropna().unique())
available_years = sorted(df["Year"].unique())

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.navigation == "dashboard":

    # ── Hero with background image ────────────────────────────────────
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-image"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-eyebrow">🌏 East Asia &amp; Pacific · 2014–2024</div>
            <div class="hero-title">Youth <span>Unemployment</span><br>Dashboard</div>
            <div class="hero-divider"></div>
            <div class="hero-sub">
                Monitoring SDG 8 indicators across 29 countries — tracking the intersection of
                economic growth, labour force participation, and youth opportunity.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Stats ──────────────────────────────────────────────────
    st.markdown('<div class="section-pill">🎯 Dataset Overview</div>', unsafe_allow_html=True)

    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    with qcol1:
        st.metric("🌏 Total Countries",  len(df['Country Name'].unique()),
                  help="Countries tracked in the region")
    with qcol2:
        st.metric("📅 Total Records",    len(df),
                  help="Total annual data points")
    with qcol3:
        st.metric("📆 Latest Data Year", int(df['Year'].max()),
                  help="Most recent year in the dataset")
    with qcol4:
        st.metric("🕒 Date Range",       f"{int(df['Year'].min())}–{int(df['Year'].max())}",
                  help="Time span covered")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Key Statistical Insights ─────────────────────────────────────
    st.markdown('<div class="section-pill">🔬 Regional Highlights</div>', unsafe_allow_html=True)

    overall_avg_unemp   = df['Youth_Unemployment_Rate'].mean()
    overall_avg_gdp     = df['GDP_Growth'].mean()
    avg_by_country      = df.groupby('Country Name')['Youth_Unemployment_Rate'].mean()
    highest_unemp_cntry = avg_by_country.idxmax()
    highest_unemp_val   = avg_by_country.max()

    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        st.metric("💡 Regional Avg Youth Unemployment", f"{overall_avg_unemp:.2f}%")
    with ci2:
        st.metric("📈 Regional Avg GDP Growth",         f"{overall_avg_gdp:.2f}%")
    with ci3:
        st.metric("⚠️ Highest Youth Unemployment",      highest_unemp_cntry,
                  delta=f"{highest_unemp_val:.2f}%")

    st.markdown("---")

    # ── Country Selector ─────────────────────────────────────────────
    st.markdown('<div class="section-pill">🗺️ Country Analysis</div>', unsafe_allow_html=True)

    sel_col1, _ = st.columns([1, 2])
    with sel_col1:
        selected_country = st.selectbox("Select Country:", all_countries,
                                        key="dashboard_country_select")

    country_df = df[df['Country Name'] == selected_country].sort_values('Year')

    # KPI cards
    if not country_df.empty:
        latest_data = country_df.iloc[-1]
        avg_unemp   = country_df['Youth_Unemployment_Rate'].mean()
        avg_gdp     = country_df['GDP_Growth'].mean()

        def pct_change(series):
            if len(series) > 1 and series.iloc[0] != 0:
                return (series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100
            return 0

        unemp_change = pct_change(country_df['Youth_Unemployment_Rate'])
        gdp_change   = pct_change(country_df['GDP_Growth'])

        kc1, kc2, kc3, kc4 = st.columns(4)
        with kc1:
            st.metric("Latest Youth Unemployment",
                      f"{latest_data['Youth_Unemployment_Rate']:.2f}%",
                      delta=f"{unemp_change:.1f}% overall")
        with kc2:
            st.metric("Latest GDP Growth",
                      f"{latest_data['GDP_Growth']:.2f}%",
                      delta=f"{gdp_change:.1f}% overall")
        with kc3:
            st.metric("Avg Youth Unemployment", f"{avg_unemp:.2f}%")
        with kc4:
            st.metric("Avg GDP Growth",         f"{avg_gdp:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.subheader("📈 Youth Unemployment Trend")
        fig = px.area(country_df, x='Year', y='Youth_Unemployment_Rate',
                      title=f"{selected_country} – Youth Unemployment")
        fig.update_traces(
            line=dict(color='#f87171', width=2.5),
            fillcolor='rgba(248,113,113,0.12)',
            marker=dict(size=7, color='#f87171',
                        line=dict(width=1.5, color='white'))
        )
        fig.update_layout(**PLOT_LAYOUT,
                          title_font=dict(size=13, color='#c8d8ea'))
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        st.subheader("💰 GDP Growth Trend")
        fig2 = px.bar(country_df, x='Year', y='GDP_Growth',
                      color='GDP_Growth', color_continuous_scale='Teal',
                      title=f"{selected_country} – GDP Growth")
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(**PLOT_LAYOUT,
                           title_font=dict(size=13, color='#c8d8ea'))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🔵 GDP Growth vs Youth Unemployment")
    fig3 = px.scatter(country_df, x='GDP_Growth', y='Youth_Unemployment_Rate',
                      color='Year', color_continuous_scale='Bluyl',
                      title=f"Correlation – {selected_country}",
                      labels={'GDP_Growth': 'GDP Growth (%)',
                              'Youth_Unemployment_Rate': 'Youth Unemployment (%)'},
                      text='Year', size_max=14)
    fig3.update_traces(textposition="top center",
                       marker=dict(size=10, line=dict(width=1, color='rgba(255,255,255,0.2)')))
    fig3.update_layout(**PLOT_LAYOUT,
                       title_font=dict(size=13, color='#c8d8ea'))
    st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: FORECASTING
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.navigation == "forecasting":

    st.markdown("""
    <div class="page-hero">
        <h1>🔮 Unemployment Forecasting Engine</h1>
        <p>Project youth unemployment trajectories using linear regression on historical country data.</p>
    </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_fc = st.selectbox("Select Country:", all_countries,
                                   key="forecasting_country_select")
    with f_col2:
        forecast_years = st.slider("Forecast horizon (years ahead):",
                                   min_value=1, max_value=5, value=3)

    show_ci = st.checkbox("Show Prediction Interval Bounds", value=True)

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, r2_score

    base_df = df[df['Country Name'] == selected_fc].sort_values('Year')

    if len(base_df) >= 3:
        ann = base_df[['Year', 'Youth_Unemployment_Rate']].dropna().sort_values('Year').reset_index(drop=True)
        ann['Idx'] = range(len(ann))

        model = LinearRegression()
        model.fit(ann[['Idx']], ann['Youth_Unemployment_Rate'])

        y_pred    = model.predict(ann[['Idx']])
        mae       = mean_absolute_error(ann['Youth_Unemployment_Rate'], y_pred)
        r2        = r2_score(ann['Youth_Unemployment_Rate'], y_pred)
        last_idx  = ann['Idx'].max()
        last_yr   = int(ann['Year'].max())

        fut_idx   = np.arange(last_idx + 1, last_idx + forecast_years + 1).reshape(-1, 1)
        fut_preds = model.predict(fut_idx)
        fut_years = [last_yr + i for i in range(1, forecast_years + 1)]
        margin    = mae * 1.5

        fc_df = pd.DataFrame({
            'Year':                    fut_years,
            'Forecasted_Unemployment': fut_preds,
            'Lower_Bound':             fut_preds - margin,
            'Upper_Bound':             fut_preds + margin,
        })

        # Metrics
        st.markdown('<div class="section-pill">📊 Model Performance</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("R² Fitness Score",        f"{r2:.3f}",
                      help="Variance alignment (closer to 1 is better)")
        with m2:
            st.metric("Mean Absolute Error",     f"{mae:.2f}%",
                      help="Average historical prediction error")
        with m3:
            st.metric("Forecast Window",          f"{forecast_years} Years")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-pill">📈 Historical &amp; Projected Trajectory</div>',
                    unsafe_allow_html=True)

        fig_f = go.Figure()

        fig_f.add_trace(go.Scatter(
            x=ann['Year'], y=ann['Youth_Unemployment_Rate'],
            mode='lines+markers', name='Historical',
            line=dict(color='#34d399', width=3),
            marker=dict(size=8, color='#34d399',
                        line=dict(width=1.5, color='white'))
        ))
        fig_f.add_trace(go.Scatter(
            x=fc_df['Year'], y=fc_df['Forecasted_Unemployment'],
            mode='lines+markers', name='Forecast',
            line=dict(color='#f87171', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond', color='#f87171',
                        line=dict(width=1.5, color='white'))
        ))

        if show_ci:
            fig_f.add_trace(go.Scatter(
                x=pd.concat([fc_df['Year'], fc_df['Year'][::-1]]),
                y=pd.concat([fc_df['Upper_Bound'], fc_df['Lower_Bound'][::-1]]),
                fill='toself', fillcolor='rgba(248,113,113,0.10)',
                line=dict(color='rgba(0,0,0,0)'), name='Prediction Interval',
                hoverinfo='skip'
            ))

        # connector line between last historical and first forecast
        fig_f.add_trace(go.Scatter(
            x=[ann['Year'].iloc[-1], fc_df['Year'].iloc[0]],
            y=[ann['Youth_Unemployment_Rate'].iloc[-1], fc_df['Forecasted_Unemployment'].iloc[0]],
            mode='lines', line=dict(color='rgba(255,255,255,0.15)', width=1.5, dash='dot'),
            showlegend=False, hoverinfo='skip'
        ))

        fig_f.update_layout(**PLOT_LAYOUT,
                            xaxis_title='Year',
                            yaxis_title='Youth Unemployment Rate (%)',
                            hovermode='x unified',
                            title=dict(text=f"<b>{selected_fc}</b> – Forecast",
                                       font=dict(size=13, color='#c8d8ea')))
        st.plotly_chart(fig_f, use_container_width=True)

        # Table
        st.markdown('<div class="section-pill">📋 Projection Detail</div>', unsafe_allow_html=True)
        st.dataframe(
            fc_df.style.format({
                'Forecasted_Unemployment': '{:.2f}%',
                'Lower_Bound':             '{:.2f}%',
                'Upper_Bound':             '{:.2f}%',
            }),
            use_container_width=True
        )

        # Summary insight
        baseline  = ann['Youth_Unemployment_Rate'].iloc[-1]
        terminal  = fut_preds[-1]
        delta     = terminal - baseline
        delta_pct = (delta / baseline * 100) if baseline != 0 else 0

        st.markdown("<br>", unsafe_allow_html=True)
        if delta > 0:
            st.warning(
                f"⚠️ **Projection:** Youth unemployment in **{selected_fc}** is forecast to "
                f"**increase by {delta_pct:+.2f}%** over {forecast_years} year(s), "
                f"reaching **{terminal:.2f}%** by {fut_years[-1]}."
            )
        else:
            st.success(
                f"✅ **Projection:** Youth unemployment in **{selected_fc}** is forecast to "
                f"**decrease by {abs(delta_pct):.2f}%** over {forecast_years} year(s), "
                f"reaching **{terminal:.2f}%** by {fut_years[-1]}."
            )
        st.info("💡 Projections are linear-regression-based. Actual outcomes may differ due to policy, global conditions, or structural shifts.")

    else:
        st.warning(f"⚠️ Insufficient data for **{selected_fc}**. Need ≥ 3 years of records.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: COUNTRY COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.navigation == "comparison":

    st.markdown("""
    <div class="page-hero">
        <h1>🌏 Multi-Country Comparison</h1>
        <p>Compare youth unemployment and economic indicators across countries over time.</p>
    </div>
    """, unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns([1, 1, 2])
    with cc1:
        compare_metric = st.selectbox(
            "Metric:",
            ['Youth_Unemployment_Rate', 'GDP_Growth',
             'Labor_Force_Participation', 'Electricity_Access'],
            format_func=lambda x: x.replace('_', ' '),
            key="comp_metric_select"
        )
    with cc2:
        compare_year = st.selectbox("Year:", available_years,
                                    index=len(available_years) - 2,
                                    key="comp_year_select")
    with cc3:
        compare_countries = st.multiselect(
            "Countries (up to 5):",
            options=all_countries,
            default=all_countries[:5] if len(all_countries) >= 5 else all_countries,
            key="comp_countries_select"
        )

    if compare_countries:
        metric_label = compare_metric.replace('_', ' ').title()

        trend_df = (df[df['Country Name'].isin(compare_countries)]
                    .groupby(['Year', 'Country Name'])[compare_metric]
                    .mean().reset_index())

        fig_line = px.line(
            trend_df, x='Year', y=compare_metric, color='Country Name',
            markers=True, title=f"{metric_label} — Country Trend Comparison",
            labels={compare_metric: metric_label},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_line.add_vline(x=compare_year, line_dash='dot',
                           line_color='rgba(255,255,255,0.25)')
        fig_line.update_layout(
            **PLOT_LAYOUT, height=470,
            title_font=dict(size=13, color='#c8d8ea'),
        )
        fig_line.update_layout(
            legend=dict(orientation='h', y=1.04, x=0.5, xanchor='center',
                        bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Rankings table + bar side by side
        rank_df = (df[(df['Year'] == compare_year) & (df['Country Name'].isin(compare_countries))]
                   [['Country Name', compare_metric]].dropna()
                   .sort_values(compare_metric, ascending=False))

        rt_col, rb_col = st.columns([1, 1])

        with rt_col:
            st.subheader(f"🏅 {metric_label} Rankings — {compare_year}")
            cmap_dict = {
                'Youth_Unemployment_Rate': 'RdYlGn_r',
                'GDP_Growth':              'RdYlGn',
            }
            cmap = cmap_dict.get(compare_metric, 'Blues')
            st.dataframe(
                rank_df.style
                    .format({compare_metric: "{:.2f}%"})
                    .background_gradient(subset=[compare_metric], cmap=cmap),
                use_container_width=True
            )

        with rb_col:
            st.subheader(f"📊 {metric_label} — {compare_year}")
            fig_bar = px.bar(
                rank_df, x='Country Name', y=compare_metric,
                color=compare_metric,
                color_continuous_scale='Teal' if compare_metric != 'Youth_Unemployment_Rate' else 'RdYlGn_r',
                title=f"{metric_label} by Country ({compare_year})",
                labels={compare_metric: metric_label, 'Country Name': ''}
            )
            fig_bar.update_coloraxes(showscale=False)
            fig_bar.update_layout(**PLOT_LAYOUT,
                                  title_font=dict(size=12, color='#c8d8ea'))
            st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("Select at least one country to begin comparison.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: TREND ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.navigation == "trends":

    st.markdown("""
    <div class="page-hero">
        <h1>📉 Trend Analysis</h1>
        <p>Explore regional and country-level metric trajectories with year-over-year change breakdowns.</p>
    </div>
    """, unsafe_allow_html=True)

    tr1, tr2 = st.columns(2)
    with tr1:
        metric_to_show = st.selectbox(
            "Metric:",
            ['Youth_Unemployment_Rate', 'GDP_Growth',
             'Labor_Force_Participation', 'Electricity_Access'],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="trends_metric_select"
        )
    with tr2:
        trends_country = st.selectbox(
            "Country (or Regional Average):",
            ['Regional Average'] + all_countries,
            key="trends_country_select"
        )

    metric_label = metric_to_show.replace('_', ' ').title()
    line_color   = COLOR_MAP.get(metric_to_show, '#94a3b8')

    if trends_country == 'Regional Average':
        trend_df     = df.groupby('Year')[metric_to_show].mean().reset_index()
        title_suffix = "East Asia & Pacific – Regional Average"
    else:
        trend_df     = df[df['Country Name'] == trends_country][['Year', metric_to_show]].dropna()
        title_suffix = trends_country

    if not trend_df.empty:
        # Parse hex to rgba for fill
        r_ = int(line_color[1:3], 16)
        g_ = int(line_color[3:5], 16)
        b_ = int(line_color[5:7], 16)

        max_val  = trend_df[metric_to_show].max()
        min_val  = trend_df[metric_to_show].min()
        max_year = trend_df.loc[trend_df[metric_to_show].idxmax(), 'Year']
        min_year = trend_df.loc[trend_df[metric_to_show].idxmin(), 'Year']

        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(
            x=trend_df['Year'], y=trend_df[metric_to_show],
            mode='lines+markers',
            line=dict(color=line_color, width=3),
            marker=dict(size=8, color=line_color,
                        line=dict(width=1.5, color='rgba(255,255,255,0.5)')),
            fill='tozeroy',
            fillcolor=f'rgba({r_},{g_},{b_},0.10)',
            name=metric_label
        ))
        fig_t.add_annotation(x=max_year, y=max_val,
                             text=f"Peak: {max_val:.2f}%",
                             showarrow=True, arrowhead=2,
                             arrowcolor=line_color,
                             bgcolor='rgba(11,22,40,0.90)',
                             font=dict(size=11, color=line_color))
        fig_t.add_annotation(x=min_year, y=min_val,
                             text=f"Low: {min_val:.2f}%",
                             showarrow=True, arrowhead=2,
                             arrowcolor='#546a82',
                             bgcolor='rgba(11,22,40,0.90)',
                             font=dict(size=11, color='#7a90a8'))

        fig_t.update_layout(
            **PLOT_LAYOUT, height=460,
            title=dict(text=f"<b>{metric_label}</b> — {title_suffix} (2014–2024)",
                       font=dict(size=13, color='#c8d8ea')),
            xaxis_title='Year',
            yaxis_title=f"{metric_label} (%)"
        )
        st.plotly_chart(fig_t, use_container_width=True)

        # Insight metrics
        ins1, ins2, ins3 = st.columns(3)
        first_val  = trend_df[metric_to_show].iloc[0]
        last_val   = trend_df[metric_to_show].iloc[-1]
        change     = last_val - first_val
        change_pct = (change / first_val * 100) if first_val != 0 else 0
        volatility = trend_df[metric_to_show].std()

        with ins1:
            label = f"{change_pct:.1f}% {'increase' if change > 0 else 'decrease'}"
            st.metric("Overall Change", f"{change:+.2f} pp", delta=label)
        with ins2:
            st.metric("Volatility (Std Dev)", f"±{volatility:.2f} pp",
                      help="Higher = more year-to-year fluctuation")
        with ins3:
            st.metric(f"Peak Year", f"{int(max_year)}", delta=f"{max_val:.2f}%")

        # YoY bar chart
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Year-over-Year Change")
        trend_df = trend_df.copy()
        trend_df['YoY'] = trend_df[metric_to_show].diff()

        fig_yoy = px.bar(
            trend_df.dropna(subset=['YoY']),
            x='Year', y='YoY',
            color='YoY',
            color_continuous_scale='RdYlGn_r',
            labels={'YoY': 'Change (pp)', 'Year': 'Year'},
            title=f"Year-over-Year Δ {metric_label}"
        )
        fig_yoy.add_hline(y=0, line_dash='dot',
                          line_color='rgba(255,255,255,0.25)', line_width=1.5)
        fig_yoy.update_coloraxes(showscale=False)
        fig_yoy.update_layout(**PLOT_LAYOUT,
                              title_font=dict(size=12, color='#c8d8ea'))
        st.plotly_chart(fig_yoy, use_container_width=True)

    else:
        st.warning(f"No data available for **{trends_country}** on **{metric_label}**.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: REGRESSION INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.navigation == "regression_insights":

    st.markdown("""
    <div class="page-hero">
        <h1>📐 Regression Insights</h1>
        <p>OLS statistical modelling of youth unemployment determinants across the East Asia &amp; Pacific region.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Coefficient table ────────────────────────────────────────────
    st.markdown('<div class="section-pill">📊 Model Coefficients</div>', unsafe_allow_html=True)

    vars_ = ['const', 'GDP_Growth', 'Labor_Force_Participation', 'Electricity_Access']
    labels_ = ['Intercept (Constant)', 'GDP Growth (%)',
               'Labor Force Participation (%)', 'Electricity Access (%)']

    coef_df = pd.DataFrame({
        'Variable':   labels_,
        'Coefficient':[f"{ols_model.params[v]:.4f}"    for v in vars_],
        'Std Error':  [f"{ols_model.bse[v]:.4f}"       for v in vars_],
        't-statistic':[f"{ols_model.tvalues[v]:.3f}"   for v in vars_],
        'p-value':    [f"{ols_model.pvalues[v]:.4f}"   for v in vars_],
        'Significant':['✅ Yes' if ols_model.pvalues[v] < 0.05 else '❌ No' for v in vars_],
    })
    st.dataframe(coef_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fit stats ────────────────────────────────────────────────────
    st.markdown('<div class="section-pill">📈 Model Fit Statistics</div>', unsafe_allow_html=True)

    fs1, fs2, fs3, fs4 = st.columns(4)
    with fs1: st.metric("R-squared",         f"{ols_model.rsquared:.3f}")
    with fs2: st.metric("Adj. R-squared",    f"{ols_model.rsquared_adj:.3f}")
    with fs3: st.metric("F-statistic",       f"{ols_model.fvalue:.2f}")
    with fs4: st.metric("Prob (F-statistic)",f"{ols_model.f_pvalue:.2e}")

    st.markdown("---")

    # ── Key findings ─────────────────────────────────────────────────
    st.markdown('<div class="section-pill">🔑 Findings</div>', unsafe_allow_html=True)

    kf1, kf2 = st.columns(2)
    lfp_coef  = ols_model.params['Labor_Force_Participation']
    lfp_pval  = ols_model.pvalues['Labor_Force_Participation']
    gdp_coef  = ols_model.params['GDP_Growth']
    gdp_pval  = ols_model.pvalues['GDP_Growth']
    elec_coef = ols_model.params['Electricity_Access']
    elec_pval = ols_model.pvalues['Electricity_Access']

    with kf1:
        st.subheader("📉 Labor Force Participation")
        st.info(f"""
**Coefficient:** {lfp_coef:.4f} &nbsp;|&nbsp; **p-value:** {lfp_pval:.4e}

For every 1 pp increase in Labor Force Participation, Youth Unemployment **decreases by {abs(lfp_coef):.2f} pp**.  
This is statistically significant (p < 0.001) — the strongest predictor in the model.
        """)

        st.subheader("📈 GDP Growth")
        st.info(f"""
**Coefficient:** {gdp_coef:.4f} &nbsp;|&nbsp; **p-value:** {gdp_pval:.4f}

GDP Growth does **not** have a statistically significant impact on Youth Unemployment (p > 0.05).  
Macroeconomic expansion alone does not reduce youth unemployment in the EAP region.
        """)

    with kf2:
        st.subheader("⚡ Electricity Access")
        st.info(f"""
**Coefficient:** {elec_coef:.4f} &nbsp;|&nbsp; **p-value:** {elec_pval:.4e}

For every 1 pp increase in Electricity Access, Youth Unemployment **increases by {elec_coef:.2f} pp**.  
This positive correlation may reflect more robust labor reporting in highly electrified economies.
        """)

        st.subheader("🎯 Model Significance")
        st.info(f"""
**R² = {ols_model.rsquared:.3f}** — the model explains {ols_model.rsquared*100:.1f}% of variance in Youth Unemployment across the EAP region.

**F-statistic p-value:** {ols_model.f_pvalue:.2e} — model is statistically significant overall.
        """)

    st.markdown("---")

    # ── Regression equation ──────────────────────────────────────────
    st.markdown('<div class="section-pill">📐 Regression Equation</div>', unsafe_allow_html=True)
    st.latex(r"""
    \text{Youth Unemployment} = 24.68
    - 0.053(\text{GDP Growth})
    - 0.434(\text{Labor Force Participation})
    + 0.156(\text{Electricity Access})
    """)
    st.caption("Intercept and coefficients rounded to 2–3 decimal places for readability.")

    st.markdown("---")

    # ── Coefficient visual ───────────────────────────────────────────
    st.markdown('<div class="section-pill">📊 Coefficient Comparison</div>', unsafe_allow_html=True)

    coef_plot = pd.DataFrame({
        'Variable':    ['GDP Growth', 'Labor Force Participation', 'Electricity Access'],
        'Coefficient': [ols_model.params['GDP_Growth'],
                        ols_model.params['Labor_Force_Participation'],
                        ols_model.params['Electricity_Access']],
        'Color':       ['#34d399', '#38bdf8', '#fb923c'],
    })

    fig_coef = px.bar(
        coef_plot, x='Variable', y='Coefficient',
        color='Variable',
        color_discrete_sequence=['#34d399', '#38bdf8', '#fb923c'],
        title='OLS Coefficients (effect on Youth Unemployment Rate)',
        labels={'Coefficient': 'Coefficient Value', 'Variable': ''}
    )
    fig_coef.add_hline(y=0, line_dash='dot',
                       line_color='rgba(255,255,255,0.25)', line_width=1.5)
    fig_coef.update_layout(**PLOT_LAYOUT, showlegend=False,
                           title_font=dict(size=12, color='#c8d8ea'))
    st.plotly_chart(fig_coef, use_container_width=True)

    # ── Conclusion ───────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("💡 Conclusion")
    st.markdown("""
> The inferential modeling confirms that **macroeconomic growth (GDP) has a negligible impact**
> on youth unemployment across the EAP region. This means that GDP growth alone doesn't reduce youth unemployment.
> Even when a country's economy is growing, that doesn't automatically mean more young people find jobs.
> The data shows this connection is too weak to be considered reliable.

> In contrast, **Labor Force Participation is the most significant inverse determinant**
> of youth unemployment. Countries where more people are looking for or already have jobs tend to have lower youth unemployment. 
> Getting young people engaged in the labour market matters more than economic growth on its own.

> Additionally, Better access to electricity is linked to higher reported unemployment — but not for bad reasons,
> This sounds counterintuitive, but more developed, electrified countries tend to have better systems for tracking and recording unemployment. 
> So the number looks higher simply because it's being measured more accurately.

    """)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;opacity:0.35;font-size:0.75rem;"
    "font-family:\"Plus Jakarta Sans\",sans-serif;letter-spacing:0.03em;'>"
    "📊 Data: <a href='https://databank.worldbank.org/' target='_blank' "
    "style='color:#38bdf8;text-decoration:none;'>World Bank WDI</a>"
    " &nbsp;·&nbsp; East Asia &amp; Pacific 2014–2024"
    " &nbsp;·&nbsp; SDG 8: Decent Work &amp; Economic Growth</p>",
    unsafe_allow_html=True
)
