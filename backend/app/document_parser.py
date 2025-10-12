
import pytesseract
from PIL import Image
import os
from modules.logger import system_logger
from PyPDF2 import PdfReader
import re

class DocumentParser:
    def __init__(self):
        # Ensure Tesseract is installed and accessible in PATH
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # Example path, adjust as needed
        pass

    def ocr_image(self, image_path):
        """Performs OCR on an image file and returns the extracted text."""
        if not os.path.exists(image_path):
            system_logger.error(f"Image file not found: {image_path}")
            return None
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            system_logger.info(f"OCR successful for {image_path}")
            return text
        except Exception as e:
            system_logger.error(f"Error during OCR for {image_path}: {e}")
            return None

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from a PDF file."""
        if not os.path.exists(pdf_path):
            system_logger.error(f"PDF file not found: {pdf_path}")
            return None
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            system_logger.info(f"Text extraction successful for PDF: {pdf_path}")
            return text
        except Exception as e:
            system_logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return None

    def identify_remittance_slip(self, text):
        """Basic heuristic to identify if text resembles a remittance slip."""
        text_lower = text.lower()
        keywords = ["remit", "payment due", "account number", "amount due", "please pay", "return this portion"]
        
        if any(keyword in text_lower for keyword in keywords):
            system_logger.info("Text contains remittance slip keywords.")
            return True
        system_logger.info("Text does not appear to be a remittance slip (basic check).")
        return False

    def parse_document_for_entities(self, text):
        """Extracts common entities like names, addresses, dates, and amounts from general text."""
        extracted_data = {
            "names": [],
            "addresses": [],
            "dates": [],
            "amounts": []
        }

        # Basic regex for names (simple, can be improved)
        names = re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}', text)
        extracted_data["names"] = [name for name in names if len(name.split()) > 1] # Filter single words

        # Basic regex for addresses (simple, can be improved)
        addresses = re.findall(r'\d+\s[A-Za-z0-9\s,]+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\.?,?\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?', text)
        extracted_data["addresses"] = addresses

        # Basic regex for dates (YYYY-MM-DD, MM/DD/YYYY, etc.)
        dates = re.findall(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b', text)
        extracted_data["dates"] = dates

        # Basic regex for amounts ($X.XX)
        amounts = re.findall(r'\$[\d,]+\.\d{2}', text)
        extracted_data["amounts"] = amounts

        return extracted_data

    def parse_court_summons(self, text):
        """Attempts to parse a court summons for key information."""
        data = {
            "case_number": "",
            "court_name": "",
            "plaintiff": "",
            "defendant": "",
            "hearing_date": "",
            "hearing_time": ""
        }
        text_lower = text.lower()

        # Example: Case Number
        case_match = re.search(r'case\s*number:?\s*([\w-]+)', text_lower)
        if case_match: data["case_number"] = case_match.group(1).upper()

        # Example: Court Name (very basic)
        court_match = re.search(r'(?:district|superior|circuit)\s+court\s+of\s+([\w\s]+)', text_lower)
        if court_match: data["court_name"] = court_match.group(1).title()

        # Example: Plaintiff/Defendant (requires more context usually)
        plaintiff_match = re.search(r'plaintiff:?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2})', text)
        if plaintiff_match: data["plaintiff"] = plaintiff_match.group(1)

        defendant_match = re.search(r'defendant:?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2})', text)
        if defendant_match: data["defendant"] = defendant_match.group(1)

        # Example: Hearing Date/Time
        hearing_date_match = re.search(r'hearing\s+date:?\s*(\d{2}/\d{2}/\d{4})', text_lower)
        if hearing_date_match: data["hearing_date"] = hearing_date_match.group(1)

        hearing_time_match = re.search(r'hearing\s+time:?\s*(\d{1,2}:\d{2}\s*(?:am|pm))', text_lower)
        if hearing_time_match: data["hearing_time"] = hearing_time_match.group(1).upper()

        return data

# Singleton instance
document_parser = DocumentParser()
