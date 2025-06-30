import json
from PIL import Image
import receipt_parser_utils as rpu
import pprint

class ReceiptParser:
    def __init__(self, ocr_json_path: str, image_path: str):
        with open(ocr_json_path, "r") as f:
            self.ocr_data = json.load(f)

        # image width/height
        with Image.open(image_path) as img:
            self.width, self.height = img.size

        self.width = int(self.width/2)

        # ocr data
        self.raw_texts = self.ocr_data["rec_texts"]
        self.confidences = self.ocr_data["rec_scores"]
        self.bboxes = self.ocr_data["rec_polys"]

        # combining data into list of dicts for each text box
        self.entries = self._combine_data()

        # information on blocks
        self.block_min_area, self.block_max_area = rpu.get_min_max_area(self.entries)

        # weights for each data point
        self.STORE_NAME_WEIGHTS = {
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
            pprint.pprint(rpu.block_store_score(block, self.height, self.width, self.block_min_area, self.block_max_area, self.STORE_NAME_WEIGHTS))
            print("\n")
    
    def extract_store_name(self) -> str:
        scores = [rpu.block_store_score(block, self.height, self.width, self.block_min_area, self.block_max_area, self.STORE_NAME_WEIGHTS)['SCORE'] for block in self.entries]
        max_index = scores.index(max(scores))

        return self.entries[max_index]['text']
    
    
json_path = "cleaning-layer/test_receipts/receipt1_res.json"
img_path = "cleaning-layer/test_receipts/receipt1_ocr_res_img.png"
receipt_parser = ReceiptParser(json_path, img_path)

receipt_parser.store_name_scores()
print(receipt_parser.extract_store_name())

print(receipt_parser.entries[0])
