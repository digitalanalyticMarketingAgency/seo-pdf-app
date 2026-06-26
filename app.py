import streamlit as st
import datetime
from weasyprint import HTML

# Page Config
st.set_page_config(page_title="SEO Report Generator", layout="wide")
st.title("📈 SEO Performance Report Generator")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Report Settings")
    agency_name = st.text_input("Agency Name", value="Digital Analytic")
    report_date = st.text_input("Reporting Period", value=datetime.date.today().strftime("%B %Y"))
    st.info("Logo will be handled in the final PDF template.")

# Inputs
sc_clicks = st.number_input("Total Clicks", value=450)

# PDF HTML Template
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; }}
    .header {{ background: #081426; color: white; padding: 20px; text-align: center; }}
</style>
</head>
<body>
    <div class="header">
        <h1>{agency_name}</h1>
        <p>Report Date: {report_date}</p>
    </div>
    <h2>Search Console Performance</h2>
    <p>Total Clicks: {sc_clicks}</p>
</body>
</html>
"""

# Download Logic
if st.button("Generate PDF"):
    pdf_bytes = HTML(string=html_content).write_pdf()
    st.download_button("📥 Download PDF", pdf_bytes, "report.pdf", "application/pdf")
