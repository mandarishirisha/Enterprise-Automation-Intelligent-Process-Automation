# chatbot.py
from flask import Flask, request, jsonify
import pandas as pd
import zipfile
import os
import json

app = Flask(__name__)

def load_faq_from_excel(zip_filepath: str, excel_filename: str = None) -> dict:
    """
    Loads an Excel file from the provided ZIP archive and creates a dictionary mapping
    customer queries (from the 'Text' column) to agent responses (from the 'Customer Comment' column).
    """
    with zipfile.ZipFile(zip_filepath, 'r') as z:
        # List all Excel files in the ZIP
        excel_files = [f for f in z.namelist() if f.endswith('.xlsx')]
        if not excel_files:
            print("No Excel file found in zip")
            return {}
        # Use the first Excel file found (or a specific one if provided)
        excel_file = excel_files[0] if excel_filename is None else excel_filename
        with z.open(excel_file) as f:
            df = pd.read_excel(f)
    
    # Debug: print out the column names to verify
    print("Excel columns found:", df.columns.tolist())
    
    faq_dict = {}
    # Use 'Text' as the customer query and 'Customer Comment' as the answer.
    for idx, row in df.iterrows():
        question = str(row.get('Text', '')).strip().lower()
        answer = str(row.get('Customer Comment', '')).strip()
        if question and answer:
            faq_dict[question] = answer
    return faq_dict

# Default FAQ responses in case the Excel file doesn't provide any
FAQ_RESPONSES = {
    "what is your return policy": "Returns are accepted within 30 days of purchase.",
    "how can i track my order": "You can track your order using the tracking link sent to your email."
}

# Update FAQ_RESPONSES using the data from the Excel file in the provided ZIP
faq_zip_path = r"C:\\Users\\manda\\OneDrive\\Desktop\\Enterprise_Automation\\datasets\\Chat_Team_CaseStudy FINAL.xlsx.zip"
faq_from_excel = load_faq_from_excel(faq_zip_path)
if faq_from_excel:
    FAQ_RESPONSES.update(faq_from_excel)

def classify_intent(message: str) -> str:
    """
    A simple rule-based intent classifier that matches the user message to the FAQ dictionary.
    """
    for question, answer in FAQ_RESPONSES.items():
        if question in message.lower():
            return answer
    return "Sorry, I didn't understand that. Could you please rephrase?"

@app.route("/")
def home():
    """
    Home route that provides a welcome message.
    """
    return "Welcome to the Customer Service Chatbot API. Use the /chat endpoint for interactions."

@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat route that processes POST requests containing a JSON payload with a 'message' field.
    Returns a JSON response with the appropriate answer.
    """
    data = request.get_json()
    user_message = data.get("message", "")
    response = classify_intent(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
