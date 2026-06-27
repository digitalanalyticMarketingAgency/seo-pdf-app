# app.py - SEO Performance Report Generator (FPDF2 Master Version)
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import random
import os
from fpdf import FPDF

# ============================================================
# APP CONFIG & CSS (শুধু একবার)
# ============================================================
st.set_page_config(
    page_title="SEO Performance Report Generator",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f172a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-card .label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .metric-card .value {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 8px;
    }
    
    .backlink-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
    }
    .backlink-card .label {
        font-size: 10px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
    }
    .backlink-card .value {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 6px;
    }
    
    .traffic-summary-label {
        font-size: 12px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        text-align: center;
    }
    .traffic-summary-value {
        font-size: 36px;
        font-weight: 900;
        color: #0f172a;
        text-align: center;
        margin-top: 4px;
    }
    
    .error-row {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 8px;
        color: #991b1b;
    }
    .warn-row {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 8px;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def fmt_int(v):
    return f"{int(v):,}"

def fmt_money(v):
    return f"${v:,.2f}"

def fmt_compact(v):
    v = float(v)
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return f"{v:.0f}"

# ============================================================
# PDF CLASS (FPDF2)
# ============================================================
class PDF(FPDF):
    def __init__(self, agency_name, report_date):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.agency_name = agency_name
        self.report_date = report_date
        
    def header(self):
        # Background image (যদি থাকে)
        if os.path.exists('a4.png'):
            self.image('a4.png', 0, 0, 210, 297)
    
    def add_title_page(self):
        self.add_page()
        self.set_font("Helvetica", 'B', 28)
        self.set_text_color(255, 255, 255)
        self.set_y(100)
        self.cell(0, 15, 'SEO PERFORMANCE', 0, 1, 'C')
        self.cell(0, 15, 'REPORT', 0, 1, 'C')
        self.set_font("Helvetica", '', 14)
        self.set_text_color(180, 180, 180)
        self.set_y(140)
        self.cell(0, 10, f'{self.agency_name}  |  {self.report_date}', 0, 1, 'C')
    
    def add_section_header(self, title):
        self.set_font("Helvetica", 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(139, 92, 246)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', fill=True)
        self.ln(5)
    
    def add_metric_row(self, metrics):
        """metrics = [(label, value, color), ...]"""
        self.set_font("Helvetica", '', 9)
        col_width = 190 / len(metrics)
        
        # Labels
        self.set_text_color(150, 150, 150)
        for label, _, _ in metrics:
            self.cell(col_width, 6, label.upper(), 0, 0, 'C')
        self.ln()
        
        # Values
        self.set_font("Helvetica", 'B', 16)
        for _, value, color in metrics:
            self.set_text_color(*color)
            self.cell(col_width, 10, str(value), 0, 0, 'C')
        self.ln(15)
    
    def add_chart_image(self, image_path, width=180):
        if os.path.exists(image_path):
            x = (210 - width) / 2
            self.image(image_path, x=x, w=width)
            self.ln(5)
    
    def add_error_warning_section(self, indexed, error_404, crawled, discovered):
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(22, 163, 74)
        self.cell(95, 10, f'Indexed Pages: {fmt_int(indexed)}', 0, 0, 'C')
        
        self.set_x(105)
        self.set_font("Helvetica", '', 10)
        self.set_text_color(239, 68, 68)
        self.cell(95, 8, f'404 Errors: {fmt_int(error_404)} pages', 0, 1, 'L')
        
        self.set_x(105)
        self.set_text_color(245, 158, 11)
        self.cell(95, 8, f'Crawled - Not Indexed: {fmt_int(crawled)} pages', 0, 1, 'L')
        
        self.set_x(105)
        self.cell(95, 8, f'Discovered - Not Indexed: {fmt_int(discovered)} pages', 0, 1, 'L')
        self.ln(10)
    
    def add_thank_you_page(self):
        self.add_page()
        self.set_y(100)
        self.set_font("Helvetica", 'B', 32)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'Thank You!', 0, 1, 'C')
        
        self.ln(10)
        self.set_font("Helvetica", '', 11)
        self.set_text_color(180, 180, 180)
        
        thank_text = (
            "Thank you for taking the time to review this SEO performance report. "
            "We are committed to driving continuous digital growth, optimizing your "
            "web presence, and ensuring top-tier search engine rankings for your business."
        )
        self.set_x(30)
        self.multi_cell(150, 7, thank_text, 0, 'C')
        
        self.ln(20)
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'{self.agency_name}  |  {self.report_date}', 0, 1, 'C')


def create_pdf(data, chart_paths):
    """Main PDF creation function"""
    pdf = PDF(data['agency_name'], data['report_date'])
    
    # Page 1: Title
    pdf.add_title_page()
    
    # Page 2: Search Console & Revenue
    pdf.add_page()
    pdf.set_y(20)
    
    pdf.add_section_header('1. Search Console Performance')
    pdf.add_metric_row([
        ('Total Clicks', fmt_int(data['sc_clicks']), (66, 133, 244)),
        ('Impressions', fmt_int(data['sc_impressions']), (142, 36, 170)),
        ('Avg CTR', f"{data['sc_ctr']:.2f}%", (22, 163, 74)),
        ('Avg Position', f"{data['sc_position']:.1f}", (245, 158, 11))
    ])
    pdf.add_chart_image(chart_paths['sc_chart'])
    
    pdf.add_section_header('2. Revenue & Traffic Dashboard')
    pdf.add_metric_row([
        ('Visit', fmt_int(data['rt_visit']), (255, 255, 255)),
        ('Total Revenue', fmt_money(data['rt_revenue']), (255, 255, 255)),
        ('Impression', fmt_int(data['rt_impression']), (255, 255, 255))
    ])
    pdf.add_metric_row([
        ('Ecommerce', fmt_int(data['rt_ecommerce']), (255, 255, 255)),
        ('Purchase Rev', fmt_money(data['rt_purchase_revenue']), (255, 255, 255)),
        ('Transaction', fmt_int(data['rt_transaction']), (255, 255, 255))
    ])
    
    # Page 3: Keywords & Backlinks
    pdf.add_page()
    pdf.set_y(20)
    
    pdf.add_section_header('3. Keyword Ranking Distribution')
    pdf.add_chart_image(chart_paths['kw_chart'])
    
    pdf.add_section_header('4. Backlink Profile')
    pdf.add_metric_row([
        ('Profile', fmt_compact(data['bl_profile']), (37, 99, 235)),
        ('Citation', fmt_compact(data['bl_citation']), (139, 92, 246)),
        ('Web 2.0', fmt_compact(data['bl_web2']), (22, 163, 74))
    ])
    pdf.add_metric_row([
        ('Social', fmt_compact(data['bl_social']), (245, 158, 11)),
        ('Guest Post', fmt_compact(data['bl_guest']), (239, 68, 68)),
        ('Comment', fmt_compact(data['bl_comment']), (6, 182, 212))
    ])
    pdf.add_chart_image(chart_paths['bl_chart'], width=100)
    
    # Page 4: Traffic & Technical
    pdf.add_page()
    pdf.set_y(20)
    
    pdf.add_section_header('5. Traffic Analytics Summary')
    pdf.add_metric_row([
        ('Click', fmt_compact(data['ta_click']), (255, 255, 255)),
        ('Impression', fmt_compact(data['ta_impression']), (255, 255, 255)),
        ('CTR', f"{data['ta_ctr']:.2f}%", (255, 255, 255)),
        ('Avg Position', f"{data['ta_position']:.2f}", (255, 255, 255))
    ])
    
    pdf.add_section_header('6. Technical SEO & Indexing Health')
    pdf.add_error_warning_section(
        data['tech_indexed'],
        data['tech_404'],
        data['tech_crawled_not_indexed'],
        data['tech_discovered_not_indexed']
    )
    
    # Page 5: Thank You
    pdf.add_thank_you_page()
    
    return bytes(pdf.output())


# ============================================================
# MAIN APP HEADER
# ============================================================
st.title("📈 SEO Performance Report Generator")
st.caption("Manually enter your SEO data below to generate a live dashboard and export a professional PDF report.")

# ============================================================
# SIDEBAR — DATA INPUT
# ============================================================
with st.sidebar:
    st.header("⚙️ Report Settings")
    
    if os.path.exists("digital-analytic-logo.png"):
        st.image("digital-analytic-logo.png", width=150)
    
    agency_name = st.text_input("Agency/Brand Name", value="Digital Analytic")
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
    st.header("3️⃣ Keyword Ranking")
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
    st.header("5️⃣ Traffic Analytics")
    ta_click = st.number_input("Click", min_value=0, value=872700, step=100)
    ta_impression = st.number_input("Total Impression", min_value=0, value=248800000, step=1000)
    ta_ctr = st.number_input("CTR (%)", min_value=0.0, value=5.36, step=0.01, format="%.2f")
    ta_position = st.number_input("Average Position ", min_value=0.0, value=13.38, step=0.01, format="%.2f")

    st.divider()
    st.header("6️⃣ Technical SEO")
    tech_indexed = st.number_input("Indexing Page (Valid)", min_value=0, value=1240, step=1)
    tech_404 = st.number_input("Not Found (404)", min_value=0, value=3, step=1)
    tech_crawled_not_indexed = st.number_input("Crawled - Not Indexed", min_value=0, value=42, step=1)
    tech_discovered_not_indexed = st.number_input("Discovered - Not Indexed", min_value=0, value=18, step=1)

# ============================================================
# SECTION 1 — SEARCH CONSOLE PERFORMANCE
# ============================================================
st.header("1. Search Console Performance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="label">Total Clicks</div><div class="value" style="color:#4285F4;">{fmt_int(sc_clicks)}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="label">Total Impressions</div><div class="value" style="color:#8E24AA;">{fmt_int(sc_impressions)}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="label">Average CTR</div><div class="value" style="color:#16a34a;">{sc_ctr:.2f}%</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="label">Average Position</div><div class="value" style="color:#f59e0b;">{sc_position:.1f}</div></div>', unsafe_allow_html=True)

# Generate trend data
_seed = int(sc_clicks + sc_impressions)
_rng = random.Random(_seed)

def _trend(final_val, n=7, volatility=0.12):
    base = final_val / n
    days = []
    for i in range(n):
        noise = _rng.uniform(1 - volatility, 1 + volatility)
        drift = 0.85 + 0.15 * (i / (n - 1))
        days.append(max(0, round(base * drift * noise)))
    scale = final_val / max(sum(days), 1)
    days = [round(d * scale) for d in days]
    days[-1] = final_val
    return days

today = datetime.date.today()
trend_dates = [(today - datetime.timedelta(days=6 - i)).strftime("%b %d") for i in range(7)]
clicks_trend = _trend(sc_clicks)
impressions_trend = _trend(sc_impressions)

# Search Console Chart
sc_fig = go.Figure()
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=clicks_trend,
    mode="lines+markers", name="Clicks",
    line=dict(color="#4285F4", width=3),
    marker=dict(size=8),
    yaxis="y1"
))
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=impressions_trend,
    mode="lines+markers", name="Impressions",
    line=dict(color="#8E24AA", width=3),
    marker=dict(size=8),
    yaxis="y2"
))
sc_fig.update_layout(
    height=350,
    margin=dict(l=60, r=60, t=40, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    yaxis=dict(title="Clicks", titlefont=dict(color="#4285F4"), tickfont=dict(color="#4285F4"), showgrid=True, gridcolor="#f1f5f9"),
    yaxis2=dict(title="Impressions", titlefont=dict(color="#8E24AA"), tickfont=dict(color="#8E24AA"), overlaying="y", side="right", showgrid=False),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(sc_fig, use_container_width=True)
st.caption(f"📅 Timeframe: {sc_date}")

st.divider()

# ============================================================
# SECTION 2 — REVENUE & TRAFFIC DASHBOARD
# ============================================================
st.header("2. Revenue & Traffic Dashboard")

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1:
    st.markdown(f'<div class="metric-card">🧑‍💻<div class="label">Visit</div><div class="value">{fmt_int(rt_visit)}</div></div>', unsafe_allow_html=True)
with r1c2:
    st.markdown(f'<div class="metric-card">💵<div class="label">Total Revenue</div><div class="value">{fmt_money(rt_revenue)}</div></div>', unsafe_allow_html=True)
with r1c3:
    st.markdown(f'<div class="metric-card">👁️<div class="label">Impression</div><div class="value">{fmt_int(rt_impression)}</div></div>', unsafe_allow_html=True)
with r2c1:
    st.markdown(f'<div class="metric-card">🛒<div class="label">Ecommerce Purchases</div><div class="value">{fmt_int(rt_ecommerce)}</div></div>', unsafe_allow_html=True)
with r2c2:
    st.markdown(f'<div class="metric-card">💰<div class="label">Purchases Revenue</div><div class="value">{fmt_money(rt_purchase_revenue)}</div></div>', unsafe_allow_html=True)
with r2c3:
    st.markdown(f'<div class="metric-card">🧾<div class="label">Transaction</div><div class="value">{fmt_int(rt_transaction)}</div></div>', unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 3 — KEYWORD RANKING DISTRIBUTION
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
    textfont=dict(size=14, color="#0f172a")
))
kw_fig.update_layout(
    height=320,
    margin=dict(l=80, r=60, t=20, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(title="Number of Keywords", showgrid=True, gridcolor="#f1f5f9"),
    yaxis=dict(title="Ranking Position", autorange="reversed")
)
st.plotly_chart(kw_fig, use_container_width=True)

st.divider()

# ============================================================
# SECTION 4 — BACKLINK PROFILE
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
            st.markdown(f'<div class="backlink-card"><div class="label">{label}</div><div class="value">{fmt_compact(value)}</div></div>', unsafe_allow_html=True)

with bl_col2:
    donut_fig = go.Figure(go.Pie(
        labels=bl_labels,
        values=bl_values,
        hole=0.55,
        marker=dict(colors=bl_colors),
        textinfo="percent",
        textfont=dict(size=12)
    ))
    donut_fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    st.plotly_chart(donut_fig, use_container_width=True)

st.divider()

# ============================================================
# SECTION 5 — TRAFFIC ANALYTICS SUMMARY
# ============================================================
st.header("5. Traffic Analytics Summary")

ta_col1, ta_col2, ta_col3, ta_col4 = st.columns(4)
with ta_col1:
    st.markdown(f'<div class="traffic-summary-label">Click</div><div class="traffic-summary-value">{fmt_compact(ta_click)}</div>', unsafe_allow_html=True)
with ta_col2:
    st.markdown(f'<div class="traffic-summary-label">Total Impression</div><div class="traffic-summary-value">{fmt_compact(ta_impression)}</div>', unsafe_allow_html=True)
with ta_col3:
    st.markdown(f'<div class="traffic-summary-label">CTR</div><div class="traffic-summary-value">{ta_ctr:.2f}%</div>', unsafe_allow_html=True)
with ta_col4:
    st.markdown(f'<div class="traffic-summary-label">Average Position</div><div class="traffic-summary-value">{ta_position:.2f}</div>', unsafe_allow_html=True)

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
        number={"font": {"size": 42, "color": "#16a34a"}},
        title={"text": "Indexed Pages (Valid)", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, max(tech_indexed * 1.2, 1)], "visible": False},
            "bar": {"color": "#16a34a"},
            "bgcolor": "#f1f5f9",
            "borderwidth": 0,
        }
    ))
    gauge_fig.update_layout(height=280, margin=dict(l=40, r=40, t=60, b=30))
    st.plotly_chart(gauge_fig, use_container_width=True)

with tech_col2:
    st.markdown("**Errors & Warnings**")
    st.markdown(f'<div class="error-row">🔴 <b>Not Found (404):</b> {fmt_int(tech_404)} pages</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warn-row">🟠 <b>Crawled - Currently Not Indexed:</b> {fmt_int(tech_crawled_not_indexed)} pages</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warn-row">🟠 <b>Discovered - Currently Not Indexed:</b> {fmt_int(tech_discovered_not_indexed)} pages</div>', unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 7 — THANK YOU PAGE
# ============================================================
st.header("7. Closing Page Preview")
st.markdown(f"""
<div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 16px; margin: 20px 0;">
    <h1 style="color: #ffffff; font-size: 36px; margin-bottom: 20px;">Thank You!</h1>
    <p style="max-width:650px; margin:0 auto; color:#94a3b8; font-size:16px; line-height:1.8;">
        Thank you for taking the time to review this SEO performance report. We are committed to driving
        continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings
        for your business. Should you have any questions, please feel free to reach out to us.
    </p>
    <p style="margin-top:35px; color:#64748b; font-size:14px;">
        <b>{agency_name}</b> &nbsp;|&nbsp; {report_date}
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# PDF EXPORT SECTION
# ============================================================
st.header("📥 Export Report")

if st.button("🚀 Generate PDF Report", type="primary", use_container_width=True):
    with st.spinner("Generating PDF report..."):
        # Save charts as images
        sc_fig.write_image("sc_chart.png", width=800, height=300, scale=2)
        kw_fig.write_image("kw_chart.png", width=800, height=280, scale=2)
        donut_fig.write_image("bl_chart.png", width=400, height=350, scale=2)
        
        # Prepare data dictionary
        data = {
            'agency_name': agency_name,
            'report_date': report_date,
            'sc_clicks': sc_clicks,
            'sc_impressions': sc_impressions,
            'sc_ctr': sc_ctr,
            'sc_position': sc_position,
            'rt_visit': rt_visit,
            'rt_revenue': rt_revenue,
            'rt_impression': rt_impression,
            'rt_ecommerce': rt_ecommerce,
            'rt_purchase_revenue': rt_purchase_revenue,
            'rt_transaction': rt_transaction,
            'bl_profile': bl_profile,
            'bl_citation': bl_citation,
            'bl_web2': bl_web2,
            'bl_social': bl_social,
            'bl_guest': bl_guest,
            'bl_comment': bl_comment,
            'ta_click': ta_click,
            'ta_impression': ta_impression,
            'ta_ctr': ta_ctr,
            'ta_position': ta_position,
            'tech_indexed': tech_indexed,
            'tech_404': tech_404,
            'tech_crawled_not_indexed': tech_crawled_not_indexed,
            'tech_discovered_not_indexed': tech_discovered_not_indexed
        }
        
        chart_paths = {
            'sc_chart': 'sc_chart.png',
            'kw_chart': 'kw_chart.png',
            'bl_chart': 'bl_chart.png'
        }
        
        # Generate PDF
        pdf_bytes = create_pdf(data, chart_paths)
        
        st.success("✅ PDF generated successfully!")
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"SEO_Report_{report_date.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.caption("Click the button above to generate and download your professional SEO report as PDF.")
