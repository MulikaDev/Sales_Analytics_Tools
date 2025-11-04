import streamlit as st
from main import setup_logger, load_data, prepare_data, export_excel, create_pdf, upload_summary_to_gsheet
from config import *

st.title("📊 Sales Analytics Dashboard")

if st.button("Load & Generate All"):
    st.info("Processing data...")
    try:
        # Main process
        import main  # Executes main.py workflow
        st.success("✅ Reports generated successfully!")
    except Exception as e:
        st.error(f"❌ Error: {e}")
