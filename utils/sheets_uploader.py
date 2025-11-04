def upload_summary_to_gsheet(gc, sheet_name, tab_name, summary):
    try:
        try:
            ws = gc.open(sheet_name).worksheet(tab_name)
            ws.clear()
        except Exception:
            ws = gc.open(sheet_name).add_worksheet(title=tab_name, rows=100, cols=10)
        ws.update([summary.columns.values.tolist()] + summary.values.tolist())
        return True
    except Exception as e:
        print(f"⚠️ Error uploading to Google Sheets: {e}")
        return False
