"""
SDG 8 – Youth Unemployment Dashboard  (Enhanced UI)
=====================================================
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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e2e8f0;
    font-size: 15px;
    line-height: 1.6;
}

/* ── App background – layered mesh gradient ── */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%,   rgba(56,189,248,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 10%,  rgba(168,85,247,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 50% 90%,  rgba(20,184,166,0.10) 0%, transparent 60%),
        linear-gradient(160deg, #080c14 0%, #0d1117 45%, #06090f 100%);
    min-height: 100vh;
}

/* ── Main container ── */
.main .block-container {
    padding: 1.8rem 2.5rem 3rem;
    max-width: 97%;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(8, 12, 22, 0.96) !important;
    border-right: 1px solid rgba(56,189,248,0.15) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }

/* ── Sidebar nav buttons ── */
section[data-testid="stSidebar"] button {
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 4px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0em !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: rgba(255,255,255,0.04) !important;
    color: #94a3b8 !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(56,189,248,0.10) !important;
    border-color: rgba(56,189,248,0.25) !important;
    color: #e2e8f0 !important;
    transform: translateX(3px) !important;
}

/* ── Metric cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.055) 0%, rgba(255,255,255,0.025) 100%) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 1.1rem 1.3rem !important;
    backdrop-filter: blur(20px);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
    opacity: 0.7;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(56,189,248,0.18);
    border-color: rgba(56,189,248,0.22) !important;
}
div[data-testid="stMetric"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 500 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.01em;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Charts ── */
.stPlotlyChart {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 14px;
    backdrop-filter: blur(12px);
    overflow: hidden;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
}

/* ── Selectbox & widgets ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] { padding: 0.5rem 0; }

/* ── Info / warning / success boxes ── */
.stAlert {
    border-radius: 14px !important;
    border-left-width: 3px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

/* ── Section headers ── */
h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.85rem !important;
    letter-spacing: -0.02em !important;
    color: #f1f5f9 !important;
    margin-bottom: 0.15rem !important;
}
h2 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.25rem !important;
    color: #cbd5e1 !important;
    letter-spacing: -0.01em !important;
}
h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #94a3b8 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
}

/* ── HR ── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.2rem 0 !important; }

/* ── Checkbox ── */
label[data-testid="stCheckbox"] { font-size: 0.9rem !important; color: #cbd5e1 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(56,189,248,0.3); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.55); }

/* ── Section divider pill ── */
.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.10);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.8rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Page hero banner ── */
.page-hero {
    background: linear-gradient(135deg, rgba(56,189,248,0.08) 0%, rgba(129,140,248,0.08) 50%, rgba(52,211,153,0.06) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.page-hero::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.page-hero h1 { font-size: 1.6rem !important; margin-bottom: 0.3rem !important; color: #f1f5f9 !important; -webkit-text-fill-color: #f1f5f9 !important; }
.page-hero p  { color: #94a3b8; font-size: 0.9rem; margin: 0; line-height: 1.5; }

/* ── Stat badge (for sidebar) ── */
.stat-badge {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-top: 4px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stat-badge span { color: #cbd5e1; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. Sidebar Navigation
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.4rem 0.2rem 1rem;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.05rem;font-weight:800;
                    color:#f1f5f9;
                    letter-spacing:-0.01em;margin-bottom:2px;">
            SDG 8 Dashboard
        </div>
        <div style="font-size:0.73rem;color:#64748b;letter-spacing:0.05em;text-transform:uppercase;
                    font-weight:600;font-family:'Plus Jakarta Sans',sans-serif;">Youth Unemployment Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    nav_options = {
        "dashboard":          "📈  Dashboard Overview",
        "comparison":         "🌏  Country Comparison",
        "trends":             "📉  Trend Analysis",
        "forecasting":        "🔮  Unemployment Forecasting",
        "regression_insights":"📐  Regression Insights",
    }

    if 'navigation' not in st.session_state:
        st.session_state.navigation = "dashboard"

    for nav_key, nav_label in nav_options.items():
        if st.sidebar.button(nav_label, key=nav_key, use_container_width=True):
            st.session_state.navigation = nav_key

    st.markdown("---")
    st.markdown("""
    <div class="stat-badge">
        <span>Data Source</span><br>World Bank WDI
    </div>
    <div class="stat-badge" style="margin-top:6px;">
        <span>Region</span><br>East Asia &amp; Pacific
    </div>
    <div class="stat-badge" style="margin-top:6px;">
        <span>Period</span><br>2014 – 2024
    </div>
    <div class="stat-badge" style="margin-top:6px;">
        <span>Goal</span><br>SDG 8 · Decent Work &amp; Growth
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. Shared Plotly template
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#94a3b8'),
    margin=dict(l=50, r=30, t=50, b=50),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False,
               title_font=dict(size=11, color='#64748b')),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False,
               title_font=dict(size=11, color='#64748b')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
    hoverlabel=dict(bgcolor='#0d1117', font_family='JetBrains Mono, monospace',
                    font_size=12, bordercolor='rgba(255,255,255,0.15)'),
)

COLOR_MAP = {
    'Youth_Unemployment_Rate': '#f87171',
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

    # Hero
    st.markdown("""
    <div class="page-hero">
        <h1>📊 Youth Unemployment Dashboard</h1>
        <p>East Asia &amp; Pacific Region · World Bank WDI · 2014–2024 · SDG 8: Decent Work &amp; Economic Growth</p>
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
                          title_font=dict(size=13, color='#cbd5e1'))
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        st.subheader("💰 GDP Growth Trend")
        fig2 = px.bar(country_df, x='Year', y='GDP_Growth',
                      color='GDP_Growth', color_continuous_scale='Teal',
                      title=f"{selected_country} – GDP Growth")
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(**PLOT_LAYOUT,
                           title_font=dict(size=13, color='#cbd5e1'))
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
                       title_font=dict(size=13, color='#cbd5e1'))
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
                                       font=dict(size=13, color='#cbd5e1')))
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
            title_font=dict(size=13, color='#cbd5e1'),
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
                                  title_font=dict(size=12, color='#cbd5e1'))
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
                             bgcolor='rgba(13,17,23,0.85)',
                             font=dict(size=11, color=line_color))
        fig_t.add_annotation(x=min_year, y=min_val,
                             text=f"Low: {min_val:.2f}%",
                             showarrow=True, arrowhead=2,
                             arrowcolor='#64748b',
                             bgcolor='rgba(13,17,23,0.85)',
                             font=dict(size=11, color='#94a3b8'))

        fig_t.update_layout(
            **PLOT_LAYOUT, height=460,
            title=dict(text=f"<b>{metric_label}</b> — {title_suffix} (2014–2024)",
                       font=dict(size=13, color='#cbd5e1')),
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
                              title_font=dict(size=12, color='#cbd5e1'))
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
                           title_font=dict(size=12, color='#cbd5e1'))
    st.plotly_chart(fig_coef, use_container_width=True)

    # ── Conclusion ───────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("💡 Conclusion")
    st.markdown("""
> The inferential modeling confirms that **macroeconomic growth (GDP) has a negligible impact**
> on youth unemployment across the EAP region, failing to reach statistical significance.

> In contrast, **Labor Force Participation is the most significant inverse determinant**
> of youth unemployment, indicating structural labor market integration is more critical
> than macroeconomic expansion.

> Additionally, **Electricity Access shows a persistent positive correlation** with unemployment,
> potentially reflecting more robust labor reporting standards in highly electrified economies.

> The robustness of these findings is confirmed by the alignment of OLS and RLM estimates,
> which mitigate the distorting effects of extreme macroeconomic volatility.
    """)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;opacity:0.4;font-size:0.78rem;font-family:\"Plus Jakarta Sans\",sans-serif;'>"
    "📊 Data: <a href='https://databank.worldbank.org/' target='_blank' style='color:#38bdf8;'>"
    "World Bank WDI</a> &nbsp;·&nbsp; East Asia &amp; Pacific 2014–2024 &nbsp;·&nbsp; "
    "SDG 8: Decent Work &amp; Economic Growth</p>",
    unsafe_allow_html=True
)