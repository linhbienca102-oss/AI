# processors/__init__.py

from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .office_processor import OfficeProcessor
from .image_processor import ImageProcessor
from .audio_processor import AudioProcessor
from .video_processor import VideoProcessor
from .archive_processor import ArchiveProcessor

__all__ = [
    'BaseProcessor',
    'PDFProcessor', 
    'OfficeProcessor',
    'ImageProcessor',
    'AudioProcessor',
    'VideoProcessor',
    'ArchiveProcessor'
]