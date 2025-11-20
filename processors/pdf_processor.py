import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io
from typing import List
from processors.base_processor import BaseProcessor
from config.settings import config

class PDFProcessor(BaseProcessor):
    """Xử lý file PDF (text-based và scanned)"""
    
    def extract_text(self) -> str:
        """Trích xuất văn bản từ PDF"""
        try:
            # Thử trích xuất text-based trước
            text = self._extract_text_based()
            if text and len(text.strip()) > 100:  # Có đủ nội dung
                return text
            else:
                # Fallback sang OCR cho scanned PDF
                return self._extract_ocr_based()
        except Exception as e:
            return f"Lỗi xử lý PDF: {str(e)}"
    
    def _extract_text_based(self) -> str:
        """Trích xuất từ PDF text-based"""
        text_parts = []
        
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                processed_text = self.handle_special_content(page_text)
                text_parts.append(processed_text)
        
        return "\n".join(text_parts)
    
    def _extract_ocr_based(self) -> str:
        """Trích xuất từ scanned PDF bằng OCR"""
        text_parts = []
        
        try:
            # Chuyển PDF sang images
            images = convert_from_path(self.file_path, dpi=300)
            
            for i, image in enumerate(images):
                # Xử lý ảnh trước khi OCR
                processed_image = self._preprocess_image(image)
                
                # OCR với cấu hình tiếng Việt
                page_text = pytesseract.image_to_string(
                    processed_image,
                    lang=config.OCR_CONFIG['lang'],
                    config=f'--oem {config.OCR_CONFIG["oem"]} --psm {config.OCR_CONFIG["psm"]}'
                )
                
                processed_text = self.handle_special_content(page_text)
                text_parts.append(processed_text)
                
        except Exception as e:
            text_parts.append(f"(Lỗi OCR: {str(e)})")
        
        return "\n".join(text_parts)
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Tiền xử lý ảnh để cải thiện OCR"""
        # Chuyển sang grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        return image