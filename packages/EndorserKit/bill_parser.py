import re
import os
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import requests

class BillParser:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.patterns = {
            "bill_number": r"(?:Account Number|Account No|Invoice Number|Bill No|Reference No)[:\s]*([\w-]+)",
            "total_amount": r"(?:Total Amount|Amount Due|Balance Due)[:\s]*[\$€£¥]?\s*([\d.,]+)",
            "currency": r"(?:Total Amount|Amount Due|Balance Due)[:\s]*([\$€£¥])",
            "customer_name": r"(?:Customer Name|Client Name|Name)[:\s]*(.+)",
            "remittance_coupon_keywords": r"(?:Remittance Coupon|Payment Stub|Please Detach|Return with Payment|please return bottom portion with your payment)"
        }

    def parse_bill_with_api(self, file_path):
        if not self.api_key:
            return None

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Bearer {self.api_key}'}
                response = requests.post('https://api.example.com/parse_bill', files=files, headers=headers)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling bill parsing API: {e}")
            return None

    @staticmethod
    def get_bill_data_from_source(bill_source_path: str) -> dict:
        parser = BillParser(api_key=os.environ.get("BILL_PARSER_API_KEY"))
        
        # Try parsing with API first
        api_result = parser.parse_bill_with_api(bill_source_path)
        if api_result:
            return api_result

        # Fallback to local parsing
        if not bill_source_path.lower().endswith(".pdf"):
            return {"error": "Unsupported bill source format. Only PDF files are supported."}

        text = ""
        try:
            with open(bill_source_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            return {"error": f"Failed to read PDF file: {e}"}

        if not text.strip():
            try:
                text = pytesseract.image_to_string(Image.open(bill_source_path))
                if not text.strip():
                    return {"error": "Could not parse bill data from PDF (no text extracted and OCR failed)."}
            except pytesseract.TesseractNotFoundError:
                return {"error": "Tesseract is not installed or not in PATH. Cannot perform OCR."}
            except Exception as e:
                return {"error": f"OCR failed: {e}"}
        
        bill_data = parser.parse_bill(text)

        if not bill_data.get("bill_number"):
            return {"error": "Could not parse bill number from PDF."}
            
        return bill_data

    def find_remittance_coupon(self, bill_text: str) -> str:
        coupon_text = ""
        lines = bill_text.split('\n')
        found_coupon = False
        coupon_start_line = -1

        for i, line in enumerate(lines):
            if re.search(self.patterns["remittance_coupon_keywords"], line, re.IGNORECASE):
                found_coupon = True
                coupon_start_line = i
                break
        
        if found_coupon:
            for i in range(coupon_start_line, min(coupon_start_line + 10, len(lines))):
                coupon_text += lines[i] + "\n"
        
        return coupon_text.strip()

    def parse_bill(self, bill_text: str) -> dict:
        bill_data = {}
        
        match = re.search(self.patterns["bill_number"], bill_text, re.IGNORECASE)
        if match:
            bill_data["bill_number"] = match.group(1).strip()
        
        match = re.search(self.patterns["total_amount"], bill_text, re.IGNORECASE)
        if match:
            bill_data["total_amount"] = match.group(1).strip()

        match = re.search(self.patterns["currency"], bill_text)
        if match:
            currency_symbol = match.group(1)
            if currency_symbol == "$":
                bill_data["currency"] = "USD"
            else:
                bill_data["currency"] = currency_symbol
        else:
            bill_data["currency"] = "N/A"

        match = re.search(self.patterns["customer_name"], bill_text, re.IGNORECASE)
        if match:
            bill_data["customer_name"] = match.group(1).strip()
        else:
            bill_data["customer_name"] = "Valued Customer"

        remittance_coupon_text = self.find_remittance_coupon(bill_text)
        if remittance_coupon_text:
            print(f"\n--- Remittance Coupon Found ---\n{remittance_coupon_text}\n---")

        return bill_data