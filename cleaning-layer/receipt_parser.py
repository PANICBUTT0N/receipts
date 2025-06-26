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

        # weights for each data point
        self.STORE_NAME_WEIGHTS = {
            'top': 10,
            'area': 1000,
            'confidence': 10,
            'center': 10,
            'caps': 10,
            'address': 10,
            'blacklist': 10
        }

    def _combine_data(self):
        return [
            {"text": t, "confidence": c, "bbox": b}
            for t, c, b in zip(self.raw_texts, self.confidences, self.bboxes)
        ]
    
    def store_name_scores(self) -> list[str]:
        scores = [f"{block['text']} {rpu.debug_block_score(block, self.height, self.width, self.STORE_NAME_WEIGHTS)}" for block in self.entries]
        return scores
    
    def store_name_score(self, index: int) -> dict:
        return rpu.debug_block_score(self.entries[index], self.height, self.width, self.STORE_NAME_WEIGHTS)
    
    def extract_store_name(self) -> str:
        scores = [rpu.score_text_block(block, self.height, self.width, self.STORE_NAME_WEIGHTS) for block in self.entries]
        max_index = scores.index(max(scores))

        return self.entries[max_index]['text']

    def __str__(self):
        return "ReceiptParser"
    
json_path = "cleaning-layer/test_receipts/receipt1_res.json"
img_path = "cleaning-layer/test_receipts/receipt1_ocr_res_img.png"
receipt_parser = ReceiptParser(json_path, img_path)


for i in range(len(receipt_parser.entries)):
    pprint.pprint(receipt_parser.store_name_score(i))
    print('\n')

print(f"STORE NAME: {receipt_parser.extract_store_name()}")
