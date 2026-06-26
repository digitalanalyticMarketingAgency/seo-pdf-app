import streamlit as st
import datetime
from weasyprint import HTML

st.set_page_config(page_title="Premium SEO Report Builder", page_icon="💎", layout="centered")

st.title("💎 Premium SEO Report Builder")
st.write("Fill in the details to generate a high-end, premium PDF report.")

# --- 1. AGENCY & CLIENT SETTINGS ---
with st.expander("⚙️ Agency & Client Settings", expanded=True):
    col1, col2 = st.columns(2)
    agency_name = col1.text_input("Agency Name", value="Digital Analytic")
    agency_website = col2.text_input("Agency Website", value="www.digital-analytic.com")
    agency_email = col1.text_input("Agency Email", value="support@digital-analytic.com")
    client_domain = col2.text_input("Client Domain", value="client-website.com")
    report_date = st.text_input("Report Month/Year", value=datetime.date.today().strftime("%B %Y"))

# --- 2. DATA INPUTS ---
with st.expander("📊 1. Search Console"):
    col1, col2 = st.columns(2)
    sc_clicks = col1.text_input("Total Clicks", value="45")
    sc_imp = col2.text_input("Total Impressions", value="17.6K")
    sc_ctr = col1.text_input("Avg CTR", value="0.3%")
    sc_pos = col2.text_input("Avg Position", value="30.3")

with st.expander("💰 2. Revenue & Traffic Dashboard"):
    col1, col2 = st.columns(2)
    rev_conv = col1.text_input("Conversions", value="5,436")
    rev_total = col2.text_input("Total Revenue", value="$5,934.48")
    rev_imp = col1.text_input("Event/Impression", value="9,238")
    rev_ecom = col2.text_input("Ecommerce Purchases", value="423")
    rev_pur_rev = col1.text_input("Purchase Revenue", value="$9,785.37")
    rev_trans = col2.text_input("Transactions", value="823")

with st.expander("🎯 3. Keyword Ranking"):
    col1, col2 = st.columns(2)
    kw_15 = col1.text_input("Pos 1 to 15", value="42")
    kw_30 = col2.text_input("Pos 16 to 30", value="28")
    kw_45 = col1.text_input("Pos 31 to 45", value="19")
    kw_60 = col2.text_input("Pos 46 to 60", value="12")
    kw_100 = col1.text_input("Pos 60 to 100", value="8")

with st.expander("🔗 4. Backlink Profile"):
    col1, col2 = st.columns(2)
    bl_prof = col1.text_input("Profile Backlinks", value="335.3K")
    bl_cit = col2.text_input("Citation Links", value="32.0K")
    bl_web2 = col1.text_input("Web 2.0 Blogs", value="97.4K")
    bl_soc = col2.text_input("Social Shares", value="237.8K")
    bl_guest = col1.text_input("Guest Posts", value="51.9K")
    bl_com = col2.text_input("Comment Links", value="16.9K")

with st.expander("🚦 5. Traffic Quality Summary (Growth % included)"):
    col1, col2 = st.columns(2)
    tq_clicks = col1.text_input("Clicks (Number & Growth)", value="872.7K | ▼ 3.90%")
    tq_imp = col2.text_input("Impressions (Number & Growth)", value="248.8M | ▼ 1.74%")
    tq_ctr = col1.text_input("CTR (Number & Growth)", value="5.36% | ▼ 5.41%")
    tq_pos = col2.text_input("Position (Number & Growth)", value="13.38 | ▲ 1.61%")

with st.expander("🛠️ 6. Technical SEO"):
    col1, col2 = st.columns(2)
    tech_idx = col1.text_input("Indexing Pages", value="1,240")
    tech_404 = col2.text_input("Not Found (404)", value="3")
    tech_crawl = col1.text_input("Crawled - Not Indexed", value="42")
    tech_disc = col2.text_input("Discovered - Not Indexed", value="18")

# --- HTML TEMPLATE (PREMIUM HEAVY DESIGN) ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 0;
        background-color: #f1f5f9;
    }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1e293b;
        margin: 0;
        padding: 0;
    }}
    .container {{
        padding: 25px 40px;
    }}
    .header {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 40px 40px;
        border-bottom: 8px solid #16a34a;
    }}
    .header h1 {{ font-size: 28pt; margin: 0; font-weight: 900; letter-spacing: 1px; }}
    .header p {{ color: #cbd5e1; font-size: 11pt; margin-top: 8px; }}
    .agency-badge {{
        float: right;
        background: rgba(255,255,255,0.1);
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .section-title {{
        font-size: 15pt;
        color: #0f172a;
        margin: 30px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 3px solid #2563eb;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .grid {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; }}
    .grid td {{ vertical-align: top; }}
    .card {{
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }}
    .card-dark {{
        background: #0f172a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #16a34a;
    }}
    .metric-title {{ font-size: 9pt; color: #64748b; font-weight: bold; text-transform: uppercase; }}
    .card-dark .metric-title {{ color: #94a3b8; }}
    .metric-value {{ font-size: 18pt; font-weight: 900; margin-top: 5px; color: #0f172a; }}
    .card-dark .metric-value {{ color: white; }}
    .bar-bg {{ background: #e2e8f0; height: 12px; border-radius: 6px; width: 100%; margin-top: 5px; }}
    .bar-fill-1 {{ background: linear-gradient(90deg, #2563eb, #3b82f6); height: 100%; border-radius: 6px; width: 85%; }}
    .bar-fill-2 {{ background: linear-gradient(90deg, #16a34a, #22c55e); height: 100%; border-radius: 6px; width: 65%; }}
    .bar-fill-3 {{ background: linear-gradient(90deg, #8b5cf6, #a855f7); height: 100%; border-radius: 6px; width: 45%; }}
    .error-box {{ background: #fee2e2; border-left: 5px solid #ef4444; padding: 12px 15px; margin-bottom: 10px; border-radius: 0 8px 8px 0; }}
    .warn-box {{ background: #fef3c7; border-left: 5px solid #f59e0b; padding: 12px 15px; margin-bottom: 10px; border-radius: 0 8px 8px 0; }}
    .footer-box {{
        background: #0f172a; color: white; text-align: center; padding: 50px 30px; margin-top: 40px;
        border-top: 8px solid #2563eb; page-break-inside: avoid;
    }}
</style>
</head>
<body>

    <div class="header">
        <div class="agency-badge">
            <span style="color:#22c55e; font-weight:900; font-size:16pt;">{agency_name.split()[0] if ' ' in agency_name else agency_name}</span> 
            <span style="color:#60a5fa; font-weight:900; font-size:16pt;">{' '.join(agency_name.split()[1:]) if ' ' in agency_name else ''}</span>
        </div>
        <h1>EXECUTIVE SEO REPORT</h1>
        <p>Target Domain: <strong>{client_domain}</strong> &nbsp;|&nbsp; Period: <strong>{report_date}</strong></p>
    </div>

    <div class="container">
        <div class="section-title">1. Search Console Performance</div>
        <table class="grid">
            <tr>
                <td style="width:25%"><div class="card" style="border-top: 4px solid #2563eb;"><div class="metric-title">Total Clicks</div><div class="metric-value" style="color:#2563eb;">{sc_clicks}</div></div></td>
                <td style="width:25%"><div class="card" style="border-top: 4px solid #8b5cf6;"><div class="metric-title">Impressions</div><div class="metric-value" style="color:#8b5cf6;">{sc_imp}</div></div></td>
                <td style="width:25%"><div class="card"><div class="metric-title">Average CTR</div><div class="metric-value">{sc_ctr}</div></div></td>
                <td style="width:25%"><div class="card"><div class="metric-title">Average Pos</div><div class="metric-value">{sc_pos}</div></div></td>
            </tr>
        </table>
        
        <div class="card" style="padding: 25px; margin-top: -5px;">
            <div style="font-size: 9pt; font-weight: bold; color:#64748b; margin-bottom: 15px;">PERFORMANCE TREND (30 DAYS)</div>
            <svg width="100%" height="120" viewBox="0 0 700 120" preserveAspectRatio="none">
                <line x1="0" y1="20" x2="700" y2="20" stroke="#f1f5f9" stroke-width="2"/>
                <line x1="0" y1="60" x2="700" y2="60" stroke="#f1f5f9" stroke-width="2"/>
                <line x1="0" y1="100" x2="700" y2="100" stroke="#f1f5f9" stroke-width="2"/>
                <polygon points="0,100 100,70 250,80 400,30 550,50 700,20 700,120 0,120" fill="rgba(139, 92, 246, 0.1)" />
                <path d="M 0 100 L 100 70 L 250 80 L 400 30 L 550 50 L 700 20" fill="none" stroke="#8b5cf6" stroke-width="4" stroke-linecap="round"/>
                <polygon points="0,110 100,100 250,90 400,60 550,75 700,45 700,120 0,120" fill="rgba(37, 99, 235, 0.1)" />
                <path d="M 0 110 L 100 100 L 250 90 L 400 60 L 550 75 L 700 45" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
            </svg>
        </div>

        <div class="section-title">2. Revenue & Traffic Dashboard</div>
        <table class="grid">
            <tr>
                <td style="width:33%"><div class="card"><div class="metric-title">Conversions</div><div class="metric-value">{rev_conv}</div></div></td>
                <td style="width:33%"><div class="card"><div class="metric-title">Total Revenue</div><div class="metric-value" style="color:#16a34a;">{rev_total}</div></div></td>
                <td style="width:33%"><div class="card"><div class="metric-title">Transactions</div><div class="metric-value">{rev_trans}</div></div></td>
            </tr>
        </table>

        <table class="grid">
            <tr>
                <td style="width:50%;">
                    <div class="section-title" style="margin-top:10px;">3. Keyword Spread</div>
                    <div class="card" style="padding: 25px;">
                        <div style="margin-bottom:12px;"><span class="metric-title">POS 1-15:</span> <b style="float:right;">{kw_15}</b><div class="bar-bg"><div class="bar-fill-1"></div></div></div>
                        <div style="margin-bottom:12px;"><span class="metric-title">POS 16-30:</span> <b style="float:right;">{kw_30}</b><div class="bar-bg"><div class="bar-fill-2"></div></div></div>
                        <div style="margin-bottom:12px;"><span class="metric-title">POS 31-45:</span> <b style="float:right;">{kw_45}</b><div class="bar-bg"><div class="bar-fill-3"></div></div></div>
                    </div>
                </td>
                <td style="width:50%;">
                    <div class="section-title" style="margin-top:10px;">4. Backlink Profile</div>
                    <div class="card-dark" style="padding: 25px;">
                        <table style="width:100%; color:white; line-height:2.2;">
                            <tr><td>Profile Links:</td><td style="text-align:right; font-weight:bold;">{bl_prof}</td></tr>
                            <tr><td>Citation Links:</td><td style="text-align:right; font-weight:bold;">{bl_cit}</td></tr>
                            <tr><td>Web 2.0 Blogs:</td><td style="text-align:right; font-weight:bold;">{bl_web2}</td></tr>
                            <tr><td>Social Shares:</td><td style="text-align:right; font-weight:bold;">{bl_soc}</td></tr>
                            <tr><td>Guest Posts:</td><td style="text-align:right; font-weight:bold;">{bl_guest}</td></tr>
                        </table>
                    </div>
                </td>
            </tr>
        </table>

        <div class="section-title">5. Quality Summary</div>
        <div class="card-dark">
            <table style="width:100%; text-align:center;">
                <tr>
                    <td style="border-right:1px solid rgba(255,255,255,0.2);"><div class="metric-title">Clicks</div><div class="metric-value">{tq_clicks}</div></td>
                    <td style="border-right:1px solid rgba(255,255,255,0.2);"><div class="metric-title">Impressions</div><div class="metric-value">{tq_imp}</div></td>
                    <td><div class="metric-title">Avg Position</div><div class="metric-value" style="color:#22c55e;">{tq_pos}</div></td>
                </tr>
            </table>
        </div>
        
        <div class="section-title">6. Technical Health</div>
        <table class="grid">
            <tr>
                <td style="width:40%;">
                    <div class="card" style="text-align:center; padding: 40px 20px; border:2px solid #16a34a;">
                        <div class="metric-title">Valid Indexing Pages</div>
                        <div style="font-size:36pt; font-weight:900; color:#16a34a; margin:10px 0;">{tech_idx}</div>
                        <div style="color:#64748b; font-weight:bold;">Healthy Status</div>
                    </div>
                </td>
                <td style="width:60%;">
                    <div class="error-box"><b style="color:#ef4444;">Not Found (404):</b> <span style="float:right; font-weight:bold;">{tech_404} Pages</span></div>
                    <div class="warn-box"><b style="color:#f59e0b;">Crawled - Not Indexed:</b> <span style="float:right; font-weight:bold;">{tech_crawl} Pages</span></div>
                    <div class="warn-box" style="border-color:#3b82f6; background:#eff6ff;"><b style="color:#3b82f6;">Discovered - Not Indexed:</b> <span style="float:right; font-weight:bold;">{tech_disc} Pages</span></div>
                </td>
            </tr>
        </table>
    </div>

    <div class="footer-box">
        <h2 style="font-size:24pt; margin:0 0 15px 0;">Thank You For Your Business!</h2>
        <p style="color:#94a3b8; max-width:600px; margin:0 auto 30px auto; line-height:1.6; font-size:11pt;">
            We are committed to driving continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings. Should you have any questions regarding these analytics, please reach out.
        </p>
        <div style="padding-top:20px; border-top:1px solid rgba(255,255,255,0.1); color:#cbd5e1; font-weight:bold;">
            {agency_name} &nbsp; | &nbsp; {agency_website} &nbsp; | &nbsp; {agency_email}
        </div>
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
            st.error("Error generating PDF. Please ensure packages.txt is set up correctly in GitHub.")
            st.write(e)
