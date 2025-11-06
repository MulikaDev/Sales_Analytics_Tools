# Sales Analytics Tools

**Sales Analytics Tools** is a professional toolkit for sales analysis, creating dashboards, and generating reports in PDF and Excel formats.  
Perfect for business analytics, quick KPI evaluation, and data visualization.

---

## 📊 Key Features
- Calculate **KPI**: total profit, margin, total sales, average unit price.  
- Visualize data with **bar charts** and **sparklines** in a professional dark theme.  
- Generate **Excel reports** with proper currency and percentage formatting.  
- Create **PDF dashboards** with tables, charts, and KPIs.  
- Automated connection to **Google Sheets** for data loading.

---

## ⚡ Installation

1. Clone the repository:
```bash
git clone https://github.com/MulikaDev/Sales-Analytics-Tools.git
cd Sales-Analytics-Tools
2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies:
pip install -r requirements.txt
🚀 Usage
1. Load data from Google Sheets:
from utils.gs_loader import load_data_from_gsheet

df = load_data_from_gsheet(
    sheet_url="YOUR_SHEET_URL",
    worksheet_name="Sheet1",
    service_account_file="credentials/service_account.json"
)
2. Generate reports:
from utils.excel_exporter import create_excel_report
from utils.pdf_reporter import create_dashboard_pdf

create_excel_report(df_summary, "output/sales_report.xlsx")
create_dashboard_pdf(df_summary, "output/sales_chart.png", "output/dashboard.pdf")
3. Run Streamlit (optional):
streamlit run app.py

---

## 👀 Preview

Here is a quick preview of the **Sales Analytics Dashboard**:

![Dashboard Preview](output)

*Example of generated PDF dashboard with KPI indicators, charts, and sales summary.*



🗂 Project Structure
Sales-Analytics-Tools/
│
├─ app.py
├─ main.py
├─ requirements.txt
├─ README.md
├─ utils/
│   ├─ excel_exporter.py
│   ├─ pdf_report.py
│   ├─ gs_loader.py
├─ output/          # Generated Excel and PDF files
├─ credentials/     # Secret files (not in the repo!)
└─ logs.txt

⚠️ Important Notes
Never commit secrets to the repository! .gitignore already includes keys and config files.
Use your own Google Service Account credentials for accessing Google Sheets.
📧 Contact
Author: Ihor Mulika
Email: igor.data.analytics@gmail.com
GitHub: MulikaDev
<img width="721" height="723" alt="Dash" src="https://github.com/user-attachments/assets/7447b921-1302-443b-9736-6dc9286b55e0" />
