# Enterprise-Automation-Intelligent-Process-Automation

Overview This repository provides a solution for automating repetitive business processes including invoice processing, document processing, and customer service interactions. The code is written in Python using standard open-source libraries and leverages AI techniques for improved efficiency.


Environment Setup
1.Clone the Repository:

git clone https://github.com/yourusername/enterprise-automation.git
cd enterprise-automation

2.Create a Virtual Environment (Optional but Recommended):

python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate

3.Install Dependencies:

pip install -r requirements.txt

4.Configure External Tools:

Tesseract OCR:
Download and install Tesseract from Tesseract OCR. Update the Tesseract path in document_processing.py if needed.

Poppler:
Download and install Poppler (required by pdf2image). Update the poppler_path in document_processing.py with the correct location on your system.

How to Run the Code
Invoice Processing Pipeline:
Run the main script to process invoices:

python main.py

This pipeline loads invoice data from a zipped CSV file, processes the data, trains a machine learning model to predict overdue invoices, and prints sample outputs to the console.


Document Processing Pipeline:

The document processing module automatically extracts PDFs from a ZIP archive, converts them to images, performs OCR, and extracts entities using NLP. Check the console output for results.

Chatbot Service:
To start the chatbot API:
python chatbot.py
Test the API using a tool like curl:
curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is your return policy?"}'


Additional Information

The repository is structured modularly to support scalability and ease of maintenance.
All necessary instructions for environment setup and code execution are provided in this document.
