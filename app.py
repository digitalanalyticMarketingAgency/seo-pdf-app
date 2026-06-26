import streamlit as st
from fpdf import FPDF
import datetime

# --- Page Config ---
st.set_page_config(page_title="SEO Report Generator", page_icon="📈", layout="centered")
st.title("📈 SEO Performance Report Builder")
st.write("Fill in the data below to generate a professional PDF report for your clients.")

# --- Custom FPDF Class for Header/Footer ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42) # Dark Blue Header
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'SEO PERFORMANCE REPORT', ln=1, align='L')
        self.set_font('helvetica', '', 10)
        self.set_text_color(200, 200, 200)
        self.cell(0, 8, f'Generated on: {datetime.date.today().strftime("%B %d, %Y")}', ln=1, align='L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'TrackPal Digital Agency - Confidential SEO Report', align='C')

# --- INPUT SECTIONS ---
with st.expander("1. Search Console Performance", expanded=True):
    col1, col2 = st.columns(2)
    sc_clicks = col1.text_input("Total Clicks", value="45")
    sc_impressions = col2.text_input("Total Impressions", value="17.6K")
    sc_ctr = col1.text_input("Average CTR", value="0.3%")
    sc_pos = col2.text_input("Average Position", value="30.3")

with st.expander("2. Revenue & Traffic Dashboard"):
    col1, col2 = st.columns(2)
    rev_visits = col1.text_input("Total Visits", value="9,238")
    rev_total = col2.text_input("Total Revenue", value="$5,934")
    rev_ecommerce = col1.text_input("Ecommerce Purchases", value="423")
    rev_transactions = col2.text_input("Transactions", value="823")

with st.expander("3. Keyword Ranking"):
    col1, col2 = st.columns(2)
    kw_1_15 = col1.number_input("Position 1 to 15", value=42)
    kw_16_30 = col2.number_input("Position 16 to 30", value=28)
    kw_31_45 = col1.number_input("Position 31 to 45", value=19)
    kw_46_60 = col2.number_input("Position 46 to 60", value=12)

with st.expander("4. Backlink Profile"):
    col1, col2, col3 = st.columns(3)
    bl_profile = col1.text_input("Profile Backlinks", value="335K")
    bl_citation = col2.text_input("Citation", value="32K")
    bl_web2 = col3.text_input("Web 2.0", value="97K")
    bl_social = col1.text_input("Social Share", value="237K")
    bl_guest = col2.text_input("Guest Post", value="51K")
    bl_comment = col3.text_input("Comment", value="16K")

with st.expander("5. Technical SEO & Indexing"):
    col1, col2 = st.columns(2)
    tech_indexed = col1.text_input("Indexing Pages", value="1,240")
    tech_404 = col2.text_input("Not Found (404)", value="3")
    tech_crawl_no = col1.text_input("Crawled - Not Indexed", value="42")
    tech_disc_no = col2.text_input("Discovered - Not Indexed", value="18")

# --- PDF GENERATION LOGIC ---
def generate_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def add_section_title(title):
        pdf.ln(5)
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 10, title, ln=1, border='B')
        pdf.ln(3)

    def add_data_row(label1, val1, label2, val2):
        pdf.set_font('helvetica', 'B', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(95, 6, label1, ln=0)
        pdf.cell(95, 6, label2, ln=1)
        
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(95, 8, str(val1), ln=0)
        pdf.cell(95, 8, str(val2), ln=1)
        pdf.ln(2)

    # Section 1
    add_section_title("1. Search Console Performance")
    add_data_row("Total Clicks", sc_clicks, "Total Impressions", sc_impressions)
    add_data_row("Average CTR", sc_ctr, "Average Position", sc_pos)

    # Section 2
    add_section_title("2. Revenue & Traffic Dashboard")
    add_data_row("Total Visits", rev_visits, "Total Revenue", rev_total)
    add_data_row("Ecommerce Purchases", rev_ecommerce, "Transactions", rev_transactions)

    # Section 3
    add_section_title("3. Top Keyword Ranking")
    add_data_row("Position 1 to 15", kw_1_15, "Position 16 to 30", kw_16_30)
    add_data_row("Position 31 to 45", kw_31_45, "Position 46 to 60", kw_46_60)

    # Section 4
    add_section_title("4. Backlink Profile")
    add_data_row("Profile Backlinks", bl_profile, "Citation", bl_citation)
    add_data_row("Web 2.0", bl_web2, "Social Share", bl_social)
    add_data_row("Guest Post", bl_guest, "Comment Links", bl_comment)

    # Section 5
    add_section_title("5. Technical SEO Health")
    add_data_row("Valid Indexing Pages", tech_indexed, "Not Found (404 Error)", tech_404)
    add_data_row("Crawled - Not Indexed", tech_crawl_no, "Discovered - Not Indexed", tech_disc_no)

    # Thank you page
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(66, 133, 244) # Google Blue
    pdf.cell(0, 10, 'Thank You!', ln=1, align='C')
    pdf.ln(10)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(50, 50, 50)
    msg = "Thank you for taking the time to review this SEO performance report. We are committed to driving continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings for your business."
    pdf.multi_cell(0, 8, msg, align='C')

    # Save to binary string for Streamlit download
    return pdf.output(dest='S').encode('latin-1')

# --- SUBMIT BUTTON ---
st.markdown("---")
if st.button("🚀 Generate PDF Report", use_container_width=True):
    with st.spinner("Generating PDF..."):
        pdf_bytes = generate_pdf()
        st.success("Report Generated Successfully!")
        
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name=f"SEO_Report_{datetime.date.today()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )