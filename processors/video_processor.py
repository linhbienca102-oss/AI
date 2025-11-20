import os
import tempfile
from processors.base_processor import BaseProcessor

class VideoProcessor(BaseProcessor):
    """Xử lý file video (MP4)"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.whisper_model = None
        self.moviepy_available = False
        
        # Kiểm tra và load whisper
        try:
            import whisper
            self.whisper_model = whisper.load_model("base")
        except ImportError:
            print("⚠️  Whisper chưa được cài đặt")
        
        # Kiểm tra moviepy
        try:
            from moviepy import VideoFileClip
            self.moviepy_available = True
        except ImportError:
            print("⚠️  MoviePy chưa được cài đặt - không thể trích xuất audio từ video")
    
    def extract_text(self) -> str:
        """Trích xuất văn bản từ video"""
        text_parts = []
        
        try:
            # Thử trích xuất phụ đề trước
            subtitle_text = self._extract_subtitles()
            if subtitle_text:
                text_parts.append("--- PHỤ ĐỀ ---")
                text_parts.append(subtitle_text)
            
            # Trích xuất audio và chuyển thành văn bản
            audio_text = self._extract_audio_text()
            if audio_text:
                text_parts.append("--- NỘI DUNG AUDIO ---")
                text_parts.append(audio_text)
            
        except Exception as e:
            return f"Lỗi xử lý video: {str(e)}"
        
        if text_parts:
            return "\n".join(text_parts)
        else:
            return "(Không thể trích xuất nội dung từ video - cần cài đặt MoviePy và Whisper)"
    
    def _extract_subtitles(self) -> str:
        """Trích xuất phụ đề từ video"""
        # TODO: Triển khai trích xuất phụ đề từ stream
        # Hiện tại trả về chuỗi rỗng
        return ""
    
    def _extract_audio_text(self) -> str:
        """Trích xuất audio và chuyển thành văn bản"""
        if not self.moviepy_available:
            return "(Cần cài đặt MoviePy để trích xuất audio từ video)"
        
        if not self.whisper_model:
            return "(Cần cài đặt Whisper để chuyển audio thành văn bản)"
        
        # Trích xuất audio từ video
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            try:
                from moviepy import VideoFileClip
                
                video = VideoFileClip(self.file_path)
                video.audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
                video.close()
                
                # Transcribe audio
                result = self.whisper_model.transcribe(temp_audio.name)
                return result["text"]
                
            except Exception as e:
                return f"(Lỗi trích xuất audio: {str(e)})"
            finally:
                if os.path.exists(temp_audio.name):
                    os.remove(temp_audio.name)