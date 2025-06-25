from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False) # text detection + text recognition

result = ocr.predict("receipt.png")

for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")