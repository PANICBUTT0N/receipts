from paddleocr import PaddleOCR
import os

ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False) # text detection + text recognition

def scan_receipts(receipt):
    result = ocr.predict(f"receipts/{receipt}")
    output_folder = os.path.splitext(receipt)[0]

    print("reading receipt...")

    for res in result:
        print("outputting result...")
        res.save_to_img(f"ocr_output/{output_folder}")
        print("saved image...")
        res.save_to_json(f"ocr_output/{output_folder}")

    print(f"done, output in output/{output_folder}")

scan_receipts("receipt2.png")
