import streamlit as st
import datetime
from weasyprint import HTML

st.set_page_config(page_title="SEO Report Generator", layout="wide")
st.title("📈 SEO Performance Report Generator")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("⚙️ Report Settings")
    agency_name = st.text_input("Agency Name", value="Digital Analytic")
    report_date = st.text_input("Reporting Period", value=datetime.date.today().strftime("%B %Y"))

    st.divider()
    st.header("1️⃣ Search Console")
    sc_clicks = st.number_input("Total Clicks", value=450)
    sc_impressions = st.number_input("Total Impressions", value=17600)
    sc_ctr = st.number_input("Average CTR (%)", value=2.6, format="%.2f")
    sc_position = st.number_input("Average Position", value=14.3, format="%.1f")

    st.divider()
    st.header("2️⃣ Revenue & Traffic")
    rt_visit = st.number_input("Visits", value=9238)
    rt_revenue = st.number_input("Total Revenue ($)", value=5934.48, format="%.2f")
    rt_impression = st.number_input("Impressions", value=17600)
    rt_ecommerce = st.number_input("Ecommerce Purchases", value=423)
    rt_purchase_revenue = st.number_input("Purchases Revenue ($)", value=9785.37, format="%.2f")
    rt_transaction = st.number_input("Transactions", value=823)

    st.divider()
    st.header("3️⃣ Keyword Ranking")
    kw_1_15 = st.number_input("Pos 1-15", value=42)
    kw_16_30 = st.number_input("Pos 16-30", value=28)
    kw_31_45 = st.number_input("Pos 31-45", value=19)
    kw_46_60 = st.number_input("Pos 46-60", value=12)
    kw_60_100 = st.number_input("Pos 60-100", value=8)

# --- PDF HTML TEMPLATE ---
# এখানে আপনার সব ইনপুট ভেরিয়েবলগুলো যুক্ত করা হয়েছে
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; }}
        .header {{ background: #081426; color: white; padding: 20px; text-align: center; }}
        .card {{ background: #fff; padding: 20px; border: 1px solid #ccc; margin: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{agency_name}</h1>
        <p>Report Date: {report_date}</p>
    </div>
    <h2>Search Console Performance</h2>
    <p>Clicks: {sc_clicks} | Impressions: {sc_impressions} | CTR: {sc_ctr}% | Position: {sc_position}</p>
    
    <h2>Revenue & Traffic</h2>
    <p>Revenue: ${rt_revenue} | Visits: {rt_visit} | Transactions: {rt_transaction}</p>
    
    <h2>Keyword Distribution</h2>
    <p>Pos 1-15: {kw_1_15} | Pos 16-30: {kw_16_30} | Pos 31-45: {kw_31_45}</p>
</body>
</html>
"""

if st.button("Generate PDF"):
    pdf_bytes = HTML(string=html_content).write_pdf()
    st.download_button("📥 Download PDF", pdf_bytes, "report.pdf", "application/pdf")
