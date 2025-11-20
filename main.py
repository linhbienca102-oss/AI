import os
import sys
from typing import Optional

# Thêm đường dẫn để import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from utils.file_utils import get_file_type, is_supported_format, validate_file_path
from utils.text_utils import chunk_text, format_chunked_output
from processors.pdf_processor import PDFProcessor
from processors.office_processor import OfficeProcessor
from processors.image_processor import ImageProcessor
from processors.audio_processor import AudioProcessor
from processors.video_processor import VideoProcessor
from processors.archive_processor import ArchiveProcessor

class TextExtractionTool:
    """Công cụ trích xuất văn bản chính"""
    
    def __init__(self):
        self.processors = {
            'pdf': PDFProcessor,
            'office': OfficeProcessor,
            'image': ImageProcessor,
            'audio': AudioProcessor,
            'video': VideoProcessor,
            'archive': ArchiveProcessor,
            'text': self._process_text_file  # Hàm xử lý trực tiếp
        }
    
    def process_file(self, file_path: str) -> str:
        """Xử lý file và trích xuất văn bản"""
        try:
            # Kiểm tra file
            if not validate_file_path(file_path):
                return f"Lỗi: File không tồn tại hoặc không hợp lệ: {file_path}"
            
            if not is_supported_format(file_path):
                return f"Lỗi: Định dạng không được hỗ trợ: {file_path}"
            
            # Xác định loại file và processor
            file_type = get_file_type(file_path)
            processor = self.processors.get(file_type)
            
            if not processor:
                return f"Lỗi: Không tìm thấy processor cho định dạng: {file_type}"
            
            # Xử lý file
            if file_type == 'text':
                result = processor(file_path)
            else:
                processor_instance = processor(file_path)
                result = processor_instance.extract_text()
            
            # Chia nhỏ nếu kết quả quá lớn
            chunks = chunk_text(result)
            formatted_result = format_chunked_output(chunks)
            
            return formatted_result
            
        except Exception as e:
            return f"Lỗi xử lý file: {str(e)}"
    
    def _process_text_file(self, file_path: str) -> str:
        """Xử lý file văn bản thuần túy"""
        try:
            # Xác định encoding
            import chardet
            
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            # Đọc file với encoding phù hợp
            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                content = file.read()
            
            return content
            
        except Exception as e:
            return f"Lỗi đọc file text: {str(e)}"

def main():
    """Hàm main để chạy từ command line"""
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Khởi tạo và chạy công cụ
    tool = TextExtractionTool()
    result = tool.process_file(file_path)
    
    # In kết quả
    print(result)

if __name__ == "__main__":
    main()