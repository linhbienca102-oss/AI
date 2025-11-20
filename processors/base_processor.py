from abc import ABC, abstractmethod
import os
from typing import Optional
from config.settings import config

class BaseProcessor(ABC):
    """Lớp cơ sở cho tất cả processor"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.validate_file()
    
    def validate_file(self):
        """Kiểm tra file hợp lệ"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File không tồn tại: {self.file_path}")
        
        if self.file_size == 0:
            raise ValueError("File trống")
        
        if self.file_size > config.MAX_FILE_SIZE:
            raise ValueError(f"File vượt quá kích thước cho phép: {self.file_size}")
    
    @abstractmethod
    def extract_text(self) -> str:
        """Trích xuất văn bản - phương thức trừu tượng"""
        pass
    
    def handle_special_content(self, content: str) -> str:
        """Xử lý nội dung đặc biệt"""
        if not content or content.strip() == "":
            return config.EMPTY_PAGE_MESSAGE
        
        # Kiểm tra nội dung không thể đọc
        if self.is_unreadable(content):
            return config.UNREADABLE_PAGE_MESSAGE
        
        return content
    
    def is_unreadable(self, content: str) -> bool:
        """Kiểm tra nội dung không thể đọc"""
        # Nếu toàn ký tự đặc biệt hoặc quá ngắn
        import string
        printable_chars = set(string.printable)
        content_chars = set(content)
        
        if len(content_chars - printable_chars) / len(content_chars) > 0.8:
            return True
        
        return False