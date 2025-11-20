import os
from typing import Optional
from config.settings import config

def get_file_extension(file_path: str) -> str:
    """Lấy extension của file"""
    return os.path.splitext(file_path)[1].lower()

def get_file_type(file_path: str) -> Optional[str]:
    """Xác định loại file dựa trên extension"""
    ext = get_file_extension(file_path)
    
    for file_type, extensions in config.SUPPORTED_FORMATS.items():
        if ext in extensions:
            return file_type
    
    return None

def is_supported_format(file_path: str) -> bool:
    """Kiểm tra file có được hỗ trợ không"""
    return get_file_type(file_path) is not None

def validate_file_path(file_path: str) -> bool:
    """Kiểm tra đường dẫn file hợp lệ"""
    return os.path.exists(file_path) and os.path.isfile(file_path)