# general imports
from datetime import datetime
from typing import List
import os
# model imports
import paddle
from paddleocr import PaddleOCR

class ocr_processor:
    def __init__(self, is_mobile: bool = True):
        """
        Initializes the OCRProcessor with PaddleOCR model for processing images.

        Args:
            is_mobile (bool): If True, uses the mobile version of the OCR model; otherwise, uses the server version. Mobile version is optimized for speed over accuracy.
        """
        self.model = PaddleOCR(
            use_doc_unwarping = True,
            doc_unwarping_model_name = 'UVDoc',
            text_detection_model_name = 'PP-OCRv5_mobile_det' if is_mobile else 'PP-OCRv5_server_det',
            text_recognition_model_name = 'PP-OCRv5_mobile_rec' if is_mobile else 'PP-OCRv5_server_rec',
            lang = 'en',
        )
    def process_image(self, img_path: str, output_directory: str, output_file_name: str = "") -> List[str] :
        
        """
        Processes images using the PaddleOCR model and returns the OCR results.

        Args:
            imag_path (str): Path to the image file or folder to be processed. Can be local or a URL.
            output_directory (str): Directory to save the JSON output files.

        Returns:
            List[str]: List of paths to the generated JSON output files.
                (Format: image_info_year_day_hour_minute_second.json) if output_file_name is not provided.
        Example:
            >>> process_images_with_paddleocr('images/receipt.jpg', 'output/') # processes one image
            >>> process_images_with_paddleocr('images/', 'output/') # processes images in 'images' directory
        """

        now = datetime.now()
        paths: List[str] = []
        result = self.model.predict(img_path)
        for item in result:            
            if output_file_name != "":
                file_name = output_file_name
            else:
                file_name: str = f'image_info_{now.year}_{now.day}_{now.hour}_{now.minute}_{now.second}.json'
            item.save_to_json(os.path.join(output_directory, file_name))
            paths.append(os.path.join(output_directory, file_name))
        return paths