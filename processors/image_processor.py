import pytesseract
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from processors.base_processor import BaseProcessor
from config.settings import config

class ImageProcessor(BaseProcessor):
    """Xử lý file ảnh (PNG, JPG, TIFF)"""
    
    def extract_text(self) -> str:
        """Trích xuất văn bản từ ảnh bằng OCR"""
        try:
            # Mở ảnh
            image = Image.open(self.file_path)
            
            # Tiền xử lý ảnh
            processed_image = self._preprocess_image(image)
            
            # OCR
            text = pytesseract.image_to_string(
                processed_image,
                lang=config.OCR_CONFIG['lang'],
                config=f'--oem {config.OCR_CONFIG["oem"]} --psm {config.OCR_CONFIG["psm"]}'
            )
            
            return self.handle_special_content(text)
            
        except Exception as e:
            return f"Lỗi xử lý ảnh: {str(e)}"
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Tiền xử lý ảnh để cải thiện OCR accuracy"""
        # Chuyển sang OpenCV format
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()  # RGB to BGR
        
        # Chuyển sang grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng Gaussian blur để giảm noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Thresholding
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Chuyển lại sang PIL Image
        result_image = Image.fromarray(thresh)
        
        return result_image