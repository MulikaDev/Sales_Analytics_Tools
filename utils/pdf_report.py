from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, Flowable, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import pandas as pd

# ----------------- KPI WITH SPARKLINE AND LEGEND BELOW -----------------
class KPIIndicator(Flowable):
    def __init__(self, width=250, height=50, value=0, max_value=100, label="", fmt="{:.2f}", trend=None):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.value = value
        self.max_value = max_value
        self.label = label
        self.fmt = fmt
        self.trend = trend

    def draw(self):
        bar_height = 16
        spark_height = 6
        text_color = colors.white
        legend_size = 5
        legend_spacing = 40
        legend_offset = 2  # відступ між спарклайном і легендою

        # ----------------- TEXT -----------------
        self.canv.setFont("Helvetica-Bold", 9)
        self.canv.setFillColor(text_color)
        self.canv.drawString(2, bar_height + spark_height + 12, f"{self.label}")
        val_text = self.fmt.format(self.value)
        text_width = self.canv.stringWidth(val_text, "Helvetica-Bold", 9)
        self.canv.drawString(self.width - text_width, bar_height + spark_height + 12, val_text)

        # ----------------- BAR -----------------
        pct = self.value / self.max_value if self.max_value else 0
        bar_color = colors.HexColor("#27AE60") if pct > 0.7 else colors.HexColor("#F1C40F") if pct > 0.4 else colors.HexColor("#C0392B")
        self.canv.setFillColor(bar_color)
        self.canv.rect(0, spark_height + 6, self.width * pct, bar_height, fill=1)
        self.canv.setFillColor(colors.HexColor("#555555"))
        self.canv.rect(self.width * pct, spark_height + 6, self.width * (1 - pct), bar_height, fill=1)

        # ----------------- SPARKLINE -----------------
        spark_y = 6
        if self.trend and len(self.trend) > 1:
            max_trend = max(self.trend)
            min_trend = min(self.trend)
            self.canv.setLineWidth(1)
            for i in range(len(self.trend)-1):
                x1 = i * self.width / (len(self.trend)-1)
                y1 = spark_y * (self.trend[i]-min_trend)/(max_trend-min_trend+1e-5)
                x2 = (i+1) * self.width / (len(self.trend)-1)
                y2 = spark_y * (self.trend[i+1]-min_trend)/(max_trend-min_trend+1e-5)

                if self.trend[i+1] > self.trend[i]:
                    line_color = colors.green
                elif self.trend[i+1] < self.trend[i]:
                    line_color = colors.red
                else:
                    line_color = colors.white
                self.canv.setStrokeColor(line_color)
                self.canv.line(x1, y1, x2, y2)

        # ----------------- LEGEND під спарклайном -----------------
        legend_y = 0
        positions = [0, legend_spacing, legend_spacing*2]
        colors_list = [colors.green, colors.red, colors.white]
        labels = ["Growth", "Decline", "Stable"]

        for i in range(3):
            self.canv.setFillColor(colors_list[i])
            self.canv.rect(positions[i], legend_y, legend_size, legend_size, fill=1)
            self.canv.setFillColor(text_color)
            self.canv.setFont("Helvetica", 7)
            self.canv.drawString(positions[i] + legend_size + 2, legend_y, labels[i])

# ----------------- BACKGROUND -----------------
def add_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColorRGB(0.12, 0.12, 0.12)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.restoreState()

# ----------------- FOOTER -----------------
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    page_num = f"Page {doc.page} | Source: Google Sheet | Generated: {datetime.now().strftime('%d %B %Y %H:%M')}"
    canvas.drawRightString(A4[0] - 30, 15, page_num)
    canvas.restoreState()

# ----------------- CREATE DASHBOARD PDF -----------------
def create_dashboard_pdf(df_summary, chart_path, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=22, leading=26,
                                 textColor=colors.HexColor("#1ABC9C"), alignment=1)
    subtitle_style = ParagraphStyle(name='Subtitle', fontName='Helvetica', fontSize=10, leading=12,
                                    textColor=colors.HexColor("#CCCCCC"), alignment=1)
    header_style = ParagraphStyle(name='TableHeader', fontName='Helvetica-Bold', fontSize=9,
                                  textColor=colors.white, alignment=1)

    # ----------------- PAGE 1: TITLE + KPI -----------------
    elements.append(Paragraph("Sales Analytics Executive Dashboard", title_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Report generated on {datetime.now().strftime('%d %B %Y %H:%M')}", subtitle_style))
    elements.append(Spacer(1, 16))

    # ----------------- KPI calculations -----------------
    for col in ['total_profit', 'total_sales', 'avg_profit_margin', 'unit_price', 'cost_per_unit', 'units_sold']:
        df_summary[col+'_num'] = pd.to_numeric(df_summary[col].replace(r'[\$, %]', '', regex=True), errors='coerce')

    kpis = [
        # Старі KPI
        ("Top Profit", df_summary['total_profit_num'].max(), df_summary['total_profit_num'].max(), "${:,.2f}", df_summary['total_profit_num'].tolist()),
        ("Top Margin", df_summary['avg_profit_margin_num'].max(), 100, "{:.1f}%", df_summary['avg_profit_margin_num'].tolist()),
        ("Total Sales", df_summary['total_sales_num'].sum(), df_summary['total_sales_num'].sum(), "${:,.2f}", None),
        ("Avg Margin", df_summary['avg_profit_margin_num'].mean(), 100, "{:.1f}%", df_summary['avg_profit_margin_num'].tolist()),

        # Нові KPI
        ("Total Units Sold", df_summary['units_sold_num'].sum(), df_summary['units_sold_num'].sum(), "{:,.0f}", None),
        ("Avg Unit Price", df_summary['unit_price_num'].mean(), df_summary['unit_price_num'].max(), "${:,.2f}", df_summary['unit_price_num'].tolist()),
        ("Profit per Unit", (df_summary['total_profit_num'] / df_summary['units_sold_num']).mean(), (df_summary['total_profit_num'] / df_summary['units_sold_num']).max(), "${:,.2f}", None)
    ]

    for kpi in kpis:
        elements.append(KPIIndicator(width=250, height=50, value=kpi[1], max_value=kpi[2],
                                     label=kpi[0], fmt=kpi[3], trend=kpi[4]))
        elements.append(Spacer(1, 12))

    elements.append(PageBreak())

    # ----------------- PAGE 2: MAIN TABLE -----------------
    df_display = df_summary.loc[:, ~df_summary.columns.duplicated()].copy()
    if 'Date' in df_display.columns:
        df_display = df_display.drop(columns=['Date'])
    table_cols = ['product', 'units_sold', 'unit_price', 'cost_per_unit', 'total_sales', 'total_profit', 'avg_profit_margin']
    df_display = df_display[table_cols].copy()

    for col in ['unit_price', 'cost_per_unit', 'total_sales', 'total_profit', 'avg_profit_margin']:
        df_display[col] = pd.to_numeric(df_display[col].replace(r'[\$,%]', '', regex=True), errors='coerce')
    df_display['unit_price'] = df_display['unit_price'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    df_display['cost_per_unit'] = df_display['cost_per_unit'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    df_display['total_sales'] = df_display['total_sales'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    df_display['total_profit'] = df_display['total_profit'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    df_display['avg_profit_margin'] = df_display['avg_profit_margin'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "")

    col_widths = [max(50, min(120, max(df_display[col].astype(str).map(len).max(), len(col))*6)) for col in df_display.columns]
    headers = [Paragraph(col.replace('_', ' ').title(), header_style) for col in df_display.columns.tolist()]
    data = [headers] + df_display.values.tolist()

    table = Table(data, colWidths=col_widths, hAlign='CENTER')

    top_profit_indices = df_summary['total_profit_num'].nlargest(3).index.tolist()
    top_margin_indices = df_summary['avg_profit_margin_num'].nlargest(3).index.tolist()
    low_profit_indices = df_summary['total_profit_num'].nsmallest(2).index.tolist()

    row_colors = []
    for i in range(len(df_display)):
        if i in top_profit_indices or i in top_margin_indices:
            row_colors.append(colors.HexColor("#27AE60"))
        elif i in low_profit_indices:
            row_colors.append(colors.HexColor("#E74C3C"))
        else:
            row_colors.append(colors.HexColor("#34495E"))

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1ABC9C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,1), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), row_colors),
        ('GRID', (0,0), (-1,-1), 0.5, colors.white),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # ----------------- PAGE 3: CHART -----------------
    chart_width = A4[0] - doc.leftMargin - doc.rightMargin
    chart_height = chart_width * 0.5
    elements.append(Image(chart_path, width=chart_width, height=chart_height))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Figure: Total Sales and Profit per Product", subtitle_style))

    # ----------------- BUILD PDF -----------------
    doc.build(elements, onFirstPage=lambda c,d: (add_background(c,d), add_footer(c,d)),
              onLaterPages=lambda c,d: (add_background(c,d), add_footer(c,d)))
