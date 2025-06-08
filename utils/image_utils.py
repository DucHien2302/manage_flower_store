from PIL import Image, ImageTk
import urllib.request
import io
import os

def load_image_from_url(url, size=(100, 100), master=None):
    try:
        if url.startswith('http://') or url.startswith('https://'):
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(io.BytesIO(raw_data))
        else:
            # Đường dẫn local
            if not os.path.exists(url):
                # Nếu file không tồn tại và có thể là .png thay vì .jpg
                alt_url = os.path.splitext(url)[0] + '.png'
                if os.path.exists(alt_url):
                    url = alt_url
            im = Image.open(url)
        # Sử dụng Resampling.LANCZOS thay cho ANTIALIAS (Pillow >=10)
        im = im.resize(size, Image.Resampling.LANCZOS)
        
        # Sử dụng master window nếu có
        if master:
            return ImageTk.PhotoImage(im, master=master)
        else:
            return ImageTk.PhotoImage(im)
    except Exception as e:
        print(f'Lỗi tải ảnh: {e}')
        return None
