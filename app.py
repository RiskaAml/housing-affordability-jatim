import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

st.set_page_config(
    page_title="Keterjangkauan Hunian Jawa Timur",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

custom_css = """
<style>
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1.2rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] {
    display: none !important;
}
div[data-testid="stVerticalBlock"] {
    gap: 0.65rem !important;
}
[data-testid="stAlert"], .red-bubble {
    text-align: justify !important;
}
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}
div[data-baseweb="popover"] ul {
    background-color: #1e1e2e !important;
    color: white !important;
}
div[data-baseweb="popover"] li {
    color: white !important;
}
[data-testid="stDataFrame"], [data-testid="stDataFrame"] div[data-testid="stTable"] {
    background-color: #000000 !important;
}
[data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
    background-color: #000000 !important;
    color: white !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
}
div.stButton > button {
    background-color: #483D8B !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 15px !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background-color: #6A5ACD !important;
}
[data-testid="stMetric"], div[data-testid="metric-container"] {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    padding: 15px !important;
}
.year-pills { display: flex; gap: 3px; align-items: center; }
.year-pill {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 20px; padding: 3px 9px;
    font-size: 10px; font-weight: 600;
    color: rgba(255,255,255,0.55);
    cursor: pointer; transition: all 0.15s;
    user-select: none; line-height: 1.5;
}
.year-pill:hover {
    background: rgba(151,125,255,0.18);
    border-color: rgba(151,125,255,0.40);
    color: rgba(255,255,255,0.85);
}
.year-pill.active {
    background: linear-gradient(135deg, rgba(151,125,255,0.45), rgba(0,51,255,0.35));
    border-color: rgba(151,125,255,0.60);
    color: #ffffff; font-weight: 700;
    box-shadow: 0 1px 6px rgba(151,125,255,0.25);
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

bg_b64 = get_base64_image("background2.jpg")
bg_css = ""
if bg_b64:
    bg_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: fixed;
        inset: 0;
        background: rgba(15, 10, 40, 0.82);
        z-index: 0;
        pointer-events: none;
    }}
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {{
  --bg-deep:    #0A0818;
  --bg-card:    rgba(255,255,255,0.10);
  --border:     rgba(255,255,255,0.15);
  --border2:    rgba(255,255,255,0.25);
  --accent-p:   #977DFF;
  --accent-b:   #0033FF;
  --text-main:  #FFFFFF;
  --text-sub:   rgba(255,255,255,0.80);
  --text-muted: rgba(255,255,255,0.50);
  --green:      #00E5A0;
  --red:        #FF4D6D;
  --gold:       #FFD166;
  --purple-dark1: #7C6FE0;
  --purple-dark2: #4B3F8F;
  --purple-dark3: #2D2467;
  --radius:     12px;
  --radius-sm:  8px;
}}

* {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}

{bg_css}

[data-testid="stAppViewContainer"] > section > div {{
    position: relative; z-index: 1;
}}
[data-testid="stMain"] {{ background: transparent !important; }}
[data-testid="block-container"] {{
    padding: 0.6rem 1.5rem 1.6rem 1.5rem !important;
    max-width: 1600px;
}}

[data-testid="stToolbar"],
header[data-testid="stHeader"],
#MainMenu, footer,
.stDeployButton,
[data-testid="stAppDeployButton"],
[data-testid="stStatusWidget"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
}}

.main .block-container {{
    padding-top: 0.4rem !important;
    margin-top: 0 !important;
}}

/* ── Collapse gap dari radio year filter di home ── */
.home-year-filter {{
    margin-top: -10px !important;
    margin-bottom: -4px !important;
    padding-bottom: 0 !important;
}}
.home-year-filter [data-testid="stVerticalBlock"] {{
    gap: 0 !important;
}}
/* Hilangkan padding bawah bawaan radio di home */
.home-year-filter [data-testid="stRadio"] {{
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}}
.home-year-filter .element-container {{
    margin-bottom: 0 !important;
}}

/* ── KPI Cards ── */
.kpi-grid {{ display: grid; grid-template-columns: repeat(5,1fr); gap: 10px; margin-bottom: 12px; }}
.kpi-card {{
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: var(--radius);
    padding: 15px 17px;
    position: relative; overflow: hidden;
    transition: transform 0.2s;
}}
.kpi-card:hover {{ transform: translateY(-2px); border-color: var(--border2); }}
.kpi-card::before {{
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
}}
.kpi-card.purple::before {{ background: linear-gradient(90deg, #6C5DD3, var(--purple-dark2)); }}
.kpi-card.green::before  {{ background: linear-gradient(90deg, #6C5DD3, var(--purple-dark2)); }}
.kpi-card.red::before    {{ background: linear-gradient(90deg, var(--purple-dark2), var(--purple-dark3)); }}
.kpi-card.gold::before   {{ background: linear-gradient(90deg, var(--purple-dark2), var(--purple-dark3)); }}
.kpi-card.blue::before   {{ background: linear-gradient(90deg, #5B4B9E, var(--purple-dark3)); }}
.kpi-card.pink::before   {{ background: linear-gradient(90deg, #F2E6EE, #977DFF); }}
.kpi-glow {{
    position: absolute; width: 70px; height: 70px;
    border-radius: 50%; opacity: 0.12; top: -15px; right: -15px; filter: blur(18px);
}}
.kpi-card.purple .kpi-glow {{ background: #6C5DD3; }}
.kpi-card.green .kpi-glow  {{ background: #6C5DD3; }}
.kpi-card.red .kpi-glow    {{ background: var(--purple-dark2); }}
.kpi-card.gold .kpi-glow   {{ background: var(--purple-dark2); }}
.kpi-card.blue .kpi-glow   {{ background: #5B4B9E; }}
.kpi-card.pink .kpi-glow   {{ background: #F2E6EE; }}
.kpi-label {{ font-size: 9px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.55); margin-bottom: 5px; }}
.kpi-value {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #FFFFFF; line-height: 1.1; margin-bottom: 3px; }}
.kpi-sub   {{ font-size: 10px; color: rgba(255,255,255,0.50); }}

/* ── Section titles ── */
.sec-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12.5px; font-weight: 700; color: #FFFFFF;
    padding-left: 8px; margin: 4px 0 10px 0;
    border-left: 3px solid var(--accent-p);
}}
.sec-insight {{
    background: rgba(255,255,255,0.08); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.14); border-radius: var(--radius-sm);
    padding: 12px 16px; font-size: 11.5px; color: rgba(255,255,255,0.80);
    margin-top: 10px; line-height: 1.7;
}}

/* ── Card-style containers ── */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: var(--radius) !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
    transition: border-color 0.2s;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: var(--border2) !important;
}}

/* ── Dashboard header ── */
.dash-header {{
    background: linear-gradient(135deg, rgba(151,125,255,0.15), rgba(0,51,255,0.12), rgba(242,230,238,0.06));
    border: 1px solid rgba(151,125,255,0.25);
    border-radius: var(--radius); padding: 16px 22px; margin-bottom: 6px;
    position: relative; overflow: hidden; backdrop-filter: blur(16px);
}}
.dash-header::after {{
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 130px; height: 130px;
    background: radial-gradient(circle, rgba(151,125,255,0.18), transparent 70%);
    border-radius: 50%;
}}
.dash-header h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px; font-weight: 800; color: white; margin: 0 0 4px 0; letter-spacing: -0.3px;
}}
.dash-header p {{ font-size: 11.5px; color: rgba(255,255,255,0.65); margin: 0; }}

/* ── Page header ── */
.page-header {{
    display: flex; align-items: center; gap: 10px;
    padding: 11px 16px; margin-bottom: 10px;
    background: rgba(151,125,255,0.12);
    border: 1px solid rgba(151,125,255,0.20);
    border-radius: var(--radius); backdrop-filter: blur(12px);
}}
.page-header-icon {{ font-size: 20px; line-height: 1; }}
.page-header-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 800; color: white; }}
.page-header-sub   {{ font-size: 11px; color: rgba(255,255,255,0.55); }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 3px; background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important; margin-bottom: 12px;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: var(--radius-sm) !important;
    color: rgba(255,255,255,0.62) !important;
    font-weight: 500; font-size: 12px;
    border: none !important; padding: 6px 13px !important;
    transition: all 0.2s;
}}
.stTabs [data-baseweb="tab"]:hover {{ background: rgba(255,255,255,0.06) !important; color: white !important; }}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #977DFF, #0033FF) !important;
    color: white !important; font-weight: 700 !important;
    box-shadow: 0 3px 12px rgba(151,125,255,0.28) !important;
}}

/* ── Result boxes ── */
.result-ok {{
    border-radius: var(--radius); padding: 18px 22px; margin-top: 12px; text-align: center;
    background: linear-gradient(135deg, rgba(0,229,160,0.14), rgba(0,184,148,0.09));
    border: 1px solid rgba(0,229,160,0.28);
}}
.result-stress {{
    border-radius: var(--radius); padding: 18px 22px; margin-top: 12px; text-align: center;
    background: linear-gradient(135deg, rgba(255,77,109,0.14), rgba(214,48,49,0.09));
    border: 1px solid rgba(255,77,109,0.28);
}}
.result-ok h2    {{ color: #00E5A0; font-size: 18px; margin: 0 0 6px 0; }}
.result-stress h2 {{ color: #FF4D6D; font-size: 18px; margin: 0 0 6px 0; }}
.result-ok p, .result-stress p {{ color: rgba(255,255,255,0.80); font-size: 12.5px; margin: 0; }}

/* ── Formula box ── */
.formula-box {{
    background: rgba(0,51,255,0.10);
    border: 1px solid rgba(0,51,255,0.22);
    border-left: 4px solid var(--accent-b);
    border-radius: var(--radius-sm); padding: 14px 20px;
    font-size: 12px; color: rgba(255,255,255,0.88);
    font-weight: 500; line-height: 2;
    font-family: 'Space Grotesk', monospace;
}}

/* ── Glossary ── */
.gloss-box {{
    background: rgba(255,255,255,0.07); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: var(--radius-sm);
    padding: 10px 14px; margin-bottom: 8px;
    transition: border-color 0.2s;
}}
.gloss-box:hover {{ border-color: rgba(151,125,255,0.35); }}
.gloss-term {{ font-size: 12px; font-weight: 700; color: #977DFF; }}
.gloss-def  {{ font-size: 11px; color: rgba(255,255,255,0.72); line-height: 1.6; margin-top: 3px; }}

/* ── Divider ── */
.dash-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(151,125,255,0.22), transparent);
    margin: 8px 0;
}}

/* ── Nav menu cards ── */
.nav-card {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: var(--radius);
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
    backdrop-filter: blur(10px);
    height: 100%;
}}
.nav-card:hover {{
    background: rgba(151,125,255,0.15);
    border-color: rgba(151,125,255,0.35);
    transform: translateY(-2px);
}}
.nav-card-icon {{ font-size: 22px; margin-bottom: 6px; }}
.nav-card-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px; font-weight: 700; color: white; margin-bottom: 3px;
}}
.nav-card-desc {{ font-size: 10.5px; color: rgba(255,255,255,0.45); line-height: 1.4; }}

/* Force nav buttons */
div[data-testid="stHorizontalBlock"] .stButton > button {{
    height: 48px !important;
    min-height: 48px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    padding: 0 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 11.5px !important;
    background: linear-gradient(135deg, #5B45C8, #3B2FA8) !important;
    border: 1px solid rgba(151,125,255,0.55) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(91,69,200,0.35) !important;
}}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
    background: linear-gradient(135deg, #7C60E8, #5040C8) !important;
    border-color: rgba(151,125,255,0.80) !important;
    box-shadow: 0 4px 16px rgba(124,96,232,0.50) !important;
    transform: translateY(-2px) !important;
}}

/* ── Metric cards ── */
.metric-card {{
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: var(--radius-sm);
    padding: 14px 16px;
    text-align: center;
}}
.metric-label {{ font-size: 9px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.50); margin-bottom: 6px; }}
.metric-value {{ font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 700; color: white; }}
.metric-delta {{ font-size: 10px; margin-top: 4px; }}

/* ── Streamlit overrides ── */
.stMetric {{
    background: rgba(255,255,255,0.09) !important;
    border-radius: var(--radius-sm) !important;
    padding: 12px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
}}
.stMetric label {{ color: rgba(255,255,255,0.55) !important; font-size: 10px !important; text-transform: uppercase; letter-spacing: 0.8px; }}
.stMetric [data-testid="stMetricValue"] {{ color: white !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 18px !important; }}
.stMetric [data-testid="stMetricDelta"] {{ font-size: 11px !important; }}

/* All buttons */
.stButton > button {{
    background: rgba(255,255,255,0.09) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 12.5px !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
    padding: 0.6rem 1rem !important;
}}
.stButton > button:hover {{
    background: rgba(151,125,255,0.18) !important;
    border-color: rgba(151,125,255,0.40) !important;
    transform: translateY(-1px) !important;
}}

/* Primary button */
[data-testid="stMainBlockContainer"] button[kind="primary"],
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #977DFF, #0033FF) !important;
    border: none !important;
    box-shadow: 0 3px 12px rgba(151,125,255,0.30) !important;
}}

/* Number input */
.stNumberInput input,
.stNumberInput > div,
.stNumberInput > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] > div {{
    background: #111111 !important;
    background-color: #111111 !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    border-radius: 8px !important;
    color: white !important;
}}
.stNumberInput [data-testid="stNumberInputStepDown"],
.stNumberInput [data-testid="stNumberInputStepUp"] {{
    background: #222222 !important;
    color: white !important;
}}

/* Selectbox */
.stSelectbox > div > div,
[data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    border-radius: 8px !important;
}}
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] input,
[data-testid="stSelectbox"] span {{
    color: white !important;
    background: transparent !important;
}}
[data-baseweb="menu"],
[data-baseweb="menu"] ul {{
    background: #1a1436 !important;
}}
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"] {{
    color: rgba(255,255,255,0.85) !important;
    background: transparent !important;
}}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover {{
    background: rgba(151,125,255,0.18) !important;
    color: white !important;
}}

/* Download button */
[data-testid="stDownloadButton"] > button {{
    background: rgba(255,255,255,0.09) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important; border-radius: 8px !important; font-weight: 600 !important;
}}

/* Dataframe - aggressive black background */
.stDataFrame, [data-testid="stDataFrameResizable"],
.stDataFrame > div, [data-testid="stDataFrameResizable"] > div,
.stDataFrame iframe, [data-testid="stDataFrameResizable"] iframe,
[data-testid="stDataFrame"], [data-testid="stDataFrame"] > div,
[data-testid="stDataFrame"] > div > div,
[data-testid="stDataFrame"] > div > div > div {{
    background: #0a0a0a !important;
    background-color: #0a0a0a !important;
}}
[data-testid="stDataFrame"] thead tr th,
[data-testid="stDataFrame"] th {{
    background: rgba(151,125,255,0.25) !important;
    background-color: rgba(151,125,255,0.25) !important;
    color: white !important;
}}
[data-testid="stDataFrame"] tbody tr td,
[data-testid="stDataFrame"] td {{
    background: #0a0a0a !important;
    background-color: #0a0a0a !important;
    color: rgba(255,255,255,0.85) !important;
}}
[data-testid="stDataFrame"] tbody tr:hover td {{
    background: rgba(151,125,255,0.15) !important;
}}

/* General text */
p, li {{ color: rgba(255,255,255,0.80) !important; }}
h1, h2, h3, h4 {{ color: white !important; }}
.stCaption {{ color: rgba(255,255,255,0.48) !important; font-size: 10.5px !important; }}
.stInfo {{
    background: rgba(0,51,255,0.10) !important;
    border: 1px solid rgba(0,51,255,0.25) !important;
    border-radius: var(--radius-sm) !important;
}}
.stInfo p {{ color: rgba(255,255,255,0.88) !important; }}

.element-container {{ margin-bottom: 6px !important; }}
label {{ color: rgba(255,255,255,0.65) !important; font-size: 11px !important; }}

/* Hide year-filter hidden buttons row */
.hidden-year-row {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; position: absolute !important; left: -9999px !important; }}

/* ── Kompres gap radio year di homepage ── */
[data-testid="stRadio"] > div {{
    gap: 2px !important;
}}
/* Wrapper kolom radio di home — tarik ke atas */
.year-radio-wrap {{
    margin-top: -8px !important;
    margin-bottom: 2px !important;
}}
/* Hapus padding bawaan div.element-container yang nge-wrap radio */
.year-radio-wrap .element-container {{
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}}
</style>
""", unsafe_allow_html=True)


# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    FILE = "ANALISIS_KETERJANGKAUAN_KPR.xlsx"
    xl   = pd.read_excel(FILE, sheet_name=None, engine="openpyxl")

    df = xl["union"].copy()
    df = df[df.iloc[:,0].notna()].iloc[:, :8]
    df.columns = ["TAHUN","KABUPATEN_KOTA","UMK","BATAS_30",
                  "CICILAN","GARIS_KEMISKINAN","STATUS_LAJANG","STATUS_KELUARGA"]
    for col in ["UMK","CICILAN","GARIS_KEMISKINAN"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["TAHUN"]    = df["TAHUN"].astype(int)
    df["BATAS_30"] = df["UMK"] * 0.3
    df["RESIDUAL"] = df["UMK"] - df["CICILAN"] - df["GARIS_KEMISKINAN"]
    df["STATUS_LAJANG"] = df.apply(
        lambda r: "Terjangkau"
        if (r["CICILAN"] <= r["BATAS_30"]) and (r["RESIDUAL"] >= 0)
        else "Tidak Terjangkau", axis=1)
    df["STATUS_KELUARGA"] = df.apply(
        lambda r: "Terjangkau"
        if (r["CICILAN"] <= r["BATAS_30"]) and (r["RESIDUAL"] >= r["GARIS_KEMISKINAN"]*2)
        else "Tidak Terjangkau", axis=1)
    df = df.dropna(subset=["UMK"])
    df["KABUPATEN_KOTA"] = df["KABUPATEN_KOTA"].astype(str).str.strip().str.upper()

    ihpr = xl["IHPR SBY"].copy()
    ihpr.columns = ["TAHUN","TRIWULAN","TIPE_KECIL","TIPE_MENENGAH","TIPE_BESAR","TOTAL"]
    ihpr["TAHUN"] = ihpr["TAHUN"].ffill()
    ihpr = ihpr.dropna(subset=["TRIWULAN"])
    ihpr["TAHUN_INT"] = ihpr["TAHUN"].astype(float).astype(int)
    ihpr["PERIODE"]   = ihpr["TAHUN_INT"].astype(str) + " Q" + ihpr["TRIWULAN"].astype(str)
    for c in ["TIPE_KECIL","TIPE_MENENGAH","TIPE_BESAR","TOTAL"]:
        ihpr[c] = pd.to_numeric(ihpr[c], errors="coerce")

    gk = xl["garis kemiskinan"].copy().iloc[:,:6]
    gk.columns = ["PERIODE","GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]
    gk = gk[gk["PERIODE"].notna()]
    gk = gk[~gk["PERIODE"].astype(str).str.lower().str.startswith("tahun")]
    for c in ["GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]:
        gk[c] = pd.to_numeric(
            gk[c].astype(str).str.replace(",","").str.replace("-","0").str.strip(),
            errors="coerce")
    gk = gk[gk["PERIODE"].astype(str).str.contains("202", na=False)].dropna(subset=["GK_KOTA"])

    kp = xl["kepemilikan rumah"].copy()
    kp.columns = ["KAB_KOTA","MILIK","KONTRAK","LAINNYA","TOTAL"]
    kp = kp[kp["KAB_KOTA"].notna()]
    skip = ["kabupaten/kota","catatan","jumlah","jawa timur"]
    kp = kp[~kp["KAB_KOTA"].astype(str).str.lower().str[:10].isin(skip)]
    for c in ["MILIK","KONTRAK","LAINNYA"]:
        kp[c] = pd.to_numeric(
            kp[c].astype(str).str.replace("–","0").str.replace(",",""),
            errors="coerce").fillna(0)
    kp["KAB_KOTA_UPPER"] = kp["KAB_KOTA"].astype(str).str.upper().str.strip()

    return df, ihpr, gk, kp

main_df, ihpr_df, gk_df, kp_df = load_data()
KAB_LIST = sorted(main_df["KABUPATEN_KOTA"].unique().tolist())
YEARS    = [2020, 2021, 2022, 2023, 2024, 2025]
COLORS   = ["#977DFF","#00E5A0","#FFD166","#FF6B9D","#38BDF8","#F2E6EE"]

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(255,255,255,0.82)", family="Inter, sans-serif", size=11),
    xaxis=dict(showgrid=False, color="rgba(255,255,255,0.55)",
               linecolor="rgba(255,255,255,0.12)", tickcolor="rgba(255,255,255,0.3)"),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)",
               color="rgba(255,255,255,0.55)", linecolor="rgba(255,255,255,0.12)"),
    legend=dict(bgcolor="rgba(20,15,50,0.80)", bordercolor="rgba(255,255,255,0.18)",
                borderwidth=1, font=dict(size=11, color="rgba(255,255,255,0.90)")),
    margin=dict(l=10, r=10, t=30, b=10),
)

# ─── Session state ────────────────────────────────────────────────────────────
if "active_page" not in st.session_state:
    st.session_state.active_page = -1
if "home_year" not in st.session_state:
    st.session_state.home_year = 2025

pages = [
    ("Status & Proporsi",  "Distribusi keterjangkauan per daerah"),
    ("UMK vs Cicilan",     "Gap UMK vs beban KPR FLPP"),
    ("Tren UMK",           "Perkembangan UMK 2020–2025"),
    ("IHPR Properti",      "Indeks harga properti Surabaya"),
    ("Sosial Ekonomi",     "Kemiskinan & kepemilikan rumah"),
    ("Cek Kemampuan",      "Simulasi affordability personal"),
    ("Data & Glosarium",   "Tabel lengkap & definisi"),
]

page = st.session_state.active_page

def render_filter(page_idx, default_year=2025, default_kab="Semua"):
    fc1, fc2 = st.columns([1, 2])
    with fc1:
        sel_year = st.selectbox("Tahun", YEARS,
            index=YEARS.index(default_year), key=f"sy_{page_idx}")
    with fc2:
        sel_kab = st.selectbox("Kabupaten / Kota", ["Semua"] + KAB_LIST,
            key=f"sk_{page_idx}")
    return sel_year, sel_kab

def back_button():
    if st.button("← Kembali", key="back_btn"):
        st.session_state.active_page = -1
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == -1:

    sel_home_year = st.session_state.home_year

    # ── Header ──
    st.markdown(f"""
    <div class='dash-header'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px;'>
        <div>
          <h1>Dashboard Keterjangkauan Hunian Jawa Timur</h1>
        </div>
        <div style='display:flex;gap:5px;flex-wrap:wrap;align-items:center;'>
          <div style='background:rgba(0,229,160,0.14);border:1px solid rgba(0,229,160,0.30);
               border-radius:20px;padding:3px 10px;font-size:9.5px;font-weight:700;color:#00E5A0;'>2020–2025</div>
          <div style='background:rgba(151,125,255,0.14);border:1px solid rgba(151,125,255,0.30);
               border-radius:20px;padding:3px 10px;font-size:9.5px;font-weight:700;color:#977DFF;'>38 Kab/Kota</div>
        </div>
      </div>
      <div style='display:flex;justify-content:space-between;align-items:flex-end;margin-top:8px;flex-wrap:wrap;gap:6px;'>
        <p>UMK vs KPR FLPP · Metode <em>The 30% Rule</em> &amp; <em>Residual Income</em> · 38 Kabupaten/Kota · 2020–2025</p>
        <span style='font-size:9px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:rgba(255,255,255,0.40);'>FILTER TAHUN ↓</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Radio pill tahun — langsung rapat di bawah header ──
    # Wrap dalam div CSS khusus untuk kompres gap
    st.markdown("<div class='year-radio-wrap'>", unsafe_allow_html=True)
    _c_left, _c_right = st.columns([1, 2])
    with _c_right:
        sel_home_year = st.radio(
            "Tahun",
            options=YEARS,
            index=YEARS.index(st.session_state.home_year),
            horizontal=True,
            key="home_year_radio",
            label_visibility="collapsed",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if sel_home_year != st.session_state.home_year:
        st.session_state.home_year = sel_home_year
        st.rerun()

    # ── Hitung data KPI berdasarkan tahun terpilih ──
    df_home = main_df[main_df["TAHUN"] == sel_home_year].copy()
    n_ok    = (df_home["STATUS_LAJANG"] == "Terjangkau").sum()
    n_no    = (df_home["STATUS_LAJANG"] == "Tidak Terjangkau").sum()
    total   = len(df_home)
    pct_ok  = round(n_ok / total * 100, 1) if total else 0
    umk_med = int(df_home["UMK"].median()) if not df_home.empty else 0
    cicilan_home = int(df_home["CICILAN"].iloc[0]) if not df_home.empty else 0

    # ── KPI Cards ──
    k1, k2, k3, k4, k5 = st.columns(5)
    cards = [
        (k1, "green",  f"TERJANGKAU {sel_home_year}",      str(n_ok),                     f"dari {total} daerah"),
        (k2, "red",    f"HOUSING STRESS {sel_home_year}",   str(n_no),                     "cicilan > 30% UMK"),
        (k3, "purple", "% HOUSING STRESS",                  f"{round(100-pct_ok,1)}%",     "daerah tidak aman"),
        (k4, "gold",   f"CICILAN KPR FLPP {sel_home_year}", f"Rp {cicilan_home/1e6:.2f}jt","per bulan"),
        (k5, "blue",   f"MEDIAN UMK {sel_home_year}",       f"Rp {umk_med/1e6:.2f}jt",    "se-Jawa Timur"),
    ]
    for col, color, label, value, sub in cards:
        with col:
            st.markdown(f"""
            <div class='kpi-card {color}'>
              <div class='kpi-glow'></div>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value'>{value}</div>
              <div class='kpi-sub'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='dash-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10.5px;font-weight:700;color:rgba(255,255,255,0.40);letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px;'>Menu Analisis</div>", unsafe_allow_html=True)

    hidden_cols = st.columns(7, gap="small")
    nav_clicked = [-1]
    for col, (idx, label_raw) in zip(hidden_cols, [
        (0,"Status & Proporsi"),(1,"UMK vs Cicilan"),(2,"Tren UMK"),
        (3,"IHPR Properti"),(4,"Sosial Ekonomi"),(5,"Cek Kemampuan"),(6,"Data & Glosarium")]):
        with col:
            if st.button(label_raw, key=f"qnav_{idx}", use_container_width=True):
                nav_clicked[0] = idx

    if nav_clicked[0] >= 0:
        st.session_state.active_page = nav_clicked[0]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — STATUS & PROPORSI
# ══════════════════════════════════════════════════════════════════════════════
elif page == 0:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>Status & Proporsi</div>
      <div class='page-header-sub'>Distribusi keterjangkauan KPR FLPP per kabupaten/kota</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(0)
    is_single = sel_kab != "Semua"
    df_year = main_df[main_df["TAHUN"] == sel_year].copy()
    df_focus = df_year[df_year["KABUPATEN_KOTA"] == sel_kab] if is_single else df_year
    df_trend_focus = main_df[main_df["KABUPATEN_KOTA"] == sel_kab] if is_single else main_df

    n_ok  = (df_year["STATUS_LAJANG"] == "Terjangkau").sum()
    n_no  = (df_year["STATUS_LAJANG"] == "Tidak Terjangkau").sum()
    total = len(df_year)
    pct_ok = round(n_ok / total * 100, 1) if total else 0

    if is_single:
        hist = df_trend_focus[["TAHUN","UMK","CICILAN","BATAS_30","RESIDUAL","STATUS_LAJANG"]].copy()
        st.markdown('<div class="sec-title">Ringkasan per Tahun</div>', unsafe_allow_html=True)
        tbl_hist = hist.copy()
        tbl_hist.columns = ["Tahun","UMK","Cicilan","Batas 30%","Residual","Status"]
        tbl_hist["% Cicilan"] = (tbl_hist["Cicilan"]/tbl_hist["UMK"]*100).round(1).astype(str)+"%"

        def clr(v):
            if v == "Terjangkau": return "background:rgba(0,229,160,0.18);color:#00E5A0;font-weight:700"
            return "background:rgba(255,77,109,0.18);color:#FF4D6D;font-weight:700"

        # Render sebagai HTML table agar background bisa dikontrol
        fmt_tbl = tbl_hist.copy()
        fmt_tbl["UMK"]      = fmt_tbl["UMK"].apply(lambda v: f"Rp {v:,.0f}")
        fmt_tbl["Cicilan"]  = fmt_tbl["Cicilan"].apply(lambda v: f"Rp {v:,.0f}")
        fmt_tbl["Batas 30%"]= fmt_tbl["Batas 30%"].apply(lambda v: f"Rp {v:,.0f}")
        fmt_tbl["Residual"] = fmt_tbl["Residual"].apply(lambda v: f"Rp {v:,.0f}")

        rows_html = ""
        for _, row in fmt_tbl.iterrows():
            status_style = ("background:rgba(0,229,160,0.20);color:#00E5A0;font-weight:700"
                            if row["Status"]=="Terjangkau"
                            else "background:rgba(255,77,109,0.20);color:#FF4D6D;font-weight:700")
            rows_html += f"""<tr>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['Tahun']}</td>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['UMK']}</td>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['Cicilan']}</td>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['Batas 30%']}</td>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['Residual']}</td>
              <td style='{status_style};padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);text-align:center;border-radius:4px;'>{row['Status']}</td>
              <td style='background:#0a0a0a;color:rgba(255,255,255,0.85);padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.07);'>{row['% Cicilan']}</td>
            </tr>"""
        st.markdown(f"""
        <div style='overflow-x:auto;border-radius:8px;border:1px solid rgba(255,255,255,0.12);'>
        <table style='width:100%;border-collapse:collapse;background:#0a0a0a;'>
          <thead><tr>
            {''.join(f"<th style='background:rgba(151,125,255,0.25);color:white;padding:8px 10px;font-size:11px;font-weight:700;text-align:left;border-bottom:1px solid rgba(255,255,255,0.15);'>{c}</th>" for c in fmt_tbl.columns)}
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table></div>
        """, unsafe_allow_html=True)

        n_aman_hist = (hist["STATUS_LAJANG"]=="Terjangkau").sum()
        st.markdown(f"""<div class="sec-insight">
          <b>{sel_kab.title()}</b> terjangkau di <b>{n_aman_hist} dari {len(hist)} tahun</b>.
          % cicilan terhadap UMK: <b>{round(hist['CICILAN'].iloc[0]/hist['UMK'].iloc[0]*100,1)}%</b> (2020) →
          <b>{round(hist['CICILAN'].iloc[-1]/hist['UMK'].iloc[-1]*100,1)}%</b> ({sel_year}).
        </div>""", unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown(f'<div class="sec-title">Proporsi Keterjangkauan {sel_year}</div>', unsafe_allow_html=True)
                fig = go.Figure(go.Pie(
                    labels=["Terjangkau","Housing Stress"], values=[n_ok, n_no],
                    hole=0.62,
                    marker=dict(colors=["#00E5A0","#FF4D6D"], line=dict(color="rgba(0,0,0,0)", width=0)),
                    textinfo="label+percent", textfont=dict(size=12, color="white"),
                    hovertemplate="<b>%{label}</b><br>%{value} daerah (%{percent})<extra></extra>"))
                fig.update_layout(height=300,
                    annotations=[dict(
                        text=f"<b>{n_no}</b><br><span style='font-size:10px;'>Housing<br>Stress</span>",
                        x=0.5, y=0.5, font_size=18, showarrow=False, font_color="white")],
                    showlegend=False, **PLOT_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f"""<div class="sec-insight">
                  Tahun <b>{sel_year}</b>: <b>{n_ok} dari 38 daerah</b> ({pct_ok}%) terjangkau.
                  <b>{n_no} daerah</b> ({round(100-pct_ok,1)}%) housing stress.
                </div>""", unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.markdown('<div class="sec-title">Tren 2020–2025 — Seluruh Jawa Timur</div>', unsafe_allow_html=True)
                yc = []
                for y in YEARS:
                    dy = main_df[main_df["TAHUN"]==y]
                    yc.append({"Tahun": y,
                        "Terjangkau": (dy["STATUS_LAJANG"]=="Terjangkau").sum(),
                        "Housing Stress": (dy["STATUS_LAJANG"]=="Tidak Terjangkau").sum()})
                yc_df = pd.DataFrame(yc)
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=yc_df["Tahun"], y=yc_df["Terjangkau"],
                    name="Terjangkau", marker_color="#00E5A0", marker_line_width=0,
                    hovertemplate="<b>Terjangkau</b><br>%{x}: %{y} daerah<extra></extra>"))
                fig2.add_trace(go.Bar(x=yc_df["Tahun"], y=yc_df["Housing Stress"],
                    name="Housing Stress", marker_color="#FF4D6D", marker_line_width=0,
                    hovertemplate="<b>Housing Stress</b><br>%{x}: %{y} daerah<extra></extra>"))
                fig2.update_layout(height=300, barmode="stack",
                    xaxis=dict(tickmode="linear", **PLOT_LAYOUT["xaxis"]),
                    yaxis=dict(title="Jumlah Daerah", **PLOT_LAYOUT["yaxis"]),
                    **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis"]})
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown("""<div class="sec-insight">
                  Stagnansi absolut: jumlah daerah terjangkau tidak berubah signifikan.
                  Kenaikan UMK tahunan tidak cukup menggeser daerah dari bawah ambang keterjangkauan.
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — UMK VS CICILAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == 1:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>UMK vs Cicilan KPR FLPP</div>
      <div class='page-header-sub'>Perbandingan beban cicilan terhadap upah minimum per daerah</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(1)
    is_single = sel_kab != "Semua"
    df_year = main_df[main_df["TAHUN"] == sel_year].copy()
    df_focus = df_year[df_year["KABUPATEN_KOTA"] == sel_kab] if is_single else df_year
    cicilan = int(df_year["CICILAN"].iloc[0]) if not df_year.empty else 0

    if is_single and not df_focus.empty:
        kab_umk_val = float(df_focus["UMK"].iloc[0])
        kab_pct_cic = round(cicilan / kab_umk_val * 100, 1)
        kab_ok      = cicilan <= kab_umk_val * 0.3
        color_stat  = "#00E5A0" if kab_ok else "#FF4D6D"
        bg_stat     = "rgba(0,229,160,0.09)" if kab_ok else "rgba(255,77,109,0.09)"
        border_stat = "rgba(0,229,160,0.28)" if kab_ok else "rgba(255,77,109,0.28)"
        verdict = "TERJANGKAU" if kab_ok else "HOUSING STRESS"
        st.markdown(f"""
        <div style='background:{bg_stat};border:1px solid {border_stat};
             border-left:4px solid {color_stat};border-radius:10px;
             padding:14px 20px;margin-bottom:14px;
             display:flex;align-items:center;gap:18px;flex-wrap:wrap;backdrop-filter:blur(8px);'>
          <div>
            <div style='font-size:9px;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:1px;font-weight:700;'>Daerah Dipilih</div>
            <div style='font-size:15px;font-weight:800;color:white;'>{sel_kab.title()}</div>
            <div style='font-size:12px;font-weight:800;color:{color_stat};'>{verdict}</div>
          </div>
          <div style='border-left:1px solid rgba(255,255,255,0.12);padding-left:16px;'>
            <div style='font-size:9px;color:rgba(255,255,255,0.50);'>UMK {sel_year}</div>
            <div style='font-size:13px;font-weight:700;color:white;'>Rp {kab_umk_val:,.0f}</div>
          </div>
          <div style='border-left:1px solid rgba(255,255,255,0.12);padding-left:16px;'>
            <div style='font-size:9px;color:rgba(255,255,255,0.50);'>Cicilan KPR FLPP</div>
            <div style='font-size:13px;font-weight:700;color:white;'>Rp {cicilan:,}</div>
          </div>
          <div style='border-left:1px solid rgba(255,255,255,0.12);padding-left:16px;'>
            <div style='font-size:9px;color:rgba(255,255,255,0.50);'>% Cicilan dari UMK</div>
            <div style='font-size:24px;font-weight:900;color:{color_stat};line-height:1;'>{kab_pct_cic}%</div>
            <div style='font-size:9px;color:rgba(255,255,255,0.45);'>batas aman ≤ 30%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f'<div class="sec-title">UMK vs Cicilan KPR FLPP — Semua Kab/Kota ({sel_year})</div>', unsafe_allow_html=True)

        # Sort: Tidak Terjangkau dulu (UMK kecil→besar), lalu Terjangkau (UMK kecil→besar)
        # Karena horizontal bar chart plotly menampilkan dari bawah ke atas,
        # kita taruh Terjangkau di index awal agar muncul di BAWAH, Tidak Terjangkau di atas
        # Tapi user minta Terjangkau di ATAS → sort Terjangkau terakhir (index tinggi = atas di chart)
        df_no_sort = df_year[df_year["STATUS_LAJANG"]!="Terjangkau"].sort_values("UMK", ascending=True)
        df_ok_sort = df_year[df_year["STATUS_LAJANG"]=="Terjangkau"].sort_values("UMK", ascending=True)
        df_s = pd.concat([df_no_sort, df_ok_sort], ignore_index=True)
        df_s["LABEL"] = df_s["KABUPATEN_KOTA"].str.replace("KABUPATEN ","KAB. ")
        def get_color(row):
            if is_single and row["KABUPATEN_KOTA"] == sel_kab: return "#FFD166"
            return "#00E5A0" if row["STATUS_LAJANG"]=="Terjangkau" else "#FF4D6D"
        df_s["COLOR"]   = df_s.apply(get_color, axis=1)
        df_s["BATAS30"] = df_s["UMK"] * 0.3

        # Urutan kategori Y: list dari bawah ke atas
        category_order = df_s["LABEL"].tolist()

        fig3 = go.Figure()

        # Trace tunggal UMK dengan warna per bar
        fig3.add_trace(go.Bar(
            y=df_s["LABEL"], x=df_s["UMK"], orientation="h",
            name="UMK",
            marker=dict(color=df_s["COLOR"].tolist(), line=dict(width=0)),
            text=df_s["UMK"].apply(lambda x: f"Rp {x/1e6:.2f}jt"),
            textposition="outside", textfont=dict(size=9, color="rgba(255,255,255,0.60)"),
            hovertemplate="<b>%{y}</b><br>UMK: Rp %{x:,.0f}<extra></extra>",
            showlegend=False))

        # Legend dummy untuk Terjangkau & Tidak Terjangkau
        fig3.add_trace(go.Bar(
            y=[None], x=[None], orientation="h", name="Terjangkau",
            marker=dict(color="#00E5A0"), showlegend=True))
        fig3.add_trace(go.Bar(
            y=[None], x=[None], orientation="h", name="Tidak Terjangkau",
            marker=dict(color="#FF4D6D"), showlegend=True))

        # Batas 30%
        fig3.add_trace(go.Bar(
            y=df_s["LABEL"], x=df_s["BATAS30"], orientation="h", name="Batas 30% Gaji",
            marker=dict(color="rgba(151,125,255,0.55)", line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>30% UMK: Rp %{x:,.0f}<extra></extra>"))

        if is_single:
            df_sel = df_s[df_s["KABUPATEN_KOTA"]==sel_kab]
            if not df_sel.empty:
                fig3.add_trace(go.Bar(
                    y=df_sel["LABEL"], x=df_sel["UMK"], orientation="h", name="Daerah Dipilih",
                    marker=dict(color="#FFD166", line=dict(width=0)),
                    text=df_sel["UMK"].apply(lambda x: f"Rp {x/1e6:.2f}jt"),
                    textposition="outside", textfont=dict(size=9, color="rgba(255,255,255,0.60)"),
                    hovertemplate="<b>%{y}</b><br>UMK: Rp %{x:,.0f}<extra></extra>"))

        fig3.add_vline(x=cicilan, line_dash="dash", line_color="#FFD166", line_width=2,
            annotation_text=f"  KPR Rp {cicilan/1e6:.2f}jt",
            annotation_font_color="#FFD166", annotation_position="top")

        fig3.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines",
            name=f"Cicilan KPR FLPP (Rp {cicilan/1e6:.2f}jt)",
            line=dict(color="#FFD166", width=2, dash="dash"), showlegend=True))

        fig3.update_layout(height=1000, barmode="overlay", showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                font=dict(size=11, color="white"), bgcolor="rgba(20,15,50,0.80)",
                bordercolor="rgba(255,255,255,0.18)", borderwidth=1, traceorder="normal"),
            margin=dict(l=10, r=160, t=60, b=10),
            xaxis=dict(title="UMK (Rp)", tickformat=",", **PLOT_LAYOUT["xaxis"]),
            yaxis=dict(
                tickfont=dict(size=9.5, color="rgba(255,255,255,0.80)"),
                categoryorder="array",
                categoryarray=category_order,
                **{k: v for k, v in PLOT_LAYOUT["yaxis"].items() if k != "categoryorder"}),
            **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","margin","legend"]})
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TREN UMK
# ══════════════════════════════════════════════════════════════════════════════
elif page == 2:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>Tren UMK 2020–2025</div>
      <div class='page-header-sub'>Perkembangan upah minimum vs cicilan KPR dan batas 30%</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(2)
    is_single = sel_kab != "Semua"
    df_year = main_df[main_df["TAHUN"] == sel_year].copy()
    df_focus = df_year[df_year["KABUPATEN_KOTA"] == sel_kab] if is_single else df_year
    cicilan = int(df_year["CICILAN"].iloc[0]) if not df_year.empty else 0

    if is_single:
        kabs_show = [sel_kab]
    else:
        kabs_show = df_year.nlargest(5,"UMK")["KABUPATEN_KOTA"].tolist()

    with st.container(border=True):
        trend  = main_df[main_df["KABUPATEN_KOTA"].isin(kabs_show)].copy()
        cic_yr = main_df.groupby("TAHUN")["CICILAN"].first().reset_index()

        fig4 = go.Figure()
        for i, kab in enumerate(kabs_show):
            d   = trend[trend["KABUPATEN_KOTA"]==kab].sort_values("TAHUN")
            lbl = kab.replace("KABUPATEN ","KAB. ")
            c   = COLORS[i % len(COLORS)]
            fig4.add_trace(go.Scatter(x=d["TAHUN"], y=d["UMK"],
                name=f"UMK {lbl}", mode="lines+markers",
                line=dict(color=c, width=2.5),
                marker=dict(size=7, color=c, line=dict(color="rgba(255,255,255,0.4)", width=1.5)),
                hovertemplate=f"<b>UMK {lbl}</b><br>%{{x}}: Rp %{{y:,.0f}}<extra></extra>"))
            fig4.add_trace(go.Scatter(x=d["TAHUN"], y=d["BATAS_30"],
                name=f"30% UMK {lbl}", mode="lines+markers",
                line=dict(color=c, width=1.5), marker=dict(size=5, color=c), opacity=0.50,
                hovertemplate=f"<b>30% UMK {lbl}</b><br>%{{x}}: Rp %{{y:,.0f}}<extra></extra>"))

        fig4.add_trace(go.Scatter(x=cic_yr["TAHUN"], y=cic_yr["CICILAN"],
            mode="lines+markers", name="Cicilan KPR FLPP",
            line=dict(color="#FFD166", width=2.5),
            marker=dict(symbol="diamond", size=8, color="#FFD166"),
            hovertemplate="Cicilan KPR FLPP<br>%{x}: Rp %{y:,.0f}<extra></extra>"))

        fig4.update_layout(height=480,
            xaxis=dict(tickmode="linear", title="Tahun", **PLOT_LAYOUT["xaxis"]),
            yaxis=dict(title="Rp", tickformat=",", **PLOT_LAYOUT["yaxis"]),
            legend=dict(bgcolor="rgba(20,15,50,0.80)", bordercolor="rgba(255,255,255,0.18)",
                        borderwidth=1, font=dict(size=11, color="white"),
                        orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
            **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","legend"]})
        st.plotly_chart(fig4, use_container_width=True)

        if is_single and not df_focus.empty:
            umk_2020   = main_df[(main_df["KABUPATEN_KOTA"]==sel_kab)&(main_df["TAHUN"]==2020)]["UMK"].iloc[0]
            umk_last   = main_df[(main_df["KABUPATEN_KOTA"]==sel_kab)&(main_df["TAHUN"]==sel_year)]["UMK"].iloc[0]
            growth     = round((umk_last/umk_2020-1)*100,1)
            cic_2020   = main_df[main_df["TAHUN"]==2020]["CICILAN"].iloc[0]
            cic_last   = main_df[main_df["TAHUN"]==sel_year]["CICILAN"].iloc[0]
            cic_growth = round((cic_last/cic_2020-1)*100,1)
            umk_sel    = float(df_focus["UMK"].iloc[0])
            pct_sel    = round(cicilan/umk_sel*100,1)
            ok_sel     = cicilan <= umk_sel*0.3
            trend_lbl  = "mereda" if growth > cic_growth else "makin tertekan"
            trend_color = "#00E5A0" if growth > cic_growth else "#FF4D6D"

            st.markdown(f"""<div class="sec-insight">
              <b>Tren 2020–{sel_year}:</b> UMK naik <b>{growth}%</b> vs Cicilan KPR naik <b>{cic_growth}%</b>
              → Keterjangkauan <span style='color:{trend_color};font-weight:700;'>{trend_lbl}</span>.<br>
              Tahun {sel_year}: cicilan = <b>{pct_sel}%</b> dari UMK —
              {'di bawah ambang 30%, terjangkau.' if ok_sel else 'melampaui batas 30%, housing stress.'}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="sec-insight">
              <b>Cara membaca:</b> Garis UMK per daerah (solid) vs 30% UMK (tipis) vs Cicilan KPR FLPP (emas).
              Jika garis UMK di atas garis cicilan → terjangkau. Ditampilkan 5 daerah UMK tertinggi.
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — IHPR PROPERTI
# ══════════════════════════════════════════════════════════════════════════════
elif page == 3:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>IHPR Properti Surabaya</div>
      <div class='page-header-sub'>Indeks Harga Properti Residensial (2018=100)</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(3)

    with st.container(border=True):
        st.markdown('<div class="sec-title">Indeks Harga Properti Residensial Surabaya (2018=100)</div>', unsafe_allow_html=True)

        ihpr_colors = {
            "TIPE_KECIL":   "#977DFF",
            "TIPE_MENENGAH":"#00E5A0",
            "TIPE_BESAR":   "#FFD166",
            "TOTAL":        "#FF6B9D"
        }
        ihpr_names = {
            "TIPE_KECIL":"Tipe Kecil",
            "TIPE_MENENGAH":"Tipe Menengah",
            "TIPE_BESAR":"Tipe Besar",
            "TOTAL":"Total Surabaya"
        }

        fig5 = go.Figure()
        for col, color in ihpr_colors.items():
            fig5.add_trace(go.Scatter(
                x=ihpr_df["PERIODE"], y=ihpr_df[col],
                name=ihpr_names[col], mode="lines+markers",
                line=dict(width=2.5, color=color), marker=dict(size=5, color=color),
                hovertemplate=f"<b>{ihpr_names[col]}</b><br>%{{x}}: %{{y:.2f}}<extra></extra>"))

        mark_periods = ihpr_df[ihpr_df["TAHUN_INT"]==sel_year]["PERIODE"].tolist()
        for mp in mark_periods:
            fig5.add_vline(x=mp, line_color="rgba(151,125,255,0.35)", line_width=1.5)

        fig5.update_layout(height=420,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), **PLOT_LAYOUT["xaxis"]),
            yaxis=dict(title="Indeks (2018=100)", **PLOT_LAYOUT["yaxis"]),
            legend=dict(bgcolor="rgba(20,15,50,0.80)", bordercolor="rgba(255,255,255,0.18)",
                        borderwidth=1, font=dict(size=12, color="white"),
                        orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
            **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","legend"]})
        st.plotly_chart(fig5, use_container_width=True)

        ihpr_sel = ihpr_df[ihpr_df["TAHUN_INT"]==sel_year]
        avg_k    = ihpr_sel["TIPE_KECIL"].mean() if not ihpr_sel.empty else 0
        st.markdown(f"""<div class="sec-insight">
          <b>Tahun {sel_year} — Tipe Kecil:</b> rata-rata indeks <b>{avg_k:.2f}</b>
          → harga naik <b>{avg_k-100:.1f}%</b> sejak 2018.
          Tipe kecil cenderung naik lebih cepat karena permintaan tinggi dari pencari hunian pertama.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SOSIAL EKONOMI
# ══════════════════════════════════════════════════════════════════════════════
elif page == 4:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>Sosial Ekonomi</div>
      <div class='page-header-sub'>Kepemilikan rumah & tren kemiskinan Jawa Timur</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(4)
    is_single = sel_kab != "Semua"

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown(f'<div class="sec-title">Kepemilikan Rumah{" — "+sel_kab.title() if is_single else " — Jawa Timur"}</div>', unsafe_allow_html=True)
            if is_single:
                kab_clean = sel_kab.replace("KABUPATEN ","").replace("KOTA ","").title()
                kp_f = kp_df[kp_df["KAB_KOTA"].str.contains(kab_clean, case=False, na=False)]
                if not kp_f.empty:
                    row_kp   = kp_f.iloc[0]
                    total_kp = row_kp["MILIK"] + row_kp["KONTRAK"] + row_kp["LAINNYA"]
                    fig_kp = go.Figure(go.Pie(
                        labels=["Milik Sendiri","Kontrak/Sewa","Lainnya"],
                        values=[row_kp["MILIK"], row_kp["KONTRAK"], row_kp["LAINNYA"]],
                        hole=0.55,
                        marker=dict(colors=["#00E5A0","#FF4D6D","#FFD166"],
                                    line=dict(color="rgba(0,0,0,0)", width=0)),
                        textinfo="label+percent", textfont=dict(size=12, color="white")))
                    pct_milik = round(row_kp["MILIK"]/total_kp*100,1) if total_kp>0 else 0
                    fig_kp.update_layout(height=320, showlegend=False,
                        annotations=[dict(
                            text=f"<b>{pct_milik}%</b><br><span style='font-size:10px;'>Milik</span>",
                            x=0.5, y=0.5, font_size=16, showarrow=False, font_color="white")],
                        **PLOT_LAYOUT)
                    st.plotly_chart(fig_kp, use_container_width=True)
                    st.markdown(f"""<div class="sec-insight">
                      Di <b>{sel_kab.title()}</b>, <b>{pct_milik}%</b> rumah tangga memiliki hunian sendiri.
                    </div>""", unsafe_allow_html=True)
                else:
                    st.info(f"Data kepemilikan untuk {sel_kab.title()} tidak tersedia.")
            else:
                kp_plot = kp_df[~kp_df["KAB_KOTA"].str.upper().str.strip().isin(["JAWA TIMUR"])].copy()
                kp_plot = kp_plot[kp_plot["MILIK"] + kp_plot["KONTRAK"] + kp_plot["LAINNYA"] > 0].copy()
                kp_plot["TOTAL_ALL"] = kp_plot["MILIK"] + kp_plot["KONTRAK"] + kp_plot["LAINNYA"]
                kp_plot = kp_plot.sort_values("TOTAL_ALL", ascending=True)
                kp_plot["LABEL"] = kp_plot["KAB_KOTA"].astype(str).str.title().str.replace("Kabupaten ","Kab. ")

                fig6 = go.Figure()
                fig6.add_trace(go.Bar(
                    y=kp_plot["LABEL"], x=kp_plot["MILIK"], name="Milik Sendiri", orientation="h",
                    marker=dict(color="#00E5A0", line=dict(width=0)),
                    hovertemplate="<b>%{y}</b><br>Milik: %{x:,.0f}<extra></extra>"))
                fig6.add_trace(go.Bar(
                    y=kp_plot["LABEL"], x=kp_plot["KONTRAK"], name="Kontrak/Sewa", orientation="h",
                    marker=dict(color="#FF4D6D", line=dict(width=0)),
                    hovertemplate="<b>%{y}</b><br>Kontrak: %{x:,.0f}<extra></extra>"))
                fig6.add_trace(go.Bar(
                    y=kp_plot["LABEL"], x=kp_plot["LAINNYA"], name="Lainnya", orientation="h",
                    marker=dict(color="#FFD166", line=dict(width=0)),
                    hovertemplate="<b>%{y}</b><br>Lainnya: %{x:,.0f}<extra></extra>"))

                n_kab = len(kp_plot)
                bar_height = max(500, n_kab * 18)

                fig6.update_layout(
                    height=bar_height, barmode="stack", showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
                        font=dict(size=11, color="white"), bgcolor="rgba(20,15,50,0.80)",
                        bordercolor="rgba(255,255,255,0.18)", borderwidth=1),
                    margin=dict(l=10, r=20, t=50, b=10),
                    xaxis=dict(title="Jumlah Rumah Tangga", tickformat=",", **PLOT_LAYOUT["xaxis"]),
                    yaxis=dict(tickfont=dict(size=9, color="rgba(255,255,255,0.80)"), **PLOT_LAYOUT["yaxis"]),
                    **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","margin","legend"]})
                st.plotly_chart(fig6, use_container_width=True)
                st.markdown("""<div class="sec-insight">
                  <b>Data BPS 2022.</b> Mayoritas rumah tangga Jawa Timur sudah memiliki hunian sendiri —
                  namun ini tidak menjawab apakah generasi baru mampu membeli hunian baru.
                </div>""", unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown('<div class="sec-title">Tren Garis Kemiskinan Jawa Timur</div>', unsafe_allow_html=True)
            fig7 = go.Figure()
            fig7.add_trace(go.Scatter(x=gk_df["PERIODE"], y=gk_df["GK_KOTA"],
                name="Perkotaan", mode="lines+markers",
                line=dict(color="#977DFF", width=2.5), marker=dict(size=6),
                hovertemplate="Kota<br>%{x}<br>Rp %{y:,.0f}<extra></extra>"))
            fig7.add_trace(go.Scatter(x=gk_df["PERIODE"], y=gk_df["GK_DESA"],
                name="Perdesaan", mode="lines+markers",
                line=dict(color="#00E5A0", width=2.5), marker=dict(size=6),
                hovertemplate="Desa<br>%{x}<br>Rp %{y:,.0f}<extra></extra>"))
            gk_sel = gk_df[gk_df["PERIODE"].astype(str).str.contains(str(sel_year))]
            for _, rr in gk_sel.iterrows():
                fig7.add_vline(x=rr["PERIODE"], line_color="rgba(255,209,102,0.40)", line_width=2)
            fig7.update_layout(height=230,
                xaxis=dict(tickangle=-30, tickfont=dict(size=9), **PLOT_LAYOUT["xaxis"]),
                yaxis=dict(title="Rp/kapita/bln", tickformat=",", **PLOT_LAYOUT["yaxis"]),
                legend=dict(bgcolor="rgba(20,15,50,0.80)", font=dict(size=12, color="white"),
                            bordercolor="rgba(255,255,255,0.18)", borderwidth=1),
                **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","legend"]})
            st.plotly_chart(fig7, use_container_width=True)

            st.markdown('<div class="sec-title">Penduduk Miskin (ribu jiwa)</div>', unsafe_allow_html=True)
            fig8 = go.Figure()
            fig8.add_trace(go.Scatter(
                x=gk_df["PERIODE"], y=gk_df["TOTAL_MISKIN"],
                fill="tozeroy", fillcolor="rgba(255,77,109,0.12)",
                line=dict(color="#FF4D6D", width=2), mode="lines",
                hovertemplate="%{x}<br>%{y:,.0f} ribu jiwa<extra></extra>"))
            fig8.update_layout(height=200,
                xaxis=dict(tickangle=-30, tickfont=dict(size=9), **PLOT_LAYOUT["xaxis"]),
                yaxis=dict(title="ribu jiwa", **PLOT_LAYOUT["yaxis"]),
                showlegend=False,
                **{k: v for k, v in PLOT_LAYOUT.items() if k not in ["xaxis","yaxis","showlegend"]})
            st.plotly_chart(fig8, use_container_width=True)
            st.markdown(f"""<div class="sec-insight">
              <b>Kemiskinan:</b> Garis kemiskinan terus naik — biaya hidup minimum makin mahal.
              Bersamaan dengan cicilan KPR yang juga naik, pekerja terjepit dari dua arah.
              Garis kuning vertikal = periode tahun {sel_year} yang dipilih.
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CEK KEMAMPUAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == 5:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>Cek Kemampuan</div>
      <div class='page-header-sub'>Simulasi affordability personal berdasarkan gaji dan daerah</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(5)
    is_single = sel_kab != "Semua"

    with st.container(border=True):
        ck1, ck2, ck3, ck4 = st.columns([3, 2, 2, 1])
        with ck1:
            user_gaji = st.number_input("Penghasilan Bulanan (Rp)",
                min_value=0, max_value=50_000_000, value=3_000_000, step=100_000, format="%d")
        with ck2:
            default_idx = KAB_LIST.index(sel_kab) if is_single and sel_kab in KAB_LIST else 0
            user_kab = st.selectbox("Daerah", KAB_LIST, index=default_idx, key="kk")
        with ck3:
            user_year = st.selectbox("Tahun", YEARS, index=YEARS.index(sel_year), key="ky")
        with ck4:
            st.markdown("<div style='height:26px;'></div>", unsafe_allow_html=True)
            hitung = st.button("Hitung", type="primary", use_container_width=True)

        if hitung:
            row = main_df[(main_df["KABUPATEN_KOTA"]==user_kab)&(main_df["TAHUN"]==user_year)]
            if not row.empty:
                cic_val  = float(row["CICILAN"].iloc[0])
                umk_val  = float(row["UMK"].iloc[0])
                gk_val   = float(row["GARIS_KEMISKINAN"].iloc[0])
                batas_30 = user_gaji * 0.3
                pct_g    = (cic_val / user_gaji * 100) if user_gaji > 0 else 0
                sisa     = user_gaji - cic_val
                cond1    = cic_val <= batas_30
                cond2    = sisa >= gk_val
                is_aman  = cond1 and cond2
                gaji_min = cic_val / 0.3

                r1, r2, r3, r4 = st.columns(4)
                metrics = [
                    (r1, "Gaji Kamu",         f"Rp {user_gaji:,.0f}", None, None),
                    (r2, "Cicilan KPR FLPP",  f"Rp {cic_val:,.0f}",  None, None),
                    (r3, "Batas Aman (30%)",  f"Rp {batas_30:,.0f}", None, None),
                    (r4, "% Gaji ke Cicilan", f"{pct_g:.1f}%",
                        "Aman" if cond1 else "Melewati batas",
                        "#00E5A0" if cond1 else "#FF4D6D"),
                ]
                for col, label, value, delta, dcolor in metrics:
                    with col:
                        dc = f"color:{dcolor};font-weight:700;" if dcolor else ""
                        st.markdown(f"""
                        <div class='metric-card'>
                          <div class='metric-label'>{label}</div>
                          <div class='metric-value'>{value}</div>
                          {"<div class='metric-delta' style='" + dc + "'>" + delta + "</div>" if delta else ""}
                        </div>
                        """, unsafe_allow_html=True)

                if is_aman:
                    st.markdown(f"""<div class="result-ok">
                      <h2>Terjangkau</h2>
                      <p>Dengan gaji <b>Rp {user_gaji:,.0f}</b> di <b>{user_kab.title()}</b> tahun {user_year},
                      cicilan KPR hanya memakan <b>{pct_g:.1f}%</b> penghasilanmu.
                      Sisa setelah cicilan: <b>Rp {sisa:,.0f}/bulan</b>.</p>
                    </div>""", unsafe_allow_html=True)
                else:
                    alasan = []
                    if not cond1: alasan.append(f"cicilan ({pct_g:.1f}%) melampaui batas 30%")
                    if not cond2: alasan.append(f"sisa Rp {sisa:,.0f} kurang dari GK Rp {gk_val:,.0f}")
                    st.markdown(f"""<div class="result-stress">
                      <h2>Housing Stress</h2>
                      <p>Tidak terjangkau: <b>{' dan '.join(alasan)}</b>.<br>
                      Gaji minimum agar terjangkau: <b>Rp {gaji_min:,.0f}/bulan</b>.</p>
                    </div>""", unsafe_allow_html=True)

                st.markdown(f"""<div class="sec-insight">
                  <b>Konteks {user_kab.title()} {user_year}</b><br>
                  · UMK resmi: <b>Rp {umk_val:,.0f}/bulan</b><br>
                  · Garis Kemiskinan: <b>Rp {gk_val:,.0f}/kapita/bulan</b><br>
                  · Gaji minimum agar terjangkau: <b>Rp {gaji_min:,.0f}/bulan</b><br>
                  · {'Gajimu di atas UMK' if user_gaji >= umk_val else f'Gajimu di bawah UMK (selisih Rp {umk_val-user_gaji:,.0f})'}
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — DATA & GLOSARIUM
# ══════════════════════════════════════════════════════════════════════════════
elif page == 6:
    back_button()
    st.markdown("""<div class='page-header'>
      <div class='page-header-icon'>&#9642;</div>
      <div><div class='page-header-title'>Data & Glosarium</div>
      <div class='page-header-sub'>Tabel data lengkap dan referensi istilah</div></div>
    </div>""", unsafe_allow_html=True)

    sel_year, sel_kab = render_filter(6)
    is_single = sel_kab != "Semua"
    df_year = main_df[main_df["TAHUN"] == sel_year].copy()

    sub1, sub2 = st.tabs(["Tabel Data", "Glosarium & Metodologi"])

    with sub1:
        st.markdown(f'<div class="sec-title">Data Keterjangkauan Lengkap — {sel_year}</div>', unsafe_allow_html=True)
        tbl = df_year[["KABUPATEN_KOTA","UMK","BATAS_30","CICILAN",
                       "GARIS_KEMISKINAN","RESIDUAL","STATUS_LAJANG","STATUS_KELUARGA"]].copy()
        tbl.columns = ["Kabupaten/Kota","UMK (Rp)","Batas 30% (Rp)","Cicilan KPR (Rp)",
                       "Garis Kemiskinan","Residual Income","Status Lajang","Status Kel. Kecil"]
        tbl.index = range(1, len(tbl)+1)

        def style_row(row):
            is_sel = is_single and row["Kabupaten/Kota"] == sel_kab
            base = ["background:rgba(255,209,102,0.12);font-weight:600"]*len(row) if is_sel else [""]*len(row)
            for i, col in enumerate(row.index):
                if col in ["Status Lajang","Status Kel. Kecil"]:
                    if row[col] == "Terjangkau":
                        base[i] = "background:rgba(0,229,160,0.18);color:#00E5A0;font-weight:700"
                    elif row[col] == "Tidak Terjangkau":
                        base[i] = "background:rgba(255,77,109,0.18);color:#FF4D6D;font-weight:700"
            return base

        # Format kolom angka
        fmt6 = tbl.copy()
        for col in ["UMK (Rp)","Batas 30% (Rp)","Cicilan KPR (Rp)","Garis Kemiskinan","Residual Income"]:
            fmt6[col] = fmt6[col].apply(lambda v: f"Rp {v:,.0f}")

        def status_style(val):
            if val == "Terjangkau":    return "background:rgba(0,229,160,0.20);color:#00E5A0;font-weight:700"
            if val == "Tidak Terjangkau": return "background:rgba(255,77,109,0.20);color:#FF4D6D;font-weight:700"
            return ""

        rows6 = ""
        for idx, row in fmt6.iterrows():
            is_sel = is_single and row["Kabupaten/Kota"] == sel_kab
            row_bg = "background:rgba(255,209,102,0.10);" if is_sel else "background:#0a0a0a;"
            cells = ""
            for col in fmt6.columns:
                val = row[col]
                if col in ["Status Lajang","Status Kel. Kecil"]:
                    cell_style = status_style(val) + ";padding:5px 8px;border-bottom:1px solid rgba(255,255,255,0.07);font-size:11px;text-align:center;"
                else:
                    cell_style = row_bg + "color:rgba(255,255,255,0.85);padding:5px 8px;border-bottom:1px solid rgba(255,255,255,0.07);font-size:11px;"
                cells += f"<td style='{cell_style}'>{val}</td>"
            rows6 += f"<tr>{cells}</tr>"

        header6 = "".join(f"<th style='background:rgba(151,125,255,0.25);color:white;padding:7px 8px;font-size:10.5px;font-weight:700;text-align:left;border-bottom:1px solid rgba(255,255,255,0.15);white-space:nowrap;'>{c}</th>" for c in fmt6.columns)
        st.markdown(f"""
        <div style='overflow:auto;max-height:500px;border-radius:8px;border:1px solid rgba(255,255,255,0.12);'>
        <table style='width:100%;border-collapse:collapse;background:#0a0a0a;'>
          <thead style='position:sticky;top:0;z-index:1;'><tr>{header6}</tr></thead>
          <tbody>{rows6}</tbody>
        </table></div>
        """, unsafe_allow_html=True)

        if is_single:
            st.caption(f"Baris kuning = {sel_kab.title()} (daerah dipilih)")

        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        _, dl_right = st.columns([5, 1])
        with dl_right:
            csv = tbl.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download CSV", csv,
                f"keterjangkauan_jatim_{sel_year}.csv", "text/csv",
                use_container_width=True)

    with sub2:
        st.markdown('<div class="sec-title">Glosarium Istilah Utama</div>', unsafe_allow_html=True)
        glossary = [
            ("UMK — Upah Minimum Kabupaten/Kota",
             "Batas upah minimum yang wajib dibayar pengusaha kepada pekerja baru (<1 tahun). Ditetapkan Gubernur tiap tahun. Disparitas besar: Surabaya Rp 4,96 juta vs Sampang Rp 2,34 juta (2025)."),
            ("KPR FLPP — Fasilitas Likuiditas Pembiayaan Perumahan",
             "Kredit rumah bersubsidi pemerintah: bunga tetap 5%/tahun, tenor ≤20 tahun, DP minimal 1%. Cicilan lebih rendah dari KPR komersial karena ada subsidi likuiditas APBN."),
            ("The 30% Rule",
             "Standar internasional: pengeluaran hunian tidak boleh melebihi 30% penghasilan bruto bulanan. Jika melebihi → Housing Stress."),
            ("Housing Stress",
             "Kondisi cicilan KPR >30% penghasilan. Sebuah daerah Housing Stress jika cicilan FLPP melampaui 30% UMK-nya."),
            ("Residual Income",
             "Sisa pendapatan setelah cicilan KPR dan Garis Kemiskinan. Formula: UMK − Cicilan − GK. Terjangkau hanya jika Residual ≥ 0 DAN cicilan ≤ 30% UMK."),
            ("IHPR — Indeks Harga Properti Residensial",
             "Indeks Bank Indonesia untuk kecepatan kenaikan harga properti. Dasar 2018=100. Indeks 111 → harga naik 11% sejak 2018."),
            ("Garis Kemiskinan",
             "Pengeluaran minimum per kapita/bulan untuk kebutuhan dasar (BPS). Dipakai sebagai proksi biaya hidup minimum dalam formula Residual Income."),
        ]
        for term, defn in glossary:
            st.markdown(f"""<div class="gloss-box">
              <div class="gloss-term">{term}</div>
              <div class="gloss-def">{defn}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title" style="margin-top:12px;">Metodologi Perhitungan</div>', unsafe_allow_html=True)
        st.markdown("""<div class="formula-box">
          Batas 30% = UMK × 30%<br>
          Residual Income = UMK − Cicilan KPR − Garis Kemiskinan<br>
          Status Lajang = "Terjangkau" jika Cicilan ≤ Batas 30% <b>DAN</b> Residual Income ≥ 0<br>
          Status Kel. Kecil = "Terjangkau" jika Cicilan ≤ Batas 30% <b>DAN</b> Residual Income ≥ 2×GK
        </div>""", unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;margin-top:24px;padding:10px 18px;
     background:linear-gradient(135deg,rgba(151,125,255,0.10),rgba(0,51,255,0.07));
     border:1px solid rgba(151,125,255,0.16);
     border-radius:10px;backdrop-filter:blur(8px);'>
  <div style='font-family:Space Grotesk,sans-serif;font-size:11.5px;font-weight:700;
       background:linear-gradient(135deg,#F2E6EE,#977DFF,#0033FF);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:2px;'>
    Dashboard Keterjangkauan Hunian Jawa Timur 2020–2025
  </div>
  <div style='font-size:9.5px;color:rgba(255,255,255,0.38);'>
    SK UMK Gubernur Jatim · SHPR Bank Indonesia · BPS – Jawa Timur Dalam Angka 2025 · Kementerian PUPR
  </div>
</div>
""", unsafe_allow_html=True)