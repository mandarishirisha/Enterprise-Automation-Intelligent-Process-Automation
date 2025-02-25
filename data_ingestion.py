# data_ingestion.py
import pandas as pd
import zipfile

def load_invoice_data(filepath: str) -> pd.DataFrame:
    # Load the CSV from a zip file
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if not csv_files:
                raise ValueError("No CSV file found in zip")
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f)
    else:
        df = pd.read_csv(filepath)
    
    # Updated date column names based on your CSV output
    date_cols = ['clear_date', 'posting_date', 'document_date', 'document_create_date', 'due_in_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calculate processing time if the required columns exist
    if 'clear_date' in df.columns and 'posting_date' in df.columns:
        df['processing_time'] = (df['clear_date'] - df['posting_date']).dt.days
    else:
        df['processing_time'] = None
    
    # Create binary target: overdue if clear_date > due_in_date
    if 'clear_date' in df.columns and 'due_in_date' in df.columns:
        df['overdue'] = (df['clear_date'] > df['due_in_date']).astype(int)
    else:
        df['overdue'] = 0
    
    return df
