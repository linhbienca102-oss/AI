import unittest
import os
import tempfile
from main import TextExtractionTool

class TestTextExtraction(unittest.TestCase):
    
    def setUp(self):
        self.tool = TextExtractionTool()
        self.test_dir = tempfile.mkdtemp()
    
    def test_text_file(self):
        # Tạo file test
        test_content = "Xin chào thế giới!\nĐây là văn bản tiếng Việt."
        test_file = os.path.join(self.test_dir, "test.txt")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = self.tool.process_file(test_file)
        self.assertIn("Xin chào thế giới", result)
    
    def test_empty_page_handling(self):
        # Test xử lý trang trống
        from processors.base_processor import BaseProcessor
        
        processor = BaseProcessor(__file__)  # Sử dụng file hiện tại cho test
        result = processor.handle_special_content("")
        self.assertEqual(result, "(Trang trống)")
    
    def tearDown(self):
        # Dọn dẹp
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()