# invoice_processing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from data_ingestion import load_invoice_data

def calculate_overdue_invoices(df: pd.DataFrame) -> pd.DataFrame:
    # Flag invoices as overdue using rule-based condition
    df['is_overdue_rule'] = df['overdue']
    return df

def train_overdue_model(df: pd.DataFrame):
    features = ['processing_time']  # Additional features can be added here
    target = 'overdue'
    
    # Drop rows with missing processing_time
    df = df.dropna(subset=features)
    num_samples = df.shape[0]
    print(f"Number of samples after cleaning: {num_samples}")
    
    if num_samples == 0:
        print("No data available for training. Skipping model training.")
        return None

    X = df[features]
    y = df[target]
    
    # Split data into training and testing sets
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except ValueError as e:
        print("Error during train_test_split:", e)
        return None
    
    # Initialize and train Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = rf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("Random Forest Classification Report:\n", report)
    
    return rf

def process_invoices(filepath: str):
    df = load_invoice_data(filepath)
    print("Invoice data loaded. DataFrame shape:", df.shape)
    df = calculate_overdue_invoices(df)
    model = train_overdue_model(df)
    return df, model

if __name__ == "__main__":
    # Process invoices from the zipped CSV file
    invoice_zip_path = r"C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\dataset.csv.zip"
    df_processed, model = process_invoices(invoice_zip_path)
    print(df_processed.head())
