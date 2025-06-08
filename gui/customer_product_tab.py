import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, get_cart_id
from utils.image_utils import load_image_from_url
import datetime

def format_currency_vnd(amount):
    try:
        return f"{int(amount):,}".replace(",", ".") + " VNĐ"
    except:
        return str(amount)

def format_freeship(value):
    return "Miễn phí" if value == 1 else "Có phí"

def format_date_vn(date_str):
    try:
        d = datetime.datetime.strptime(str(date_str), "%Y-%m-%d")
        return d.strftime("%d/%m/%Y")
    except Exception:
        try:
            d = datetime.datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S")
            return d.strftime("%d/%m/%Y")
        except Exception:
            return str(date_str)

class CustomerProductTab:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(search_frame, text='Tìm kiếm:', font=('Segoe UI', 11)).pack(side='left')
        self.search_entry = ttk.Entry(search_frame, font=('Segoe UI', 11), width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_btn = ttk.Button(search_frame, text='Tìm', style='Accent.TButton', command=self.search_products)
        self.search_btn.pack(side='left', padx=5)
        self.reload_btn = ttk.Button(search_frame, text='Tải lại', command=self.load_products)
        self.reload_btn.pack(side='left', padx=5)

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Tên', 'Giá', 'Giá giảm', 'Số lượng', 'Miễn phí ship'), show='headings', height=14, style='Custom.Treeview')
        for col in ('ID', 'Tên', 'Giá', 'Giá giảm', 'Số lượng', 'Miễn phí ship'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.add_cart_btn = ttk.Button(btn_frame, text='Thêm vào giỏ', style='Accent.TButton', command=self.add_to_cart)
        self.add_cart_btn.pack(side='left', padx=5)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT id, Name, Price, DiscountedPrice, StockQuantity, IsFreeship, ImageURL, FlowerTypeID FROM Products''')
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_currency_vnd(row[2])
                row[3] = format_currency_vnd(row[3])
                row[5] = format_freeship(row[5])
                self.tree.insert('', 'end', values=row[:6])
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải sản phẩm: {e}')

    def get_image_path(self, image_url, flower_type_id):
        # Map FlowerTypeID sang tên thư mục
        type_map = {1: 'daisy', 2: 'dandelion', 3: 'rose', 4: 'sunflower', 5: 'tulip'}
        folder = type_map.get(flower_type_id, 'rose')
        return f'flowers_shop/{folder}/{image_url}.jpg'

    def search_products(self):
        keyword = self.search_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = '''SELECT id, Name, Price, DiscountedPrice, StockQuantity, IsFreeship, ImageURL, FlowerTypeID FROM Products WHERE Name LIKE %s'''
            like_kw = f'%{keyword}%'
            cursor.execute(query, (like_kw,))
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_currency_vnd(row[2])
                row[3] = format_currency_vnd(row[3])
                row[5] = format_freeship(row[5])
                self.tree.insert('', 'end', values=row[:6])
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tìm kiếm: {e}')

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để thêm vào giỏ!')
            return
        item = self.tree.item(selected[0])
        prod_id = item['values'][0]
        def save():
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    messagebox.showerror('Lỗi', 'Số lượng phải lớn hơn 0!')
                    return
                cart_id = get_cart_id(self.user_id)
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO Carts (CartId, ProductId, Quantity, IsChecked) VALUES (%s, %s, %s, 0)
                                  ON DUPLICATE KEY UPDATE Quantity = Quantity + %s''', (cart_id, prod_id, qty, qty))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Đã thêm vào giỏ hàng!')
                top.destroy()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi thêm vào giỏ: {e}')
        top = tk.Toplevel(self.master)
        top.title('Chọn số lượng')
        tk.Label(top, text='Số lượng:').grid(row=0, column=0, padx=10, pady=5)
        qty_entry = tk.Entry(top)
        qty_entry.insert(0, '1')
        qty_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(top, text='Xác nhận', command=save).grid(row=1, column=0, columnspan=2, pady=10)
