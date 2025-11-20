from config.settings import config

def preserve_text_formatting(text: str) -> str:
    """Bảo toàn định dạng văn bản"""
    # Không thay đổi gì - giữ nguyên hoàn toàn
    return text

def chunk_text(text: str, chunk_size: int = None) -> list:
    """Chia văn bản thành các chunk"""
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Chia theo dòng để tránh cắt ngữ cảnh
    lines = text.splitlines(keepends=True)
    
    for line in lines:
        if len(current_chunk) + len(line) <= chunk_size:
            current_chunk += line
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def format_chunked_output(chunks: list) -> str:
    """Định dạng output với các phần được đánh số"""
    if not chunks:
        return ""
    
    if len(chunks) == 1:
        return chunks[0]
    
    formatted_chunks = []
    for i, chunk in enumerate(chunks, 1):
        formatted_chunks.append(f"--- PHẦN {i} ---")
        formatted_chunks.append(chunk)
    
    return "\n".join(formatted_chunks)