import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Keterjangkauan Hunian Jawa Timur",
    page_icon="🏠", layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #F7F5FF; }

[data-testid="stSidebar"] { background: linear-gradient(180deg,#2D2B55 0%,#4A3F9F 100%); }
[data-testid="stSidebar"] *:not([data-baseweb="select"] *):not(input) { color:#FFFFFF !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color:#2D2B55 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background-color:#EDE9FF !important; }
[data-testid="stSidebar"] input { color:#2D2B55 !important; background-color:#EDE9FF !important; }
[data-testid="stSidebar"] .stSelectbox svg { fill:#2D2B55 !important; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,0.2) !important; }

.kpi-card { background:white; border-radius:14px; padding:18px 20px;
    box-shadow:0 2px 16px rgba(108,92,231,0.10); border-top:4px solid #6C5CE7; margin-bottom:8px; }
.kpi-card.green { border-top-color:#00B894; }
.kpi-card.red   { border-top-color:#D63031; }
.kpi-card.pink  { border-top-color:#E84393; }
.kpi-card.gold  { border-top-color:#FDCB6E; }
.kpi-card.blue  { border-top-color:#0984E3; }
.kpi-label { font-size:11px; color:#888; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
.kpi-value { font-size:26px; font-weight:800; color:#2D2B55; line-height:1.2; margin:4px 0; }
.kpi-sub   { font-size:12px; color:#aaa; }

.sec-title { font-size:16px; font-weight:700; color:#2D2B55;
    border-left:4px solid #6C5CE7; padding-left:10px; margin:18px 0 6px 0; }
.sec-q { background:linear-gradient(135deg,#EDE9FF,#F7F5FF); border-radius:10px;
    padding:12px 16px; font-size:14px; color:#4A3F9F; font-weight:600;
    margin-bottom:10px; border-left:3px solid #6C5CE7; }
.sec-insight { background:white; border-radius:10px; padding:14px 18px;
    font-size:13px; color:#555; margin-top:8px; border:1px solid #EDE9FF; line-height:1.75; }
.formula-box { background:#EEF2FA; border-radius:10px; padding:16px 22px;
    border-left:5px solid #4472C4; margin:12px 0; font-size:14px;
    color:#1F3864; font-weight:600; line-height:2; }
.mode-badge { display:inline-block; padding:4px 14px; border-radius:20px;
    font-size:12px; font-weight:700; margin-bottom:10px; }
.mode-all  { background:#EDE9FF; color:#4A3F9F; }
.mode-kab  { background:#D4EDDA; color:#155724; }

.result-ok { border-radius:14px; padding:20px 24px; margin-top:16px; text-align:center;
    background:linear-gradient(135deg,#00B894,#00CEC9); }
.result-stress { border-radius:14px; padding:20px 24px; margin-top:16px; text-align:center;
    background:linear-gradient(135deg,#D63031,#E84393); }
.result-ok h2, .result-stress h2 { color:white; font-size:22px; margin:0 0 8px 0; }
.result-ok p,  .result-stress p  { color:rgba(255,255,255,0.9); font-size:14px; margin:0; }

.stTabs [data-baseweb="tab-list"] { gap:6px; background:transparent; }
.stTabs [data-baseweb="tab"] { background:white; border-radius:8px 8px 0 0;
    color:#4A3F9F !important; font-weight:600; font-size:13px;
    border:1px solid #EDE9FF; border-bottom:none; padding:8px 14px; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#6C5CE7,#A29BFE) !important;
    color:white !important; border-color:transparent !important; }

.gloss-box { background:white; border-radius:12px; padding:16px 20px;
    border:1px solid #EDE9FF; margin-bottom:10px; }
.gloss-term { font-size:14px; font-weight:700; color:#6C5CE7; }
.gloss-def  { font-size:13px; color:#555; line-height:1.65; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    FILE = "ANALISIS_KETERJANGKAUAN_KPR.xlsx"
    xl   = pd.read_excel(FILE, sheet_name=None, engine="openpyxl")

    # ── Per-tahun ─────────────────────────────────────────────────────────────
    years, dfs = [2020,2021,2022,2023,2024,2025], []
    for y in years:
        df = xl[str(y)].copy()
        df = df[df.iloc[:,0].notna() & df.iloc[:,0].astype(str).str.strip().ne("")]
        df = df.iloc[:,:7]
        df.columns = ["KABUPATEN_KOTA","UMK","BATAS_30","CICILAN","GARIS_KEMISKINAN","STATUS_LAJANG","STATUS_KELUARGA"]
        df["UMK"]              = pd.to_numeric(df["UMK"],              errors="coerce")
        df["CICILAN"]          = pd.to_numeric(df["CICILAN"],          errors="coerce")
        df["GARIS_KEMISKINAN"] = pd.to_numeric(df["GARIS_KEMISKINAN"], errors="coerce")
        df["BATAS_30"]         = df["UMK"] * 0.3
        df["RESIDUAL"]         = df["UMK"] - df["CICILAN"] - df["GARIS_KEMISKINAN"]
        df["STATUS_LAJANG"]    = df.apply(
            lambda r: "Terjangkau" if (r["CICILAN"] <= r["BATAS_30"]) and (r["RESIDUAL"] >= 0)
            else "Tidak Terjangkau", axis=1)
        df["STATUS_KELUARGA"]  = df.apply(
            lambda r: "Terjangkau" if (r["CICILAN"] <= r["BATAS_30"]) and (r["RESIDUAL"] >= r["GARIS_KEMISKINAN"]*2)
            else "Tidak Terjangkau", axis=1)
        df["TAHUN"] = y
        df = df.dropna(subset=["UMK"])
        df["KABUPATEN_KOTA"] = df["KABUPATEN_KOTA"].astype(str).str.strip().str.upper()
        dfs.append(df)
    main = pd.concat(dfs, ignore_index=True)

    # ── IHPR ──────────────────────────────────────────────────────────────────
    ihpr = xl["IHPR SBY"].copy()
    ihpr.columns = ["TAHUN","TRIWULAN","TIPE_KECIL","TIPE_MENENGAH","TIPE_BESAR","TOTAL"]
    ihpr["TAHUN"] = ihpr["TAHUN"].ffill()
    ihpr = ihpr.dropna(subset=["TRIWULAN"])
    ihpr["TAHUN_INT"] = ihpr["TAHUN"].astype(float).astype(int)
    ihpr["PERIODE"]   = ihpr["TAHUN_INT"].astype(str) + " Q" + ihpr["TRIWULAN"].astype(str)
    for c in ["TIPE_KECIL","TIPE_MENENGAH","TIPE_BESAR","TOTAL"]:
        ihpr[c] = pd.to_numeric(ihpr[c], errors="coerce")

    # ── Garis Kemiskinan ──────────────────────────────────────────────────────
    gk = xl["garis kemiskinan"].copy()
    gk = gk.iloc[:,:6]
    gk.columns = ["PERIODE","GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]
    gk = gk[gk["PERIODE"].notna()]
    gk = gk[~gk["PERIODE"].astype(str).str.lower().str.startswith("tahun")]
    for c in ["GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]:
        gk[c] = pd.to_numeric(
            gk[c].astype(str).str.replace(",","").str.replace("-","0").str.strip(),
            errors="coerce")
    gk = gk[gk["PERIODE"].astype(str).str.contains("202", na=False)]
    gk = gk.dropna(subset=["GK_KOTA"])   # buang baris 2023 Sep yang kosong

    # ── Kepemilikan Rumah ─────────────────────────────────────────────────────
    kp = xl["kepemilikan rumah"].copy()
    kp.columns = ["KAB_KOTA","MILIK","KONTRAK","LAINNYA","TOTAL"]
    kp = kp[kp["KAB_KOTA"].notna()]
    skip = ["kabupaten/kota","catatan","jumlah","jawa timur"]
    kp = kp[~kp["KAB_KOTA"].astype(str).str.lower().str[:10].isin(skip)]
    for c in ["MILIK","KONTRAK","LAINNYA"]:
        kp[c] = pd.to_numeric(
            kp[c].astype(str).str.replace("–","0").str.replace(",",""),
            errors="coerce").fillna(0)
    # Normalkan nama: "Kota Surabaya" → "KOTA SURABAYA" agar bisa di-join
    kp["KAB_KOTA_UPPER"] = kp["KAB_KOTA"].astype(str).str.upper().str.strip()

    return main, ihpr, gk, kp

main_df, ihpr_df, gk_df, kp_df = load_data()
KAB_LIST = sorted(main_df["KABUPATEN_KOTA"].unique().tolist())
YEARS    = [2020,2021,2022,2023,2024,2025]
COLORS   = ["#6C5CE7","#E84393","#0984E3","#00B894","#FDCB6E","#A29BFE"]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏠 Keterjangkauan Hunian")
    st.markdown("**Jawa Timur 2020–2025**")
    st.markdown("---")
    st.markdown("### 🎛️ Filter")
    sel_year = st.selectbox("📅 Tahun", YEARS, index=5)
    sel_kab  = st.selectbox("📍 Kabupaten/Kota", ["Semua"] + KAB_LIST)

    # Penjelasan pengaruh filter
    st.markdown("---")
    if sel_kab == "Semua":
        st.markdown("""<div style='font-size:12px;color:rgba(255,255,255,0.8);line-height:1.8;'>
        <b>Mode aktif: Jawa Timur</b><br>
        Grafik menampilkan perbandingan semua 38 daerah.
        Pilih kabupaten/kota untuk melihat analisis fokus satu daerah.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style='font-size:12px;color:rgba(255,255,255,0.9);line-height:1.8;
        background:rgba(255,255,255,0.15);padding:10px;border-radius:8px;'>
        <b>📍 Fokus: {sel_kab.title()}</b><br>
        Grafik menampilkan analisis mendalam untuk daerah ini.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style='font-size:11px;color:rgba(255,255,255,0.65);line-height:1.9;'>
    <b>📚 Sumber Data</b><br>
    • SK UMK Gubernur Jatim 2020–2025<br>
    • SHPR Bank Indonesia<br>
    • BPS – Jawa Timur Dalam Angka<br>
    • Kementerian PUPR (KPR FLPP)
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTED — shared across tabs
# ══════════════════════════════════════════════════════════════════════════════
df_year  = main_df[main_df["TAHUN"] == sel_year].copy()
cicilan  = int(df_year["CICILAN"].iloc[0]) if not df_year.empty else 0

# Mode: satu daerah vs semua
is_single = sel_kab != "Semua"
df_focus  = df_year[df_year["KABUPATEN_KOTA"] == sel_kab] if is_single else df_year
df_trend_focus = main_df[main_df["KABUPATEN_KOTA"] == sel_kab] if is_single else main_df

# KPI — selalu Jawa Timur level (gambaran besar)
n_ok    = (df_year["STATUS_LAJANG"] == "Terjangkau").sum()
n_no    = (df_year["STATUS_LAJANG"] == "Tidak Terjangkau").sum()
total   = len(df_year)
pct_ok  = round(n_ok / total * 100, 1) if total else 0
umk_med = int(df_year["UMK"].median()) if not df_year.empty else 0

# KPI untuk single mode
if is_single and not df_focus.empty:
    kab_row      = df_focus.iloc[0]
    kab_umk      = int(kab_row["UMK"])
    kab_residual = int(kab_row["RESIDUAL"])
    kab_status   = kab_row["STATUS_LAJANG"]
    kab_pct      = round(cicilan / kab_umk * 100, 1)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
if is_single:
    header_sub = f"Fokus: <b>{sel_kab.title()}</b> &nbsp;|&nbsp; Tahun <b>{sel_year}</b>"
else:
    header_sub = f"Seluruh Jawa Timur (38 kab/kota) &nbsp;|&nbsp; Tahun <b>{sel_year}</b>"

st.markdown(f"""
<div style='background:linear-gradient(135deg,#2D2B55 0%,#6C5CE7 60%,#E84393 100%);
    border-radius:18px;padding:26px 36px;margin-bottom:20px;'>
  <h1 style='color:white;margin:0;font-size:26px;font-weight:800;'>
    🏘️ Dashboard Keterjangkauan Hunian Jawa Timur
  </h1>
  <p style='color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:14px;'>
    UMK vs KPR FLPP — Metode <b>The 30% Rule</b> &amp; <b>Residual Income</b>
    &nbsp;|&nbsp; {header_sub}
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS — berubah tergantung mode
# ══════════════════════════════════════════════════════════════════════════════
if is_single and not df_focus.empty:
    # Mode satu daerah: tampilkan data spesifik daerah itu
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1:
        st.markdown(f"""<div class="kpi-card {'green' if kab_status=='Terjangkau' else 'red'}">
          <div class="kpi-label">Status {sel_year}</div>
          <div class="kpi-value" style='font-size:20px;'>{'✅ Terjangkau' if kab_status=='Terjangkau' else '❌ Stress'}</div>
          <div class="kpi-sub">{sel_kab.title()}</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card blue">
          <div class="kpi-label">UMK {sel_year}</div>
          <div class="kpi-value" style='font-size:18px;'>Rp {kab_umk:,}</div>
          <div class="kpi-sub">per bulan</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card gold">
          <div class="kpi-label">💸 Cicilan KPR FLPP</div>
          <div class="kpi-value" style='font-size:18px;'>Rp {cicilan:,}</div>
          <div class="kpi-sub">{kab_pct}% dari UMK</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        rc = "green" if kab_residual >= 0 else "red"
        st.markdown(f"""<div class="kpi-card {rc}">
          <div class="kpi-label">Residual Income</div>
          <div class="kpi-value" style='font-size:18px;'>Rp {kab_residual:,}</div>
          <div class="kpi-sub">sisa setelah cicilan & GK</div>
        </div>""", unsafe_allow_html=True)
    with k5:
        rank = df_year["UMK"].rank(ascending=False).loc[df_focus.index[0]]
        st.markdown(f"""<div class="kpi-card pink">
          <div class="kpi-label">Ranking UMK</div>
          <div class="kpi-value">#{int(rank)}</div>
          <div class="kpi-sub">dari 38 daerah</div>
        </div>""", unsafe_allow_html=True)
else:
    # Mode Jawa Timur: gambaran besar
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1:
        st.markdown(f"""<div class="kpi-card green">
          <div class="kpi-label">✅ Terjangkau</div>
          <div class="kpi-value">{n_ok}</div>
          <div class="kpi-sub">dari {total} daerah</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card red">
          <div class="kpi-label">❌ Housing Stress</div>
          <div class="kpi-value">{n_no}</div>
          <div class="kpi-sub">cicilan &gt; 30% UMK</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card pink">
          <div class="kpi-label">% Housing Stress</div>
          <div class="kpi-value">{round(100-pct_ok,1)}%</div>
          <div class="kpi-sub">daerah tidak aman</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card gold">
          <div class="kpi-label">💸 Cicilan KPR FLPP</div>
          <div class="kpi-value" style='font-size:18px;'>Rp {cicilan:,}</div>
          <div class="kpi-sub">per bulan {sel_year}</div>
        </div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""<div class="kpi-card blue">
          <div class="kpi-label">📈 Median UMK</div>
          <div class="kpi-value" style='font-size:18px;'>Rp {umk_med:,}</div>
          <div class="kpi-sub">se-Jawa Timur</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "📊 Status & Proporsi",
    "💰 UMK vs Cicilan",
    "📈 Tren UMK",
    "🏗️ IHPR Properti",
    "🌍 Sosial Ekonomi",
    "🧮 Cek Kemampuanmu",
    "📋 Tabel & Glosarium",
])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — STATUS & PROPORSI
# Filter Tahun: ✅ aktif | Filter Kota: ✅ aktif (ganti konteks)
# ──────────────────────────────────────────────────────────────────────────────
with t1:
    if is_single:
        # ── MODE SINGLE: detail historis satu daerah ──────────────────────────
        st.markdown(f'<div class="sec-q">📍 Bagaimana riwayat keterjangkauan <b>{sel_kab.title()}</b> dari 2020 hingga 2025? Apakah kondisinya membaik?</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="sec-title">Tren Status Keterjangkauan (Lajang vs Keluarga)</div>', unsafe_allow_html=True)
            hist = df_trend_focus[["TAHUN","UMK","CICILAN","BATAS_30","RESIDUAL","STATUS_LAJANG","STATUS_KELUARGA"]].copy()

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist["TAHUN"], y=hist["UMK"],
                name="UMK", mode="lines+markers",
                line=dict(color="#6C5CE7",width=2.5), marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=hist["TAHUN"], y=hist["CICILAN"],
                name="Cicilan KPR FLPP", mode="lines+markers",
                line=dict(color="#D63031",dash="dot",width=2.5), marker=dict(symbol="diamond",size=8,color="#D63031")))
            fig.add_trace(go.Scatter(x=hist["TAHUN"], y=hist["BATAS_30"],
                name="Batas 30% UMK", mode="lines",
                line=dict(color="#FDCB6E",dash="dash",width=1.5)))

            # Warnai area status
            for _, r in hist.iterrows():
                col = "rgba(0,184,148,0.15)" if r["STATUS_LAJANG"]=="Terjangkau" else "rgba(214,48,49,0.1)"
                fig.add_vrect(x0=r["TAHUN"]-0.4, x1=r["TAHUN"]+0.4, fillcolor=col, line_width=0)

            fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickmode="linear"),
                yaxis=dict(showgrid=True, gridcolor="#EEE", title="Rp", tickformat=","),
                legend=dict(bgcolor="rgba(255,255,255,0.85)"))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="sec-title">Tabel Ringkasan per Tahun</div>', unsafe_allow_html=True)
            tbl_hist = hist[["TAHUN","UMK","CICILAN","BATAS_30","RESIDUAL","STATUS_LAJANG"]].copy()
            tbl_hist.columns = ["Tahun","UMK","Cicilan","Batas 30%","Residual","Status"]
            tbl_hist["% Cicilan"] = (tbl_hist["Cicilan"]/tbl_hist["UMK"]*100).round(1).astype(str)+"%"

            def clr(v):
                if v == "Terjangkau": return "background:#d4edda;color:#155724;font-weight:700"
                return "background:#f8d7da;color:#721c24;font-weight:700"

            styled = tbl_hist.style.map(clr, subset=["Status"]).format({
                "UMK":"Rp {:,.0f}", "Cicilan":"Rp {:,.0f}",
                "Batas 30%":"Rp {:,.0f}", "Residual":"Rp {:,.0f}"})
            st.dataframe(styled, use_container_width=True, height=280)

            # Status summary
            n_aman_hist = (hist["STATUS_LAJANG"]=="Terjangkau").sum()
            st.markdown(f"""<div class="sec-insight">
              📌 <b>{sel_kab.title()}</b> terjangkau di <b>{n_aman_hist} dari 6 tahun</b> (2020–2025).<br>
              Persentase cicilan terhadap UMK: kisaran
              <b>{round(hist['CICILAN'].iloc[0]/hist['UMK'].iloc[0]*100,1)}%</b> (2020) →
              <b>{round(hist['CICILAN'].iloc[-1]/hist['UMK'].iloc[-1]*100,1)}%</b> (2025).
            </div>""", unsafe_allow_html=True)

    else:
        # ── MODE SEMUA: proporsi + tren Jawa Timur ────────────────────────────
        st.markdown(f'<div class="sec-q">🤔 Dari 38 kabupaten/kota di Jawa Timur, berapa yang terjangkau di tahun <b>{sel_year}</b>? Apakah kondisinya membaik dari tahun ke tahun?</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="sec-title">Proporsi Keterjangkauan {sel_year}</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Pie(
                labels=["Terjangkau","Housing Stress"], values=[n_ok,n_no],
                hole=0.58, marker_colors=["#00B894","#D63031"],
                textinfo="label+percent", textfont_size=13,
                hovertemplate="<b>%{label}</b><br>%{value} daerah (%{percent})<extra></extra>"))
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                annotations=[dict(text=f"<b>{n_no}</b><br><span style='font-size:10px'>Housing<br>Stress</span>",
                    x=0.5,y=0.5,font_size=18,showarrow=False,font_color="#2D2B55")])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="sec-insight">
              📌 Tahun <b>{sel_year}</b>: hanya <b>{n_ok} dari 38 daerah</b> ({pct_ok}%) terjangkau.
              <b>{n_no} daerah</b> ({round(100-pct_ok,1)}%) masuk kategori housing stress.<br>
              Pilih satu kabupaten/kota di sidebar untuk melihat detail daerahnya.
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="sec-title">Tren 2020–2025 (Seluruh Jawa Timur)</div>', unsafe_allow_html=True)
            yc = []
            for y in YEARS:
                dy = main_df[main_df["TAHUN"]==y]
                yc.append({"Tahun":y,
                    "Terjangkau":(dy["STATUS_LAJANG"]=="Terjangkau").sum(),
                    "Housing Stress":(dy["STATUS_LAJANG"]=="Tidak Terjangkau").sum()})
            yc_df = pd.DataFrame(yc)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=yc_df["Tahun"],y=yc_df["Terjangkau"],name="Terjangkau",marker_color="#00B894"))
            fig2.add_trace(go.Bar(x=yc_df["Tahun"],y=yc_df["Housing Stress"],name="Housing Stress",marker_color="#D63031"))
            fig2.update_layout(height=300, barmode="stack",
                margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False,tickmode="linear"),
                yaxis=dict(showgrid=True,gridcolor="#EEE",title="Jumlah Daerah"),
                legend=dict(bgcolor="rgba(255,255,255,0.8)"))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("""<div class="sec-insight">
              📌 <b>Stagnansi absolut</b>: jumlah daerah terjangkau tidak berubah
              selama 6 tahun — tetap 5 daerah. Kenaikan UMK tahunan tidak cukup
              menggeser daerah-daerah di bawah ambang keterjangkauan.
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — UMK VS CICILAN
# Filter Tahun: ✅ aktif | Filter Kota: ✅ aktif (highlight)
# ──────────────────────────────────────────────────────────────────────────────
with t2:
    st.markdown(f'<div class="sec-q">💡 Seberapa besar gap antara UMK tiap daerah dengan cicilan KPR FLPP di tahun <b>{sel_year}</b>?{" Daerah <b>" + sel_kab.title() + "</b> ditandai khusus." if is_single else ""}</div>', unsafe_allow_html=True)

    # ── Banner info — tampil SEBELUM grafik ────────────────────────────────────
    if is_single and not df_focus.empty:
        kab_umk_val = float(df_focus["UMK"].iloc[0])
        kab_pct_cic = round(cicilan / kab_umk_val * 100, 1)
        kab_ok      = cicilan <= kab_umk_val * 0.3
        if kab_ok:
            banner_bg     = "linear-gradient(135deg,#d4edda,#c3e6cb)"
            banner_border = "#28a745"
            icon = "✅"; verdict = "TERJANGKAU"; verdict_color = "#155724"
        else:
            banner_bg     = "linear-gradient(135deg,#f8d7da,#f5c6cb)"
            banner_border = "#D63031"
            icon = "❌"; verdict = "HOUSING STRESS"; verdict_color = "#721c24"
        st.markdown(f"""
        <div style='background:{banner_bg};border-left:5px solid {banner_border};
             border-radius:10px;padding:14px 20px;margin-bottom:10px;
             display:flex;align-items:center;gap:20px;flex-wrap:wrap;'>
          <div style='font-size:28px;'>{icon}</div>
          <div>
            <div style='font-size:11px;color:#555;font-weight:700;text-transform:uppercase;
                 letter-spacing:0.8px;'>Daerah Dipilih</div>
            <div style='font-size:18px;font-weight:800;color:#2D2B55;'>{sel_kab.title()}</div>
            <div style='font-size:16px;font-weight:800;color:{verdict_color};'>{verdict}</div>
          </div>
          <div style='border-left:2px solid rgba(0,0,0,0.12);padding-left:18px;'>
            <div style='font-size:11px;color:#666;'>UMK {sel_year}</div>
            <div style='font-size:17px;font-weight:700;color:#2D2B55;'>Rp {kab_umk_val:,.0f}</div>
          </div>
          <div style='border-left:2px solid rgba(0,0,0,0.12);padding-left:18px;'>
            <div style='font-size:11px;color:#666;'>Cicilan KPR FLPP</div>
            <div style='font-size:17px;font-weight:700;color:#2D2B55;'>Rp {cicilan:,}</div>
          </div>
          <div style='border-left:2px solid rgba(0,0,0,0.12);padding-left:18px;'>
            <div style='font-size:11px;color:#666;'>% Cicilan dari UMK</div>
            <div style='font-size:26px;font-weight:800;color:{verdict_color};'>{kab_pct_cic}%</div>
            <div style='font-size:11px;color:#888;'>batas aman ≤ 30%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:#EDE9FF;border-left:5px solid #6C5CE7;border-radius:10px;
             padding:11px 18px;margin-bottom:10px;font-size:13px;color:#4A3F9F;font-weight:600;'>
          🟢 Bar hijau = Terjangkau &nbsp;|&nbsp;
          🔴 Bar merah = Housing Stress &nbsp;|&nbsp;
          Garis merah = Cicilan KPR FLPP {sel_year}: <b>Rp {cicilan:,}/bulan</b><br>
          <span style='font-weight:400;color:#666;font-size:12px;'>
          Pilih satu daerah di sidebar untuk melihat analisis detailnya.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="sec-title">UMK vs Cicilan KPR FLPP — Semua Kabupaten/Kota ({sel_year})</div>', unsafe_allow_html=True)

    df_s = df_year.sort_values("UMK").copy()
    df_s["LABEL"] = df_s["KABUPATEN_KOTA"].str.replace("KABUPATEN ","KAB. ")

    # Warna: highlight daerah yang dipilih
    def get_color(row):
        if is_single and row["KABUPATEN_KOTA"] == sel_kab:
            return "#FDCB6E"   # kuning emas = highlight
        return "#00B894" if row["STATUS_LAJANG"]=="Terjangkau" else "#D63031"

    df_s["COLOR"] = df_s.apply(get_color, axis=1)
    df_s["OPACITY"] = df_s["KABUPATEN_KOTA"].apply(
        lambda x: 1.0 if (not is_single or x == sel_kab) else 0.5)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=df_s["LABEL"], x=df_s["UMK"], orientation="h",
        marker=dict(color=df_s["COLOR"], opacity=df_s["OPACITY"]),
        text=df_s["UMK"].apply(lambda x: f"Rp {x/1e6:.2f}jt"),
        textposition="outside", textfont_size=9,
        hovertemplate="<b>%{y}</b><br>UMK: Rp %{x:,.0f}<extra></extra>"))
    fig3.add_vline(x=cicilan, line_dash="dash", line_color="#FF6B6B", line_width=2,
        annotation_text=f"  Cicilan KPR: Rp {cicilan:,}",
        annotation_font_color="#CC0000", annotation_position="top")

    # Highlight daerah terpilih — status ditampilkan di insight box bawah
    fig3.update_layout(height=980, showlegend=False,
        margin=dict(l=10, r=160, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True,gridcolor="#EEE",title="UMK (Rp)",tickformat=","),
        yaxis=dict(showgrid=False,tickfont_size=10))
    st.plotly_chart(fig3, use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — TREN UMK
# Filter Tahun: ✅ (marker aktif tahun terpilih) | Filter Kota: ✅ aktif
# ──────────────────────────────────────────────────────────────────────────────
with t3:
    if is_single:
        kabs_show = [sel_kab]
        note      = sel_kab.title()
    else:
        kabs_show = df_year.nlargest(5,"UMK")["KABUPATEN_KOTA"].tolist()
        note      = "5 Daerah UMK Tertinggi"

    # ── Header ────────────────────────────────────────────────────────────────
    if is_single:
        st.markdown(f"""
        <div class="sec-q">
          📈 Apakah kenaikan gaji UMK di <b>{sel_kab.title()}</b> cukup mengejar
          kenaikan cicilan rumah subsidi dari tahun ke tahun?
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sec-q">
          📈 Bagaimana perkembangan UMK dibandingkan cicilan KPR FLPP (2020–2025)?
          Pilih satu daerah di sidebar untuk analisis spesifik per daerah.
        </div>
        """, unsafe_allow_html=True)

    # ── Panduan baca singkat ──────────────────────────────────────────────────
    st.markdown("""
    <div style='background:#FFF9E6;border-radius:8px;padding:9px 16px;
         margin-bottom:10px;border-left:3px solid #FDCB6E;font-size:13px;color:#555;'>
      <b>Cara membaca:</b> Batang = UMK &nbsp;·&nbsp;
      Garis merah putus-putus = cicilan KPR FLPP &nbsp;·&nbsp;
      <b>Batang di atas garis</b> = UMK melampaui cicilan (terjangkau) &nbsp;·&nbsp;
      <b>Batang di bawah garis</b> = UMK tidak mencukupi cicilan (housing stress)
    </div>
    """, unsafe_allow_html=True)

    trend  = main_df[main_df["KABUPATEN_KOTA"].isin(kabs_show)].copy()
    cic_yr = main_df.groupby("TAHUN")["CICILAN"].first().reset_index()

    fig4 = go.Figure()
    for i, kab in enumerate(kabs_show):
        d   = trend[trend["KABUPATEN_KOTA"]==kab]
        lbl = kab.replace("KABUPATEN ","KAB. ")
        c   = COLORS[i % len(COLORS)]
        fig4.add_trace(go.Bar(x=d["TAHUN"],y=d["UMK"],name=lbl,
            marker_color=c,opacity=0.75,offsetgroup=i,
            hovertemplate=f"<b>{lbl}</b><br>%{{x}} — UMK: Rp %{{y:,.0f}}<extra></extra>"))
        fig4.add_trace(go.Scatter(x=d["TAHUN"],y=d["UMK"],
            mode="lines+markers",showlegend=False,
            line=dict(color=c,width=2),marker=dict(size=6,color=c)))

    fig4.add_trace(go.Scatter(x=cic_yr["TAHUN"],y=cic_yr["CICILAN"],
        mode="lines+markers",name="Cicilan KPR FLPP",
        line=dict(color="#D63031",dash="dot",width=2.5),
        marker=dict(symbol="diamond",size=9,color="#D63031"),
        hovertemplate="Cicilan KPR FLPP<br>%{x}: Rp %{y:,.0f}<extra></extra>"))

    fig4.add_vline(x=sel_year, line_dash="solid",
        line_color="rgba(108,92,231,0.2)", line_width=20,
        annotation_text=f"  {sel_year}",
        annotation_font_color="#6C5CE7", annotation_position="top")

    fig4.update_layout(height=420, barmode="group",
        margin=dict(l=0,r=0,t=30,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickmode="linear", title="Tahun"),
        yaxis=dict(showgrid=True, gridcolor="#EEE", title="Rp", tickformat=","),
        legend=dict(bgcolor="rgba(255,255,255,0.85)", font_size=11))
    st.plotly_chart(fig4, use_container_width=True)

    # ── Insight ───────────────────────────────────────────────────────────────
    if is_single and not df_focus.empty:
        umk_2020   = main_df[(main_df["KABUPATEN_KOTA"]==sel_kab)&(main_df["TAHUN"]==2020)]["UMK"].iloc[0]
        umk_2025   = main_df[(main_df["KABUPATEN_KOTA"]==sel_kab)&(main_df["TAHUN"]==2025)]["UMK"].iloc[0]
        growth     = round((umk_2025/umk_2020-1)*100,1)
        cic_2020   = main_df[main_df["TAHUN"]==2020]["CICILAN"].iloc[0]
        cic_2025   = main_df[main_df["TAHUN"]==2025]["CICILAN"].iloc[0]
        cic_growth = round((cic_2025/cic_2020-1)*100,1)
        selisih    = round(abs(growth-cic_growth),1)
        umk_sel    = float(df_focus["UMK"].iloc[0])
        pct_sel    = round(cicilan/umk_sel*100,1)
        ok_sel     = cicilan <= umk_sel*0.3

        if ok_sel:
            status_html = f"""<div style='background:#d4edda;border-radius:8px;padding:11px 16px;
                margin-bottom:8px;color:#155724;font-size:13px;'>
                ✅ <b>Tahun {sel_year}:</b> Cicilan KPR FLPP (Rp {cicilan:,}) menyerap
                <b>{pct_sel}%</b> dari UMK — masih di bawah ambang 30%, sehingga diklasifikasikan
                <b>terjangkau</b>.</div>"""
        else:
            kekurangan = round(cicilan - umk_sel*0.3, 0)
            status_html = f"""<div style='background:#f8d7da;border-radius:8px;padding:11px 16px;
                margin-bottom:8px;color:#721c24;font-size:13px;'>
                ❌ <b>Tahun {sel_year}:</b> Cicilan KPR FLPP (Rp {cicilan:,}) menyerap
                <b>{pct_sel}%</b> dari UMK — melampaui ambang 30%.
                Dibutuhkan tambahan UMK sekitar Rp {kekurangan:,.0f} agar masuk kategori terjangkau.
                </div>"""

        if growth > cic_growth:
            tren_html = f"""<div style='background:#d4edda;border-radius:8px;padding:11px 16px;
                margin-bottom:8px;color:#155724;font-size:13px;'>
                📈 <b>Tren 2020–2025:</b> UMK tumbuh <b>{growth}%</b>, lebih tinggi dari kenaikan
                cicilan KPR yang sebesar <b>{cic_growth}%</b>. Artinya tekanan keterjangkauan
                secara bertahap <b>mereda</b> di daerah ini.</div>"""
        else:
            tren_html = f"""<div style='background:#f8d7da;border-radius:8px;padding:11px 16px;
                margin-bottom:8px;color:#721c24;font-size:13px;'>
                📉 <b>Tren 2020–2025:</b> Cicilan KPR naik <b>{cic_growth}%</b>, melampaui
                pertumbuhan UMK yang hanya <b>{growth}%</b> (selisih {selisih} poin persentase).
                Keterjangkauan hunian di daerah ini cenderung <b>makin tertekan</b> dari tahun ke tahun.
                </div>"""

        angka_html = f"""<div style='background:#F7F5FF;border-radius:8px;padding:9px 16px;
            font-size:12px;color:#888;'>
            UMK: Rp {umk_2020:,.0f} → Rp {umk_2025:,.0f} (▲{growth}%) &nbsp;|&nbsp;
            Cicilan KPR FLPP: Rp {cic_2020:,.0f} → Rp {cic_2025:,.0f} (▲{cic_growth}%)
            </div>"""

        st.markdown(status_html + tren_html + angka_html, unsafe_allow_html=True)

    else:
        st.markdown("""<div class="sec-insight">
          📌 Selama UMK berada <b>di atas garis merah</b>, daerah tersebut terjangkau.
          Perhatikan apakah jarak antara UMK dan garis cicilan makin melebar (membaik)
          atau menyempit (memburuk) dari tahun ke tahun.<br>
          <span style='color:#6C5CE7;font-weight:600;'>
          Pilih satu daerah di sidebar untuk melihat analisis tren spesifik beserta kesimpulannya.
          </span>
        </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — IHPR PROPERTI
# Filter Tahun: ✅ (marker) | Filter Kota: tidak relevan, tetap tampil + note
# ──────────────────────────────────────────────────────────────────────────────
with t4:
    st.markdown('<div class="sec-q">🏗️ Bagaimana tren harga properti residensial di Surabaya? Tipe rumah mana yang naik paling cepat — dan apa dampaknya terhadap keterjangkauan?</div>', unsafe_allow_html=True)

    if is_single:
        st.info(f"📍 Data IHPR hanya tersedia untuk **Kota Surabaya** (representasi Jawa Timur dari Bank Indonesia). Grafik ini tidak berubah meski filter daerah menunjukkan **{sel_kab.title()}**.", icon="ℹ️")
    else:
        st.info("📍 Data IHPR berasal dari SHPR Bank Indonesia untuk **Kota Surabaya** sebagai representasi pasar properti Jawa Timur (tersedia mulai Q1 2022).", icon="ℹ️")

    c1, c2 = st.columns([3,2])
    with c1:
        st.markdown('<div class="sec-title">Indeks Harga Properti Residensial Surabaya (2018=100)</div>', unsafe_allow_html=True)
        fig5 = go.Figure()
        for col, color, name in [
            ("TIPE_KECIL","#6C5CE7","Tipe Kecil"),
            ("TIPE_MENENGAH","#E84393","Tipe Menengah"),
            ("TIPE_BESAR","#0984E3","Tipe Besar"),
            ("TOTAL","#FDCB6E","Total Surabaya"),
        ]:
            fig5.add_trace(go.Scatter(x=ihpr_df["PERIODE"],y=ihpr_df[col],
                name=name,mode="lines+markers",
                line=dict(width=2.5,color=color),marker=dict(size=6),
                hovertemplate=f"<b>{name}</b><br>%{{x}}<br>Indeks: %{{y:.2f}}<extra></extra>"))

        # Tandai kuartal dari tahun yang dipilih
        mark_periods = ihpr_df[ihpr_df["TAHUN_INT"]==sel_year]["PERIODE"].tolist()
        for mp in mark_periods:
            fig5.add_vline(x=mp, line_dash="dot", line_color="rgba(108,92,231,0.4)", line_width=1.5)

        fig5.update_layout(height=380,margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False,tickangle=-45,tickfont_size=9),
            yaxis=dict(showgrid=True,gridcolor="#EEE",title="Indeks (2018=100)"),
            legend=dict(bgcolor="rgba(255,255,255,0.85)"))
        st.plotly_chart(fig5, use_container_width=True)
        st.caption(f"Garis ungu vertikal = triwulan tahun {sel_year} yang dipilih")

    with c2:
        st.markdown('<div class="sec-title">Cara Membaca Grafik Ini</div>', unsafe_allow_html=True)
        # Cari nilai IHPR untuk tahun terpilih
        ihpr_sel = ihpr_df[ihpr_df["TAHUN_INT"]==sel_year]
        if not ihpr_sel.empty:
            avg_k = ihpr_sel["TIPE_KECIL"].mean()
            st.markdown(f"""<div class="sec-insight" style='margin-top:0;'>
              <b>Indeks Harga Properti (IHPR)</b><br>
              Angka perbandingan, bukan harga asli. Tahun dasar 2018 = 100.<br>
              Indeks 113 → harga naik 13% sejak 2018.<br><br>
              <b>Tahun {sel_year} — Tipe Kecil:</b><br>
              Rata-rata indeks = <b>{avg_k:.2f}</b>
              → harga naik <b>{avg_k-100:.1f}%</b> sejak 2018.<br><br>
              <b>Mengapa tipe kecil naik paling cepat?</b><br>
              Permintaan tinggi dari pekerja yang mencari hunian pertama
              mendorong harga segmen terjangkau naik lebih agresif —
              padahal ini segmen yang paling dibutuhkan MBR.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="sec-insight" style='margin-top:0;'>
              Data IHPR tersedia mulai Q1 2022. Tahun yang dipilih berada
              di luar cakupan data IHPR.
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 5 — SOSIAL EKONOMI
# Filter Tahun: ✅ (marker GK) | Filter Kota: ✅ (kepemilikan rumah)
# ──────────────────────────────────────────────────────────────────────────────
with t5:
    st.markdown('<div class="sec-q">🌍 Bagaimana konteks sosial ekonomi yang memperparah krisis keterjangkauan hunian — dari sisi kepemilikan rumah dan tren kemiskinan?</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="sec-title">Kepemilikan Rumah{" — " + sel_kab.title() if is_single else " — Seluruh Jawa Timur"}</div>', unsafe_allow_html=True)

        if is_single:
            # Cari data kepemilikan untuk daerah yang dipilih
            # Normalisasi: "KOTA SURABAYA" → "Kota Surabaya"
            kab_clean = sel_kab.replace("KABUPATEN ","").replace("KOTA ","").title()
            kp_f = kp_df[kp_df["KAB_KOTA"].str.contains(kab_clean, case=False, na=False)]

            if not kp_f.empty:
                row_kp  = kp_f.iloc[0]
                total_kp = row_kp["MILIK"] + row_kp["KONTRAK"] + row_kp["LAINNYA"]
                fig_kp = go.Figure(go.Pie(
                    labels=["Milik Sendiri","Kontrak/Sewa","Lainnya"],
                    values=[row_kp["MILIK"], row_kp["KONTRAK"], row_kp["LAINNYA"]],
                    hole=0.5, marker_colors=["#00B894","#D63031","#FDCB6E"],
                    textinfo="label+percent", textfont_size=13))
                fig_kp.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                    paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                    annotations=[dict(text=f"<b>{sel_kab.split()[1] if len(sel_kab.split())>1 else sel_kab}</b>",
                        x=0.5,y=0.5,font_size=14,showarrow=False,font_color="#2D2B55")])
                st.plotly_chart(fig_kp, use_container_width=True)
                pct_milik = round(row_kp["MILIK"]/total_kp*100,1) if total_kp>0 else 0
                st.markdown(f"""<div class="sec-insight">
                  📌 Di <b>{sel_kab.title()}</b>, <b>{pct_milik}%</b> rumah tangga
                  sudah memiliki hunian sendiri, {row_kp['KONTRAK']:.0f} dari 10.000 RT
                  masih kontrak/sewa. Data ini menunjukkan sisa kebutuhan hunian baru
                  yang harus dipenuhi — yang terhambat oleh keterjangkauan KPR.
                </div>""", unsafe_allow_html=True)
            else:
                st.info(f"Data kepemilikan rumah untuk {sel_kab.title()} tidak tersedia.")
        else:
            # Tampilkan semua daerah dalam stacked bar
            kp_m = kp_df[~kp_df["KAB_KOTA"].str.upper().isin(["JAWA TIMUR"])].melt(
                id_vars="KAB_KOTA", value_vars=["MILIK","KONTRAK","LAINNYA"],
                var_name="KATEGORI", value_name="JUMLAH")
            fig6 = px.bar(kp_m, x="KAB_KOTA", y="JUMLAH", color="KATEGORI", barmode="stack",
                color_discrete_map={"MILIK":"#00B894","KONTRAK":"#D63031","LAINNYA":"#FDCB6E"},
                labels={"KAB_KOTA":"","JUMLAH":"per 10.000 RT","KATEGORI":"Status"})
            fig6.update_layout(height=350, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False,tickangle=-45,tickfont_size=8),
                yaxis=dict(showgrid=True,gridcolor="#EEE"),
                legend=dict(bgcolor="rgba(255,255,255,0.85)"))
            st.plotly_chart(fig6, use_container_width=True)
            st.markdown("""<div class="sec-insight">
              📌 Data BPS 2022. &gt;85% RT Jawa Timur sudah punya rumah sendiri.
              Namun ini tidak menjawab apakah generasi baru mampu membeli hunian — 
              yang terhambat oleh krisis keterjangkauan KPR.
              Pilih satu daerah di sidebar untuk tampilan pie chart per daerah.
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-title">Tren Garis Kemiskinan Jawa Timur (2020–2025)</div>', unsafe_allow_html=True)
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=gk_df["PERIODE"],y=gk_df["GK_KOTA"],
            name="Perkotaan",mode="lines+markers",
            line=dict(color="#6C5CE7",width=2.5),marker=dict(size=6),
            hovertemplate="Kota<br>%{x}<br>Rp %{y:,.0f}<extra></extra>"))
        fig7.add_trace(go.Scatter(x=gk_df["PERIODE"],y=gk_df["GK_DESA"],
            name="Perdesaan",mode="lines+markers",
            line=dict(color="#00B894",width=2.5),marker=dict(size=6),
            hovertemplate="Desa<br>%{x}<br>Rp %{y:,.0f}<extra></extra>"))

        # Highlight periode dari tahun terpilih
        gk_sel = gk_df[gk_df["PERIODE"].astype(str).str.contains(str(sel_year))]
        for _, rr in gk_sel.iterrows():
            fig7.add_vline(x=rr["PERIODE"], line_dash="dot",
                line_color="rgba(253,203,110,0.6)", line_width=2)

        fig7.update_layout(height=210,margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False,tickangle=-30,tickfont_size=9,title=""),
            yaxis=dict(showgrid=True,gridcolor="#EEE",title="Rp/kapita/bln",tickformat=","),
            legend=dict(bgcolor="rgba(255,255,255,0.85)"))
        st.plotly_chart(fig7, use_container_width=True)
        st.caption(f"Garis kuning = periode tahun {sel_year}")

        st.markdown('<div class="sec-title" style="margin-top:4px;">Penduduk Miskin (ribu jiwa)</div>', unsafe_allow_html=True)
        fig8 = px.area(gk_df,x="PERIODE",y="TOTAL_MISKIN",
            color_discrete_sequence=["#D63031"])
        fig8.update_layout(height=170,margin=dict(l=0,r=0,t=5,b=0),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False,tickangle=-30,tickfont_size=9,title=""),
            yaxis=dict(showgrid=True,gridcolor="#EEE",title="ribu jiwa"),
            showlegend=False)
        st.plotly_chart(fig8, use_container_width=True)

    st.markdown("""<div class="sec-insight">
      📌 Garis kemiskinan terus naik — biaya hidup minimum makin mahal.
      Bersamaan dengan cicilan KPR yang juga naik, pekerja terjepit dari dua arah:
      kebutuhan dasar makin tinggi sekaligus beban cicilan makin berat,
      sementara UMK banyak daerah tidak cukup mengimbangi keduanya.
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 6 — KALKULATOR
# Filter Tahun: ✅ prefill | Filter Kota: ✅ prefill
# ──────────────────────────────────────────────────────────────────────────────
with t6:
    st.markdown('<div class="sec-q">🧮 Dengan gaji yang kamu miliki, apakah kamu mampu membeli rumah subsidi KPR FLPP? Filter tahun & daerah di sidebar sudah di-prefill otomatis.</div>', unsafe_allow_html=True)

    st.markdown("""<div class="sec-insight" style='margin-bottom:14px;'>
      <b>Metodologi:</b> <b>The 30% Rule</b> (cicilan ≤ 30% gaji) + <b>Residual Income</b>
      (sisa setelah cicilan harus ≥ Garis Kemiskinan). Kedua kondisi harus terpenuhi.
    </div>""", unsafe_allow_html=True)

    ck1,ck2,ck3 = st.columns(3)
    with ck1:
        user_gaji = st.number_input("💰 Penghasilan Bulananmu (Rp)",
            min_value=0, max_value=50_000_000,
            value=3_000_000, step=100_000, format="%d")
    with ck2:
        # Prefill dari filter sidebar
        default_idx = KAB_LIST.index(sel_kab) if is_single and sel_kab in KAB_LIST else 0
        user_kab = st.selectbox("📍 Daerahmu", KAB_LIST, index=default_idx, key="kk")
    with ck3:
        user_year = st.selectbox("📅 Tahun", YEARS, index=YEARS.index(sel_year), key="ky")

    if is_single or user_kab:
        st.caption(f"💡 Daerah & tahun sudah di-prefill dari filter sidebar: **{sel_kab.title() if is_single else user_kab.title()}**, **{sel_year}**")

    if st.button("🔍 Hitung Sekarang!", type="primary"):
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

            r1,r2,r3,r4 = st.columns(4)
            r1.metric("Gaji Kamu",         f"Rp {user_gaji:,.0f}")
            r2.metric("Cicilan KPR FLPP",  f"Rp {cic_val:,.0f}")
            r3.metric("Batas Aman (30%)",  f"Rp {batas_30:,.0f}")
            r4.metric("% Gaji → Cicilan",  f"{pct_g:.1f}%",
                delta="Aman ✅" if cond1 else "Melewati batas ⚠️",
                delta_color="normal" if cond1 else "inverse")

            if is_aman:
                st.markdown(f"""<div class="result-ok">
                  <h2>✅ Kamu Terjangkau!</h2>
                  <p>Dengan gaji <b>Rp {user_gaji:,.0f}</b> di <b>{user_kab.title()}</b> tahun {user_year},
                  cicilan KPR hanya memakan <b>{pct_g:.1f}%</b> penghasilanmu.
                  Sisa pendapatan: <b>Rp {sisa:,.0f}/bulan</b>.</p>
                </div>""", unsafe_allow_html=True)
            else:
                alasan = []
                if not cond1: alasan.append(f"cicilan ({pct_g:.1f}%) melampaui batas 30%")
                if not cond2: alasan.append(f"sisa Rp {sisa:,.0f} kurang dari garis kemiskinan Rp {gk_val:,.0f}")
                st.markdown(f"""<div class="result-stress">
                  <h2>⚠️ Housing Stress!</h2>
                  <p>Tidak terjangkau karena: <b>{' dan '.join(alasan)}</b>.<br>
                  Gaji minimum agar terjangkau: <b>Rp {gaji_min:,.0f}/bulan</b>.</p>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="sec-insight" style='margin-top:14px;'>
              <b>Konteks {user_kab.title()} {user_year}:</b><br>
              • UMK resmi: <b>Rp {umk_val:,.0f}</b> &nbsp;|&nbsp;
              Garis kemiskinan: <b>Rp {gk_val:,.0f}/kapita/bulan</b><br>
              • Gaji minimum untuk terjangkau KPR FLPP: <b>Rp {gaji_min:,.0f}/bulan</b><br>
              • {'✅ Gajimu di atas UMK daerah ini' if user_gaji >= umk_val
                 else f'⚠️ Gajimu di bawah UMK (selisih Rp {umk_val-user_gaji:,.0f})'}
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 7 — TABEL & GLOSARIUM
# Filter Tahun: ✅ | Filter Kota: ✅ (highlight baris)
# ──────────────────────────────────────────────────────────────────────────────
with t7:
    sub1, sub2 = st.tabs(["📋 Tabel Data", "📚 Glosarium & Metodologi"])
    with sub1:
        st.markdown(f'<div class="sec-title">Data Keterjangkauan Lengkap — {sel_year}</div>', unsafe_allow_html=True)
        tbl = df_year[["KABUPATEN_KOTA","UMK","BATAS_30","CICILAN",
                       "GARIS_KEMISKINAN","RESIDUAL","STATUS_LAJANG","STATUS_KELUARGA"]].copy()
        tbl.columns = ["Kabupaten/Kota","UMK (Rp)","Batas 30% (Rp)","Cicilan KPR (Rp)",
                       "Garis Kemiskinan","Residual Income","Status Lajang","Status Kel. Kecil"]
        tbl.index = range(1, len(tbl)+1)

        def style_row(row):
            is_sel = is_single and row["Kabupaten/Kota"] == sel_kab
            base = ["background:#FFF9E6;font-weight:600"]*len(row) if is_sel else [""]*len(row)
            for i, col in enumerate(row.index):
                if col in ["Status Lajang","Status Kel. Kecil"]:
                    if row[col] == "Terjangkau":
                        base[i] = "background:#d4edda;color:#155724;font-weight:700"
                    elif row[col] == "Tidak Terjangkau":
                        base[i] = "background:#f8d7da;color:#721c24;font-weight:700"
            return base

        styled = (tbl.style
            .apply(style_row, axis=1)
            .format({"UMK (Rp)":"Rp {:,.0f}","Batas 30% (Rp)":"Rp {:,.0f}",
                     "Cicilan KPR (Rp)":"Rp {:,.0f}",
                     "Garis Kemiskinan":"Rp {:,.0f}","Residual Income":"Rp {:,.0f}"}))
        st.dataframe(styled, use_container_width=True, height=520)

        if is_single:
            st.caption(f"🟡 Baris kuning = {sel_kab.title()} (daerah yang dipilih di filter)")
        csv = tbl.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, f"keterjangkauan_jatim_{sel_year}.csv","text/csv")

    with sub2:
        st.markdown('<div class="sec-title">Glosarium Istilah Utama</div>', unsafe_allow_html=True)
        glossary = [
            ("UMK — Upah Minimum Kabupaten/Kota",
             "Batas upah minimum yang wajib dibayar pengusaha kepada pekerja baru (<1 tahun). Ditetapkan Gubernur tiap tahun. Disparitas besar: Surabaya Rp 4,96 juta vs Sampang Rp 2,34 juta (2025)."),
            ("KPR FLPP — Fasilitas Likuiditas Pembiayaan Perumahan",
             "Kredit rumah bersubsidi pemerintah: bunga tetap 5%/tahun, tenor ≤20 tahun, DP minimal 1%. Cicilan lebih rendah dari KPR komersial karena ada subsidi likuiditas APBN."),
            ("The 30% Rule",
             "Standar internasional: pengeluaran hunian (cicilan KPR) tidak boleh melebihi 30% penghasilan bruto bulanan. Jika melebihi → Housing Stress."),
            ("Housing Stress",
             "Kondisi cicilan KPR >30% penghasilan. Dalam dashboard ini: sebuah daerah Housing Stress jika cicilan FLPP melampaui 30% UMK-nya."),
            ("Residual Income",
             "Sisa pendapatan setelah cicilan KPR dan Garis Kemiskinan. Formula: UMK − Cicilan − GK. Terjangkau hanya jika Residual Income ≥ 0 DAN cicilan ≤ 30% UMK."),
            ("IHPR — Indeks Harga Properti Residensial",
             "Indeks Bank Indonesia untuk kecepatan kenaikan harga properti. Dasar 2018=100. Indeks 111 → harga naik 11% sejak 2018."),
            ("Garis Kemiskinan",
             "Pengeluaran minimum per kapita/bulan untuk kebutuhan dasar (BPS). Dipakai sebagai proxy biaya hidup minimum dalam formula Residual Income."),
        ]
        for term, defn in glossary:
            st.markdown(f"""<div class="gloss-box">
              <div class="gloss-term">📌 {term}</div>
              <div class="gloss-def">{defn}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title">Metodologi Perhitungan</div>', unsafe_allow_html=True)
        st.markdown("""<div class="formula-box">
          Batas 30%  =  UMK × 30%<br>
          Residual Income  =  UMK − Cicilan KPR − Garis Kemiskinan<br>
          Status Lajang  =  "Terjangkau" jika Cicilan ≤ Batas 30% <b>DAN</b> Residual Income ≥ 0<br>
          Status Kel. Kecil  =  "Terjangkau" jika Cicilan ≤ Batas 30% <b>DAN</b> Residual Income ≥ GK × 2
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;margin-top:30px;padding:16px;
     background:linear-gradient(135deg,#2D2B55,#4A3F9F);
     border-radius:12px;color:rgba(255,255,255,0.7);font-size:12px;'>
  Dashboard Keterjangkauan Hunian Jawa Timur 2020–2025 &nbsp;|&nbsp;
  SK UMK Gubernur Jatim · SHPR Bank Indonesia · BPS Jawa Timur · Kementerian PUPR
</div>
""", unsafe_allow_html=True)