import whisper
import speech_recognition as sr
from pydub import AudioSegment
import os
from processors.base_processor import BaseProcessor

class AudioProcessor(BaseProcessor):
    """Xử lý file audio (MP3, WAV)"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.whisper_model = whisper.load_model("base")
    
    def extract_text(self) -> str:
        """Trích xuất văn bản từ audio"""
        try:
            # Sử dụng Whisper AI (chính xác hơn)
            return self._extract_with_whisper()
        except Exception as e:
            # Fallback đến speech_recognition
            try:
                return self._extract_with_sr()
            except Exception as e2:
                return f"Lỗi xử lý audio: {str(e)} | {str(e2)}"
    
    def _extract_with_whisper(self) -> str:
        """Sử dụng Whisper AI for transcription"""
        result = self.whisper_model.transcribe(self.file_path)
        return result["text"]
    
    def _extract_with_sr(self) -> str:
        """Sử dụng speech_recognition như fallback"""
        # Chuyển đổi sang WAV nếu cần
        if not self.file_path.lower().endswith('.wav'):
            audio = AudioSegment.from_file(self.file_path)
            wav_path = "temp_audio.wav"
            audio.export(wav_path, format="wav")
        else:
            wav_path = self.file_path
        
        # Nhận diện speech
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='vi-VN')
        
        # Dọn dẹp file tạm
        if wav_path != self.file_path and os.path.exists(wav_path):
            os.remove(wav_path)
        
        return text