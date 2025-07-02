import json
from PIL import Image
import receipt_parser_utils1 as rpu
import pprint

class ReceiptParser:
    def __init__(self, ocr_json_path: str, image_path: str):
        with open(ocr_json_path, 'r') as f:
            self.ocr_data = json.load(f)

        # image width/height
        with Image.open(image_path) as img:
            self.width, self.height = img.size

        self.width = int(self.width/2)

        # ocr data
        self.raw_texts = self.ocr_data['rec_texts']
        self.confidences = self.ocr_data['rec_scores']
        self.bboxes = self.ocr_data['rec_polys']

        # combining data into list of dicts for each text box
        self.entries = self._combine_data()

        # information on blocks
        self.block_min_area, self.block_max_area = rpu.get_min_max_area(self.entries)

        # weights for each data point
        self.DEFAULT_WEIGHTS = {
            'top': 1,
            'area': 1,
            'confidence': 1,
            'center': 1,
            'caps': 1,
            'address': 1,
            'blacklist': 1
        }

    def _combine_data(self):
        return [
            {"text": t, "confidence": c, "bbox": b}
            for t, c, b in zip(self.raw_texts, self.confidences, self.bboxes)
        ]
    
    def store_name_scores(self) -> None:
        for block in self.entries:
            pprint.pprint(rpu.store_name_score(block, self.height, self.width, self.entries, self.DEFAULT_WEIGHTS))
            print('\n')

    def date_scores(self) -> None:
        for block in self.entries:
            pprint.pprint(rpu.date_score(block, self.DEFAULT_WEIGHTS))
            print('\n') 

    def total_price_scores(self) -> None:
        for block in self.entries:
            pprint.pprint(rpu.total_price_score(block, self.height, self.width, self.entries, self.DEFAULT_WEIGHTS))
            print('\n')
    
json_path = 'cleaning-layer/test_receipts/0.json'
img_path = 'cleaning-layer/test_receipts/ocr_output_0.jpg'
receipt_parser = ReceiptParser(json_path, img_path)

receipt_parser.total_price_scores()

print(receipt_parser.entries[0])
