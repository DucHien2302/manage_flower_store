import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
from models.product import Product
from utils.image_utils import load_image_from_url
from tkinter import filedialog
import os
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

class ProductTab:
    def __init__(self, master):
        self.master = master
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

        columns = ('ID', 'Tên', 'Giá', 'Giá giảm', 'Số lượng', 'Danh mục', 'Loại hoa', 'Miễn phí ship')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=14, style='Custom.Treeview')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.add_btn = ttk.Button(btn_frame, text='Thêm', style='Accent.TButton', command=self.add_product)
        self.add_btn.pack(side='left', padx=5)
        self.edit_btn = ttk.Button(btn_frame, text='Sửa', command=self.edit_product)
        self.edit_btn.pack(side='left', padx=5)
        self.delete_btn = ttk.Button(btn_frame, text='Xóa', command=self.delete_product)
        self.delete_btn.pack(side='left', padx=5)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT p.id, p.Name, p.Price, p.DiscountedPrice, p.StockQuantity, c.Name, f.Name, p.IsFreeship \
                              FROM Products p \
                              LEFT JOIN Categories c ON p.CategoryID = c.id \
                              LEFT JOIN FlowerTypes f ON p.FlowerTypeID = f.id''')
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_currency_vnd(row[2])
                row[3] = format_currency_vnd(row[3])
                row[7] = format_freeship(row[7])
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải sản phẩm: {e}')

    def search_products(self):
        keyword = self.search_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = '''SELECT p.id, p.Name, p.Price, p.DiscountedPrice, p.StockQuantity, c.Name, f.Name, p.IsFreeship \
                       FROM Products p \
                       LEFT JOIN Categories c ON p.CategoryID = c.id \
                       LEFT JOIN FlowerTypes f ON p.FlowerTypeID = f.id \
                       WHERE p.Name LIKE %s OR c.Name LIKE %s OR f.Name LIKE %s'''
            like_kw = f'%{keyword}%'
            cursor.execute(query, (like_kw, like_kw, like_kw))
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_currency_vnd(row[2])
                row[3] = format_currency_vnd(row[3])
                row[7] = format_freeship(row[7])
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tìm kiếm: {e}')

    def add_product(self):
        def choose_image():
            file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg;*.jpeg;*.png')])
            if file_path:
                image_url_entry.delete(0, tk.END)
                image_url_entry.insert(0, os.path.basename(file_path))
                image_url_entry.file_path = file_path
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            price = price_entry.get().strip()
            discounted_price = discounted_price_entry.get().strip()
            stock = stock_entry.get().strip()
            image_name = image_url_entry.get().strip()
            is_freeship = 1 if is_freeship_var.get() else 0
            cat_idx = category_cb.current()
            type_idx = flowertype_cb.current()
            if not name or not price or not stock or cat_idx == -1 or type_idx == -1 or not image_name:
                messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ thông tin bắt buộc!')
                return
            try:
                price = int(price)
                discounted_price = int(discounted_price) if discounted_price else 0
                stock = int(stock)
            except:
                messagebox.showerror('Lỗi', 'Giá, giá giảm, số lượng phải là số!')
                return
            try:
                cat_id = categories[cat_idx][0]
                type_id = flowertypes[type_idx][0]
                # Lưu file ảnh vào đúng thư mục
                if hasattr(image_url_entry, 'file_path') and image_url_entry.file_path:
                    folder_map = {1: 'daisy', 2: 'dandelion', 3: 'rose', 4: 'sunflower', 5: 'tulip'}
                    folder = folder_map.get(type_id, 'rose')
                    dest_dir = os.path.join('flowers_shop', folder)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, image_name)
                    import shutil
                    shutil.copy(image_url_entry.file_path, dest_path)
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO Products (Name, Description, Price, DiscountedPrice, StockQuantity, ImageURL, IsFreeship, CategoryID, FlowerTypeID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (name, desc, price, discounted_price, stock, os.path.splitext(image_name)[0], is_freeship, cat_id, type_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Thêm sản phẩm thành công!')
                top.destroy()
                self.load_products()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi thêm sản phẩm: {e}')
        # Lấy danh mục và loại hoa
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, Name FROM Categories')
            global categories
            categories = cursor.fetchall()
            cursor.execute('SELECT id, Name FROM FlowerTypes')
            global flowertypes
            flowertypes = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải danh mục/loại hoa: {e}')
            return
        top = tk.Toplevel(self.master)
        top.title('Thêm sản phẩm')
        top.configure(bg='#f8f8ff')
        for i in range(10):
            top.grid_rowconfigure(i, pad=6)
        for i in range(2):
            top.grid_columnconfigure(i, pad=8)
        tk.Label(top, text='Tên sản phẩm:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        name_entry.grid(row=0, column=1)
        tk.Label(top, text='Mô tả:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=1, column=0, sticky='e')
        desc_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        desc_entry.grid(row=1, column=1)
        tk.Label(top, text='Giá:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=2, column=0, sticky='e')
        price_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        price_entry.grid(row=2, column=1)
        tk.Label(top, text='Giá giảm:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=3, column=0, sticky='e')
        discounted_price_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        discounted_price_entry.grid(row=3, column=1)
        tk.Label(top, text='Số lượng:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=4, column=0, sticky='e')
        stock_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        stock_entry.grid(row=4, column=1)
        tk.Label(top, text='Ảnh (tên file):', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=5, column=0, sticky='e')
        image_url_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        image_url_entry.grid(row=5, column=1, sticky='w')
        img_btn = tk.Button(top, text='Chọn ảnh...', font=('Segoe UI', 11), command=choose_image, bg='#b22222', fg='white')
        img_btn.grid(row=5, column=1, sticky='e', padx=5)
        tk.Label(top, text='Miễn phí ship:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=6, column=0, sticky='e')
        is_freeship_var = tk.IntVar()
        is_freeship_cb = tk.Checkbutton(top, variable=is_freeship_var, bg='#f8f8ff')
        is_freeship_cb.grid(row=6, column=1, sticky='w')
        tk.Label(top, text='Danh mục:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=7, column=0, sticky='e')
        category_cb = ttk.Combobox(top, values=[c[1] for c in categories], state='readonly', font=('Segoe UI', 12), width=28)
        category_cb.grid(row=7, column=1)
        tk.Label(top, text='Loại hoa:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=8, column=0, sticky='e')
        flowertype_cb = ttk.Combobox(top, values=[f[1] for f in flowertypes], state='readonly', font=('Segoe UI', 12), width=28)
        flowertype_cb.grid(row=8, column=1)
        save_btn = tk.Button(top, text='Lưu', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', command=save)
        save_btn.grid(row=9, column=0, columnspan=2, pady=10)

    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để sửa!')
            return
        item = self.tree.item(selected[0])
        prod_id, old_name, old_price, old_discounted, old_stock, old_cat, old_type, old_freeship = item['values']
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            price = price_entry.get().strip()
            discounted_price = discounted_price_entry.get().strip()
            stock = stock_entry.get().strip()
            image_url = image_url_entry.get().strip()
            is_freeship = 1 if is_freeship_var.get() else 0
            cat_idx = category_cb.current()
            type_idx = flowertype_cb.current()
            if not name or not price or not stock or cat_idx == -1 or type_idx == -1:
                messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ thông tin bắt buộc!')
                return
            try:
                price = int(price)
                discounted_price = int(discounted_price) if discounted_price else 0
                stock = int(stock)
            except:
                messagebox.showerror('Lỗi', 'Giá, giá giảm, số lượng phải là số!')
                return
            try:
                cat_id = categories[cat_idx][0]
                type_id = flowertypes[type_idx][0]
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''UPDATE Products SET Name=%s, Description=%s, Price=%s, DiscountedPrice=%s, StockQuantity=%s, ImageURL=%s, IsFreeship=%s, CategoryID=%s, FlowerTypeID=%s WHERE id=%s''',
                    (name, desc, price, discounted_price, stock, image_url, is_freeship, cat_id, type_id, prod_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Cập nhật sản phẩm thành công!')
                top.destroy()
                self.load_products()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi cập nhật: {e}')
        # Lấy danh mục và loại hoa
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, Name FROM Categories')
            global categories
            categories = cursor.fetchall()
            cursor.execute('SELECT id, Name FROM FlowerTypes')
            global flowertypes
            flowertypes = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải danh mục/loại hoa: {e}')
            return
        top = tk.Toplevel(self.master)
        top.title('Sửa sản phẩm')
        tk.Label(top, text='Tên sản phẩm:').grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(top)
        name_entry.insert(0, old_name)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(top, text='Mô tả:').grid(row=1, column=0, padx=10, pady=5)
        desc_entry = tk.Entry(top)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(top, text='Giá:').grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(top)
        price_entry.insert(0, old_price)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(top, text='Giá giảm:').grid(row=3, column=0, padx=10, pady=5)
        discounted_price_entry = tk.Entry(top)
        discounted_price_entry.insert(0, old_discounted)
        discounted_price_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(top, text='Số lượng:').grid(row=4, column=0, padx=10, pady=5)
        stock_entry = tk.Entry(top)
        stock_entry.insert(0, old_stock)
        stock_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(top, text='Ảnh (tên file):').grid(row=5, column=0, padx=10, pady=5)
        image_url_entry = tk.Entry(top)
        image_url_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(top, text='Miễn phí ship:').grid(row=6, column=0, padx=10, pady=5)
        is_freeship_var = tk.IntVar(value=old_freeship)
        is_freeship_cb = tk.Checkbutton(top, variable=is_freeship_var)
        is_freeship_cb.grid(row=6, column=1, padx=10, pady=5, sticky='w')
        tk.Label(top, text='Danh mục:').grid(row=7, column=0, padx=10, pady=5)
        category_cb = ttk.Combobox(top, values=[c[1] for c in categories], state='readonly')
        category_cb.set(old_cat)
        category_cb.grid(row=7, column=1, padx=10, pady=5)
        tk.Label(top, text='Loại hoa:').grid(row=8, column=0, padx=10, pady=5)
        flowertype_cb = ttk.Combobox(top, values=[f[1] for f in flowertypes], state='readonly')
        flowertype_cb.set(old_type)
        flowertype_cb.grid(row=8, column=1, padx=10, pady=5)
        tk.Button(top, text='Lưu', command=save).grid(row=9, column=0, columnspan=2, pady=10)

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để xóa!')
            return
        item = self.tree.item(selected[0])
        prod_id = item['values'][0]
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa sản phẩm này?'):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Products WHERE id=%s', (prod_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Xóa sản phẩm thành công!')
                self.load_products()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi xóa sản phẩm: {e}')
