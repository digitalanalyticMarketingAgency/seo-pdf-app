import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import random
import base64
from weasyprint import HTML
agency_name = "Digital Analytic"
import base64
from weasyprint import HTML

agency_name = "Digital Analytic"  # এই লাইনটি এখানে বসান

st.set_page_config(page_title="SEO Performance Report Generator", page_icon="📈", layout="wide")

st.set_page_config(page_title="SEO Performance Report Generator", page_icon="📈", layout="wide")

# ============================================================
# CUSTOM CSS
# ============================================================
# এটি ২০ নম্বর লাইনের জায়গায় বসান (এর আগে কোনো স্পেস দেবেন না)
st.markdown("""
<style>
   /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] {{
        background-color: #0f172a !important;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stSidebarContent"] {{
        background-color: #0f172a !important;
    }}

    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    .stTextInput input, .stNumberInput input {{
        color: black !important;
    }}

    /* Metric Cards */
    .metric-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
    }}
    .metric-card .label {{
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .metric-card .value {{
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 6px;
    }}

    /* Backlink Cards */
    .backlink-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }}
    .backlink-card .label {{
        font-size: 10px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
    }}
    .backlink-card .value {{
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
    }}

    /* Traffic Summary & Others */
    .traffic-summary-label {{
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .traffic-summary-value {{
        font-size: 40px;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.2;
    }}
    .error-row {{
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-weight: 600;
    }}
    .warn-row {{
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-weight: 600;
    }}
    .thankyou-box {{
        text-align: center;
        padding: 60px 20px;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #0f172a;
    }}
</style>
""", unsafe_allow_html=True)

st.title("📈 SEO Performance Report Generator")
st.caption("Manually enter your SEO data below to generate a live dashboard and export a professional PDF report.")

# ============================================================
# SIDEBAR — MANUAL DATA INPUT
# ============================================================
with st.sidebar:
    st.header("⚙️ Report Settings")
# ১০২ নম্বর লাইনের জায়গায় এই কোডটি দিন:
    st.image("digital-analytic-logo.png", width=150)
    report_date = st.text_input("Reporting Period", value=datetime.date.today().strftime("%B %Y"))

    st.divider()
    st.header("1️⃣ Search Console")
    sc_date = st.text_input("Timeframe / Date", value="Last 28 Days")
    sc_clicks = st.number_input("Total Clicks", min_value=0, value=450, step=1)
    sc_impressions = st.number_input("Total Impressions", min_value=0, value=17600, step=100)
    sc_ctr = st.number_input("Average CTR (%)", min_value=0.0, value=2.6, step=0.1, format="%.2f")
    sc_position = st.number_input("Average Position", min_value=0.0, value=14.3, step=0.1, format="%.1f")

    st.divider()
    st.header("2️⃣ Revenue & Traffic")
    rt_visit = st.number_input("Visits", min_value=0, value=9238, step=1)
    rt_revenue = st.number_input("Total Revenue ($)", min_value=0.0, value=5934.48, step=0.01, format="%.2f")
    rt_impression = st.number_input("Impressions", min_value=0, value=17600, step=1)
    rt_ecommerce = st.number_input("Ecommerce Purchases", min_value=0, value=423, step=1)
    rt_purchase_revenue = st.number_input("Purchases Revenue ($)", min_value=0.0, value=9785.37, step=0.01, format="%.2f")
    rt_transaction = st.number_input("Transactions", min_value=0, value=823, step=1)

    st.divider()
    st.header("3️⃣ Keyword Ranking Distribution")
    kw_1_15 = st.number_input("1 to 15 result", min_value=0, value=42, step=1)
    kw_16_30 = st.number_input("16 to 30 result", min_value=0, value=28, step=1)
    kw_31_45 = st.number_input("31 to 45 result", min_value=0, value=19, step=1)
    kw_46_60 = st.number_input("46 to 60 result", min_value=0, value=12, step=1)
    kw_60_100 = st.number_input("60 to 100 result", min_value=0, value=8, step=1)

    st.divider()
    st.header("4️⃣ Backlink Profile")
    bl_profile = st.number_input("Profile Backlinks", min_value=0, value=335300, step=100)
    bl_citation = st.number_input("Citation", min_value=0, value=32000, step=100)
    bl_web2 = st.number_input("Web 2.0", min_value=0, value=97400, step=100)
    bl_social = st.number_input("Social Share", min_value=0, value=237800, step=100)
    bl_guest = st.number_input("Guest Post", min_value=0, value=51900, step=100)
    bl_comment = st.number_input("Comment Backlink", min_value=0, value=16900, step=100)

    st.divider()
    st.header("5️⃣ Traffic Analytics Summary")
    ta_click = st.number_input("Click", min_value=0, value=872700, step=100)
    ta_impression = st.number_input("Total Impression", min_value=0, value=248800000, step=1000)
    ta_ctr = st.number_input("CTR (%)", min_value=0.0, value=5.36, step=0.01, format="%.2f")
    ta_position = st.number_input("Average Position ", min_value=0.0, value=13.38, step=0.01, format="%.2f")

    st.divider()
    st.header("6️⃣ Technical SEO & Indexing")
    tech_indexed = st.number_input("Indexing Page (Valid)", min_value=0, value=1240, step=1)
    tech_404 = st.number_input("Not Found (404)", min_value=0, value=3, step=1)
    tech_crawled_not_indexed = st.number_input("Crawled - Not Indexed", min_value=0, value=42, step=1)
    tech_discovered_not_indexed = st.number_input("Discovered - Not Indexed", min_value=0, value=18, step=1)


# ============================================================
# HELPER FORMATTERS
# ============================================================
def fmt_int(v):
    return f"{int(v):,}"


def fmt_money(v):
    return f"${v:,.2f}"


def fmt_compact(v):
    """Compact number formatting: 335300 -> 335.3K, 248800000 -> 248.8M"""
    v = float(v)
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return f"{v:.0f}"


# ============================================================
# SECTION 1 — SEARCH CONSOLE PERFORMANCE GRAPH
# ============================================================
st.header("1. Search Console Performance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card"><div class="label">Total Clicks</div>
    <div class="value">{fmt_int(sc_clicks)}</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card"><div class="label">Total Impressions</div>
    <div class="value">{fmt_int(sc_impressions)}</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card"><div class="label">Average CTR</div>
    <div class="value">{sc_ctr:.2f}%</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card"><div class="label">Average Position</div>
    <div class="value">{sc_position:.1f}</div></div>""", unsafe_allow_html=True)

st.write("")

# ── 7-day synthetic trend (seed fixed per session values so curve stays stable on re-render)
_seed = int(sc_clicks + sc_impressions)
_rng = random.Random(_seed)

def _trend(final_val, n=7, volatility=0.12):
    """Generate n daily values that end at final_val with realistic variation."""
    base = final_val / n
    days = []
    for i in range(n):
        noise = _rng.uniform(1 - volatility, 1 + volatility)
        # Slight upward drift toward the end
        drift = 0.85 + 0.15 * (i / (n - 1))
        days.append(max(0, round(base * drift * noise)))
    # Scale last point to match the entered total
    scale = final_val / max(sum(days), 1)
    days = [round(d * scale) for d in days]
    days[-1] = final_val  # pin the last point exactly
    return days

today = datetime.date.today()
trend_dates = [(today - datetime.timedelta(days=6 - i)).strftime("%b %d") for i in range(7)]
clicks_trend = _trend(sc_clicks)
impressions_trend = _trend(sc_impressions)

sc_fig = go.Figure()
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=clicks_trend,
    mode="lines+markers", name="Clicks",
    line=dict(color="#4285F4", width=3),
    marker=dict(size=7),
    yaxis="y1"
))
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=impressions_trend,
    mode="lines+markers", name="Impressions",
    line=dict(color="#8E24AA", width=3),
    marker=dict(size=7),
    yaxis="y2"
))
sc_fig.update_layout(
    height=320,
    margin=dict(l=60, r=60, t=30, b=30),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    yaxis=dict(title=dict(text="Clicks", font=dict(color="#4285F4")), tickfont=dict(color="#4285F4"), showgrid=True, gridcolor="#f1f5f9"),
    yaxis2=dict(title=dict(text="Impressions", font=dict(color="#8E24AA")), tickfont=dict(color="#8E24AA"),
                overlaying="y", side="right", showgrid=False),
    xaxis=dict(title=None, showgrid=False)
)
st.plotly_chart(sc_fig, use_container_width=True)
st.caption("Trend shows estimated daily distribution across the last 7 days based on your total figures. Enter per-day data for exact trends.")

st.divider()

# ============================================================
# SECTION 2 — REVENUE & TRAFFIC DASHBOARD (3x2 card grid)
# ============================================================
st.header("2. Revenue & Traffic Dashboard")

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1:
    st.markdown(f"""<div class="metric-card">🧑‍💻<div class="label">Visit</div>
    <div class="value">{fmt_int(rt_visit)}</div></div>""", unsafe_allow_html=True)
with r1c2:
    st.markdown(f"""<div class="metric-card">💵<div class="label">Total Revenue</div>
    <div class="value">{fmt_money(rt_revenue)}</div></div>""", unsafe_allow_html=True)
with r1c3:
    st.markdown(f"""<div class="metric-card">👁️<div class="label">Impression</div>
    <div class="value">{fmt_int(rt_impression)}</div></div>""", unsafe_allow_html=True)
with r2c1:
    st.markdown(f"""<div class="metric-card">🛒<div class="label">Ecommerce Purchases</div>
    <div class="value">{fmt_int(rt_ecommerce)}</div></div>""", unsafe_allow_html=True)
with r2c2:
    st.markdown(f"""<div class="metric-card">💰<div class="label">Purchases Revenue</div>
    <div class="value">{fmt_money(rt_purchase_revenue)}</div></div>""", unsafe_allow_html=True)
with r2c3:
    st.markdown(f"""<div class="metric-card">🧾<div class="label">Transaction</div>
    <div class="value">{fmt_int(rt_transaction)}</div></div>""", unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 3 — TOP KEYWORD RANKING DISTRIBUTION
# ============================================================
st.header("3. Top Keyword Ranking Distribution")

kw_labels = ["1 to 15", "16 to 30", "31 to 45", "46 to 60", "60 to 100"]
kw_values = [kw_1_15, kw_16_30, kw_31_45, kw_46_60, kw_60_100]
kw_colors = ["#2563eb", "#8b5cf6", "#f59e0b", "#ef4444", "#64748b"]

kw_fig = go.Figure(go.Bar(
    x=kw_values,
    y=kw_labels,
    orientation="h",
    marker_color=kw_colors,
    text=kw_values,
    textposition="outside",
))
kw_fig.update_layout(
    height=320,
    margin=dict(l=60, r=50, t=20, b=60),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(title="Number of Keywords"),
    yaxis=dict(title="Ranking Position", autorange="reversed")
)
st.plotly_chart(kw_fig, use_container_width=True)

st.divider()

# ============================================================
# SECTION 4 — BACKLINK PROFILE (cards + donut chart)
# ============================================================
st.header("4. Backlink Profile")

bl_labels = ["Profile Backlinks", "Citation", "Web 2.0", "Social Share", "Guest Post", "Comment Backlink"]
bl_values = [bl_profile, bl_citation, bl_web2, bl_social, bl_guest, bl_comment]
bl_colors = ["#2563eb", "#8b5cf6", "#16a34a", "#f59e0b", "#ef4444", "#06b6d4"]

bl_col1, bl_col2 = st.columns([1, 1])

with bl_col1:
    card_cols = st.columns(2)
    for i, (label, value) in enumerate(zip(bl_labels, bl_values)):
        with card_cols[i % 2]:
            st.markdown(f"""<div class="backlink-card"><div class="label">{label}</div>
            <div class="value">{fmt_compact(value)}</div></div>""", unsafe_allow_html=True)
with bl_col2:
    donut_fig = go.Figure(go.Pie(
        labels=bl_labels,
        values=bl_values,
        hole=0.55,
        marker=dict(colors=bl_colors),
        textinfo="percent",
    ))
    
    donut_fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=20, b=90),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3)
    )
    
    st.plotly_chart(donut_fig, use_container_width=True)
st.divider()

# ============================================================
# SECTION 5 — TRAFFIC ANALYTICS SUMMARY (typography-led)
# ============================================================
st.header("5. Traffic Analytics Summary")

ta_col1, ta_col2, ta_col3, ta_col4 = st.columns(4)
with ta_col1:
    st.markdown(f"""<div class="traffic-summary-label">Click</div>
    <div class="traffic-summary-value">{fmt_compact(ta_click)}</div>""", unsafe_allow_html=True)
with ta_col2:
    st.markdown(f"""<div class="traffic-summary-label">Total Impression</div>
    <div class="traffic-summary-value">{fmt_compact(ta_impression)}</div>""", unsafe_allow_html=True)
with ta_col3:
    st.markdown(f"""<div class="traffic-summary-label">CTR</div>
    <div class="traffic-summary-value">{ta_ctr:.2f}%</div>""", unsafe_allow_html=True)
with ta_col4:
    st.markdown(f"""<div class="traffic-summary-label">Average Position</div>
    <div class="traffic-summary-value">{ta_position:.2f}</div>""", unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 6 — TECHNICAL SEO & INDEXING HEALTH
# ============================================================
st.header("6. Technical SEO & Indexing Health")

tech_col1, tech_col2 = st.columns([1, 1.4])

with tech_col1:
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tech_indexed,
        number={"font": {"size": 36, "color": "#16a34a"}},
        title={"text": "Indexed Pages (Valid)", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, max(tech_indexed * 1.2, 1)], "visible": False},
            "bar": {"color": "#16a34a"},
            "bgcolor": "#f1f5f9",
            "borderwidth": 0,
        }
    ))
    gauge_fig.update_layout(height=260, margin=dict(l=40, r=40, t=40, b=30))
    st.plotly_chart(gauge_fig, use_container_width=True)

with tech_col2:
    st.markdown("**Errors & Warnings**")
    st.markdown(f"""<div class="error-row">🔴 Not Found (404): <b>{fmt_int(tech_404)}</b> pages</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="warn-row">🟠 Crawled — Currently Not Indexed: <b>{fmt_int(tech_crawled_not_indexed)}</b> pages</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="warn-row">🟠 Discovered — Currently Not Indexed: <b>{fmt_int(tech_discovered_not_indexed)}</b> pages</div>""", unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 7 — FINAL THANK YOU PAGE (preview)
# ============================================================
st.header("7. Closing Page Preview")
st.markdown("""
<div style="text-align: center; padding: 40px 20px;">
    <h1>Thank You!</h1>
    <p style="max-width:600px; margin:0 auto; color:#64748b; font-size:15px; line-height:1.7;">
        Thank you for taking the time to review this SEO performance report. We are committed to driving
        continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings
        for your business. Should you have any questions, please feel free to reach out to us.
    </p>
    <p style="margin-top:30px; color:#94a3b8; font-size:13px;">
        Digital Analytic &nbsp;|&nbsp; June 2026
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ============================================================
# PDF GENERATION
# ============================================================
def fig_to_base64(fig, width=700, height=300):
    """Convert a Plotly figure to a base64-encoded PNG for PDF embedding."""
    img_bytes = pio.to_image(fig, format="png", width=width, height=height, scale=2)
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f'<img src="data:image/png;base64,{b64}" style="width:100%; border-radius:8px;" />'
def build_kw_bar_html():
    max_kw = max(kw_values) if max(kw_values) > 0 else 1
    rows = ""
    for label, value, color in zip(kw_labels, kw_values, kw_colors):
        width_pct = int((value / max_kw) * 100)
        rows += f"""
        <tr>
          <td style="width:90px; font-size:9pt; font-weight:700; color:#64748b;">{label}</td>
          <td>
            <div style="background:#f1f5f9; border-radius:4px; height:12px; width:100%;">
              <div style="background:{color}; border-radius:4px; height:12px; width:{width_pct}%;"></div>
            </div>
          </td>
          <td style="width:40px; text-align:right; font-weight:800; font-size:10pt;">{value}</td>
        </tr>"""
    return f'<table style="width:100%; border-collapse:collapse;">{rows}</table>'


def build_backlink_rows_html():
    rows = ""
    for label, value in zip(bl_labels, bl_values):
        rows += f"""
        <tr>
          <td style="padding:6px 0;">{label}</td>
          <td style="padding:6px 0; text-align:right; font-weight:800;">{fmt_compact(value)}</td>
        </tr>"""
    return f'<table style="width:100%; border-collapse:collapse; font-size:11pt;">{rows}</table>'


# আগের লাইনটি ডিলিট করে এটি বসান:
def build_pdf_html(agency_name, report_date, sc_clicks, sc_impressions, sc_ctr, sc_position, rt_visit, rt_revenue, rt_impression, rt_ecommerce, rt_purchase_revenue, rt_transaction, tech_indexed, tech_404, tech_crawled_not_indexed, tech_discovered_not_indexed, sc_date, ta_click, ta_impression, ta_ctr, ta_position):
    kw_bars_html = build_kw_bar_html()
    backlink_rows_html = build_backlink_rows_html()

    # ── Build chart images for PDF ──────────────────────────────
    # Search Console trend chart
    sc_pdf_fig = go.Figure()
    sc_pdf_fig.add_trace(go.Scatter(
        x=trend_dates, y=clicks_trend,
        mode="lines+markers", name="Clicks",
        line=dict(color="#4285F4", width=2), marker=dict(size=5), yaxis="y1"
    ))
    sc_pdf_fig.add_trace(go.Scatter(
        x=trend_dates, y=impressions_trend,
        mode="lines+markers", name="Impressions",
        line=dict(color="#8E24AA", width=2), marker=dict(size=5), yaxis="y2"
    ))
    sc_pdf_fig.update_layout(
        height=260, margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        yaxis=dict(tickfont=dict(color="#4285F4", size=8), showgrid=True, gridcolor="#f1f5f9"),
        yaxis2=dict(tickfont=dict(color="#8E24AA", size=8), overlaying="y", side="right", showgrid=False),
        xaxis=dict(tickfont=dict(size=8), showgrid=False),
    )
    sc_chart_html = fig_to_base64(sc_pdf_fig, width=680, height=260)

    # Keyword bar chart
    kw_pdf_fig = go.Figure(go.Bar(
        x=kw_values, y=kw_labels, orientation="h",
        marker_color=kw_colors, text=kw_values, textposition="outside",
    ))
    kw_pdf_fig.update_layout(
        height=220, margin=dict(l=10, r=30, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="Number of Keywords", tickfont=dict(size=8)),
        yaxis=dict(autorange="reversed", tickfont=dict(size=8)),
    )
    kw_chart_html = fig_to_base64(kw_pdf_fig, width=680, height=220)

    # Backlink donut chart
    bl_pdf_fig = go.Figure(go.Pie(
        labels=bl_labels, values=bl_values, hole=0.55,
        marker=dict(colors=bl_colors), textinfo="percent",
    ))
    bl_pdf_fig.update_layout(
        height=260, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=8)),
    )
    bl_chart_html = fig_to_base64(bl_pdf_fig, width=340, height=260)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    /* পিডিএফ পেজ সেটিংস */
    @page {{ size: A4; margin: 0; }} 
    
    body {{ 
        font-family: 'Segoe UI', Arial, sans-serif; 
        margin: 0; 
        padding: 0; 
        color: #e2e8f0; 
        background-color: #0b0f19;
        background-image: url('https://raw.githubusercontent.com/digitalanalyticMarketingAgency/seo-pdf-app/main/a4.png');
        background-size: 210mm 297mm;
        background-repeat: repeat; 
    }}
    
    /* কন্টেন্ট কন্টেইনার */
    .main-container { padding: 40px 35px 80px 35px; }
    
    /* হেডার সেকশন */
    .header-banner { 
        background-color: rgba(19, 17, 28, 0.85); 
        border: 1px solid rgba(139, 92, 246, 0.3); 
        color: #ffffff; 
        padding: 30px 20px; 
        text-align: center; 
        border-radius: 12px; 
        margin-bottom: 30px; 
        page-break-inside: avoid;
    }
    .header-title { font-size: 24pt; font-weight: 800; text-transform: uppercase; margin: 0; }
    
    /* সেকশন হেডিং */
    h2 { 
        font-size: 16pt; 
        color: #ffffff; 
        margin-top: 30px; 
        margin-bottom: 20px; 
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
        page-break-after: avoid; 
    }
    
    /* পিডিএফ-এর জন্য নিরাপদ গ্রিড সিস্টেম (Table Layout) */
    .grid { display: table; width: 100%; border-spacing: 15px; margin-bottom: 20px; }
    .card { 
        display: table-cell; 
        width: 33%; 
        background-color: rgba(17, 24, 39, 0.85); 
        border: 1px solid rgba(255,255,255,0.05); 
        border-top: 2px solid #8b5cf6; 
        border-radius: 12px; 
        padding: 25px 10px; 
        text-align: center;
        page-break-inside: avoid;
    }
    .label { font-size: 9pt; color: #9ca3af; text-transform: uppercase; margin-bottom: 8px; display: block; }
    .value { font-size: 20pt; font-weight: 800; color: #ffffff; display: block; }
    
    /* চার্ট স্টাইল */
    img { 
        max-width: 90%; 
        display: block; 
        margin: 10px auto; 
        border: 5px solid #1f2937; 
        border-radius: 12px; 
        page-break-inside: avoid; 
    }
    
    /* ওয়ার্নিং বক্স */
    .error-box, .warn-box { 
        display: block; 
        width: 95%; 
        margin: 10px auto; 
        padding: 15px; 
        border-radius: 8px; 
        background-color: rgba(69, 10, 10, 0.85); 
        border-left: 5px solid #ef4444; 
        page-break-inside: avoid; 
    }
    
    /* ফুটার ফিক্স (নিরাপদ অবস্থান) */
    .footer { 
        position: absolute; 
        bottom: 20px; 
        width: 100%; 
        text-align: center; 
        font-size: 10pt; 
        color: #9ca3af; 
    }
</style>
</head>
<body>
<div class="main-container">

<div class="header-banner">
    <div class="header-title">SEO Performance Report</div>
    <div class="header-subtitle">{agency_name} &nbsp;|&nbsp; {report_date}</div>
</div>

<h2>1. Search Console Performance ({sc_date})</h2>
<table class="grid">
  <tr>
    <td style="width:25%;"><div class="card"><div class="label">Total Clicks</div><div class="value">{fmt_int(sc_clicks)}</div></div></td>
    <td style="width:25%;"><div class="card"><div class="label">Total Impressions</div><div class="value">{fmt_int(sc_impressions)}</div></div></td>
    <td style="width:25%;"><div class="card"><div class="label">Average CTR</div><div class="value">{sc_ctr:.2f}%</div></div></td>
    <td style="width:25%;"><div class="card"><div class="label">Average Position</div><div class="value">{sc_position:.1f}</div></div></td>
  </tr>
</table>
<div style="margin-top:12px;">{sc_chart_html}</div>

<h2>2. Revenue & Traffic Dashboard</h2>
<table class="grid">
  <tr>
    <td style="width:33%;"><div class="card"><div class="label">Visit</div><div class="value">{fmt_int(rt_visit)}</div></div></td>
    <td style="width:33%;"><div class="card"><div class="label">Total Revenue</div><div class="value">{fmt_money(rt_revenue)}</div></div></td>
    <td style="width:33%;"><div class="card"><div class="label">Impression</div><div class="value">{fmt_int(rt_impression)}</div></div></td>
  </tr>
  <tr>
    <td style="width:33%;"><div class="card"><div class="label">Ecommerce Purchases</div><div class="value">{fmt_int(rt_ecommerce)}</div></div></td>
    <td style="width:33%;"><div class="card"><div class="label">Purchases Revenue</div><div class="value">{fmt_money(rt_purchase_revenue)}</div></div></td>
    <td style="width:33%;"><div class="card"><div class="label">Transaction</div><div class="value">{fmt_int(rt_transaction)}</div></div></td>
  </tr>
</table>

<h2>3. Top Keyword Ranking Distribution</h2>
{kw_chart_html}
{kw_bars_html}

<h2>4. Backlink Profile</h2>
<table style="width:100%; border-collapse:collapse;">
  <tr>
    <td style="width:48%; vertical-align:top;">{backlink_rows_html}</td>
    <td style="width:4%;"></td>
    <td style="width:48%; vertical-align:top;">{bl_chart_html}</td>
  </tr>
</table>

<h2>5. Traffic Analytics Summary</h2>
<table class="grid">
  <tr>
    <td style="width:25%; text-align:center;"><div class="label" style="font-size:9pt;">CLICK</div><div style="font-size:20pt; font-weight:900;">{fmt_compact(ta_click)}</div></td>
    <td style="width:25%; text-align:center;"><div class="label" style="font-size:9pt;">TOTAL IMPRESSION</div><div style="font-size:20pt; font-weight:900;">{fmt_compact(ta_impression)}</div></td>
    <td style="width:25%; text-align:center;"><div class="label" style="font-size:9pt;">CTR</div><div style="font-size:20pt; font-weight:900;">{ta_ctr:.2f}%</div></td>
    <td style="width:25%; text-align:center;"><div class="label" style="font-size:9pt;">AVG POSITION</div><div style="font-size:20pt; font-weight:900;">{ta_position:.2f}</div></td>
  </tr>
</table>

<h2>6. Technical SEO & Indexing Health</h2>
<table class="grid">
  <tr>
    <td style="width:35%;">
      <div class="card" style="padding:24px;">
        <div class="label">Indexed Pages (Valid)</div>
        <div class="value" style="color:#16a34a; font-size:26pt;">{fmt_int(tech_indexed)}</div>
      </div>
    </td>
    <td style="width:65%; vertical-align:top;">
      <div class="error-box">Not Found (404): {fmt_int(tech_404)} pages</div>
      <div class="warn-box">Crawled — Not Indexed: {fmt_int(tech_crawled_not_indexed)} pages</div>
      <div class="warn-box">Discovered — Not Indexed: {fmt_int(tech_discovered_not_indexed)} pages</div>
    </td>
  </tr>
</table>

<div style="page-break-before: always;"></div>
<div class="thankyou">
  <h1>Thank You!</h1>
  <p style="max-width:480px; margin:0 auto; color:#64748b; font-size:12pt; line-height:1.7;">
    Thank you for taking the time to review this SEO performance report. We are committed to driving
    continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings
    for your business. Should you have any questions, please feel free to reach out to us.
  </p>
  <p style="margin-top:40px; color:#94a3b8; font-size:11pt;">{agency_name} &nbsp;|&nbsp; {report_date}</p>
</div>

<!-- লাইন ৬৩৯ এর পর কন্টেন্ট শেষ হবে -->
</div> <!-- এই </div> টি কন্টেইনার ক্লোজ করবে (লাইন ৬৪০) -->

<div class="footer">Digital Analytic | www.digital-analytic.com</div> <!-- এরপর আপনার ফুটার থাকবে (লাইন ৬৪১) -->
</body>
</html>"""


st.subheader("📄 Export Report")
if st.button("Download as PDF", type="primary", use_container_width=True):
    with st.spinner("Building your PDF report..."):
        try:
            pdf_html = build_pdf_html(
                agency_name, report_date, sc_clicks, sc_impressions, sc_ctr, sc_position, 
                rt_visit, rt_revenue, rt_impression, rt_ecommerce, rt_purchase_revenue, 
                rt_transaction, tech_indexed, tech_404, tech_crawled_not_indexed, 
                tech_discovered_not_indexed, sc_date, ta_click, ta_impression, 
                ta_ctr, ta_position
            )
            pdf_bytes = HTML(string=pdf_html).write_pdf()
            st.success("PDF generated successfully.")
            st.download_button(
                label="📥 Click here to download the PDF",
                data=pdf_bytes,
                file_name=f"{agency_name.replace(' ', '_')}_SEO_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")
            st.error(f"Could not generate PDF: {e}")
