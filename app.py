import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Housing Affordability Jawa Timur",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── COLORS ─────────────────────────────────────────────────────────────────────
C_PURPLE      = "#6C5CE7"
C_PURPLE_DARK = "#4A3F9F"
C_PURPLE_SOFT = "#A29BFE"
C_PINK        = "#E84393"
C_PINK_SOFT   = "#FDA7DF"
C_BLUE        = "#0984E3"
C_BLUE_SOFT   = "#74B9FF"
C_GREEN       = "#00B894"
C_RED         = "#D63031"
C_GOLD        = "#FDCB6E"
C_BG          = "#F7F5FF"
C_WHITE       = "#FFFFFF"
C_DARK        = "#2D2B55"
C_GRAY        = "#636E72"
C_LIGHT       = "#EDE9FF"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #F7F5FF; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #2D2B55 0%, #4A3F9F 100%); }
[data-testid="stSidebar"] *:not([data-baseweb="select"] *):not(input) { color: #FFFFFF !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #2D2B55 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background-color: #EDE9FF !important; }
[data-testid="stSidebar"] input { color: #2D2B55 !important; background-color: #EDE9FF !important; }
[data-testid="stSidebar"] .stSelectbox svg { fill: #2D2B55 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }

/* CARDS */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 16px rgba(108,92,231,0.10);
    border-top: 4px solid #6C5CE7;
    margin-bottom: 8px;
    height: 100%;
}
.kpi-card.pink  { border-top-color: #E84393; }
.kpi-card.blue  { border-top-color: #0984E3; }
.kpi-card.green { border-top-color: #00B894; }
.kpi-card.red   { border-top-color: #D63031; }
.kpi-card.gold  { border-top-color: #FDCB6E; }
.kpi-label { font-size: 11px; color: #888; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.kpi-value { font-size: 30px; font-weight: 800; color: #2D2B55; line-height: 1.2; margin: 4px 0; }
.kpi-sub   { font-size: 12px; color: #aaa; }

/* SECTION */
.sec-title {
    font-size: 17px; font-weight: 700; color: #2D2B55;
    border-left: 4px solid #6C5CE7; padding-left: 12px;
    margin: 20px 0 6px 0;
}
.sec-question {
    background: linear-gradient(135deg, #EDE9FF, #F7F5FF);
    border-radius: 10px; padding: 12px 16px;
    font-size: 14px; color: #4A3F9F; font-weight: 600;
    margin-bottom: 8px;
    border-left: 3px solid #6C5CE7;
}
.sec-insight {
    background: white;
    border-radius: 10px; padding: 14px 18px;
    font-size: 13px; color: #636E72;
    margin-top: 8px;
    border: 1px solid #EDE9FF;
    line-height: 1.7;
}
.glossary-box {
    background: white;
    border-radius: 12px; padding: 16px 20px;
    border: 1px solid #EDE9FF;
    margin-bottom: 12px;
}
.glossary-term { font-size: 14px; font-weight: 700; color: #6C5CE7; }
.glossary-def  { font-size: 13px; color: #636E72; line-height: 1.6; margin-top: 4px; }
.calc-result {
    border-radius: 14px; padding: 20px 24px;
    margin-top: 16px; text-align: center;
}
.calc-result.aman   { background: linear-gradient(135deg, #00B894, #00CEC9); }
.calc-result.stress { background: linear-gradient(135deg, #D63031, #E84393); }
.calc-result h2 { color: white; font-size: 22px; margin: 0 0 8px 0; }
.calc-result p  { color: rgba(255,255,255,0.9); font-size: 14px; margin: 0; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: white; border-radius: 8px 8px 0 0;
    color: #4A3F9F !important; font-weight: 600; font-size: 13px;
    border: 1px solid #EDE9FF; border-bottom: none;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6C5CE7, #A29BFE) !important;
    color: white !important; border-color: transparent !important;
}
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.read_excel("ANALISIS_KETERJANGKAUAN_KPR.xlsx", sheet_name=None)
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    dfs = []
    for y in years:
        df = xl[str(y)].copy()
        umk_col  = [c for c in df.columns if "UMK" in c][0]
        stat_col = [c for c in df.columns if "LAJANG" in c][0]
        kel_col  = [c for c in df.columns if "KECIL" in c or "KELURGA" in c][0]
        df = df.rename(columns={
            umk_col:  "UMK",
            stat_col: "STATUS_LAJANG",
            kel_col:  "STATUS_KELUARGA",
            "30% RULE":            "BATAS_30",
            "CICILAN KPR BULANAN": "CICILAN",
            "GARIS KEMISKINAN":    "GARIS_KEMISKINAN",
        })
        df["TAHUN"] = y
        dfs.append(df)
    main = pd.concat(dfs, ignore_index=True)
    main.columns = [c.upper().replace("/","_").replace(" ","_") for c in main.columns]
    main["KABUPATEN_KOTA"] = main["KABUPATEN_KOTA"].str.strip()

    # Tabungan & Pinjaman (hardcoded dari SEKDA)
    fin_data = pd.DataFrame({
        "TAHUN": [2020,2021,2022,2023,2024,2025],
        "TABUNGAN":  [279077862,311167679,321517512,326897821,344622130,362157215],
        "PINJAMAN":  [162713379,169056549,182841335,199899166,219821336,232963955],
    })

    poverty  = xl["garis kemiskinan"].copy()
    housing  = xl["kepemilikan rumah"].copy()
    ihpr     = xl["IHPR SBY"].copy()

    return main, fin_data, poverty, housing, ihpr

main_df, fin_df, poverty_df, housing_df, ihpr_df = load_data()
KAB_LIST = sorted(main_df["KABUPATEN_KOTA"].unique().tolist())

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 Housing Affordability")
    st.markdown("**Jawa Timur 2020–2025**")
    st.markdown("---")
    st.markdown("### 🎛️ Filter Global")

    sel_year = st.selectbox("📅 Tahun", [2020,2021,2022,2023,2024,2025], index=5)
    sel_kab  = st.selectbox("📍 Kabupaten/Kota", ["Semua"] + KAB_LIST)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px; color:rgba(255,255,255,0.7); line-height:1.8;'>
    <b>📚 Sumber Data</b><br>
    • SK UMK Jawa Timur 2020–2025<br>
    • SHPR Bank Indonesia<br>
    • BPS Jawa Timur<br>
    • SEKDA Jawa Timur
    </div>
    """, unsafe_allow_html=True)

# ── FILTER ─────────────────────────────────────────────────────────────────────
df_year = main_df[main_df["TAHUN"] == sel_year].copy()
df_kab  = df_year[df_year["KABUPATEN_KOTA"] == sel_kab] if sel_kab != "Semua" else df_year

n_ok    = (df_year["STATUS_LAJANG"] == "Terjangkau").sum()
n_no    = (df_year["STATUS_LAJANG"] == "Tidak Terjangkau").sum()
total   = len(df_year)
pct_ok  = round(n_ok / total * 100, 1)
cicilan = int(df_year["CICILAN"].iloc[0])

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,#2D2B55 0%,#6C5CE7 60%,#E84393 100%);
     border-radius:18px;padding:28px 36px;margin-bottom:24px;'>
    <h1 style='color:white;margin:0;font-size:28px;font-weight:800;'>
        🏘️ Analisis Keterjangkauan Hunian Jawa Timur
    </h1>
    <p style='color:rgba(255,255,255,0.85);margin:8px 0 0 0;font-size:15px;'>
        Berdasarkan <b>The 30% Rule</b> — UMK vs Cicilan KPR FLPP | 
        Periode <b>2020–2025</b> | Ditampilkan: Tahun <b>{sel_year}</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ──────────────────────────────────────────────────────────────────
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
        <div class="kpi-sub">cicilan > 30% UMK</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card pink">
        <div class="kpi-label">📊 % Housing Stress</div>
        <div class="kpi-value">{100-pct_ok}%</div>
        <div class="kpi-sub">daerah tidak aman</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card gold">
        <div class="kpi-label">💸 Cicilan KPR FLPP</div>
        <div class="kpi-value" style='font-size:18px;'>Rp {cicilan:,.0f}</div>
        <div class="kpi-sub">per bulan {sel_year}</div>
    </div>""", unsafe_allow_html=True)
with k5:
    umk_med = int(df_year["UMK"].median())
    st.markdown(f"""<div class="kpi-card blue">
        <div class="kpi-label">📈 Median UMK</div>
        <div class="kpi-value" style='font-size:18px;'>Rp {umk_med:,.0f}</div>
        <div class="kpi-sub">se-Jawa Timur {sel_year}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── TABS ───────────────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "📊 Status & Proporsi",
    "💰 UMK vs Cicilan",
    "📈 Tren UMK",
    "🏡 Properti & Harga",
    "🌍 Sosial Ekonomi",
    "🧮 Cek Kemampuanmu",
    "📋 Tabel & Glosarium",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — STATUS & PROPORSI (input: tahun)
# ══════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown(f'<div class="sec-question">🤔 Dari 38 kabupaten/kota di Jawa Timur, berapa yang warganya mampu membeli rumah subsidi pada tahun {sel_year}?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown('<div class="sec-title">🔵 Proporsi Status Keterjangkauan</div>', unsafe_allow_html=True)
        fig_d = go.Figure(go.Pie(
            labels=["Terjangkau","Housing Stress"],
            values=[n_ok, n_no],
            hole=0.6,
            marker_colors=[C_GREEN, C_RED],
            textinfo="label+percent",
            textfont_size=13,
            hovertemplate="<b>%{label}</b><br>%{value} daerah (%{percent})<extra></extra>",
        ))
        fig_d.update_layout(
            height=320, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            annotations=[dict(
                text=f"<b>{n_no}</b><br><span style='font-size:11px'>Housing<br>Stress</span>",
                x=0.5, y=0.5, font_size=18, showarrow=False, font_color=C_DARK,
            )],
        )
        st.plotly_chart(fig_d, use_container_width=True)
        st.markdown(f"""<div class="sec-insight">
            📌 Pada tahun <b>{sel_year}</b>, hanya <b>{n_ok} dari {total} daerah</b> ({pct_ok}%) 
            yang warganya mampu membayar cicilan KPR FLPP tanpa menghabiskan lebih dari 30% UMK-nya.
            Artinya <b>{100-pct_ok}% daerah</b> masuk kategori <i>housing stress</i> — 
            beban cicilan terlalu berat relatif terhadap penghasilan minimum.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-title">📅 Apakah Kondisi Ini Membaik dari Tahun ke Tahun?</div>', unsafe_allow_html=True)
        yc = []
        for y in [2020,2021,2022,2023,2024,2025]:
            dy = main_df[main_df["TAHUN"]==y]
            ok  = (dy["STATUS_LAJANG"]=="Terjangkau").sum()
            nok = (dy["STATUS_LAJANG"]=="Tidak Terjangkau").sum()
            yc.append({"Tahun":y,"Terjangkau":ok,"Housing Stress":nok})
        yc_df = pd.DataFrame(yc)

        fig_bar_trend = go.Figure()
        fig_bar_trend.add_trace(go.Bar(
            x=yc_df["Tahun"], y=yc_df["Terjangkau"],
            name="Terjangkau", marker_color=C_GREEN, opacity=0.9,
        ))
        fig_bar_trend.add_trace(go.Bar(
            x=yc_df["Tahun"], y=yc_df["Housing Stress"],
            name="Housing Stress", marker_color=C_RED, opacity=0.9,
        ))
        fig_bar_trend.update_layout(
            height=320, barmode="stack",
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickmode="linear"),
            yaxis=dict(showgrid=True, gridcolor="#EEE", title="Jumlah Daerah"),
            legend=dict(bgcolor="rgba(255,255,255,0.8)"),
        )
        st.plotly_chart(fig_bar_trend, use_container_width=True)
        st.markdown("""<div class="sec-insight">
            📌 Grafik ini menunjukkan bahwa selama 6 tahun (2020–2025), jumlah daerah yang 
            terjangkau <b>tidak berubah</b> — tetap 5 daerah setiap tahunnya. 
            Ini menandakan bahwa kebijakan KPR FLPP belum cukup untuk mengatasi 
            kesenjangan antara kenaikan UMK dan kenaikan harga/cicilan rumah.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — UMK VS CICILAN (input: tahun)
# ══════════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown(f'<div class="sec-question">💡 Seberapa jauh gap antara UMK tiap daerah dengan cicilan KPR FLPP di tahun {sel_year}? Daerah mana saja yang sudah aman dan mana yang masih tertekan?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">💰 UMK vs Batas Cicilan 30% per Kabupaten/Kota</div>', unsafe_allow_html=True)

    df_s = df_year.sort_values("UMK", ascending=True).copy()
    df_s["COLOR"] = df_s["STATUS_LAJANG"].map({"Terjangkau":C_GREEN,"Tidak Terjangkau":C_RED})
    df_s["LABEL"] = df_s["KABUPATEN_KOTA"].str.replace("KABUPATEN ","KAB. ")

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=df_s["LABEL"], x=df_s["UMK"],
        orientation="h",
        marker_color=df_s["COLOR"],
        text=df_s["UMK"].apply(lambda x: f"Rp {x/1e6:.2f}jt"),
        textposition="outside", textfont=dict(size=9),
        hovertemplate="<b>%{y}</b><br>UMK: Rp %{x:,.0f}<extra></extra>",
        name="UMK",
    ))
    cic = df_year["CICILAN"].iloc[0]
    fig_bar.add_vline(
        x=cic, line_dash="dash", line_color=C_GOLD, line_width=2.5,
        annotation_text=f"  Cicilan KPR: Rp {cic:,.0f}",
        annotation_position="top", annotation_font_color=C_GOLD,
    )
    fig_bar.update_layout(
        height=950, showlegend=False,
        margin=dict(l=10,r=100,t=30,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#EEE", title="UMK (Rp)", tickformat=","),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown(f"""<div class="sec-insight">
        🟢 <b>Bar hijau</b> = UMK melampaui cicilan KPR → daerah <b>terjangkau</b><br>
        🔴 <b>Bar merah</b> = UMK di bawah cicilan KPR → daerah <b>housing stress</b><br>
        🟡 <b>Garis kuning</b> = cicilan KPR FLPP bulanan tahun {sel_year}: <b>Rp {cic:,.0f}</b><br><br>
        📌 Hanya daerah dengan UMK di atas garis kuning yang warganya aman membeli rumah subsidi. 
        Perhatikan betapa sedikitnya daerah hijau dibanding merah.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TREN UMK (input: kabupaten)
# ══════════════════════════════════════════════════════════════════════════════
with t3:
    if sel_kab == "Semua":
        kabs_show = df_year.nlargest(5,"UMK")["KABUPATEN_KOTA"].tolist()
        note = "Top 5 UMK tertinggi se-Jawa Timur"
    else:
        kabs_show = [sel_kab]
        note = sel_kab

    st.markdown(f'<div class="sec-question">📈 Bagaimana perkembangan UMK {note} dari tahun ke tahun? Apakah kenaikannya mampu mengejar kenaikan cicilan KPR?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">📈 Tren UMK vs Cicilan KPR FLPP (2020–2025)</div>', unsafe_allow_html=True)

    trend = main_df[main_df["KABUPATEN_KOTA"].isin(kabs_show)].copy()
    trend["LABEL"] = trend["KABUPATEN_KOTA"].str.replace("KABUPATEN ","KAB. ")
    cic_yr = main_df.groupby("TAHUN")["CICILAN"].first().reset_index()

    colors_line = [C_PURPLE, C_PINK, C_BLUE, C_GREEN, C_GOLD]
    fig_trend = go.Figure()

    for i, kab in enumerate(kabs_show):
        d = trend[trend["KABUPATEN_KOTA"]==kab]
        lbl = kab.replace("KABUPATEN ","KAB. ")
        c = colors_line[i % len(colors_line)]
        # Bar
        fig_trend.add_trace(go.Bar(
            x=d["TAHUN"], y=d["UMK"],
            name=lbl, marker_color=c, opacity=0.6,
            offsetgroup=i,
            hovertemplate=f"<b>{lbl}</b><br>Tahun: %{{x}}<br>UMK: Rp %{{y:,.0f}}<extra></extra>",
        ))
        # Line
        fig_trend.add_trace(go.Scatter(
            x=d["TAHUN"], y=d["UMK"],
            mode="lines+markers", showlegend=False,
            line=dict(color=c, width=2),
            marker=dict(size=6, color=c),
        ))

    fig_trend.add_trace(go.Scatter(
        x=cic_yr["TAHUN"], y=cic_yr["CICILAN"],
        mode="lines+markers", name="Cicilan KPR FLPP",
        line=dict(color=C_RED, dash="dot", width=2.5),
        marker=dict(symbol="diamond", size=9, color=C_RED),
        hovertemplate="Cicilan KPR<br>Tahun: %{x}<br>Rp %{y:,.0f}<extra></extra>",
    ))

    fig_trend.update_layout(
        height=420, barmode="group",
        margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickmode="linear", title="Tahun"),
        yaxis=dict(showgrid=True, gridcolor="#EEE", title="Rp", tickformat=","),
        legend=dict(bgcolor="rgba(255,255,255,0.8)", font=dict(size=11)),
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption(f"Menampilkan: {note} | Bar = UMK, Garis merah putus-putus = Cicilan KPR FLPP")
    st.markdown("""<div class="sec-insight">
        📌 Grafik batang menunjukkan nilai UMK absolut tiap tahun, 
        sedangkan garis merah putus-putus adalah cicilan KPR FLPP. 
        <b>Selama UMK berada di atas garis merah, daerah tersebut terjangkau.</b>
        Perhatikan apakah gap antara UMK dan cicilan makin melebar atau menyempit — 
        itu indikasi apakah kondisi membaik atau memburuk.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PROPERTI & HARGA (no filter, Surabaya only)
# ══════════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown('<div class="sec-question">🏗️ Bagaimana tren harga properti di Jawa Timur? Tipe rumah mana yang harganya naik paling cepat — dan apa artinya bagi masyarakat berpenghasilan rendah?</div>', unsafe_allow_html=True)

    st.info("📍 Data harga properti berasal dari Survei Harga Properti Residensial (SHPR) Bank Indonesia untuk **Kota Surabaya sebagai representasi Jawa Timur**. Data tersedia mulai Q1 2022.", icon="ℹ️")

    ihpr_c = ihpr_df.copy()
    ihpr_c["TAHUN_F"] = ihpr_c["Tahun"].ffill()
    ihpr_c = ihpr_c.dropna(subset=["Triwulan"])
    ihpr_c["PERIODE"] = ihpr_c["TAHUN_F"].astype(int).astype(str) + " " + ihpr_c["Triwulan"]

    # Filter 2020+ (placeholder untuk data yang belum ada)
    ihpr_c = ihpr_c[ihpr_c["TAHUN_F"] >= 2020]

    col_ihpr1, col_ihpr2 = st.columns(2)

    with col_ihpr1:
        st.markdown('<div class="sec-title">📉 Indeks Harga Properti — Surabaya (Representasi Jawa Timur)</div>', unsafe_allow_html=True)
        fig_ihpr = go.Figure()
        for tipe, color, dash in [
            ("Tipe Kecil",   C_PURPLE, "solid"),
            ("Tipe Menengah",C_PINK,   "solid"),
            ("Tipe Besar",   C_BLUE,   "solid"),
        ]:
            fig_ihpr.add_trace(go.Scatter(
                x=ihpr_c["PERIODE"], y=ihpr_c[tipe],
                name=tipe, mode="lines+markers",
                line=dict(width=2.5, color=color, dash=dash),
                marker=dict(size=6),
                hovertemplate=f"<b>{tipe}</b><br>%{{x}}<br>Indeks: %{{y:.2f}}<extra></extra>",
            ))
        fig_ihpr.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor="#EEE", title="Indeks (2018 = 100)"),
            legend=dict(bgcolor="rgba(255,255,255,0.8)"),
        )
        st.plotly_chart(fig_ihpr, use_container_width=True)

    with col_ihpr2:
        st.markdown('<div class="sec-title">💡 Cara Membaca Grafik Ini</div>', unsafe_allow_html=True)
        st.markdown("""<div class="sec-insight" style='margin-top:0;'>
            <b>Apa itu Indeks Harga Properti?</b><br>
            Ini bukan harga asli dalam Rupiah, melainkan angka perbandingan. 
            Baseline-nya adalah harga tahun 2018 = 100. Jadi kalau indeksnya 113, 
            artinya harga sudah naik 13% sejak 2018.<br><br>
            <b>Kenapa rumah kecil indeksnya paling tinggi?</b><br>
            Bukan berarti rumah kecil paling mahal — tapi rumah kecil 
            <b>kenaikannya paling cepat</b> secara persentase sejak 2018. 
            Ini karena permintaan rumah kecil sangat tinggi (banyak orang 
            cari rumah pertama dengan budget terbatas), sehingga harganya 
            terdorong naik lebih cepat.<br><br>
            <b>Apa artinya?</b><br>
            Rumah yang seharusnya paling terjangkau justru naik harganya 
            paling cepat — makin susah dikejar oleh kenaikan UMK.
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sec-insight">
        📌 <b>Kesimpulan:</b> Harga properti terus naik, terutama untuk tipe kecil yang 
        jadi incaran masyarakat berpenghasilan rendah. Kenaikan ini berjalan bersamaan 
        dengan cicilan KPR yang juga naik — sementara UMK banyak daerah tidak mampu 
        mengimbanginya. Inilah inti dari krisis keterjangkauan hunian di Jawa Timur.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SOSIAL EKONOMI (input: tahun + kabupaten)
# ══════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<div class="sec-question">🌍 Apa konteks sosial ekonomi di balik krisis keterjangkauan hunian ini? Bagaimana kondisi kemiskinan, kepemilikan rumah, dan beban utang masyarakat Jawa Timur?</div>', unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown('<div class="sec-title">🏡 Kepemilikan Rumah per Kabupaten/Kota</div>', unsafe_allow_html=True)
        h = housing_df.copy()
        h.columns = ["KAB_KOTA","MILIK_SENDIRI","KONTRAK_SEWA","LAINNYA","TOTAL"]
        for col in ["MILIK_SENDIRI","KONTRAK_SEWA","LAINNYA"]:
            h[col] = pd.to_numeric(
                h[col].astype(str).str.replace("–","0").str.replace(",",""),
                errors="coerce"
            ).fillna(0)
        h = h.dropna(subset=["KAB_KOTA"])

        if sel_kab != "Semua":
            nm = sel_kab.replace("KABUPATEN ","").replace("KOTA ","").title()
            hf = h[h["KAB_KOTA"].str.contains(nm, case=False, na=False)]
            hf = hf if not hf.empty else h
        else:
            hf = h

        hm = hf.melt(id_vars="KAB_KOTA", value_vars=["MILIK_SENDIRI","KONTRAK_SEWA","LAINNYA"],
                     var_name="KATEGORI", value_name="JUMLAH")
        fig_h = px.bar(
            hm, x="KAB_KOTA", y="JUMLAH", color="KATEGORI",
            barmode="stack",
            color_discrete_map={"MILIK_SENDIRI":C_GREEN,"KONTRAK_SEWA":C_RED,"LAINNYA":C_GOLD},
        )
        fig_h.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor="#EEE", title="per 10.000 rumah tangga"),
            legend=dict(bgcolor="rgba(255,255,255,0.8)"),
        )
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown("""<div class="sec-insight">
            📌 Mayoritas masyarakat Jawa Timur sudah memiliki rumah sendiri. 
            Tapi data ini tidak membedakan rumah layak vs tidak layak — 
            dan tidak menjawab apakah mereka <i>mampu</i> membeli rumah baru 
            jika rumahnya rusak atau anaknya sudah dewasa dan butuh hunian sendiri.
        </div>""", unsafe_allow_html=True)

    with col_s2:
        st.markdown('<div class="sec-title">💳 Tabungan vs Pinjaman Konsumsi Jawa Timur</div>', unsafe_allow_html=True)
        fin = fin_df.copy()
        fin["RASIO"] = (fin["PINJAMAN"] / fin["TABUNGAN"] * 100).round(1)

        fig_fin = go.Figure()
        fig_fin.add_trace(go.Bar(
            x=fin["TAHUN"], y=fin["TABUNGAN"],
            name="Total Tabungan", marker_color=C_BLUE, opacity=0.8,
        ))
        fig_fin.add_trace(go.Bar(
            x=fin["TAHUN"], y=fin["PINJAMAN"],
            name="Pinjaman Konsumsi", marker_color=C_PINK, opacity=0.8,
        ))
        fig_fin.add_trace(go.Scatter(
            x=fin["TAHUN"], y=fin["RASIO"],
            name="Rasio Pinjaman/Tabungan (%)",
            mode="lines+markers", yaxis="y2",
            line=dict(color=C_RED, width=2.5, dash="dot"),
            marker=dict(size=8, color=C_RED),
        ))
        fig_fin.update_layout(
            height=380, barmode="group",
            margin=dict(l=0,r=60,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickmode="linear"),
            yaxis=dict(showgrid=True, gridcolor="#EEE", title="Juta Rupiah", tickformat=","),
            yaxis2=dict(overlaying="y", side="right", title="Rasio (%)", showgrid=False),
            legend=dict(bgcolor="rgba(255,255,255,0.8)", font=dict(size=10)),
        )
        st.plotly_chart(fig_fin, use_container_width=True)
        st.markdown("""<div class="sec-insight">
            📌 Meski tabungan masyarakat terus naik, pinjaman konsumsi 
            (termasuk KPR, kredit kendaraan, KTA) naik lebih cepat secara proporsi. 
            Rasio pinjaman terhadap tabungan meningkat dari 58% (2020) menjadi 64% (2025) — 
            menunjukkan tekanan finansial yang makin besar pada masyarakat.
        </div>""", unsafe_allow_html=True)

    # Garis Kemiskinan
    st.markdown('<div class="sec-title">📉 Tren Garis Kemiskinan Jawa Timur (2020–2025)</div>', unsafe_allow_html=True)
    pov = poverty_df.copy()
    pov.columns = ["PERIODE","GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]
    for c in ["GK_KOTA","GK_DESA","MISKIN_KOTA","MISKIN_DESA","TOTAL_MISKIN"]:
        pov[c] = pd.to_numeric(pov[c].astype(str).str.replace(",",""), errors="coerce")
    pov = pov.dropna(subset=["PERIODE"])
    # Filter 2020+
    pov_f = pov[pov["PERIODE"].astype(str).str.contains("2020|2021|2022|2023|2024|2025")]

    cp1, cp2 = st.columns(2)
    with cp1:
        fig_p1 = go.Figure()
        fig_p1.add_trace(go.Scatter(
            x=pov_f["PERIODE"], y=pov_f["GK_KOTA"],
            name="Perkotaan", mode="lines+markers",
            line=dict(color=C_PURPLE, width=2.5), marker=dict(size=6),
        ))
        fig_p1.add_trace(go.Scatter(
            x=pov_f["PERIODE"], y=pov_f["GK_DESA"],
            name="Perdesaan", mode="lines+markers",
            line=dict(color=C_GREEN, width=2.5), marker=dict(size=6),
        ))
        fig_p1.update_layout(
            title="Garis Kemiskinan (Rp/Kapita/Bulan)",
            height=280, margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor="#EEE", tickformat=","),
            legend=dict(bgcolor="rgba(255,255,255,0.8)"),
        )
        st.plotly_chart(fig_p1, use_container_width=True)
    with cp2:
        fig_p2 = px.area(
            pov_f, x="PERIODE", y="TOTAL_MISKIN",
            color_discrete_sequence=[C_RED],
        )
        fig_p2.update_layout(
            title="Total Penduduk Miskin (ribu jiwa)",
            height=280, margin=dict(l=0,r=0,t=40,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(showgrid=True, gridcolor="#EEE", title="ribu jiwa"),
        )
        st.plotly_chart(fig_p2, use_container_width=True)
    st.markdown("""<div class="sec-insight">
        📌 Garis kemiskinan terus naik — artinya biaya hidup minimum makin mahal. 
        Ini berjalan bersamaan dengan cicilan KPR yang juga naik. 
        Masyarakat terjepit dari dua arah: kebutuhan hidup makin mahal, 
        sekaligus beban cicilan rumah makin berat — sementara UMK tidak naik secepat keduanya.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — CEK KEMAMPUANMU
# ══════════════════════════════════════════════════════════════════════════════
with t6:
    st.markdown('<div class="sec-question">🧮 Dengan gaji yang kamu punya sekarang, mampukah kamu membeli rumah subsidi KPR FLPP di daerahmu? Yuk hitung langsung!</div>', unsafe_allow_html=True)

    st.markdown("""<div class="sec-insight" style='margin-bottom:16px;'>
        <b>Cara kerja kalkulator ini:</b><br>
        Kita pakai <b>The 30% Rule</b> — aturan internasional yang menyatakan bahwa 
        cicilan hunian sebaiknya tidak melebihi 30% dari penghasilan bulanan. 
        Jika melebihi 30%, kamu masuk kategori <i>Housing Stress</i> — 
        terlalu banyak penghasilan yang habis hanya untuk membayar tempat tinggal.
    </div>""", unsafe_allow_html=True)

    ck1, ck2, ck3 = st.columns(3)
    with ck1:
        user_gaji = st.number_input(
            "💰 Gaji / Penghasilan Bulananmu (Rp)",
            min_value=0, max_value=50000000,
            value=3000000, step=100000,
            format="%d",
        )
    with ck2:
        user_kab = st.selectbox("📍 Daerahmu", KAB_LIST, key="calc_kab")
    with ck3:
        user_year = st.selectbox("📅 Tahun", [2020,2021,2022,2023,2024,2025], index=5, key="calc_year")

    if st.button("🔍 Hitung Sekarang!", type="primary"):
        row = main_df[(main_df["KABUPATEN_KOTA"]==user_kab) & (main_df["TAHUN"]==user_year)]
        if not row.empty:
            cic_val   = float(row["CICILAN"].iloc[0])
            umk_val   = float(row["UMK"].iloc[0])
            garis_k   = float(row["GARIS_KEMISKINAN"].iloc[0])
            batas_30  = user_gaji * 0.3
            pct_gaji  = (cic_val / user_gaji * 100) if user_gaji > 0 else 0
            sisa      = user_gaji - cic_val
            is_aman   = cic_val <= batas_30

            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.metric("Gaji Kamu", f"Rp {user_gaji:,.0f}")
            with r2:
                st.metric("Cicilan KPR FLPP", f"Rp {cic_val:,.0f}")
            with r3:
                st.metric("Batas Aman (30%)", f"Rp {batas_30:,.0f}")
            with r4:
                st.metric("% Gaji untuk Cicilan", f"{pct_gaji:.1f}%",
                          delta=f"{'✅ Aman' if is_aman else '⚠️ Stress'}",
                          delta_color="normal" if is_aman else "inverse")

            if is_aman:
                st.markdown(f"""<div class="calc-result aman">
                    <h2>✅ Kamu Terjangkau!</h2>
                    <p>Dengan gaji <b>Rp {user_gaji:,.0f}</b> di <b>{user_kab}</b>, 
                    cicilan KPR FLPP hanya memakan <b>{pct_gaji:.1f}%</b> penghasilanmu — 
                    masih di bawah batas aman 30%. Sisamu setelah cicilan: <b>Rp {sisa:,.0f}/bulan</b>.</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="calc-result stress">
                    <h2>⚠️ Kamu Masuk Housing Stress!</h2>
                    <p>Dengan gaji <b>Rp {user_gaji:,.0f}</b> di <b>{user_kab}</b>, 
                    cicilan KPR FLPP akan memakan <b>{pct_gaji:.1f}%</b> penghasilanmu — 
                    melebihi batas aman 30%. Sisamu hanya <b>Rp {sisa:,.0f}/bulan</b> 
                    untuk semua kebutuhan hidup lainnya.</p>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""<div class="sec-insight" style='margin-top:16px;'>
                <b>Konteks tambahan:</b><br>
                • UMK resmi di {user_kab} tahun {user_year}: <b>Rp {umk_val:,.0f}</b><br>
                • Garis kemiskinan per kapita: <b>Rp {garis_k:,.0f}/bulan</b><br>
                • Gaji minimum agar KPR FLPP terjangkau: <b>Rp {cic_val/0.3:,.0f}/bulan</b><br>
                • {'Gajimu sudah di atas UMK daerah ini ✅' if user_gaji >= umk_val else f'Gajimu masih di bawah UMK daerah ini (selisih Rp {umk_val-user_gaji:,.0f}) ⚠️'}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — TABEL & GLOSARIUM
# ══════════════════════════════════════════════════════════════════════════════
with t7:
    tab7a, tab7b = st.tabs(["📋 Tabel Data", "📚 Glosarium & Metodologi"])

    with tab7a:
        st.markdown(f'<div class="sec-title">📋 Data Lengkap Keterjangkauan — {sel_year}</div>', unsafe_allow_html=True)
        tbl = df_year[["KABUPATEN_KOTA","UMK","BATAS_30","CICILAN","STATUS_LAJANG","STATUS_KELUARGA"]].copy()
        tbl.columns = ["Kabupaten/Kota","UMK (Rp)","Batas 30% (Rp)","Cicilan KPR (Rp)","Status Lajang","Status Keluarga Kecil"]
        tbl.index = range(1, len(tbl)+1)

        def style_s(val):
            if val == "Terjangkau":
                return "background-color:#d4f5e9;color:#1a7a57;font-weight:600"
            elif val == "Tidak Terjangkau":
                return "background-color:#fde8e8;color:#b71c1c;font-weight:600"
            return ""

        styled = tbl.style\
            .map(style_s, subset=["Status Lajang","Status Keluarga Kecil"])\
            .format({"UMK (Rp)":"Rp {:,.0f}","Batas 30% (Rp)":"Rp {:,.0f}","Cicilan KPR (Rp)":"Rp {:,.0f}"})
        st.dataframe(styled, use_container_width=True, height=500)

        csv = tbl.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv,
                           f"housing_jatim_{sel_year}.csv", "text/csv")

        st.markdown("""<div class="sec-insight" style='margin-top:16px;'>
            <b>Catatan tentang kolom Status Lajang vs Status Keluarga Kecil:</b><br>
            Pada data ini, kedua kolom menunjukkan hasil yang sama karena cicilan KPR FLPP 
            tidak dibedakan berdasarkan status pernikahan. Secara teori, keluarga kecil 
            (2 dewasa + 1 anak) seharusnya memiliki beban yang lebih berat karena 
            sisa UMK setelah cicilan harus mencukupi kebutuhan lebih banyak orang. 
            Ini menjadi limitasi analisis yang dapat dikembangkan pada penelitian selanjutnya.
        </div>""", unsafe_allow_html=True)

    with tab7b:
        st.markdown('<div class="sec-title">📚 Glosarium Istilah</div>', unsafe_allow_html=True)

        terms = [
            ("UMK (Upah Minimum Kabupaten/Kota)",
             "Batas upah minimum yang harus dibayarkan pengusaha kepada pekerja di suatu kabupaten/kota. Ditetapkan setiap tahun oleh Gubernur berdasarkan rekomendasi Dewan Pengupahan. UMK berbeda-beda tiap daerah — Surabaya punya UMK tertinggi, sedangkan daerah pelosok seperti Pacitan punya UMK terendah."),
            ("KPR FLPP (Fasilitas Likuiditas Pembiayaan Perumahan)",
             "Program kredit rumah bersubsidi dari pemerintah dengan bunga rendah (5% per tahun) dan tenor panjang (hingga 20 tahun). Ditujukan untuk masyarakat berpenghasilan rendah (MBR). Cicilan KPR FLPP lebih rendah dari KPR komersial biasa karena ada subsidi bunga dari pemerintah."),
            ("The 30% Rule",
             "Aturan internasional yang menyatakan bahwa pengeluaran untuk hunian (termasuk cicilan KPR) sebaiknya tidak melebihi 30% dari penghasilan bulanan. Jika melebihi 30%, seseorang dianggap mengalami 'housing stress' — terlalu banyak penghasilan yang habis hanya untuk tempat tinggal, menyisakan sedikit untuk kebutuhan lain."),
            ("Housing Stress",
             "Kondisi ketika seseorang atau rumah tangga harus mengeluarkan lebih dari 30% penghasilannya untuk biaya hunian. Dalam konteks ini, daerah disebut 'housing stress' jika cicilan KPR FLPP melebihi 30% UMK-nya — artinya pekerja dengan gaji UMK tidak akan mampu membeli rumah subsidi tanpa tertekan secara finansial."),
            ("IHPR (Indeks Harga Properti Residensial)",
             "Indeks yang dihitung Bank Indonesia untuk mengukur perubahan harga properti dari waktu ke waktu. Baseline-nya adalah tahun 2018 = 100. Jika IHPR = 113, artinya harga properti sudah naik 13% sejak 2018. Ini bukan harga absolut, melainkan ukuran kecepatan kenaikan."),
            ("Garis Kemiskinan",
             "Nilai pengeluaran minimum per kapita per bulan yang dibutuhkan seseorang untuk memenuhi kebutuhan dasar (makanan dan non-makanan). Dihitung oleh BPS dua kali setahun (Maret dan September). Jika pengeluaran seseorang di bawah garis ini, dia dianggap miskin."),
        ]

        for term, defn in terms:
            st.markdown(f"""<div class="glossary-box">
                <div class="glossary-term">📌 {term}</div>
                <div class="glossary-def">{defn}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title">🔢 Metodologi Perhitungan</div>', unsafe_allow_html=True)
        st.markdown("""<div class="sec-insight">
            <b>Formula Utama:</b><br><br>
            <code>Batas 30% = UMK × 30%</code><br>
            <code>Status = "Terjangkau" jika Cicilan KPR ≤ Batas 30%, sebaliknya "Tidak Terjangkau"</code><br><br>
            <b>Contoh (Kota Surabaya 2025):</b><br>
            • UMK = Rp 4.961.753<br>
            • Batas 30% = Rp 4.961.753 × 30% = Rp 1.488.526<br>
            • Cicilan KPR FLPP = Rp 1.084.572<br>
            • Rp 1.084.572 ≤ Rp 1.488.526 → <b>Terjangkau ✅</b><br><br>
            <b>Contoh (Kabupaten Malang 2025):</b><br>
            • UMK = Rp 3.553.530<br>
            • Batas 30% = Rp 3.553.530 × 30% = Rp 1.066.059<br>
            • Cicilan KPR FLPP = Rp 1.084.572<br>
            • Rp 1.084.572 > Rp 1.066.059 → <b>Tidak Terjangkau ❌</b>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;margin-top:30px;padding:16px;
     background:linear-gradient(135deg,#2D2B55,#4A3F9F);
     border-radius:12px;color:rgba(255,255,255,0.7);font-size:12px;'>
    Dashboard Analisis Keterjangkauan Hunian Jawa Timur 2020–2025 &nbsp;|&nbsp; 
    Data: SK UMK Jawa Timur · SHPR Bank Indonesia · BPS Jawa Timur · SEKDA Jawa Timur
</div>
""", unsafe_allow_html=True)
