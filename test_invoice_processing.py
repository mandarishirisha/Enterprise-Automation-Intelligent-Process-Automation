# tests/test_invoice_processing.py
import os
import tempfile
import zipfile
from invoice_processing import process_invoices

def test_process_invoices_zip():
    # Create a temporary CSV file with sample invoice data.
    csv_content = """business_code,cust_number,clear_date,posting_date,due_in_date
U001,0200769623,2020-02-11,2020-02-01,2020-02-10
U001,0200980828,2019-08-08,2019-08-01,2019-08-05
"""
    # Create a temporary ZIP file containing the CSV.
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
        zip_filename = tmp_zip.name
    with zipfile.ZipFile(zip_filename, 'w') as zf:
        zf.writestr("test_invoices.csv", csv_content)
    
    df, model = process_invoices(zip_filename)
    
    # Check that the DataFrame is not empty.
    assert not df.empty, "DataFrame should not be empty"
    # Check that the 'processing_time' column exists.
    assert "processing_time" in df.columns, "DataFrame should contain 'processing_time' column"
    
    os.remove(zip_filename)
