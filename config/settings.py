import os
import sys
from typing import Dict, List

class Config:
    """Cấu hình hệ thống"""
    
    # Giới hạn kích thước file (1GB)
    MAX_FILE_SIZE = 1024 * 1024 * 1024
    
    # Định dạng được hỗ trợ
    SUPPORTED_FORMATS = {
        'text': ['.txt', '.rtf', '.html', '.htm', '.epub'],
        'pdf': ['.pdf'],
        'office': ['.doc', '.docx', '.xlsx', '.pptx'],
        'image': ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'],
        'audio': ['.mp3', '.wav', '.m4a', '.flac'],
        'video': ['.mp4', '.avi', '.mov', '.mkv'],
        'archive': ['.zip', '.rar', '.7z']
    }
    
    # Cài đặt OCR
    OCR_CONFIG = {
        'lang': 'vie+eng',
        'oem': 3,
        'psm': 6
    }
    
    # Kích thước chunk (1MB)
    CHUNK_SIZE = 1024 * 1024
    
    # Thông báo đặc biệt
    EMPTY_PAGE_MESSAGE = "(Trang trống)"
    UNREADABLE_PAGE_MESSAGE = "(Không thể trích xuất nội dung trang này)"

config = Config()