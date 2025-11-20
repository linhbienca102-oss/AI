from typing import List
from config.settings import config

class TextChunker:
    """Tiện ích chia nhỏ văn bản"""
    
    def __init__(self, chunk_size: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
    
    def chunk_text(self, text: str) -> List[str]:
        """Chia văn bản thành chunks"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Tìm điểm cắt tốt (xuống dòng hoặc khoảng trắng)
            if end < len(text):
                # Tìm điểm cắt gần nhất
                cut_point = text.rfind('\n', start, end)
                if cut_point == -1:
                    cut_point = text.rfind(' ', start, end)
                if cut_point == -1:
                    cut_point = end
                
                end = cut_point
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end if end > start else end + 1
        
        return chunks