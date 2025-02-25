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


You can add a section like the following to your README file:

---

## Configuration Instructions

The code currently uses absolute paths to access dataset files (for example, in `main.py` and other modules). To ensure the project runs correctly on your system, please follow these instructions:

1. Using Relative Paths (Recommended):  
   - Create a folder named `datasets` in the root directory of the repository.
   - Place all required dataset files (e.g., `dataset.csv.zip`, `archive (1).zip`, etc.) into this `datasets` folder.
   - Update the file paths in your code from absolute paths (e.g., `C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\dataset.csv.zip`) to relative paths (e.g., `./datasets/dataset.csv.zip`).

2. If You Prefer Absolute Paths:  
   - Locate each instance in the code where a dataset path is defined.
   - Replace the existing path with the full path to the dataset on your local machine.
   - For example, update:
     ```python
     invoice_zip_path = r"C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\dataset.csv.zip"
     ```
     to:
     ```python
     invoice_zip_path = r"Your\Local\Path\to\datasets\dataset.csv.zip"
     ```
   - Ensure that the paths you enter correctly point to the location of the dataset files on your computer.

By following these instructions, you can ensure that the code locates the necessary datasets regardless of whether you're using relative or absolute paths.

---
