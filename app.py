import streamlit as st
import datetime
from weasyprint import HTML

st.set_page_config(page_title="Premium SEO Report Builder", page_icon="💎", layout="wide")

st.title("💎 Premium SEO Report Builder")
st.write("Fill in the details to generate a high-end, premium PDF report.")

# --- 1. AGENCY & CLIENT SETTINGS ---
with st.expander("⚙️ Agency & Client Settings", expanded=True):
    col1, col2 = st.columns(2)
    agency_name    = col1.text_input("Agency Name",       value="Digital Analytic")
    agency_website = col2.text_input("Agency Website",    value="www.digital-analytic.com")
    agency_email   = col1.text_input("Agency Email",      value="support@digital-analytic.com")
    client_domain  = col2.text_input("Client Domain",     value="client-website.com")
    report_date    = st.text_input("Report Month/Year",   value=datetime.date.today().strftime("%B %Y"))

# --- 2. DATA INPUTS ---
with st.expander("📊 1. Search Console"):
    col1, col2 = st.columns(2)
    sc_clicks = col1.number_input("Total Clicks",       value=45,   step=1)
    sc_imp    = col2.number_input("Total Impressions",  value=17600, step=100)
    sc_ctr    = col1.number_input("Avg CTR (%)",        value=0.3,  step=0.01, format="%.2f")
    sc_pos    = col2.number_input("Avg Position",       value=30.3, step=0.1,  format="%.1f")

with st.expander("💰 2. Revenue & Traffic Dashboard"):
    col1, col2 = st.columns(2)
    rev_conv    = col1.number_input("Conversions",          value=5436,   step=1)
    rev_total   = col2.number_input("Total Revenue ($)",    value=5934.48, step=0.01, format="%.2f")
    rev_imp     = col1.number_input("Event / Impression",   value=9238,   step=1)
    rev_ecom    = col2.number_input("Ecommerce Purchases",  value=423,    step=1)
    rev_pur_rev = col1.number_input("Purchase Revenue ($)", value=9785.37, step=0.01, format="%.2f")
    rev_trans   = col2.number_input("Transactions",         value=823,    step=1)

with st.expander("🎯 3. Keyword Ranking"):
    col1, col2 = st.columns(2)
    kw_15  = col1.number_input("Pos 1 to 15",   value=42, step=1)
    kw_30  = col2.number_input("Pos 16 to 30",  value=28, step=1)
    kw_45  = col1.number_input("Pos 31 to 45",  value=19, step=1)
    kw_60  = col2.number_input("Pos 46 to 60",  value=12, step=1)
    kw_100 = col1.number_input("Pos 60 to 100", value=8,  step=1)

with st.expander("🔗 4. Backlink Profile"):
    col1, col2 = st.columns(2)
    bl_prof  = col1.text_input("Profile Backlinks", value="335.3K")
    bl_cit   = col2.text_input("Citation Links",    value="32.0K")
    bl_web2  = col1.text_input("Web 2.0 Blogs",     value="97.4K")
    bl_soc   = col2.text_input("Social Shares",     value="237.8K")
    bl_guest = col1.text_input("Guest Posts",       value="51.9K")
    bl_com   = col2.text_input("Comment Links",     value="16.9K")

with st.expander("🚦 5. Traffic Quality Summary (Growth % included)"):
    col1, col2 = st.columns(2)
    tq_clicks = col1.text_input("Clicks (Number & Growth)",       value="872.7K | ▼ 3.90%")
    tq_imp    = col2.text_input("Impressions (Number & Growth)",  value="248.8M | ▼ 1.74%")
    tq_ctr    = col1.text_input("CTR (Number & Growth)",          value="5.36% | ▼ 5.41%")
    tq_pos    = col2.text_input("Position (Number & Growth)",     value="13.38 | ▲ 1.61%")

with st.expander("🛠️ 6. Technical SEO"):
    col1, col2 = st.columns(2)
    tech_idx   = col1.number_input("Indexing Pages",            value=1240, step=1)
    tech_404   = col2.number_input("Not Found (404)",           value=3,    step=1)
    tech_crawl = col1.number_input("Crawled - Not Indexed",     value=42,   step=1)
    tech_disc  = col2.number_input("Discovered - Not Indexed",  value=18,   step=1)

# --- HELPER FUNCTIONS ---
def format_growth(val):
    if '▼' in val:
        parts = val.split('▼')
        return f"{parts[0]} <span style='color:#ef4444; font-size:12pt;'>&darr;</span><span style='color:#ef4444;'>{parts[1]}</span>"
    elif '▲' in val:
        parts = val.split('▲')
        return f"{parts[0]} <span style='color:#22c55e; font-size:12pt;'>&uarr;</span><span style='color:#22c55e;'>{parts[1]}</span>"
    return val

def fmt_revenue(v):
    return f"${v:,.2f}"

def fmt_int(v):
    return f"{int(v):,}"

# Dynamic keyword progress bars
kw_values  = [kw_15, kw_30, kw_45, kw_60, kw_100]
kw_labels  = ["POS 1-15", "POS 16-30", "POS 31-45", "POS 46-60", "POS 60-100"]
kw_colors  = ["#2563eb", "#8b5cf6", "#f59e0b", "#ef4444", "#64748b"]
max_kw     = max(kw_values) if max(kw_values) > 0 else 1

def kw_bar_row(label, value, color, max_val):
    width = int((value / max_val) * 100)
    return f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:10px;">
      <tr>
        <td style="width:90px; font-size:8pt; font-weight:700; color:#64748b; text-transform:uppercase;">{label}</td>
        <td>
          <div style="background:#f1f5f9; border-radius:4px; height:10px; width:100%;">
            <div style="background:{color}; border-radius:4px; height:10px; width:{width}%;"></div>
          </div>
        </td>
        <td style="width:36px; text-align:right; font-weight:900; font-size:10pt; color:#0f172a;">{value}</td>
      </tr>
    </table>"""

kw_bars_html = "".join(
    kw_bar_row(kw_labels[i], kw_values[i], kw_colors[i], max_kw) for i in range(5)
)

# --- HTML TEMPLATE ---
html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: A4;
    margin: 0;
    @bottom-center {{
      content: none;
    }}
  }}
  body {{
    font-family: Helvetica, Arial, sans-serif;
    color: #1e293b;
    margin: 0;
    padding: 0;
    background: #f1f5f9;
  }}
  /* ---- PAGE BREAK ---- */
  .page-break {{ page-break-before: always; }}

  /* ---- PAGE WRAPPER: each page is exactly A4 height ---- */
  .page-wrap {{
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    width: 210mm;
    height: 297mm;
    overflow: hidden;
    box-sizing: border-box;
  }}

  /* ---- COVER ---- */
  .cover-page {{
    background: #081426;
    width: 100%;
    height: 100%;
    display: block;
    padding: 0;
    box-sizing: border-box;
  }}
  .cover-inner {{
    padding: 120px 60px 60px 60px;
  }}
  .cover-badge {{
    display: inline-block;
    background: #112240;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 6px 16px;
    color: #60a5fa;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 40px;
  }}
  .cover-title {{
    font-size: 36pt;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 1px;
    margin: 0 0 12px 0;
    line-height: 1.15;
  }}
  .cover-sub {{
    font-size: 14pt;
    color: #60a5fa;
    font-weight: 700;
    margin: 0 0 60px 0;
  }}
  .cover-divider {{
    border: none;
    border-top: 2px solid #1e3a5f;
    margin: 0 0 40px 0;
  }}
  .cover-meta-table {{
    width: 100%;
    border-collapse: collapse;
    color: #cbd5e1;
    font-size: 11pt;
  }}
  .cover-meta-table td {{ padding: 8px 0; }}
  .cover-meta-label {{ color: #64748b; font-size: 8pt; font-weight:700; text-transform:uppercase; letter-spacing:1px; }}
  .cover-meta-value {{ color: #ffffff; font-size: 13pt; font-weight: 800; }}

  /* ---- CONTAINER ---- */
  .container {{
    padding: 28px 36px;
    background: #f1f5f9;
  }}

  /* ---- SECTION TITLE ---- */
  .section-title {{
    font-size: 13pt;
    color: #0f172a;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 3px solid #2563eb;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  /* ---- CARDS ---- */
  .card {{
    background: #fff;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
  }}
  .card-dark {{
    background: #0f172a;
    color: white;
    padding: 24px;
    border-radius: 16px;
    border-left: 5px solid #16a34a;
  }}
  .metric-title {{
    font-size: 9pt;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .card-dark .metric-title {{ color: #94a3b8; }}
  .metric-value {{
    font-size: 22pt;
    font-weight: 900;
    margin-top: 4px;
    color: #0f172a;
  }}
  .card-dark .metric-value {{ color: white; }}

  /* ---- GRID ---- */
  .grid {{ width: 100%; border-collapse: separate; border-spacing: 12px; }}
  .grid td {{ vertical-align: top; }}

  /* ---- TECH BOXES ---- */
  .error-box  {{ background:#fff0f0; border-left:5px solid #ef4444; border-radius:8px; padding:14px 18px; margin-bottom:12px; }}
  .warn-box   {{ background:#fffbea; border-left:5px solid #f59e0b; border-radius:8px; padding:14px 18px; margin-bottom:12px; }}
  .notice-box {{ background:#eff6ff; border-left:5px solid #3b82f6; border-radius:8px; padding:14px 18px; }}

  /* ---- FOOTER ---- */
  .page-footer {{
    background: #081426;
    color: #94a3b8;
    text-align: center;
    padding: 10px 20px;
    font-size: 8pt;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    box-sizing: border-box;
  }}

  /* ---- THANK YOU ---- */
  .thankyou-page {{
    background: #081426;
    width: 100%;
    height: 100%;
    text-align: center;
    box-sizing: border-box;
  }}
  .thankyou-inner {{
    padding: 140px 60px 60px 60px;
  }}

  /* ---- RECOMMENDATIONS ---- */
  .rec-table {{ width:100%; border-collapse:collapse; font-size:10pt; }}
  .rec-table th {{ background:#0f172a; color:#fff; padding:10px 14px; text-align:left; font-size:9pt; text-transform:uppercase; letter-spacing:0.5px; }}
  .rec-table td {{ padding:10px 14px; border-bottom:1px solid #e2e8f0; vertical-align:top; }}
  .rec-table tr:nth-child(even) td {{ background:#f8fafc; }}
  .badge-high   {{ background:#fee2e2; color:#b91c1c; border-radius:4px; padding:2px 8px; font-size:8pt; font-weight:700; }}
  .badge-medium {{ background:#fef3c7; color:#92400e; border-radius:4px; padding:2px 8px; font-size:8pt; font-weight:700; }}
  .badge-low    {{ background:#dbeafe; color:#1e40af; border-radius:4px; padding:2px 8px; font-size:8pt; font-weight:700; }}
</style>
</head>
<body>

<!-- ===================== PAGE 1: COVER ===================== -->
<div class="page-wrap">
  <div class="cover-page">
    <div class="cover-inner">
      <div class="cover-badge">SEO Performance Report</div>
      <div class="cover-title">
        <span style="color:#22c55e;">{agency_name.split()[0] if ' ' in agency_name else agency_name}</span>
        <span style="color:#60a5fa;"> {' '.join(agency_name.split()[1:]) if ' ' in agency_name else ''}</span>
      </div>
      <div class="cover-sub">Search Engine Optimization Report</div>
      <hr class="cover-divider"/>
      <table class="cover-meta-table">
        <tr>
          <td style="width:50%;">
            <div class="cover-meta-label">Client Domain</div>
            <div class="cover-meta-value">{client_domain}</div>
          </td>
          <td style="width:50%;">
            <div class="cover-meta-label">Reporting Period</div>
            <div class="cover-meta-value">{report_date}</div>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding-top:24px;">
            <div class="cover-meta-label">Prepared By</div>
            <div class="cover-meta-value">{agency_name}</div>
            <div style="color:#64748b; font-size:10pt; margin-top:4px;">{agency_website} &nbsp;|&nbsp; {agency_email}</div>
          </td>
        </tr>
      </table>
    </div>
  </div>
  <div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 2: EXECUTIVE SUMMARY ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <div class="section-title">Executive Summary</div>

  <!-- 4 KPI Cards -->
  <table class="grid">
    <tr>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #2563eb;">
          <div class="metric-title">Organic Traffic</div>
          <div class="metric-value" style="color:#2563eb;">{fmt_int(sc_clicks)}</div>
          <div style="font-size:8pt; color:#64748b; margin-top:4px;">Total Clicks</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #8b5cf6;">
          <div class="metric-title">Top Keywords</div>
          <div class="metric-value" style="color:#8b5cf6;">{kw_15}</div>
          <div style="font-size:8pt; color:#64748b; margin-top:4px;">Ranking Pos 1–15</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #16a34a;">
          <div class="metric-title">New Backlinks</div>
          <div class="metric-value" style="color:#16a34a;">{bl_prof}</div>
          <div style="font-size:8pt; color:#64748b; margin-top:4px;">Profile Backlinks</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #f59e0b;">
          <div class="metric-title">Index Health</div>
          <div class="metric-value" style="color:#f59e0b;">{fmt_int(tech_idx)}</div>
          <div style="font-size:8pt; color:#64748b; margin-top:4px;">Indexed Pages</div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Key Achievements -->
  <div class="card" style="margin-top:16px; border-top:4px solid #16a34a;">
    <div class="metric-title" style="margin-bottom:14px;">Key Achievements</div>
    <table style="width:100%; border-collapse:collapse; font-size:10pt;">
      <tr>
        <td style="width:50%; padding:8px 12px; border-right:1px solid #e2e8f0;">
          <span style="color:#16a34a; font-weight:900; font-size:14pt;">&#10003;</span>&nbsp;
          <strong>{fmt_int(sc_clicks)}</strong> total organic clicks recorded
        </td>
        <td style="width:50%; padding:8px 12px;">
          <span style="color:#16a34a; font-weight:900; font-size:14pt;">&#10003;</span>&nbsp;
          <strong>{kw_15}</strong> keywords ranking in top 15 positions
        </td>
      </tr>
      <tr>
        <td style="padding:8px 12px; border-right:1px solid #e2e8f0; border-top:1px solid #e2e8f0;">
          <span style="color:#16a34a; font-weight:900; font-size:14pt;">&#10003;</span>&nbsp;
          <strong>{fmt_int(tech_idx)}</strong> pages successfully indexed
        </td>
        <td style="padding:8px 12px; border-top:1px solid #e2e8f0;">
          <span style="color:#16a34a; font-weight:900; font-size:14pt;">&#10003;</span>&nbsp;
          <strong>{fmt_revenue(rev_total)}</strong> total revenue tracked
        </td>
      </tr>
    </table>
  </div>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 3: SEARCH CONSOLE ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <div class="section-title">Search Console Performance</div>
  <table class="grid">
    <tr>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #2563eb;">
          <div class="metric-title">Total Clicks</div>
          <div class="metric-value" style="color:#2563eb;">{fmt_int(sc_clicks)}</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #8b5cf6;">
          <div class="metric-title">Impressions</div>
          <div class="metric-value" style="color:#8b5cf6;">{fmt_int(sc_imp)}</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #f59e0b;">
          <div class="metric-title">Average CTR</div>
          <div class="metric-value" style="color:#f59e0b;">{sc_ctr:.2f}%</div>
        </div>
      </td>
      <td style="width:25%;">
        <div class="card" style="border-top:4px solid #64748b;">
          <div class="metric-title">Average Position</div>
          <div class="metric-value" style="color:#64748b;">{sc_pos:.1f}</div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Chart -->
  <div class="card" style="margin-top:6px; padding:22px;">
    <div style="font-size:9pt; font-weight:700; color:#64748b; margin-bottom:14px; text-transform:uppercase; letter-spacing:0.5px;">
      Performance Trend (30 Days)
      &nbsp;&nbsp;&nbsp;
      <span style="color:#8b5cf6; font-size:12pt; line-height:0;">&bull;</span> Impressions
      &nbsp;&nbsp;
      <span style="color:#2563eb; font-size:12pt; line-height:0;">&bull;</span> Clicks
    </div>
    <svg width="100%" height="130" viewBox="0 0 700 130" preserveAspectRatio="none">
      <line x1="0" y1="20"  x2="700" y2="20"  stroke="#f1f5f9" stroke-width="2"/>
      <line x1="0" y1="65"  x2="700" y2="65"  stroke="#f1f5f9" stroke-width="2"/>
      <line x1="0" y1="110" x2="700" y2="110" stroke="#f1f5f9" stroke-width="2"/>
      <!-- Impressions area -->
      <polygon points="0,100 100,70 250,80 400,30 550,50 700,20 700,130 0,130"
               fill="#8b5cf6" fill-opacity="0.10"/>
      <path d="M 0 100 L 100 70 L 250 80 L 400 30 L 550 50 L 700 20"
            fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>
      <!-- Clicks area -->
      <polygon points="0,110 100,100 250,90 400,60 550,75 700,45 700,130 0,130"
               fill="#2563eb" fill-opacity="0.10"/>
      <path d="M 0 110 L 100 100 L 250 90 L 400 60 L 550 75 L 700 45"
            fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
    </svg>
  </div>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 4: REVENUE DASHBOARD ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <div class="section-title">Revenue Dashboard</div>
  <table class="grid">
    <tr>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #16a34a;">
          <div class="metric-title">Conversions</div>
          <div class="metric-value" style="color:#16a34a;">{fmt_int(rev_conv)}</div>
        </div>
      </td>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #2563eb;">
          <div class="metric-title">Total Revenue</div>
          <div class="metric-value" style="color:#2563eb;">{fmt_revenue(rev_total)}</div>
        </div>
      </td>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #8b5cf6;">
          <div class="metric-title">Event / Impression</div>
          <div class="metric-value" style="color:#8b5cf6;">{fmt_int(rev_imp)}</div>
        </div>
      </td>
    </tr>
    <tr>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #f59e0b;">
          <div class="metric-title">Ecommerce Purchases</div>
          <div class="metric-value" style="color:#f59e0b;">{fmt_int(rev_ecom)}</div>
        </div>
      </td>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #16a34a;">
          <div class="metric-title">Purchase Revenue</div>
          <div class="metric-value" style="color:#16a34a;">{fmt_revenue(rev_pur_rev)}</div>
        </div>
      </td>
      <td style="width:33%;">
        <div class="card" style="border-top:4px solid #64748b;">
          <div class="metric-title">Transactions</div>
          <div class="metric-value" style="color:#64748b;">{fmt_int(rev_trans)}</div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Traffic Quality Summary -->
  <div class="section-title" style="margin-top:22px;">Traffic Quality Summary</div>
  <div class="card-dark">
    <table style="width:100%; text-align:center; border-collapse:collapse;">
      <tr>
        <td style="border-right:1px solid #1e3a5f; width:25%; padding:12px;">
          <div class="metric-title">Clicks</div>
          <div class="metric-value">{format_growth(tq_clicks)}</div>
        </td>
        <td style="border-right:1px solid #1e3a5f; width:25%; padding:12px;">
          <div class="metric-title">Impressions</div>
          <div class="metric-value">{format_growth(tq_imp)}</div>
        </td>
        <td style="border-right:1px solid #1e3a5f; width:25%; padding:12px;">
          <div class="metric-title">CTR</div>
          <div class="metric-value">{format_growth(tq_ctr)}</div>
        </td>
        <td style="width:25%; padding:12px;">
          <div class="metric-title">Avg Position</div>
          <div class="metric-value">{format_growth(tq_pos)}</div>
        </td>
      </tr>
    </table>
  </div>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 5: KEYWORD RANKINGS + BACKLINK ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <table class="grid">
    <tr>
      <td style="width:50%;">
        <div class="section-title">Keyword Rankings</div>
        <div class="card" style="min-height:280px; padding:22px;">
          {kw_bars_html}
        </div>
      </td>
      <td style="width:50%;">
        <div class="section-title">Backlink Profile</div>
        <div class="card-dark" style="min-height:280px; padding:22px;">
          <table style="width:100%; color:white; border-collapse:collapse; font-size:11pt; line-height:2.2;">
            <tr>
              <td>Profile Links:</td>
              <td style="text-align:right; font-weight:bold;">{bl_prof}</td>
            </tr>
            <tr>
              <td>Citation Links:</td>
              <td style="text-align:right; font-weight:bold;">{bl_cit}</td>
            </tr>
            <tr>
              <td>Web 2.0 Blogs:</td>
              <td style="text-align:right; font-weight:bold;">{bl_web2}</td>
            </tr>
            <tr>
              <td>Social Shares:</td>
              <td style="text-align:right; font-weight:bold;">{bl_soc}</td>
            </tr>
            <tr>
              <td>Guest Posts:</td>
              <td style="text-align:right; font-weight:bold;">{bl_guest}</td>
            </tr>
            <tr>
              <td>Comment Links:</td>
              <td style="text-align:right; font-weight:bold;">{bl_com}</td>
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 6: TECHNICAL SEO HEALTH ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <div class="section-title">Technical SEO Health</div>
  <table class="grid">
    <tr>
      <td style="width:38%;">
        <div class="card" style="text-align:center; padding:40px 20px; border:2px solid #16a34a;">
          <div class="metric-title">Valid Indexing Pages</div>
          <div style="font-size:36pt; font-weight:900; color:#16a34a; margin:10px 0;">{fmt_int(tech_idx)}</div>
          <div style="color:#64748b; font-weight:bold; font-size:10pt;">Healthy Status</div>
        </div>
      </td>
      <td style="width:62%; vertical-align:top;">
        <div class="error-box">
          <table style="width:100%; border-collapse:collapse;">
            <tr>
              <td><b style="color:#ef4444;">Not Found (404):</b></td>
              <td style="text-align:right; font-weight:bold; color:#ef4444;">{tech_404} Pages</td>
            </tr>
          </table>
        </div>
        <div class="warn-box">
          <table style="width:100%; border-collapse:collapse;">
            <tr>
              <td><b style="color:#f59e0b;">Crawled — Not Indexed:</b></td>
              <td style="text-align:right; font-weight:bold; color:#f59e0b;">{tech_crawl} Pages</td>
            </tr>
          </table>
        </div>
        <div class="notice-box">
          <table style="width:100%; border-collapse:collapse;">
            <tr>
              <td><b style="color:#3b82f6;">Discovered — Not Indexed:</b></td>
              <td style="text-align:right; font-weight:bold; color:#3b82f6;">{tech_disc} Pages</td>
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 7: RECOMMENDATIONS ===================== -->
<div class="page-wrap">
<div class="container" style="height:calc(297mm - 38px); overflow:hidden; box-sizing:border-box;">
  <div class="section-title">Recommendations Priority</div>
  <table class="rec-table">
    <thead>
      <tr>
        <th style="width:15%;">Priority</th>
        <th style="width:45%;">Recommendation</th>
        <th style="width:40%;">Expected Impact</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge-high">HIGH</span></td>
        <td>Fix 404 pages ({tech_404} currently broken)</td>
        <td>Improve crawl efficiency and user experience</td>
      </tr>
      <tr>
        <td><span class="badge-high">HIGH</span></td>
        <td>Improve low CTR pages (current avg CTR: {sc_ctr:.2f}%)</td>
        <td>Increase organic traffic from existing impressions</td>
      </tr>
      <tr>
        <td><span class="badge-medium">MEDIUM</span></td>
        <td>Improve keyword rankings (pos 16–30 currently: {kw_30})</td>
        <td>Push more keywords into top 15 for more clicks</td>
      </tr>
      <tr>
        <td><span class="badge-medium">MEDIUM</span></td>
        <td>Build authority backlinks to strengthen domain</td>
        <td>Improved domain authority and ranking signals</td>
      </tr>
      <tr>
        <td><span class="badge-low">LOW</span></td>
        <td>Improve internal linking structure</td>
        <td>Better crawlability and page authority distribution</td>
      </tr>
      <tr>
        <td><span class="badge-low">LOW</span></td>
        <td>Resolve {tech_crawl} crawled-but-not-indexed pages</td>
        <td>Expand index coverage and improve site signals</td>
      </tr>
    </tbody>
  </table>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

<!-- ===================== PAGE 8: THANK YOU ===================== -->
<div class="page-wrap">
<div class="thankyou-page">
  <div class="thankyou-inner">
    <div style="font-size:48pt; margin-bottom:24px;">&#128591;</div>
    <h1 style="font-size:36pt; font-weight:900; color:#ffffff; margin:0 0 16px 0;">Thank You!</h1>
    <p style="color:#94a3b8; font-size:13pt; max-width:520px; margin:0 auto 40px auto; line-height:1.7;">
      We are committed to driving continuous digital growth, optimizing your web presence,
      and ensuring top-tier search engine rankings. Should you have any questions regarding
      these analytics, please reach out.
    </p>
    <div style="border-top:1px solid #1e3a5f; padding-top:30px; color:#cbd5e1; font-size:13pt; font-weight:700;">
      {agency_name}
    </div>
    <div style="color:#60a5fa; font-size:11pt; margin-top:8px;">{agency_website}</div>
    <div style="color:#64748b; font-size:10pt; margin-top:4px;">{agency_email}</div>
  </div>
</div>
<div class="page-footer">Generated by {agency_name} &nbsp;|&nbsp; {agency_website} &nbsp;|&nbsp; {report_date}</div>
</div>

</body>
</html>
"""

st.markdown("---")
if st.button("🚀 Generate Premium PDF", use_container_width=True):
    with st.spinner("Rendering Premium Design..."):
        try:
            pdf_bytes = HTML(string=html_template).write_pdf()
            st.success("✨ Premium Report Generated Successfully!")
            st.download_button(
                label="📥 Download High-Quality PDF",
                data=pdf_bytes,
                file_name=f"{agency_name.replace(' ', '_')}_SEO_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error("Error generating PDF. Please ensure WeasyPrint is installed correctly.")
            st.write(e)
