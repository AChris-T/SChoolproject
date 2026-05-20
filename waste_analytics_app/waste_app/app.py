"""
╔══════════════════════════════════════════════════════════════════╗
║   HOSTEL WASTE ANALYTICS & PREDICTION SYSTEM                    ║
║   TCE 528 — Waste Management Engineering                        ║
║   University of Ibadan                                          ║
╚══════════════════════════════════════════════════════════════════╝

Run:
    streamlit run app.py
"""

import io
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hostel Waste Analytics",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    * {
        scrollbar-width: thin;
        scrollbar-color: #48bb78 #0e1117;
    }
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0e1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #48bb78;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #68d391;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main { 
        background: linear-gradient(135deg, #0e1117 0%, #0d1517 100%);
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #161b27 100%);
        border: 1.5px solid #2d3748;
        border-radius: 14px;
        padding: 24px 28px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        border-color: #48bb78;
        box-shadow: 0 12px 48px rgba(72,187,120,0.15), inset 0 1px 0 rgba(255,255,255,0.1);
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(90deg, #48bb78, #68d391);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #a0aec0;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 8px;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 0.82rem;
        color: #7d8696;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Section headers */
    .section-header {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #48bb78;
        border-left: 4px solid #48bb78;
        padding-left: 12px;
        margin-bottom: 20px;
        margin-top: 4px;
    }

    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(26,37,53,0.8) 0%, rgba(16,22,35,0.8) 100%);
        border-left: 4px solid #48bb78;
        border-radius: 0 12px 12px 0;
        border: 1px solid #1f2937;
        border-left: 4px solid #48bb78;
        padding: 16px 20px;
        margin-bottom: 12px;
        font-size: 0.9rem;
        color: #e2e8f0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    .insight-card:hover {
        border-color: #48bb78;
        background: linear-gradient(135deg, rgba(26,37,53,0.95) 0%, rgba(16,22,35,0.95) 100%);
    }
    .insight-warn {
        border-left-color: #f6ad55;
        background: linear-gradient(135deg, rgba(45,32,16,0.8) 0%, rgba(30,18,8,0.8) 100%);
    }
    .insight-danger {
        border-left-color: #fc8181;
        background: linear-gradient(135deg, rgba(45,16,16,0.8) 0%, rgba(30,8,8,0.8) 100%);
    }

    /* Sig badge */
    .sig-yes {
        background: #0d2218; color: #48bb78;
        border: 1px solid #48bb78;
        border-radius: 6px; padding: 2px 10px;
        font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    .sig-no {
        background: #1c2128; color: #718096;
        border: 1px solid #2d3748;
        border-radius: 6px; padding: 2px 10px;
        font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, #0d1117 0%, #161b27 100%);
        border-radius: 12px;
        padding: 6px;
        border: 1px solid #1f2937;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.87rem;
        transition: all 0.2s ease;
        background: #0d1117;
        border: 1px solid transparent;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #161b27;
        border-color: #48bb78;
        color: #48bb78;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0d1117 0%, #0f1419 100%);
        border-right: 1px solid #1f2937;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(72,187,120,0.3);
    }
    .stButton > button:hover {
        box-shadow: 0 8px 24px rgba(72,187,120,0.4);
        transform: translateY(-2px);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: #161b27 !important;
        border: 1px solid #21262d !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }

    /* DataFrame */
    .dataframe { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 0.8rem;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────
COLORS = {
    "bio":    "#48bb78",
    "nonbio": "#fc8181",
    "rec":    "#63b3ed",
    "haz":    "#f6ad55",
    "bg":     "#0e1117",
    "card":   "#161b22",
    "border": "#21262d",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(22,27,34,0.8)",
    font_color="#c9d1d9",
    font_family="Inter",
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262d", borderwidth=1),
    xaxis=dict(gridcolor="#21262d", linecolor="#21262d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#21262d"),
    margin=dict(l=40, r=20, t=40, b=40),
)

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────

def styled_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def metric_card(col, value, label, sub=""):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {"<div class='metric-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)


def insight(text: str, kind="normal"):
    cls = {"normal": "insight-card", "warn": "insight-card insight-warn", "danger": "insight-card insight-danger"}.get(kind, "insight-card")
    st.markdown(f'<div class="{cls}">💡 {text}</div>', unsafe_allow_html=True)


AUDIT_COLUMNS = [
    "hall", "floor_block", "date", "day_number",
    "biodegradable_kg", "non_biodegradable_kg", "recyclable_kg", "hazardous_kg", "population"
]

SURVEY_COLUMNS = [
    "respondent_id", "hall", "level",
    "meals_per_day", "packaged_food_frequency",
    "disposal_frequency_per_week", "recycling_awareness",
    "visitor_effect", "separation_behaviour", "waste_scale"
]


def empty_audit_df() -> pd.DataFrame:
    return pd.DataFrame(columns=AUDIT_COLUMNS)


def empty_survey_df() -> pd.DataFrame:
    return pd.DataFrame(columns=SURVEY_COLUMNS)


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return buf.getvalue()


def sig_badge(p: float) -> str:
    if p < 0.001:
        return '<span class="sig-yes">p &lt; 0.001 ✓</span>'
    elif p < 0.05:
        return f'<span class="sig-yes">p = {p:.3f} ✓</span>'
    else:
        return f'<span class="sig-no">p = {p:.3f}</span>'


# ─────────────────────────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────────────────────────




# ─────────────────────────────────────────────────────────────────
# ANALYTICS FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def compute_audit_analytics(df: pd.DataFrame) -> dict:
    num_cols = ["biodegradable_kg", "non_biodegradable_kg", "recyclable_kg", "hazardous_kg"]
    for c in num_cols + ["population", "day_number"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # Hall summary
    hall_grp = df.groupby("hall").agg(
        bio    =("biodegradable_kg",     "sum"),
        nonbio =("non_biodegradable_kg", "sum"),
        rec    =("recyclable_kg",        "sum"),
        haz    =("hazardous_kg",         "sum"),
        pop    =("population",           "max"),
        days   =("day_number",           "nunique"),
    ).reset_index()
    hall_grp["total"] = hall_grp[["bio","nonbio","rec","haz"]].sum(axis=1)
    hall_grp["bio_pct"]    = (hall_grp["bio"]    / hall_grp["total"] * 100).round(1)
    hall_grp["nonbio_pct"] = (hall_grp["nonbio"] / hall_grp["total"] * 100).round(1)
    hall_grp["rec_pct"]    = (hall_grp["rec"]    / hall_grp["total"] * 100).round(1)
    hall_grp["haz_pct"]    = (hall_grp["haz"]    / hall_grp["total"] * 100).round(1)
    hall_grp["days"]       = hall_grp["days"].clip(lower=1)
    hall_grp["per_capita"] = (hall_grp["total"] / (hall_grp["pop"].clip(lower=1) * hall_grp["days"])).round(4)

    # Daily trend
    df["total_kg"] = df[num_cols].sum(axis=1)
    daily = df.groupby("day_number")[["total_kg"] + num_cols].sum().reset_index()
    daily.rename(columns={
        "biodegradable_kg": "Biodegradable",
        "non_biodegradable_kg": "Non-biodegradable",
        "recyclable_kg": "Recyclable",
        "hazardous_kg": "Hazardous",
    }, inplace=True)

    # Hall × day trend
    hall_daily = df.groupby(["hall", "day_number"])["total_kg"].sum().reset_index()

    return {"hall_summary": hall_grp, "daily": daily, "hall_daily": hall_daily}


def run_regression(df: pd.DataFrame) -> dict | None:
    required = ["meals_per_day","packaged_food_frequency","disposal_frequency_per_week",
                "recycling_awareness","visitor_effect","separation_behaviour","waste_scale"]
    if not all(c in df.columns for c in required):
        return None
    sub = df[required].dropna()
    if len(sub) < 8:
        return None
    for c in required:
        sub[c] = pd.to_numeric(sub[c], errors="coerce")
    sub = sub.dropna()

    X_raw = sub[required[:-1]]
    y     = sub["waste_scale"]
    X     = sm.add_constant(X_raw)

    try:
        model = sm.OLS(y, X).fit()
    except Exception:
        return None

    labels = ["Intercept","Meals/day","Packaged food freq","Disposal freq/week",
              "Recycling awareness","Visitor effect","Separation behaviour"]

    return {
        "model":    model,
        "labels":   labels,
        "beta":     model.params.values,
        "se":       model.bse.values,
        "tstat":    model.tvalues.values,
        "pval":     model.pvalues.values,
        "r2":       model.rsquared,
        "adj_r2":   model.rsquared_adj,
        "f_stat":   model.fvalue,
        "f_pval":   model.f_pvalue,
        "n":        int(model.nobs),
        "X_cols":   required[:-1],
    }


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 10px;">
            <div style="font-size:2.5rem">♻️</div>
            <div style="font-size:1rem; font-weight:700; color:#e2e8f0; margin-top:8px;">
                Waste Analytics
            </div>
            <div style="font-size:0.7rem; color:#718096; margin-top:4px; letter-spacing:0.1em;">
                TCE 528 · UNIV. IBADAN
            </div>
        </div>
        <hr style="border-color:#1f2937; margin:12px 0;">
        """, unsafe_allow_html=True)

        st.markdown("### 📌 Navigation")
        page = st.radio(
            "", ["🏠 Overview", "📊 Audit Analysis", "📋 Survey & Regression", "🔮 Predictor", "📥 Data Entry"],
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border-color:#1f2937; margin:16px 0;'>", unsafe_allow_html=True)

        st.markdown("### 📂 Load Data")
        audit_file  = st.file_uploader("Audit CSV / Excel", type=["csv","xlsx"], key="audit_upload")
        survey_file = st.file_uploader("Survey CSV / Excel", type=["csv","xlsx"], key="survey_upload")

        st.markdown("<hr style='border-color:#1f2937; margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.7rem; color:#4a5568; text-align:center;">
            Group 1 · 2025/2026<br>
            Waste Management Engineering
        </div>
        """, unsafe_allow_html=True)

    return page, audit_file, survey_file


# ─────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────

def page_overview(audit_df, survey_df):
    st.markdown("""
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:4px;
               background:linear-gradient(90deg,#e2e8f0,#48bb78);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        Hostel Waste Analytics & Prediction System
    </h1>
    <p style="color:#718096; margin-bottom:32px; font-size:0.92rem;">
        University of Ibadan · Student Halls of Residence · Academic Session 2025/2026
    </p>
    """, unsafe_allow_html=True)

    # Status cards
    c1, c2, c3, c4 = st.columns(4)
    if audit_df is not None:
        halls = audit_df["hall"].nunique()
        total = (audit_df["biodegradable_kg"].sum() + audit_df["non_biodegradable_kg"].sum() +
                 audit_df["recyclable_kg"].sum()    + audit_df["hazardous_kg"].sum())
        metric_card(c1, f"{total:.1f} kg", "Total Waste Recorded", f"{halls} halls sampled")
        metric_card(c2, str(len(audit_df)), "Audit Records", "Physical measurements")
    else:
        metric_card(c1, "—", "Total Waste", "Upload audit data")
        metric_card(c2, "—", "Audit Records", "No data loaded")

    if survey_df is not None:
        metric_card(c3, str(len(survey_df)), "Survey Responses", "Student behaviour data")
        visitor_pct = (survey_df["visitor_effect"].sum() / len(survey_df) * 100) if len(survey_df) > 0 else 0
        metric_card(c4, f"{visitor_pct:.0f}%", "Visitor Effect", "Report increased waste")
    else:
        metric_card(c3, "—", "Survey Responses", "Upload survey data")
        metric_card(c4, "—", "Visitor Effect", "No data loaded")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    styled_header("System Capabilities")
    cols = st.columns(3)
    features = [
        ("📊", "Waste Characterisation",
         "Break down waste by hall, category, and day. Visualise biodegradable vs non-biodegradable vs recyclable vs hazardous fractions.",
         "#48bb78", "0.1"),
        ("📈", "Per Capita Analytics",
         "Calculate daily and weekly per-capita generation rates per hall and compare against Nigerian university benchmarks (0.3–0.8 kg/person/day).",
         "#63b3ed", "0.05"),
        ("🔮", "Predictive Modelling",
         "Multiple linear regression identifies which student behaviours drive waste generation. Visitor effect, meals per day, recycling awareness and more.",
         "#f6ad55", "0"),
    ]
    for col, (icon, title, desc, accent_color, delay) in zip(cols, features):
        col.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(22,27,34,0.8) 0%, rgba(13,17,23,0.9) 100%);
            border: 1.5px solid {accent_color}26;
            border-radius: 14px;
            padding: 28px;
            height: 220px;
            box-shadow: 0 8px 32px rgba({accent_color[1:].upper()}, 0.15),
                        inset 0 1px 0 rgba(255,255,255,0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideUp 0.6s ease-out {delay}s both;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                right: 0;
                width: 100px;
                height: 100px;
                background: radial-gradient(circle, {accent_color}15 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
            "></div>
            <div style="
                position: relative;
                z-index: 1;
                display: flex;
                flex-direction: column;
                height: 100%;
            ">
                <div>
                    <div style="
                        font-size: 2.2rem;
                        margin-bottom: 14px;
                        display: inline-block;
                        padding: 10px 12px;
                        background: {accent_color}15;
                        border-radius: 10px;
                        border: 1px solid {accent_color}30;
                    ">
                        {icon}
                    </div>
                    <div style="
                        font-weight: 700;
                        color: #e2e8f0;
                        margin-bottom: 10px;
                        font-size: 1.05rem;
                        background: linear-gradient(90deg, #e2e8f0 0%, {accent_color} 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">
                        {title}
                    </div>
                    <div style="
                        color: #a0aec0;
                        font-size: 0.85rem;
                        line-height: 1.6;
                        margin-bottom: 16px;
                    ">
                        {desc}
                    </div>
                </div>
                <div style="
                    margin-top: auto;
                    padding-top: 12px;
                    border-top: 1px solid {accent_color}20;
                    font-size: 0.72rem;
                    color: {accent_color};
                    font-weight: 600;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    opacity: 0.8;
                ">
                    ✓ Enabled
                </div>
            </div>
        </div>
        <style>
            @keyframes slideUp {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    styled_header("Quick Start")
    st.markdown("""
    <div class="insight-card">
        <strong>Step 1:</strong> Upload your data using the sidebar — Audit CSV and Survey CSV separately.
        Or check <em>Use built-in sample data</em> to explore with real-looking data from UI hostels.
    </div>
    <div class="insight-card">
        <strong>Step 2:</strong> Go to <em>Audit Analysis</em> for waste quantity and composition charts.
    </div>
    <div class="insight-card">
        <strong>Step 3:</strong> Go to <em>Survey & Regression</em> to see what drives waste generation.
    </div>
    <div class="insight-card">
        <strong>Step 4:</strong> Use the <em>Predictor</em> to estimate waste scale for any student profile.
    </div>
    <div class="insight-card">
        <strong>Step 5:</strong> Use <em>Data Entry</em> to manually type in records row by row.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# PAGE: AUDIT ANALYSIS
# ─────────────────────────────────────────────────────────────────

def page_audit(audit_df):
    st.markdown("## 📊 Physical Audit Analysis")

    if audit_df is None:
        st.info("No audit data loaded. Upload a CSV or enable sample data in the sidebar.")
        return

    ana = compute_audit_analytics(audit_df.copy())
    hall_sum = ana["hall_summary"]
    daily    = ana["daily"]
    h_daily  = ana["hall_daily"]

    # ── KPI row
    styled_header("Hall Summary — Weekly Totals")
    kpi_cols = st.columns(len(hall_sum))
    for col, (_, row) in zip(kpi_cols, hall_sum.iterrows()):
        pc_color = "#48bb78" if 0.3 <= row["per_capita"] <= 0.8 else "#f6ad55"
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{row['total']:.1f}</div>
            <div class="metric-label">kg / week</div>
            <div style="font-weight:700; color:#e2e8f0; margin-top:8px;">{row['hall']}</div>
            <div style="font-size:0.78rem; color:{pc_color}; margin-top:4px;">
                {row['per_capita']:.3f} kg/person/day
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Benchmark note
    st.markdown("<br>", unsafe_allow_html=True)
    below = hall_sum[hall_sum["per_capita"] < 0.3]
    within = hall_sum[(hall_sum["per_capita"] >= 0.3) & (hall_sum["per_capita"] <= 0.8)]
    if len(within) > 0:
        insight(f"{', '.join(within['hall'].tolist())} — per capita rates fall within the Nigerian university benchmark (0.3–0.8 kg/person/day).")
    if len(below) > 0:
        insight(f"{', '.join(below['hall'].tolist())} — below benchmark range. Check if population estimate is accurate or if students dispose outside the hall.", "warn")

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Composition", "📅 Daily Trend", "🏠 Hall × Day", "📋 Raw Table"])

    # ── Tab 1: Composition
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            styled_header("Weekly Waste by Category & Hall")
            fig = go.Figure()
            cats = [("bio","Biodegradable",COLORS["bio"]),
                    ("nonbio","Non-biodegradable",COLORS["nonbio"]),
                    ("rec","Recyclable",COLORS["rec"]),
                    ("haz","Hazardous",COLORS["haz"])]
            for key, name, color in cats:
                fig.add_trace(go.Bar(
                    name=name, x=hall_sum["hall"], y=hall_sum[key],
                    marker_color=color, marker_line_width=0,
                ))
            fig.update_layout(**PLOTLY_LAYOUT, barmode="group", height=360,
                              yaxis_title="kg", title="")
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            styled_header("Composition % by Hall")
            fig2 = make_subplots(
                rows=1, cols=len(hall_sum),
                specs=[[{"type":"pie"}] * len(hall_sum)],
                subplot_titles=hall_sum["hall"].tolist(),
            )
            for i, (_, row) in enumerate(hall_sum.iterrows(), start=1):
                fig2.add_trace(go.Pie(
                    values=[row["bio"], row["nonbio"], row["rec"], row["haz"]],
                    labels=["Bio","NonBio","Rec","Haz"],
                    marker_colors=[COLORS["bio"],COLORS["nonbio"],COLORS["rec"],COLORS["haz"]],
                    hole=0.42,
                    textinfo="percent",
                    showlegend=(i == 1),
                ), row=1, col=i)
            fig2.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)

        # Detailed table
        styled_header("Detailed Composition Table")
        display = hall_sum.rename(columns={
            "hall":"Hall","total":"Total (kg)","bio":"Bio (kg)","nonbio":"NonBio (kg)",
            "rec":"Rec (kg)","haz":"Haz (kg)","bio_pct":"Bio %","nonbio_pct":"NonBio %",
            "rec_pct":"Rec %","haz_pct":"Haz %","per_capita":"kg/person/day","days":"Days Sampled"
        })
        st.dataframe(
            display[["Hall","Total (kg)","Bio (kg)","NonBio (kg)","Rec (kg)","Haz (kg)",
                      "Bio %","NonBio %","Rec %","Haz %","kg/person/day","Days Sampled"]],
            use_container_width=True, hide_index=True,
        )

        # Download
        st.download_button(
            "📥 Download Summary (Excel)",
            to_excel_bytes(display),
            "hall_summary.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # ── Tab 2: Daily trend
    with tab2:
        styled_header("Daily Total Waste Generation (All Halls)")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=daily["day_number"], y=daily["total_kg"],
            mode="lines+markers", name="Total",
            line=dict(color=COLORS["bio"], width=3),
            marker=dict(size=8, color=COLORS["bio"]),
        ))
        for cat, color in [("Biodegradable",COLORS["bio"]),("Non-biodegradable",COLORS["nonbio"]),
                           ("Recyclable",COLORS["rec"]),("Hazardous",COLORS["haz"])]:
            if cat in daily.columns:
                fig3.add_trace(go.Scatter(
                    x=daily["day_number"], y=daily[cat],
                    mode="lines", name=cat,
                    line=dict(color=color, width=1.5, dash="dot"),
                ))
        fig3.update_layout(**PLOTLY_LAYOUT, height=380,
                           xaxis_title="Day", yaxis_title="kg",
                           xaxis=dict(tickmode="linear", dtick=1, **PLOTLY_LAYOUT["xaxis"]))
        st.plotly_chart(fig3, use_container_width=True)

        peak_day = daily.loc[daily["total_kg"].idxmax(), "day_number"]
        min_day  = daily.loc[daily["total_kg"].idxmin(), "day_number"]
        insight(f"Peak generation on Day {peak_day} — likely weekend cooking and visitor activity.")
        insight(f"Lowest generation on Day {min_day}.")

    # ── Tab 3: Hall × Day
    with tab3:
        styled_header("Daily Generation by Hall")
        fig4 = px.line(
            h_daily, x="day_number", y="total_kg", color="hall",
            markers=True,
            color_discrete_sequence=[COLORS["bio"], COLORS["rec"], COLORS["haz"], COLORS["nonbio"]],
        )
        fig4.update_layout(**PLOTLY_LAYOUT, height=380,
                           xaxis_title="Day", yaxis_title="kg")
        st.plotly_chart(fig4, use_container_width=True)

    # ── Tab 4: Raw
    with tab4:
        styled_header("Raw Audit Data")
        hall_filter = st.multiselect("Filter by Hall", audit_df["hall"].unique().tolist(),
                                     default=audit_df["hall"].unique().tolist())
        filtered = audit_df[audit_df["hall"].isin(hall_filter)]
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.download_button("📥 Download Filtered Data (CSV)",
                           filtered.to_csv(index=False).encode(),
                           "audit_filtered.csv", "text/csv")


# ─────────────────────────────────────────────────────────────────
# PAGE: SURVEY & REGRESSION
# ─────────────────────────────────────────────────────────────────

def page_survey(survey_df):
    st.markdown("## 📋 Survey Analysis & Regression Model")

    if survey_df is None:
        st.info("No survey data loaded. Upload a CSV or enable sample data in the sidebar.")
        return

    n = len(survey_df)
    result = run_regression(survey_df)

    # ── Descriptive stats
    styled_header("Respondent Overview")
    c1, c2, c3, c4 = st.columns(4)
    metric_card(c1, str(n), "Responses", "Valid survey records")

    if "recycling_awareness" in survey_df.columns:
        avg_aw = pd.to_numeric(survey_df["recycling_awareness"], errors="coerce").mean()
        metric_card(c2, f"{avg_aw:.2f}/5", "Avg Recycling Awareness", "Low = needs campaigns")

    if "visitor_effect" in survey_df.columns:
        vis = pd.to_numeric(survey_df["visitor_effect"], errors="coerce").sum()
        metric_card(c3, f"{vis}/{n}", "Visitor Effect Reported", f"{vis/n*100:.0f}% of respondents")

    if "separation_behaviour" in survey_df.columns:
        never = (pd.to_numeric(survey_df["separation_behaviour"], errors="coerce") == 0).sum()
        metric_card(c4, f"{never}/{n}", "Never Separate Waste", "Segregation gap")

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Descriptive Charts", "📐 Regression Results", "📋 Raw Data"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            styled_header("Recycling Awareness Distribution")
            if "recycling_awareness" in survey_df.columns:
                aw = pd.to_numeric(survey_df["recycling_awareness"], errors="coerce").dropna()
                counts = aw.value_counts().sort_index().reset_index()
                counts.columns = ["Rating","Count"]
                fig = px.bar(counts, x="Rating", y="Count",
                             color_discrete_sequence=[COLORS["rec"]])
                fig.update_traces(marker_cornerradius=6)
                fig.update_layout(**PLOTLY_LAYOUT, height=280)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            styled_header("Waste Scale Distribution")
            if "waste_scale" in survey_df.columns:
                ws = pd.to_numeric(survey_df["waste_scale"], errors="coerce").dropna()
                lmap = {1:"Small",2:"Medium",3:"Large"}
                counts2 = ws.map(lmap).value_counts().reset_index()
                counts2.columns = ["Scale","Count"]
                fig2 = px.pie(counts2, values="Count", names="Scale",
                              color_discrete_sequence=[COLORS["bio"],COLORS["haz"],COLORS["nonbio"]],
                              hole=0.4)
                fig2.update_layout(**PLOTLY_LAYOUT, height=280)
                st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            styled_header("Separation Behaviour")
            if "separation_behaviour" in survey_df.columns:
                sb = pd.to_numeric(survey_df["separation_behaviour"], errors="coerce").dropna()
                lmap2 = {0:"Never",1:"Rarely",2:"Sometimes",3:"Often",4:"Always"}
                counts3 = sb.map(lmap2).value_counts().reset_index()
                counts3.columns = ["Behaviour","Count"]
                fig3 = px.bar(counts3, x="Behaviour", y="Count",
                              color_discrete_sequence=[COLORS["haz"]])
                fig3.update_traces(marker_cornerradius=6)
                fig3.update_layout(**PLOTLY_LAYOUT, height=260)
                st.plotly_chart(fig3, use_container_width=True)

        with col4:
            styled_header("Visitor Effect vs Waste Scale")
            if all(c in survey_df.columns for c in ["visitor_effect","waste_scale"]):
                ve = pd.to_numeric(survey_df["visitor_effect"], errors="coerce")
                ws2 = pd.to_numeric(survey_df["waste_scale"], errors="coerce")
                box_df = pd.DataFrame({"Visitor Effect": ve.map({0:"No Visitors",1:"Has Visitors"}),
                                       "Waste Scale": ws2}).dropna()
                fig4 = px.box(box_df, x="Visitor Effect", y="Waste Scale",
                              color="Visitor Effect",
                              color_discrete_sequence=[COLORS["rec"], COLORS["nonbio"]])
                fig4.update_layout(**PLOTLY_LAYOUT, height=260, showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        if result is None:
            st.warning("Not enough valid data for regression (need ≥ 8 complete rows with all columns).")
            return

        styled_header("Regression Model Performance")
        rc1, rc2, rc3, rc4 = st.columns(4)
        metric_card(rc1, f"{result['r2']:.3f}", "R²", "Variance explained")
        metric_card(rc2, f"{result['adj_r2']:.3f}", "Adjusted R²", "Penalised for predictors")
        metric_card(rc3, f"{result['f_stat']:.3f}", "F-Statistic", f"p = {result['f_pval']:.3f}")
        metric_card(rc4, str(result["n"]), "Observations", "Used in model")

        if result["f_pval"] < 0.05:
            insight("Overall model is statistically significant (F-test p < 0.05).")
        else:
            insight("Overall model not significant — likely due to small sample size. Increase survey responses for a stronger model.", "warn")

        st.markdown("<br>", unsafe_allow_html=True)
        styled_header("Coefficient Table")

        coef_rows = []
        for i, lbl in enumerate(result["labels"]):
            p = result["pval"][i]
            coef_rows.append({
                "Predictor":  lbl,
                "β (coeff)":  f"{result['beta'][i]:+.4f}",
                "Std Error":  f"{result['se'][i]:.4f}",
                "t-stat":     f"{result['tstat'][i]:.3f}",
                "p-value":    f"{p:.4f}",
                "Significant": "✓ Yes" if p < 0.05 else "—",
            })

        coef_df = pd.DataFrame(coef_rows)

        def highlight_sig(row):
            if row["Significant"] == "✓ Yes":
                return ["background-color:#0d2218; color:#48bb78"] * len(row)
            return [""] * len(row)

        st.dataframe(
            coef_df.style.apply(highlight_sig, axis=1),
            use_container_width=True, hide_index=True,
        )

        # Coefficient plot
        styled_header("Coefficient Importance (excluding intercept)")
        coef_plot = pd.DataFrame({
            "Predictor": result["labels"][1:],
            "Beta":      result["beta"][1:],
            "p":         result["pval"][1:],
        }).sort_values("Beta")
        colors_bar = [COLORS["bio"] if v > 0 else COLORS["nonbio"] for v in coef_plot["Beta"]]
        fig5 = go.Figure(go.Bar(
            x=coef_plot["Beta"], y=coef_plot["Predictor"],
            orientation="h", marker_color=colors_bar, marker_line_width=0,
        ))
        fig5.add_vline(x=0, line_color="#4a5568", line_width=1)
        fig5.update_layout(**PLOTLY_LAYOUT, height=320,
                           xaxis_title="β coefficient", yaxis_title="")
        st.plotly_chart(fig5, use_container_width=True)

        # Regression equation
        eq_parts = [f"{result['beta'][0]:.3f}"]
        for i, lbl in enumerate(result["labels"][1:], start=1):
            sign = "+" if result["beta"][i] >= 0 else "−"
            eq_parts.append(f"{sign} {abs(result['beta'][i]):.3f}·{lbl}")
        st.markdown(f"""
        <div style="background:#0d1117; border:1px solid #21262d; border-radius:10px;
                    padding:16px 20px; font-family:'JetBrains Mono',monospace;
                    font-size:0.78rem; color:#a0aec0; margin-top:12px; overflow-x:auto;">
            <span style="color:#718096">Ŷ (waste scale) = </span>
            <span style="color:#e2e8f0">{" ".join(eq_parts)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.download_button("📥 Download Coefficient Table (CSV)",
                           coef_df.to_csv(index=False).encode(),
                           "regression_coefficients.csv", "text/csv")

    with tab3:
        styled_header("Raw Survey Data")
        st.dataframe(survey_df, use_container_width=True, hide_index=True)
        st.download_button("📥 Download Survey Data (CSV)",
                           survey_df.to_csv(index=False).encode(),
                           "survey_data.csv","text/csv")


# ─────────────────────────────────────────────────────────────────
# PAGE: PREDICTOR
# ─────────────────────────────────────────────────────────────────

def page_predictor(survey_df, audit_df):
    st.markdown("## 🔮 Waste Generation Predictor")
    st.markdown(
        '<p style="color:#718096;margin-bottom:24px;">Enter a student or hall profile below '
        'to predict expected waste generation.</p>',
        unsafe_allow_html=True,
    )

    result = run_regression(survey_df) if survey_df is not None else None

    tab1, tab2 = st.tabs(["🎓 Student Profile Predictor", "🏠 Hall-Level Forecast"])

    with tab1:
        styled_header("Student Behaviour Profile")
        c1, c2, c3 = st.columns(3)
        meals   = c1.slider("Meals per day in hostel", 1, 3, 2)
        pkg     = c2.select_slider("Packaged food frequency",
                                   options=["Never (0)","Occasionally (1)","Often (2)"], value="Occasionally (1)")
        pkg_v   = {"Never (0)":0,"Occasionally (1)":1,"Often (2)":2}[pkg]
        disp    = c3.slider("Disposal trips per week", 1, 7, 4)

        c4, c5, c6 = st.columns(3)
        aware   = c4.slider("Recycling awareness (1–5)", 1, 5, 3)
        visitor = c5.radio("Visitors increase your waste?", ["No","Yes"])
        visitor_v = 1 if visitor == "Yes" else 0
        sep     = c6.select_slider("Separation behaviour",
                                   options=["Never(0)","Rarely(1)","Sometimes(2)","Often(3)","Always(4)"],
                                   value="Rarely(1)")
        sep_v   = int(sep[-2])

        st.markdown("<br>", unsafe_allow_html=True)

        if result is not None:
            beta = result["beta"]
            pred = (beta[0] + beta[1]*meals + beta[2]*pkg_v + beta[3]*disp +
                    beta[4]*aware + beta[5]*visitor_v + beta[6]*sep_v)
            pred = float(np.clip(pred, 1.0, 3.0))
            label = "Small" if pred < 1.5 else "Medium" if pred < 2.5 else "Large"
            label_color = COLORS["bio"] if label=="Small" else COLORS["haz"] if label=="Medium" else COLORS["nonbio"]

            # Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred,
                number={"font":{"color":"#e2e8f0","size":36,"family":"JetBrains Mono"}},
                gauge={
                    "axis":       {"range":[1,3],"tickcolor":"#718096","tickwidth":1},
                    "bar":        {"color":label_color,"thickness":0.3},
                    "bgcolor":    "#161b22",
                    "bordercolor":"#21262d",
                    "steps": [
                        {"range":[1,1.5],  "color":"#0d2218"},
                        {"range":[1.5,2.5],"color":"#2d2010"},
                        {"range":[2.5,3],  "color":"#2d1010"},
                    ],
                    "threshold": {"line":{"color":label_color,"width":4},"thickness":0.75,"value":pred},
                },
                title={"text":"Predicted Waste Scale","font":{"color":"#718096","size":13}},
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300,
                                    font_color="#e2e8f0", margin=dict(l=30,r=30,t=30,b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

            rc1, rc2 = st.columns(2)
            rc1.markdown(f"""
            <div class="metric-card" style="border-color:{label_color}">
                <div class="metric-value" style="background:none;-webkit-text-fill-color:{label_color}">
                    {label}
                </div>
                <div class="metric-label">Waste Scale Category</div>
                <div class="metric-sub">Score: {pred:.3f} / 3.000</div>
            </div>
            """, unsafe_allow_html=True)

            contrib = {
                "Meals/day":            beta[1]*meals,
                "Packaged food":        beta[2]*pkg_v,
                "Disposal frequency":   beta[3]*disp,
                "Recycling awareness":  beta[4]*aware,
                "Visitor effect":       beta[5]*visitor_v,
                "Separation behaviour": beta[6]*sep_v,
            }
            contrib_df = pd.DataFrame(list(contrib.items()), columns=["Factor","Contribution"])
            contrib_df = contrib_df.sort_values("Contribution", key=abs, ascending=True)
            fig_c = go.Figure(go.Bar(
                x=contrib_df["Contribution"], y=contrib_df["Factor"],
                orientation="h",
                marker_color=[COLORS["bio"] if v>0 else COLORS["nonbio"] for v in contrib_df["Contribution"]],
                marker_line_width=0,
            ))
            fig_c.add_vline(x=0,line_color="#4a5568",line_width=1)
            fig_c.update_layout(**PLOTLY_LAYOUT, height=260,
                                xaxis_title="Contribution to Ŷ", title="Factor Contributions")
            rc2.plotly_chart(fig_c, use_container_width=True)

        else:
            st.info("Load survey data (or enable sample data) to activate the regression predictor.")

    with tab2:
        styled_header("Hall-Level Weekly Forecast")
        if audit_df is None:
            st.info("Load audit data to enable hall-level forecasting.")
            return

        ana = compute_audit_analytics(audit_df.copy())
        hall_sum = ana["hall_summary"]

        st.markdown("Adjust the expected occupancy and visitor activity to forecast next week's waste.")
        hall_choice = st.selectbox("Select Hall", hall_sum["hall"].tolist())
        row = hall_sum[hall_sum["hall"] == hall_choice].iloc[0]

        fc1, fc2, fc3 = st.columns(3)
        new_pop     = fc1.number_input("Expected population", min_value=1, value=int(row["pop"]), step=5)
        pc_rate     = row["per_capita"] if row["per_capita"] > 0 else 0.3
        days        = fc2.slider("Days to forecast", 1, 14, 7)
        visitor_adj = fc3.slider("Visitor activity multiplier", 0.8, 1.5, 1.0, step=0.05,
                                 help="1.0 = same as sampled week. >1 = more visitors expected.")

        if result:
            visitor_boost = 1.0 + (result["beta"][5] * visitor_adj * 0.1)
        else:
            visitor_boost = visitor_adj

        forecast_total = new_pop * pc_rate * days * visitor_boost

        # Build day-by-day forecast
        base_daily = new_pop * pc_rate * visitor_boost
        day_df = pd.DataFrame({
            "Day": range(1, days+1),
            "Forecast (kg)": [round(base_daily * (1 + 0.04 * max(0, d-4)), 2) for d in range(1, days+1)],
        })

        fa, fb = st.columns(2)
        metric_card(fa, f"{forecast_total:.1f} kg", f"{days}-Day Forecast", f"{hall_choice} hall")
        metric_card(fb, f"{pc_rate:.3f}", "kg/person/day baseline", "From sampled data")

        fig_f = px.bar(day_df, x="Day", y="Forecast (kg)",
                       color_discrete_sequence=[COLORS["bio"]])
        fig_f.update_traces(marker_cornerradius=5)
        fig_f.update_layout(**PLOTLY_LAYOUT, height=300, xaxis=dict(tickmode="linear",dtick=1,**PLOTLY_LAYOUT["xaxis"]))
        st.plotly_chart(fig_f, use_container_width=True)

        insight(f"At current per-capita rate with visitor multiplier {visitor_adj:.1f}×, "
                f"{hall_choice} hall is expected to generate approximately {forecast_total:.1f} kg over {days} days.")
        if visitor_adj > 1.1:
            insight("High visitor activity expected — consider scheduling an extra collection pickup.", "warn")


# ─────────────────────────────────────────────────────────────────
# PAGE: DATA ENTRY
# ─────────────────────────────────────────────────────────────────

def page_data_entry():
    st.markdown("## 📥 Manual Data Entry")
    st.markdown(
        '<p style="color:#718096;margin-bottom:24px;">'
        'Type in records directly. Download the filled template when done.</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["🏗️ Audit Record Entry", "📋 Survey Record Entry"])

    # ── AUDIT ENTRY
    with tab1:
        styled_header("Enter Physical Audit Record")

        if "audit_manual" not in st.session_state:
            st.session_state["audit_manual"] = []

        with st.form("audit_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            hall   = c1.text_input("Hall name", placeholder="e.g. Awo")
            floor  = c2.text_input("Floor / Block", placeholder="e.g. Floor 1")
            date   = c3.date_input("Date")

            c4, c5 = st.columns(2)
            day_num = c4.number_input("Day number (1–7)", min_value=1, max_value=7, value=1)
            pop     = c5.number_input("Population (students on floor/block)", min_value=1, value=40)

            st.markdown("**Waste weights (kg)**")
            w1, w2, w3, w4 = st.columns(4)
            bio    = w1.number_input("Biodegradable kg",     min_value=0.0, step=0.01, format="%.2f")
            nonbio = w2.number_input("Non-biodegradable kg", min_value=0.0, step=0.01, format="%.2f")
            rec    = w3.number_input("Recyclable kg",        min_value=0.0, step=0.01, format="%.2f")
            haz    = w4.number_input("Hazardous kg",         min_value=0.0, step=0.01, format="%.2f")

            submitted = st.form_submit_button("➕ Add Record", use_container_width=True)
            if submitted:
                if not hall:
                    st.error("Hall name is required.")
                else:
                    st.session_state["audit_manual"].append({
                        "hall": hall, "floor_block": floor,
                        "date": str(date), "day_number": int(day_num),
                        "biodegradable_kg": bio, "non_biodegradable_kg": nonbio,
                        "recyclable_kg": rec, "hazardous_kg": haz,
                        "population": int(pop),
                    })
                    st.success(f"Record added! ({len(st.session_state['audit_manual'])} total)")

        if st.session_state["audit_manual"]:
            df_m = pd.DataFrame(st.session_state["audit_manual"])
            st.dataframe(df_m, use_container_width=True, hide_index=True)
            cola, colb = st.columns(2)
            cola.download_button("📥 Download as CSV",
                                 df_m.to_csv(index=False).encode(),
                                 "audit_manual.csv","text/csv",
                                 use_container_width=True)
            colb.download_button("📥 Download as Excel",
                                 to_excel_bytes(df_m),
                                 "audit_manual.xlsx",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 use_container_width=True)
            if st.button("🗑️ Clear all manual records"):
                st.session_state["audit_manual"] = []
                st.rerun()

        # Template download
        st.markdown("---")
        styled_header("Download Empty Templates")
        tc1, tc2 = st.columns(2)
        tc1.download_button("📄 Audit Template (CSV)",
                            empty_audit_df().to_csv(index=False).encode(),
                            "audit_template.csv","text/csv",
                            use_container_width=True)
        tc1.download_button("📄 Audit Template (Excel)",
                            to_excel_bytes(empty_audit_df()),
                            "audit_template.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True)

    # ── SURVEY ENTRY
    with tab2:
        styled_header("Enter Survey Response")

        if "survey_manual" not in st.session_state:
            st.session_state["survey_manual"] = []

        with st.form("survey_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            s_hall  = c1.text_input("Hall", placeholder="e.g. Tedder")
            s_level = c2.selectbox("Academic Level", [100,200,300,400,500])
            s_id    = c3.number_input("Respondent ID", min_value=1,
                                      value=len(st.session_state["survey_manual"])+1)

            c4, c5, c6 = st.columns(3)
            meals2 = c4.selectbox("Meals per day in hostel", [1,2,3])
            pkg2   = c5.selectbox("Packaged food frequency",
                                  [("Never",0),("Occasionally",1),("Often",2)],
                                  format_func=lambda x: x[0])
            disp2  = c6.slider("Disposal trips per week", 1, 7, 4, key="s_disp")

            c7, c8, c9 = st.columns(3)
            aware2   = c7.slider("Recycling awareness (1–5)", 1, 5, 2, key="s_aw")
            visitor2 = c8.radio("Visitors increase waste?", ["No","Yes"], key="s_vis")
            sep2     = c9.select_slider("Separation behaviour",
                                        options=["Never(0)","Rarely(1)","Sometimes(2)","Often(3)","Always(4)"],
                                        key="s_sep")

            waste2 = st.select_slider("Self-reported waste scale",
                                      options=["Small (1)","Medium (2)","Large (3)"])

            submitted2 = st.form_submit_button("➕ Add Response", use_container_width=True)
            if submitted2:
                st.session_state["survey_manual"].append({
                    "respondent_id":              int(s_id),
                    "hall":                       s_hall,
                    "level":                      int(s_level),
                    "meals_per_day":              int(meals2),
                    "packaged_food_frequency":    pkg2[1],
                    "disposal_frequency_per_week":int(disp2),
                    "recycling_awareness":        int(aware2),
                    "visitor_effect":             1 if visitor2=="Yes" else 0,
                    "separation_behaviour":       int(sep2[-2]),
                    "waste_scale":                int(waste2[-2]),
                })
                st.success(f"Response added! ({len(st.session_state['survey_manual'])} total)")

        if st.session_state["survey_manual"]:
            df_s = pd.DataFrame(st.session_state["survey_manual"])
            st.dataframe(df_s, use_container_width=True, hide_index=True)
            sa, sb = st.columns(2)
            sa.download_button("📥 Download as CSV",
                               df_s.to_csv(index=False).encode(),
                               "survey_manual.csv","text/csv",
                               use_container_width=True)
            sb.download_button("📥 Download as Excel",
                               to_excel_bytes(df_s),
                               "survey_manual.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
            if st.button("🗑️ Clear all survey responses"):
                st.session_state["survey_manual"] = []
                st.rerun()

        st.markdown("---")
        tc1b, tc2b = st.columns(2)
        tc1b.download_button("📄 Survey Template (CSV)",
                             empty_survey_df().to_csv(index=False).encode(),
                             "survey_template.csv","text/csv",
                             use_container_width=True)
        tc1b.download_button("📄 Survey Template (Excel)",
                             to_excel_bytes(empty_survey_df()),
                             "survey_template.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             use_container_width=True)


# ─────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────

def load_df(file) -> pd.DataFrame | None:
    if file is None:
        return None
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.sidebar.error(f"Failed to load {file.name}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

def main():
    page, audit_file, survey_file = sidebar()

    # Resolve data sources
    if audit_file:
        audit_df = load_df(audit_file)
    else:
        audit_df = None

    if survey_file:
        survey_df = load_df(survey_file)
    else:
        survey_df = None

    # Merge manual entries if they exist
    if "audit_manual" in st.session_state and st.session_state["audit_manual"]:
        manual_a = pd.DataFrame(st.session_state["audit_manual"])
        audit_df = pd.concat([audit_df, manual_a], ignore_index=True) if audit_df is not None else manual_a

    if "survey_manual" in st.session_state and st.session_state["survey_manual"]:
        manual_s = pd.DataFrame(st.session_state["survey_manual"])
        survey_df = pd.concat([survey_df, manual_s], ignore_index=True) if survey_df is not None else manual_s

    # Route pages
    if page == "🏠 Overview":
        page_overview(audit_df, survey_df)
    elif page == "📊 Audit Analysis":
        page_audit(audit_df)
    elif page == "📋 Survey & Regression":
        page_survey(survey_df)
    elif page == "🔮 Predictor":
        page_predictor(survey_df, audit_df)
    elif page == "📥 Data Entry":
        page_data_entry()


if __name__ == "__main__":
    main()
