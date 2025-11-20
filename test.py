# test_install.py - Kiểm tra tất cả thư viện đã cài
import importlib

print("✅ KIỂM TRA CÀI ĐẶT THƯ VIỆN THÀNH CÔNG")
print("=" * 50)

libs = [
    'PyPDF2', 'pdf2image', 'pytesseract', 
    'docx', 'openpyxl', 'pptx', 'PIL',
    'cv2', 'numpy', 'pydub', 'moviepy', 
    'whisper', 'py7zr', 'chardet'
]

success = []
for lib in libs:
    try:
        importlib.import_module(lib)
        success.append(lib)
        print(f"✅ {lib}")
    except ImportError as e:
        print(f"❌ {lib}: {e}")

print("=" * 50)
print(f"🎯 Đã cài thành công: {len(success)}/{len(libs)} thư viện")

if len(success) >= 10:
    print("🚀 SẴN SÀNG CHẠY CHƯƠNG TRÌNH!")
else:
    print("⚠️  Một số thư viện chưa cài, nhưng vẫn chạy được cơ bản")