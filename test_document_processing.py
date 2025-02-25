# tests/test_document_processing.py
import os
import tempfile
import pytest
from document_processing import convert_pdf_to_images, process_document_file

@pytest.fixture
def sample_pdf_path():
    path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    if not os.path.exists(path):
        pytest.skip("sample.pdf not found in tests folder")
    return path

@pytest.fixture
def sample_image_path():
    path = os.path.join(os.path.dirname(__file__), "sample_image.png")
    if not os.path.exists(path):
        pytest.skip("sample_image.png not found in tests folder")
    return path

def test_convert_pdf_to_images(sample_pdf_path):
    with tempfile.TemporaryDirectory() as tmp_dir:
        image_paths = convert_pdf_to_images(sample_pdf_path, tmp_dir)
        # At least one image should be generated.
        assert len(image_paths) > 0, "Should generate at least one image"
        for img_path in image_paths:
            assert os.path.exists(img_path), f"Image file {img_path} does not exist"

def test_process_document_file(sample_image_path):
    result = process_document_file(sample_image_path)
    # The result should be a dictionary.
    assert isinstance(result, dict), "Result should be a dictionary"
    # Even if OCR returns an empty string, we expect a key (or default to empty string).
    assert isinstance(result.get("text", ""), str), "Extracted text should be a string"
