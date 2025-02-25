# main.py
import os
from invoice_processing import process_invoices
from document_processing import convert_pdf_to_images, process_document_file
import threading
import subprocess
import zipfile

def run_invoice_pipeline():
    print("Running Invoice Processing Pipeline...")
    # Use the zipped CSV file for data entry/invoice processing
    invoice_zip_path = r"C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\dataset.csv.zip"
    df, model = process_invoices(invoice_zip_path)
    print("Invoice processing complete. Sample output:")
    print(df.head())

def run_document_pipeline():
    print("Running Document Processing Pipeline...")
    # Use the ZIP file containing PDFs
    zip_pdf_path = r"C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\archive (1).zip"
    output_folder = "extracted_pdfs"
    os.makedirs(output_folder, exist_ok=True)
    # Extract PDF files from the ZIP archive
    with zipfile.ZipFile(zip_pdf_path, 'r') as z:
        z.extractall(output_folder)
    # Process each PDF file
    for file in os.listdir(output_folder):
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(output_folder, file)
            # Create a folder for images generated from this PDF
            pdf_image_folder = os.path.join("pdf_images", os.path.splitext(file)[0])
            os.makedirs(pdf_image_folder, exist_ok=True)
            image_paths = convert_pdf_to_images(pdf_path, pdf_image_folder)
            for img_path in image_paths:
                result = process_document_file(img_path)
                print(f"Processed {img_path}: Extracted Entities:", result.get("entities", {}))

def run_chatbot():
    print("Starting Chatbot API...")
    subprocess.run(["python", "chatbot.py"])

if __name__ == "__main__":
    # Run each pipeline in separate threads
    invoice_thread = threading.Thread(target=run_invoice_pipeline)
    document_thread = threading.Thread(target=run_document_pipeline)
    chatbot_thread = threading.Thread(target=run_chatbot)

    invoice_thread.start()
    document_thread.start()
    # Uncomment the following line if you want to start the chatbot as well:
    chatbot_thread.start()

    invoice_thread.join()
    document_thread.join()
    # chatbot_thread.join()
