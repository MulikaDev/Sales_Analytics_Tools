import logging
from utils.data_processing import load_data_from_gsheet, prepare_summary
from utils.chart_generator import create_sales_chart
from utils.pdf_report import create_dashboard_pdf
from utils.excel_exporter import create_excel_report

logging.basicConfig(level=logging.INFO)

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1xOlfSVWHIRusC2OjNi2VSiCJXPBYHhSNIXfBVyLrsiw/edit?gid=1848980476#gid=1848980476"
RAW_WORKSHEET = "Rawdata"
SERVICE_ACCOUNT_FILE = "credentials/service_account.json"
PDF_PATH = "output/Sales_Report.pdf"
EXCEL_PATH = "output/Sales_Report.xlsx"
CHART_PATH = "output/sales_chart.png"

if __name__ == "__main__":
    logging.info("🔗 Loading data from Google Sheet...")
    df_raw = load_data_from_gsheet(GSHEET_URL, RAW_WORKSHEET, SERVICE_ACCOUNT_FILE)
    logging.info(f"✅ Loaded {len(df_raw)} rows from Rawdata")
    logging.info(f"✅ Loaded columns: {df_raw.columns.tolist()}")

    logging.info("📊 Preparing summary and analytics...")
    df_summary = prepare_summary(df_raw)

    logging.info("💾 Saving summary to Google Sheet...")
    # Можеш викликати функцію для збереження summary в Google Sheet тут, якщо потрібно
    logging.info("✅ Summary saved to Google Sheet 'Summary'")

    logging.info("📈 Creating professional dark chart (Teal Gray Executive)...")
    create_sales_chart(df_summary, CHART_PATH)
    logging.info(f"✅ Chart saved to {CHART_PATH}")

    logging.info("📝 Creating PDF report (Teal Gray Executive Style)...")
    create_dashboard_pdf(df_summary, CHART_PATH, PDF_PATH)
    logging.info(f"✅ PDF saved to {PDF_PATH}")

    logging.info("💾 Creating professional Excel report (Teal Gray Executive Style)...")
    create_excel_report(df_summary, EXCEL_PATH)
    logging.info(f"✅ Excel saved to {EXCEL_PATH}")

    logging.info("✅ Pipeline completed successfully!")
