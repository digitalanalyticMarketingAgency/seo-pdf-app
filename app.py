# ============================================================
# SEO PERFORMANCE REPORT GENERATOR - PROFESSIONAL EDITION
# Agency: Digital Analytic | digital-analytic.com
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import datetime
import random
import tempfile
import os
import requests
from fpdf import FPDF

# ============================================================
# 1. APP CONFIG
# ============================================================
st.set_page_config(
    page_title="SEO Report Generator | Digital Analytic",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. THEME & AGENCY CONFIGURATION
# ============================================================
THEMES = {
    "Light": {
        "bg_primary": (255, 255, 255),
        "bg_secondary": (248, 250, 252),
        "text_primary": (15, 23, 42),
        "text_secondary": (100, 116, 139),
        "accent": (139, 92, 246),
        "success": (22, 163, 74),
        "warning": (245, 158, 11),
        "error": (239, 68, 68),
        "border": (226, 232, 240),
    },
    "Dark": {
        "bg_primary": (15, 23, 42),
        "bg_secondary": (30, 41, 59),
        "text_primary": (255, 255, 255),
        "text_secondary": (200, 200, 200),
        "accent": (150, 100, 255),
        "success": (22, 163, 74),
        "warning": (245, 158, 11),
        "error": (239, 68, 68),
        "border": (51, 65, 85),
    }
}

AGENCY_INFO = {
    "name": "Digital Analytic",
    "website": "digital-analytic.com",
    "phone": "+8801940222254",
    "email": "digitalanalyticofficial@gmail.com",
    "logo_url": "https://github.com/digitalanalyticMarketingAgency/seo-pdf-app/blob/main/digital-analytic-logo.png?raw=true"
}

# ============================================================
# 3. SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    defaults = {
        "client_name": "",
        "client_website": "",
        "report_title": "Monthly SEO Performance Report",
        "report_description": "",
        "selected_theme": "Light",
        "selected_font": "Helvetica",
        "report_date": datetime.date.today().strftime("%B %Y"),
        "comparison_enabled": True,
        "sc_clicks": 450,
        "sc_impressions": 17600,
        "sc_ctr": 2.6,
        "sc_position": 14.3,
        "sc_clicks_prev": 380,
        "sc_impressions_prev": 15200,
        "sc_ctr_prev": 2.5,
        "sc_position_prev": 15.1,
        "rt_visit": 9238,
        "rt_revenue": 5934.48,
        "rt_impression": 17600,
        "rt_ecommerce": 423,
        "rt_purchase_revenue": 9785.37,
        "rt_transaction": 823,
        "kw_1_15": 42,
        "kw_16_30": 28,
        "kw_31_45": 19,
        "kw_46_60": 12,
        "kw_60_100": 8,
        "top_keywords": [
            {"keyword": "seo service bangladesh", "position": 3, "volume": 1200, "difficulty": 45},
            {"keyword": "digital marketing agency", "position": 5, "volume": 2400, "difficulty": 62},
            {"keyword": "website development", "position": 7, "volume": 1800, "difficulty": 55},
            {"keyword": "social media marketing", "position": 4, "volume": 3200, "difficulty": 58},
            {"keyword": "google ads service", "position": 8, "volume": 900, "difficulty": 42},
        ],
        "bl_profile": 335300,
        "bl_citation": 32000,
        "bl_web2": 97400,
        "bl_social": 237800,
        "bl_guest": 51900,
        "bl_comment": 16900,
        "ta_click": 872700,
        "ta_impression": 248800000,
        "ta_ctr": 5.36,
        "ta_position": 13.38,
        "tech_indexed": 1240,
        "tech_404": 3,
        "tech_crawled_not_indexed": 42,
        "tech_discovered_not_indexed": 18,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================
# 4. HELPER FUNCTIONS
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

def calc_growth(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def growth_indicator(growth, for_pdf=False):
    if growth > 0:
        if for_pdf:
            return f"+{growth:.1f}%", "#16a34a"
        return f"↑ {growth:.1f}%", "#16a34a"
    elif growth < 0:
        if for_pdf:
            return f"-{abs(growth):.1f}%", "#ef4444"
        return f"↓ {abs(growth):.1f}%", "#ef4444"
    else:
        if for_pdf:
            return "0%", "#64748b"
        return "→ 0%", "#64748b"

def download_agency_logo(tmpdir):
    """Download agency logo from URL and save to temp directory"""
    try:
        response = requests.get(AGENCY_INFO["logo_url"], timeout=10)
        if response.status_code == 200:
            logo_path = os.path.join(tmpdir, "agency_logo.png")
            with open(logo_path, "wb") as f:
                f.write(response.content)
            return logo_path
    except Exception as e:
        st.warning(f"Could not download logo: {e}")
    return None


# ============================================================
# 5. PDF CLASS (FPDF2 - DYNAMIC FLOW WITH WHITE TEXT)
# ============================================================
class SEOReportPDF(FPDF):
    def __init__(self, theme="Light", font="Helvetica"):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.theme = THEMES[theme]
        self.selected_font = font
        self.page_width = 210
        self.page_height = 297
        self.margin = 15
        self.content_width = self.page_width - (2 * self.margin)
        self.usable_height = self.page_height - 50
        
    def header(self):
        if os.path.exists('a4.png'):
            self.image('a4.png', 0, 0, 210, 297)
        
        if self.page_no() > 1:
            self.set_font(self.selected_font, 'B', 9)
            self.set_text_color(200, 200, 200)
            self.set_xy(self.margin, 8)
            self.cell(0, 5, AGENCY_INFO["name"], 0, 0, 'L')
            self.cell(0, 5, st.session_state.report_date, 0, 0, 'R')
        
        self.set_y(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font(self.selected_font, '', 7)
        self.set_text_color(180, 180, 180)
        footer_text = f"{AGENCY_INFO['website']} | {AGENCY_INFO['phone']}"
        self.cell(0, 4, footer_text, 0, 0, 'C')
        self.set_font(self.selected_font, 'B', 8)
        self.set_text_color(*self.theme["accent"])
        self.set_y(-10)
        self.cell(0, 4, f"Page {self.page_no()}", 0, 0, 'C')
    
    def get_current_y(self):
        return self.get_y()
    
    def check_page_break(self, height_needed):
        if self.get_y() + height_needed > self.usable_height:
            self.add_page()
            return True
        return False
    
    def set_white_text(self):
        self.set_text_color(255, 255, 255)
    
    def set_light_gray_text(self):
        self.set_text_color(200, 200, 200)
        
    def set_fill_theme(self, color_type):
        self.set_fill_color(*self.theme[color_type])
    
    def add_cover_page(self, logo_path, client_name, client_website, report_title, report_description):
        self.add_page()
        
        # Accent bar
        self.set_fill_color(*self.theme["accent"])
        self.rect(0, 0, 210, 6, 'F')
        
        # Agency Logo (always shown)
        y = 45
        if logo_path and os.path.exists(logo_path):
            self.image(logo_path, x=65, y=35, w=80)
            y = 105
        
        # Title
        self.set_y(y)
        self.set_font(self.selected_font, 'B', 26)
        self.set_white_text()
        self.multi_cell(0, 11, report_title, 0, 'C')
        
        # Decorative line
        self.set_fill_color(*self.theme["accent"])
        self.rect(70, self.get_y() + 3, 70, 2, 'F')
        self.ln(15)
        
        # Client info
        if client_name:
            self.set_font(self.selected_font, '', 12)
            self.set_light_gray_text()
            self.cell(0, 7, "Prepared for:", 0, 1, 'C')
            self.set_font(self.selected_font, 'B', 16)
            self.set_white_text()
            self.cell(0, 9, client_name, 0, 1, 'C')
            if client_website:
                self.set_font(self.selected_font, '', 11)
                self.set_text_color(*self.theme["accent"])
                self.cell(0, 7, client_website, 0, 1, 'C')
        
        # Description
        if report_description:
            self.ln(8)
            self.set_font(self.selected_font, '', 10)
            self.set_light_gray_text()
            self.set_x(30)
            self.multi_cell(150, 5, report_description, 0, 'C')
        
        # Bottom info
        self.set_y(250)
        self.set_font(self.selected_font, '', 11)
        self.set_light_gray_text()
        self.cell(0, 6, st.session_state.report_date, 0, 1, 'C')
        self.set_font(self.selected_font, 'B', 12)
        self.set_text_color(*self.theme["accent"])
        self.cell(0, 7, AGENCY_INFO["name"], 0, 1, 'C')
    
    def add_section_title(self, title, section_num=None, space_needed=15):
        self.check_page_break(space_needed)
        self.ln(3)
        self.set_fill_color(*self.theme["accent"])
        self.rect(self.margin, self.get_y(), 3, 8, 'F')
        self.set_x(self.margin + 6)
        self.set_font(self.selected_font, 'B', 12)
        self.set_white_text()
        text = f"{section_num}. {title}" if section_num else title
        self.cell(0, 8, text, 0, 1, 'L')
        self.ln(2)
    
    def add_metrics_row(self, metrics, card_height=28):
        self.check_page_break(card_height + 5)
        
        num_cards = len(metrics)
        card_width = (self.content_width - (num_cards - 1) * 3) / num_cards
        start_x = self.margin
        start_y = self.get_y()
        
        for i, (label, value, color) in enumerate(metrics):
            x = start_x + i * (card_width + 3)
            
            self.set_fill_color(30, 41, 59)
            self.rect(x, start_y, card_width, card_height, 'F')
            
            self.set_fill_color(*color)
            self.rect(x, start_y, card_width, 2, 'F')
            
            self.set_xy(x, start_y + 5)
            self.set_font(self.selected_font, '', 7)
            self.set_light_gray_text()
            self.cell(card_width, 4, label.upper(), 0, 0, 'C')
            
            self.set_xy(x, start_y + 12)
            self.set_font(self.selected_font, 'B', 12)
            self.set_text_color(*color)
            self.cell(card_width, 8, str(value), 0, 0, 'C')
        
        self.set_y(start_y + card_height + 3)
    
    def add_chart(self, image_path, width=170, height_estimate=60):
        if not os.path.exists(image_path):
            return
        
        self.check_page_break(height_estimate)
        x = (self.page_width - width) / 2
        self.image(image_path, x=x, w=width)
        self.ln(3)
    
    def add_keywords_table(self, keywords):
        row_height = 7
        total_height = (len(keywords) + 1) * row_height + 5
        self.check_page_break(total_height)
        
        col_widths = [65, 25, 30, 30]
        headers = ["Keyword", "Pos", "Volume", "Diff"]
        x_start = self.margin + 5
        
        self.set_fill_color(*self.theme["accent"])
        self.set_text_color(255, 255, 255)
        self.set_font(self.selected_font, 'B', 8)
        self.set_x(x_start)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], row_height, header, 1, 0, 'C', fill=True)
        self.ln()
        
        self.set_font(self.selected_font, '', 8)
        for kw in keywords:
            self.set_x(x_start)
            
            self.set_fill_color(30, 41, 59)
            
            self.set_white_text()
            self.cell(col_widths[0], row_height, kw["keyword"][:30], 1, 0, 'L', fill=True)
            
            pos = kw["position"]
            if pos <= 10:
                self.set_text_color(*self.theme["success"])
            elif pos <= 30:
                self.set_text_color(*self.theme["warning"])
            else:
                self.set_text_color(*self.theme["error"])
            self.cell(col_widths[1], row_height, str(pos), 1, 0, 'C', fill=True)
            
            self.set_white_text()
            self.cell(col_widths[2], row_height, fmt_int(kw["volume"]), 1, 0, 'C', fill=True)
            
            diff = kw["difficulty"]
            if diff <= 40:
                self.set_text_color(*self.theme["success"])
            elif diff <= 60:
                self.set_text_color(*self.theme["warning"])
            else:
                self.set_text_color(*self.theme["error"])
            self.cell(col_widths[3], row_height, f"{diff}%", 1, 0, 'C', fill=True)
            self.ln()
        
        self.ln(3)
    
    def add_backlinks_grid(self, backlinks):
        self.check_page_break(45)
        
        colors = [
            (37, 99, 235), (139, 92, 246), (22, 163, 74),
            (245, 158, 11), (239, 68, 68), (6, 182, 212)
        ]
        
        card_width = 55
        card_height = 20
        start_x = self.margin + 5
        start_y = self.get_y()
        
        for i, (label, value) in enumerate(backlinks.items()):
            col = i % 3
            row = i // 3
            x = start_x + col * (card_width + 5)
            y = start_y + row * (card_height + 3)
            
            self.set_fill_color(30, 41, 59)
            self.rect(x, y, card_width, card_height, 'F')
            self.set_fill_color(*colors[i])
            self.rect(x, y, card_width, 2, 'F')
            
            self.set_xy(x + 3, y + 5)
            self.set_font(self.selected_font, '', 6)
            self.set_light_gray_text()
            self.cell(card_width - 6, 3, label[:20], 0, 0, 'L')
            
            self.set_xy(x + 3, y + 11)
            self.set_font(self.selected_font, 'B', 10)
            self.set_text_color(*colors[i])
            self.cell(card_width - 6, 5, fmt_compact(value), 0, 0, 'L')
        
        self.set_y(start_y + 2 * (card_height + 3) + 5)
    
    def add_technical_section(self, indexed, error_404, crawled, discovered):
        self.check_page_break(40)
        
        start_y = self.get_y()
        
        self.set_fill_color(30, 41, 59)
        self.rect(self.margin, start_y, 70, 35, 'F')
        self.set_fill_color(*self.theme["success"])
        self.rect(self.margin, start_y, 70, 3, 'F')
        
        self.set_xy(self.margin, start_y + 8)
        self.set_font(self.selected_font, '', 8)
        self.set_light_gray_text()
        self.cell(70, 4, "INDEXED PAGES", 0, 0, 'C')
        
        self.set_xy(self.margin, start_y + 16)
        self.set_font(self.selected_font, 'B', 20)
        self.set_text_color(*self.theme["success"])
        self.cell(70, 10, fmt_int(indexed), 0, 0, 'C')
        
        x_error = self.margin + 80
        errors = [
            ("404 Errors", error_404, self.theme["error"]),
            ("Crawled-Not Indexed", crawled, self.theme["warning"]),
            ("Discovered-Not Indexed", discovered, self.theme["warning"])
        ]
        
        for i, (label, value, color) in enumerate(errors):
            y = start_y + i * 12
            self.set_fill_color(*color)
            self.rect(x_error, y, 3, 10, 'F')
            
            self.set_xy(x_error + 6, y + 1)
            self.set_font(self.selected_font, '', 7)
            self.set_light_gray_text()
            self.cell(60, 4, label, 0, 0, 'L')
            
            self.set_xy(x_error + 6, y + 5)
            self.set_font(self.selected_font, 'B', 9)
            self.set_text_color(*color)
            self.cell(60, 4, f"{fmt_int(value)} pages", 0, 0, 'L')
        
        self.set_y(start_y + 40)
    
    def add_thank_you(self):
        self.add_page()
        
        self.set_y(80)
        self.set_font(self.selected_font, 'B', 28)
        self.set_white_text()
        self.cell(0, 15, "Thank You!", 0, 1, 'C')
        
        self.ln(8)
        self.set_font(self.selected_font, '', 10)
        self.set_light_gray_text()
        msg = """Thank you for reviewing your SEO performance report.

At Digital Analytic, we believe that data tells a story beyond just numbers; it is the roadmap for the digital evolution of your brand. We are deeply committed to driving your business growth by optimizing your web presence and ensuring you stay ahead in the competitive search landscape.

Your goals remain at the heart of our strategy. We are constantly analyzing these insights to refine our approach and maximize your impact. If you have any questions regarding these metrics or would like to discuss our strategic roadmap for the coming month, please feel free to reach out. We are always here to support your success."""
        self.set_x(35)
        self.multi_cell(140, 5, msg, 0, 'C')
        
        self.ln(15)
        self.set_font(self.selected_font, 'B', 12)
        self.set_text_color(*self.theme["accent"])
        self.cell(0, 6, AGENCY_INFO["name"], 0, 1, 'C')
        self.set_font(self.selected_font, '', 9)
        self.set_light_gray_text()
        self.cell(0, 5, f"{AGENCY_INFO['website']} | {AGENCY_INFO['phone']}", 0, 1, 'C')


# ============================================================
# 6. PDF GENERATION FUNCTION
# ============================================================
def generate_pdf(chart_paths, logo_path=None):
    pdf = SEOReportPDF(
        theme=st.session_state.selected_theme,
        font=st.session_state.selected_font
    )
    
    pdf.add_cover_page(
        logo_path=logo_path,
        client_name=st.session_state.client_name,
        client_website=st.session_state.client_website,
        report_title=st.session_state.report_title,
        report_description=st.session_state.report_description
    )
    
    pdf.add_page()
    
    # Section 1: Search Console
    pdf.add_section_title("Search Console Performance", 1)
    pdf.add_metrics_row([
        ("Clicks", fmt_int(st.session_state.sc_clicks), (66, 133, 244)),
        ("Impressions", fmt_int(st.session_state.sc_impressions), (142, 36, 170)),
        ("CTR", f"{st.session_state.sc_ctr:.2f}%", (22, 163, 74)),
        ("Position", f"{st.session_state.sc_position:.1f}", (245, 158, 11))
    ])
    pdf.add_chart(chart_paths['sc_chart'], width=170, height_estimate=55)
    
    # Section 2: Revenue & Traffic
    pdf.add_section_title("Revenue & Traffic Dashboard", 2)
    pdf.add_metrics_row([
        ("Visits", fmt_int(st.session_state.rt_visit), (100, 200, 255)),
        ("Revenue", fmt_money(st.session_state.rt_revenue), (22, 163, 74)),
        ("Purchases", fmt_int(st.session_state.rt_ecommerce), (139, 92, 246))
    ])
    pdf.add_metrics_row([
        ("Impressions", fmt_int(st.session_state.rt_impression), (66, 133, 244)),
        ("Purchase Rev", fmt_money(st.session_state.rt_purchase_revenue), (245, 158, 11)),
        ("Transactions", fmt_int(st.session_state.rt_transaction), (150, 180, 200))
    ])
    
    # Section 3: Keywords
    pdf.add_section_title("Keyword Ranking Distribution", 3)
    pdf.add_chart(chart_paths['kw_chart'], width=170, height_estimate=50)
    
    # Section 4: Top Keywords Table
    pdf.add_section_title("Top Performing Keywords", 4)
    pdf.add_keywords_table(st.session_state.top_keywords)
    
    # Section 5: Backlinks
    pdf.add_section_title("Backlink Profile", 5)
    backlinks = {
        "Profile": st.session_state.bl_profile,
        "Citation": st.session_state.bl_citation,
        "Web 2.0": st.session_state.bl_web2,
        "Social": st.session_state.bl_social,
        "Guest Post": st.session_state.bl_guest,
        "Comment": st.session_state.bl_comment
    }
    pdf.add_backlinks_grid(backlinks)
    pdf.add_chart(chart_paths['bl_chart'], width=100, height_estimate=60)
    
    # Section 6: Technical SEO
    pdf.add_section_title("Technical SEO & Indexing", 6)
    pdf.add_technical_section(
        st.session_state.tech_indexed,
        st.session_state.tech_404,
        st.session_state.tech_crawled_not_indexed,
        st.session_state.tech_discovered_not_indexed
    )
    
    # Section 7: Traffic Analytics
    pdf.add_section_title("Traffic Analytics Summary", 7)
    pdf.add_metrics_row([
        ("Clicks", fmt_compact(st.session_state.ta_click), (66, 133, 244)),
        ("Impressions", fmt_compact(st.session_state.ta_impression), (142, 36, 170)),
        ("CTR", f"{st.session_state.ta_ctr:.2f}%", (22, 163, 74)),
        ("Position", f"{st.session_state.ta_position:.2f}", (245, 158, 11))
    ])
    
    pdf.add_thank_you()
    
    return bytes(pdf.output())


# ============================================================
# 7. CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%) !important; 
    }
    [data-testid="stSidebar"] label {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-card .label {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
    }
    .metric-card .value {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 8px;
    }
    .metric-card .growth {
        font-size: 12px;
        font-weight: 700;
        margin-top: 6px;
    }
    .growth-up { color: #16a34a; }
    .growth-down { color: #ef4444; }
    
    .backlink-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
    }
    .backlink-card .label {
        font-size: 10px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
    .backlink-card .value {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
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
    
    .section-header {
        background: linear-gradient(90deg, #8b5cf6 0%, #a78bfa 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 20px 0 15px 0;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 8. SIDEBAR (LOGO UPLOAD REMOVED)
# ============================================================
with st.sidebar:
    st.image(AGENCY_INFO["logo_url"], width=180)
    
    st.markdown("---")
    st.header("📋 Report Settings")
    
    st.text_input("Report Title", value=st.session_state.report_title, key="report_title")
    st.text_input("Reporting Period", value=st.session_state.report_date, key="report_date")
    st.text_area("Report Description", value=st.session_state.report_description, 
                 placeholder="Brief overview of this month's SEO activities...", key="report_description")
    
    st.markdown("---")
    st.header("👤 Client Information")
    
    st.text_input("Client Name", value=st.session_state.client_name, placeholder="ABC Company Ltd.", key="client_name")
    st.text_input("Client Website", value=st.session_state.client_website, placeholder="www.example.com", key="client_website")
    
    st.markdown("---")
    st.header("🎨 Theme & Style")
    
    st.selectbox("PDF Theme", options=["Light", "Dark"], key="selected_theme")
    st.selectbox("Font Style", options=["Helvetica", "Times", "Courier"], key="selected_font")
    st.checkbox("Show Month-over-Month Comparison", value=True, key="comparison_enabled")
    
    st.markdown("---")
    st.header("1️⃣ Search Console - Current")
    
    st.number_input("Total Clicks", min_value=0, key="sc_clicks")
    st.number_input("Total Impressions", min_value=0, key="sc_impressions")
    st.number_input("Average CTR (%)", min_value=0.0, format="%.2f", key="sc_ctr")
    st.number_input("Average Position", min_value=0.0, format="%.1f", key="sc_position")
    
    if st.session_state.comparison_enabled:
        st.markdown("**Previous Month:**")
        st.number_input("Clicks (Prev)", min_value=0, key="sc_clicks_prev")
        st.number_input("Impressions (Prev)", min_value=0, key="sc_impressions_prev")
        st.number_input("CTR (Prev) %", min_value=0.0, format="%.2f", key="sc_ctr_prev")
        st.number_input("Position (Prev)", min_value=0.0, format="%.1f", key="sc_position_prev")
    
    st.markdown("---")
    st.header("2️⃣ Revenue & Traffic")
    
    st.number_input("Visits", min_value=0, key="rt_visit")
    st.number_input("Total Revenue ($)", min_value=0.0, format="%.2f", key="rt_revenue")
    st.number_input("Impressions", min_value=0, key="rt_impression")
    st.number_input("Ecommerce Purchases", min_value=0, key="rt_ecommerce")
    st.number_input("Purchases Revenue ($)", min_value=0.0, format="%.2f", key="rt_purchase_revenue")
    st.number_input("Transactions", min_value=0, key="rt_transaction")
    
    st.markdown("---")
    st.header("3️⃣ Keyword Ranking")
    
    st.number_input("1 to 15 result", min_value=0, key="kw_1_15")
    st.number_input("16 to 30 result", min_value=0, key="kw_16_30")
    st.number_input("31 to 45 result", min_value=0, key="kw_31_45")
    st.number_input("46 to 60 result", min_value=0, key="kw_46_60")
    st.number_input("60 to 100 result", min_value=0, key="kw_60_100")
    
    st.markdown("---")
    st.header("4️⃣ Backlink Profile")
    
    st.number_input("Profile Backlinks", min_value=0, key="bl_profile")
    st.number_input("Citation", min_value=0, key="bl_citation")
    st.number_input("Web 2.0", min_value=0, key="bl_web2")
    st.number_input("Social Share", min_value=0, key="bl_social")
    st.number_input("Guest Post", min_value=0, key="bl_guest")
    st.number_input("Comment Backlink", min_value=0, key="bl_comment")
    
    st.markdown("---")
    st.header("5️⃣ Traffic Analytics")
    
    st.number_input("Click", min_value=0, key="ta_click")
    st.number_input("Total Impression", min_value=0, key="ta_impression")
    st.number_input("CTR (%)", min_value=0.0, format="%.2f", key="ta_ctr")
    st.number_input("Average Position", min_value=0.0, format="%.2f", key="ta_position")
    
    st.markdown("---")
    st.header("6️⃣ Technical SEO")
    
    st.number_input("Indexing Page (Valid)", min_value=0, key="tech_indexed")
    st.number_input("Not Found (404)", min_value=0, key="tech_404")
    st.number_input("Crawled - Not Indexed", min_value=0, key="tech_crawled_not_indexed")
    st.number_input("Discovered - Not Indexed", min_value=0, key="tech_discovered_not_indexed")


# ============================================================
# 9. MAIN DASHBOARD
# ============================================================
st.title("📈 SEO Performance Report Generator")
st.caption(f"Professional SEO Reports by {AGENCY_INFO['name']} | {AGENCY_INFO['website']}")

if st.session_state.client_name:
    st.info(f"📋 **Report for:** {st.session_state.client_name} | {st.session_state.client_website}")

st.markdown("---")

# SECTION 1: SEARCH CONSOLE
st.markdown('<div class="section-header">1. Search Console Performance</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

clicks_growth = calc_growth(st.session_state.sc_clicks, st.session_state.sc_clicks_prev)
impr_growth = calc_growth(st.session_state.sc_impressions, st.session_state.sc_impressions_prev)
ctr_growth = calc_growth(st.session_state.sc_ctr, st.session_state.sc_ctr_prev)
pos_growth = calc_growth(st.session_state.sc_position_prev, st.session_state.sc_position)

def render_metric_card(label, value, growth=None, color="#0f172a"):
    growth_html = ""
    if growth is not None and st.session_state.comparison_enabled:
        indicator, ind_color = growth_indicator(growth)
        growth_class = "growth-up" if growth > 0 else "growth-down"
        growth_html = f'<div class="growth {growth_class}">{indicator}</div>'
    return f'''
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value" style="color:{color};">{value}</div>
        {growth_html}
    </div>
    '''

with c1:
    st.markdown(render_metric_card("Total Clicks", fmt_int(st.session_state.sc_clicks), clicks_growth, "#4285F4"), unsafe_allow_html=True)
with c2:
    st.markdown(render_metric_card("Total Impressions", fmt_int(st.session_state.sc_impressions), impr_growth, "#8E24AA"), unsafe_allow_html=True)
with c3:
    st.markdown(render_metric_card("Average CTR", f"{st.session_state.sc_ctr:.2f}%", ctr_growth, "#16a34a"), unsafe_allow_html=True)
with c4:
    st.markdown(render_metric_card("Average Position", f"{st.session_state.sc_position:.1f}", pos_growth, "#f59e0b"), unsafe_allow_html=True)

# Trend Chart
_seed = int(st.session_state.sc_clicks + st.session_state.sc_impressions)
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
clicks_trend = _trend(st.session_state.sc_clicks)
impressions_trend = _trend(st.session_state.sc_impressions)

sc_fig = go.Figure()
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=clicks_trend,
    mode="lines+markers", name="Clicks",
    line=dict(color="#4285F4", width=3),
    marker=dict(size=8), yaxis="y1"
))
sc_fig.add_trace(go.Scatter(
    x=trend_dates, y=impressions_trend,
    mode="lines+markers", name="Impressions",
    line=dict(color="#8E24AA", width=3),
    marker=dict(size=8), yaxis="y2"
))
sc_fig.update_layout(
    height=350,
    margin=dict(l=60, r=60, t=40, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    yaxis=dict(title=dict(text="Clicks", font=dict(color="#4285F4")), tickfont=dict(color="#4285F4"), showgrid=True, gridcolor="#f1f5f9"),
    yaxis2=dict(title=dict(text="Impressions", font=dict(color="#8E24AA")), tickfont=dict(color="#8E24AA"), overlaying="y", side="right", showgrid=False),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(sc_fig, use_container_width=True)

st.markdown("---")

# SECTION 2: REVENUE & TRAFFIC
st.markdown('<div class="section-header">2. Revenue & Traffic Dashboard</div>', unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1:
    st.markdown(f'<div class="metric-card">🧑‍💻<div class="label">Visit</div><div class="value">{fmt_int(st.session_state.rt_visit)}</div></div>', unsafe_allow_html=True)
with r1c2:
    st.markdown(f'<div class="metric-card">💵<div class="label">Total Revenue</div><div class="value">{fmt_money(st.session_state.rt_revenue)}</div></div>', unsafe_allow_html=True)
with r1c3:
    st.markdown(f'<div class="metric-card">👁️<div class="label">Impression</div><div class="value">{fmt_int(st.session_state.rt_impression)}</div></div>', unsafe_allow_html=True)
with r2c1:
    st.markdown(f'<div class="metric-card">🛒<div class="label">Ecommerce Purchases</div><div class="value">{fmt_int(st.session_state.rt_ecommerce)}</div></div>', unsafe_allow_html=True)
with r2c2:
    st.markdown(f'<div class="metric-card">💰<div class="label">Purchases Revenue</div><div class="value">{fmt_money(st.session_state.rt_purchase_revenue)}</div></div>', unsafe_allow_html=True)
with r2c3:
    st.markdown(f'<div class="metric-card">🧾<div class="label">Transaction</div><div class="value">{fmt_int(st.session_state.rt_transaction)}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# SECTION 3: KEYWORD RANKING
st.markdown('<div class="section-header">3. Top Keyword Ranking Distribution</div>', unsafe_allow_html=True)

kw_labels = ["1 to 15", "16 to 30", "31 to 45", "46 to 60", "60 to 100"]
kw_values = [st.session_state.kw_1_15, st.session_state.kw_16_30, st.session_state.kw_31_45, 
             st.session_state.kw_46_60, st.session_state.kw_60_100]
kw_colors = ["#2563eb", "#8b5cf6", "#f59e0b", "#ef4444", "#64748b"]

kw_fig = go.Figure(go.Bar(
    x=kw_values, y=kw_labels, orientation="h",
    marker_color=kw_colors, text=kw_values, textposition="outside",
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

# Top Keywords Table
st.subheader("📊 Top Performing Keywords")

for i, kw in enumerate(st.session_state.top_keywords):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    with col1:
        new_kw = st.text_input(f"Keyword {i+1}", value=kw["keyword"], key=f"kw_name_{i}", label_visibility="collapsed")
        st.session_state.top_keywords[i]["keyword"] = new_kw
    with col2:
        new_pos = st.number_input(f"Pos {i+1}", value=kw["position"], min_value=1, key=f"kw_pos_{i}", label_visibility="collapsed")
        st.session_state.top_keywords[i]["position"] = new_pos
    with col3:
        new_vol = st.number_input(f"Vol {i+1}", value=kw["volume"], min_value=0, key=f"kw_vol_{i}", label_visibility="collapsed")
        st.session_state.top_keywords[i]["volume"] = new_vol
    with col4:
        new_diff = st.number_input(f"Diff {i+1}", value=kw["difficulty"], min_value=0, max_value=100, key=f"kw_diff_{i}", label_visibility="collapsed")
        st.session_state.top_keywords[i]["difficulty"] = new_diff
    with col5:
        if st.button("🗑️", key=f"del_kw_{i}"):
            st.session_state.top_keywords.pop(i)
            st.rerun()

if st.button("➕ Add Keyword"):
    st.session_state.top_keywords.append({"keyword": "new keyword", "position": 10, "volume": 500, "difficulty": 50})
    st.rerun()

st.markdown("---")

# SECTION 4: BACKLINK PROFILE
st.markdown('<div class="section-header">4. Backlink Profile</div>', unsafe_allow_html=True)

bl_labels = ["Profile Backlinks", "Citation", "Web 2.0", "Social Share", "Guest Post", "Comment Backlink"]
bl_values = [st.session_state.bl_profile, st.session_state.bl_citation, st.session_state.bl_web2, 
             st.session_state.bl_social, st.session_state.bl_guest, st.session_state.bl_comment]
bl_colors = ["#2563eb", "#8b5cf6", "#16a34a", "#f59e0b", "#ef4444", "#06b6d4"]

bl_col1, bl_col2 = st.columns([1, 1])

with bl_col1:
    card_cols = st.columns(2)
    for i, (label, value) in enumerate(zip(bl_labels, bl_values)):
        with card_cols[i % 2]:
            st.markdown(f'<div class="backlink-card"><div class="label">{label}</div><div class="value">{fmt_compact(value)}</div></div>', unsafe_allow_html=True)

with bl_col2:
    donut_fig = go.Figure(go.Pie(
        labels=bl_labels, values=bl_values, hole=0.55,
        marker=dict(colors=bl_colors), textinfo="percent", textfont=dict(size=12)
    ))
    donut_fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    st.plotly_chart(donut_fig, use_container_width=True)

st.markdown("---")

# SECTION 5: TRAFFIC ANALYTICS
st.markdown('<div class="section-header">5. Traffic Analytics Summary</div>', unsafe_allow_html=True)

ta_col1, ta_col2, ta_col3, ta_col4 = st.columns(4)
with ta_col1:
    st.markdown(f'<div class="traffic-summary-label">Click</div><div class="traffic-summary-value">{fmt_compact(st.session_state.ta_click)}</div>', unsafe_allow_html=True)
with ta_col2:
    st.markdown(f'<div class="traffic-summary-label">Total Impression</div><div class="traffic-summary-value">{fmt_compact(st.session_state.ta_impression)}</div>', unsafe_allow_html=True)
with ta_col3:
    st.markdown(f'<div class="traffic-summary-label">CTR</div><div class="traffic-summary-value">{st.session_state.ta_ctr:.2f}%</div>', unsafe_allow_html=True)
with ta_col4:
    st.markdown(f'<div class="traffic-summary-label">Average Position</div><div class="traffic-summary-value">{st.session_state.ta_position:.2f}</div>', unsafe_allow_html=True)

st.markdown("---")

# SECTION 6: TECHNICAL SEO
st.markdown('<div class="section-header">6. Technical SEO & Indexing Health</div>', unsafe_allow_html=True)

tech_col1, tech_col2 = st.columns([1, 1.4])

with tech_col1:
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.tech_indexed,
        number={"font": {"size": 42, "color": "#16a34a"}},
        title={"text": "Indexed Pages (Valid)", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, max(st.session_state.tech_indexed * 1.2, 1)], "visible": False},
            "bar": {"color": "#16a34a"},
            "bgcolor": "#f1f5f9",
            "borderwidth": 0,
        }
    ))
    gauge_fig.update_layout(height=280, margin=dict(l=40, r=40, t=60, b=30))
    st.plotly_chart(gauge_fig, use_container_width=True)

with tech_col2:
    st.markdown("**Errors & Warnings**")
    st.markdown(f'<div class="error-row">🔴 <b>Not Found (404):</b> {fmt_int(st.session_state.tech_404)} pages</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warn-row">🟠 <b>Crawled - Currently Not Indexed:</b> {fmt_int(st.session_state.tech_crawled_not_indexed)} pages</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warn-row">🟠 <b>Discovered - Currently Not Indexed:</b> {fmt_int(st.session_state.tech_discovered_not_indexed)} pages</div>', unsafe_allow_html=True)

st.markdown("---")

# SECTION 7: THANK YOU PREVIEW
st.markdown('<div class="section-header">7. Closing Page Preview</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 16px; margin: 20px 0; border: 1px solid #cbd5e1;">
    <h1 style="color: #0f172a; font-size: 36px; margin-bottom: 20px;">Thank You!</h1>
    <p style="max-width:650px; margin:0 auto; color:#64748b; font-size:16px; line-height:1.8;">
        Thank you for taking the time to review this SEO performance report. We are committed to driving
        continuous digital growth, optimizing your web presence, and ensuring top-tier search engine rankings
        for your business. Should you have any questions, please feel free to reach out to us.
    </p>
    <p style="margin-top:35px; color:#8b5cf6; font-size:14px; font-weight:700;">
        {AGENCY_INFO['name']} | {AGENCY_INFO['website']}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 10. PDF EXPORT (AUTOMATIC AGENCY LOGO)
# ============================================================
st.markdown('<div class="section-header">📥 Export Report</div>', unsafe_allow_html=True)

col_preview, col_download = st.columns(2)

with col_preview:
    if st.button("👁️ Preview PDF", use_container_width=True):
        st.info("PDF Preview feature coming soon...")

with col_download:
    if st.button("🚀 Generate & Download PDF", type="primary", use_container_width=True):
        with st.spinner("Generating professional PDF report..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                # Generate charts
                sc_chart_path = os.path.join(tmpdir, "sc_chart.png")
                kw_chart_path = os.path.join(tmpdir, "kw_chart.png")
                bl_chart_path = os.path.join(tmpdir, "bl_chart.png")
                
                sc_fig.write_image(sc_chart_path, width=800, height=300, scale=2)
                kw_fig.write_image(kw_chart_path, width=800, height=280, scale=2)
                donut_fig.write_image(bl_chart_path, width=400, height=350, scale=2)
                
                chart_paths = {
                    'sc_chart': sc_chart_path,
                    'kw_chart': kw_chart_path,
                    'bl_chart': bl_chart_path
                }
                
                # Download agency logo automatically
                logo_path = download_agency_logo(tmpdir)
                
                # Generate PDF
                pdf_bytes = generate_pdf(chart_paths, logo_path)
                
                st.success("✅ PDF generated successfully!")
                
                client_name_clean = st.session_state.client_name.replace(" ", "_") if st.session_state.client_name else "Client"
                filename = f"SEO_Report_{client_name_clean}_{st.session_state.report_date.replace(' ', '_')}.pdf"
                
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )

st.caption(f"© {datetime.date.today().year} {AGENCY_INFO['name']} | All reports are confidential.")
