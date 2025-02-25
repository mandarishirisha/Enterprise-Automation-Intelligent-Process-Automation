# document_processing.py
import os
import zipfile
import pytesseract
from PIL import Image, ImageFilter
import spacy
from pdf2image import convert_from_path
import subprocess

# Configure Tesseract OCR command path (update this if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load spaCy model (make sure to run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess the image: convert to grayscale, apply a median filter, and thresholding.
    """
    gray = image.convert("L")
    filtered = gray.filter(ImageFilter.MedianFilter())
    threshold = 150  # Adjust as needed
    bw = filtered.point(lambda x: 0 if x < threshold else 255, '1')
    return bw

def convert_pdf_to_images(pdf_path: str, output_folder: str) -> list:
    """
    Convert a PDF into images (one per page). First, try pdf2image (Poppler). 
    If that fails, fallback to PyMuPDF.
    Returns a list of image file paths.
    """
    poppler_path = r"C:\Users\manda\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"  # Update as needed

    # Attempt conversion using pdf2image with increased DPI for clarity
    try:
        images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        print(f"pdf2image conversion successful for {pdf_path}. Number of pages: {len(images)}")
        image_paths = []
        for idx, img in enumerate(images):
            img_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{idx}.png"
            img_path = os.path.join(output_folder, img_filename)
            img.save(img_path, "PNG")
            image_paths.append(img_path)
        return image_paths
    except Exception as e:
        print(f"pdf2image conversion failed for {pdf_path} with error: {e}")

    # Fallback: Try using PyMuPDF
    try:
        import fitz  # PyMuPDF
    except ImportError as ie:
        print(f"PyMuPDF import failed: {ie}. Install it with 'pip install --upgrade PyMuPDF'.")
        return []
    
    try:
        print(f"Attempting conversion with PyMuPDF for {pdf_path}...")
        os.makedirs(output_folder, exist_ok=True)
        doc = fitz.open(pdf_path)
        image_paths = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap()
            img_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_num}.png"
            img_path = os.path.join(output_folder, img_filename)
            pix.save(img_path)
            image_paths.append(img_path)
        print(f"PyMuPDF conversion successful for {pdf_path}. Number of pages: {len(image_paths)}")
        return image_paths
    except Exception as e2:
        print(f"PyMuPDF conversion also failed for {pdf_path} with error: {e2}")
        return []

def perform_ocr(image_path: str, timeout: int = 60) -> str:
    """
    Extract text from an image using Tesseract OCR with a timeout.
    Preprocess the image first.
    """
    try:
        img = Image.open(image_path)
        preprocessed_img = preprocess_image(img)
        custom_config = r'--psm 6'
        text = pytesseract.image_to_string(preprocessed_img, config=custom_config, timeout=timeout)
        return text
    except subprocess.TimeoutExpired as te:
        print(f"OCR timeout for {image_path}: {te}")
        return ""
    except Exception as e:
        print(f"OCR error for {image_path}: {e}")
        return ""

def extract_entities(text: str) -> dict:
    """
    Use spaCy to extract named entities from the text.
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)
    return entities

def process_document_file(image_path: str):
    """
    Process an image file: perform OCR and extract entities.
    """
    try:
        text = perform_ocr(image_path)
        if text:
            entities = extract_entities(text)
            return {"text": text, "entities": entities}
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return {}

def process_documents_from_zip(zip_path: str, extract_folder: str, images_folder: str):
    """
    Extract PDFs from the ZIP archive, convert them to images, and process each image.
    """
    os.makedirs(extract_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            all_files = z.namelist()
            print("Files in ZIP archive:", all_files)

            pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
            if not pdf_files:
                print("No PDF files found in the ZIP archive.")
                return

            for pdf_file in pdf_files:
                try:
                    z.extract(pdf_file, path=extract_folder)
                    pdf_path = os.path.join(extract_folder, pdf_file)
                    print(f"Processing PDF: {pdf_path}")

                    pdf_images_folder = os.path.join(images_folder, os.path.splitext(os.path.basename(pdf_file))[0])
                    os.makedirs(pdf_images_folder, exist_ok=True)

                    image_paths = convert_pdf_to_images(pdf_path, pdf_images_folder)
                    for img_path in image_paths:
                        try:
                            result = process_document_file(img_path)
                            print(f"Processed {img_path}: Extracted Entities:", result.get("entities", {}))
                        except Exception as img_e:
                            print(f"Error processing image {img_path}: {img_e}")
                except Exception as pdf_e:
                    print(f"Error processing PDF file {pdf_file}: {pdf_e}")
    except Exception as zip_e:
        print(f"Error opening ZIP archive {zip_path}: {zip_e}")

if __name__ == "__main__":
    # Update these paths as needed:
    zip_path = r"C:\Users\manda\OneDrive\Desktop\Enterprise_Automation\datasets\archive (1).zip"
    extract_folder = "extracted_pdfs"  # Folder where PDFs will be extracted
    images_folder = "pdf_images"       # Folder where generated images will be saved

    process_documents_from_zip(zip_path, extract_folder, images_folder)
