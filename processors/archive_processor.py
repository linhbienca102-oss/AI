import zipfile
import py7zr
import os
import tempfile
import shutil
from typing import List
from processors.base_processor import BaseProcessor
from config.settings import config  # THÊM IMPORT NÀY

class ArchiveProcessor(BaseProcessor):
    """Xử lý file nén (ZIP, RAR, 7Z)"""
    
    def extract_text(self) -> str:
        """Trích xuất văn bản từ archive"""
        text_parts = []
        
        try:
            ext = os.path.splitext(self.file_path)[1].lower()
            
            if ext == '.zip':
                files_content = self._extract_zip()
            elif ext == '.7z':
                files_content = self._extract_7z()
            else:
                return f"Định dạng archive không được hỗ trợ: {ext}"
            
            for filename, content in files_content:
                text_parts.append(f"--- FILE: {filename} ---")
                text_parts.append(content)
                
        except Exception as e:
            return f"Lỗi xử lý archive: {str(e)}"
        
        return "\n".join(text_parts)
    
    def _extract_zip(self) -> List[tuple]:
        """Trích xuất từ ZIP"""
        contents = []
        
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir():
                    # Kiểm tra định dạng được hỗ trợ
                    ext = os.path.splitext(file_info.filename)[1].lower()
                    supported = any(ext in formats for formats in 
                                  config.SUPPORTED_FORMATS.values())
                    
                    if supported:
                        with zip_ref.open(file_info) as file:
                            # Extract to temp file và xử lý
                            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                                temp_file.write(file.read())
                                temp_file_path = temp_file.name
                            
                            try:
                                # Sử dụng TextExtractionTool để xử lý file
                                from main import TextExtractionTool  # IMPORT TRONG HÀM
                                tool = TextExtractionTool()
                                content = tool.process_file(temp_file_path)
                                contents.append((file_info.filename, content))
                            finally:
                                if os.path.exists(temp_file_path):
                                    os.remove(temp_file_path)
        
        return contents
    
    def _extract_7z(self) -> List[tuple]:
        """Trích xuất từ 7Z"""
        contents = []
        
        with py7zr.SevenZipFile(self.file_path, 'r') as archive:
            temp_dir = tempfile.mkdtemp()
            try:
                archive.extractall(path=temp_dir)
                
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        ext = os.path.splitext(file)[1].lower()
                        
                        # Kiểm tra định dạng được hỗ trợ
                        supported = any(ext in formats for formats in 
                                      config.SUPPORTED_FORMATS.values())
                        
                        if supported:
                            try:
                                from main import TextExtractionTool  # IMPORT TRONG HÀM
                                tool = TextExtractionTool()
                                content = tool.process_file(file_path)
                                contents.append((file, content))
                            except Exception as e:
                                contents.append((file, f"Lỗi xử lý: {str(e)}"))
                
            finally:
                # Dọn dẹp thư mục tạm
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
        
        return contents

    def _is_supported_format(self, ext: str) -> bool:
        """Kiểm tra định dạng có được hỗ trợ không"""
        return any(ext in formats for formats in config.SUPPORTED_FORMATS.values())