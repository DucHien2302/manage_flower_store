import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

class CustomerInvoiceTab:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_invoices()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Ngày', 'Tổng tiền', 'Trạng thái'), show='headings', height=12, style='Custom.Treeview')
        for col in ('ID', 'Ngày', 'Tổng tiền', 'Trạng thái'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.detail_btn = ttk.Button(btn_frame, text='Xem chi tiết', style='Accent.TButton', command=self.view_detail)
        self.detail_btn.pack(side='left', padx=5)

    def load_invoices(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, CreatedAt, Amount, Status FROM Invoices WHERE CustomerId=%s', (self.user_id,))
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải hóa đơn: {e}')

    def view_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn hóa đơn để xem chi tiết!')
            return
        item = self.tree.item(selected[0])
        invoice_id = item['values'][0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = '''SELECT d.id, d.ProductId, d.InvoiceId, d.Quantity, d.Price, p.Name, p.ImageURL, p.FlowerTypeID
                       FROM InvoiceDetails d JOIN Products p ON d.ProductId = p.id
                       WHERE d.InvoiceId = %s'''
            cursor.execute(query, (invoice_id,))
            details = cursor.fetchall()
            cursor.close()
            conn.close()
            if not details:
                messagebox.showinfo('Thông báo', 'Hóa đơn không có sản phẩm!')
                return
            
            # Giao diện đẹp: có ảnh, tên, số lượng, giá, thành tiền, tổng cộng
            top = tk.Toplevel(self.master)
            top.title(f'Chi tiết hóa đơn {invoice_id}')
            top.geometry('650x400')
            style = ttk.Style(top)
            style.configure('Detail.Treeview.Heading', font=('Segoe UI', 11, 'bold'))
            style.configure('Detail.Treeview', font=('Segoe UI', 10), rowheight=60)
            columns = ('Ảnh', 'Tên sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền')
            tree = ttk.Treeview(top, columns=columns, show='headings', height=6, style='Detail.Treeview')
            for col, w in zip(columns, [80, 220, 80, 100, 120]):
                tree.heading(col, text=col)
                tree.column(col, width=w, anchor='center')
            tree.pack(fill='both', expand=True, padx=10, pady=10)
            
            from utils.image_utils import load_image_from_url
            import os
            images = []
            total = 0
            for d in details:
                thanh_tien = d[3] * d[4]
                total += thanh_tien
                # Lấy đường dẫn ảnh
                type_map = {1: 'daisy', 2: 'dandelion', 3: 'rose', 4: 'sunflower', 5: 'tulip'}
                folder = type_map.get(d[7], 'rose')
                img_url = d[6]  # ImageURL từ database
                
                # Thử các phần mở rộng khác nhau
                img_path = None
                for ext in ['.jpg', '.png']:
                    temp_path = f'flowers_shop/{folder}/{img_url}{ext}'
                    if os.path.exists(temp_path):
                        img_path = temp_path
                        break
                
                if img_path is None:
                    img_path = f'flowers_shop/{folder}/{img_url}.jpg'  # default
                
                print(f"Loading image: {img_path}, exists: {os.path.exists(img_path)}")
                img = load_image_from_url(img_path, size=(60, 60), master=top)
                print(f"Image loaded: {img is not None}")
                images.append(img)  # giữ tham chiếu
                tree.insert('', 'end', values=('', d[5], d[3], f'{d[4]:,.0f}', f'{thanh_tien:,.0f}'))
            
            # Giữ tham chiếu ảnh để tránh garbage collection
            top.images = images
            
            # Hiển thị ảnh trong từng dòng
            for i, img in enumerate(images):
                if img:
                    tree.set(tree.get_children()[i], column='Ảnh', value='')
                    tree.item(tree.get_children()[i], image=img)
            
            # Tổng cộng
            total_lbl = tk.Label(top, text=f'Tổng cộng: {total:,.0f} VNĐ', font=('Segoe UI', 12, 'bold'), fg='#d2691e')
            total_lbl.pack(pady=(0, 10))
            tk.Button(top, text='Đóng', command=top.destroy, font=('Segoe UI', 11)).pack(pady=5)
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi lấy chi tiết hóa đơn: {e}')
