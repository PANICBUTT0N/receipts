import json
from PIL import Image
import receipt_parser_utils

class ReceiptParser:
    def __init__(self, ocr_json_path: str, image_path):
        with open(ocr_json_path, "r") as f:
            self.ocr_data = json.load(f)

        # image width/height
        with Image.open(image_path) as img:
            self.width, self.height = img.size

        # ocr data
        self.raw_texts = self.ocr_data["rec_texts"]
        self.confidences = self.ocr_data["rec_scores"]
        self.bboxes = self.ocr_data["rec_polys"]

        # combining data into list of dicts for each text box
        self.entries = self._combine_data()

    def _combine_data(self):
        return [
            {"text": t, "confidence": c, "bbox": b}
            for t, c, b in zip(self.raw_texts, self.confidences, self.bboxes)
        ]
    
    def extract_store_name(self):
        pass

    def __str__(self):
        return str(self.entries[:5])
    
path = "ocr_output/receipt1/receipt1_res.json"
receiptParser = ReceiptParser(path)

print(receiptParser)