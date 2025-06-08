import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
import datetime
import os

def format_currency_vnd(amount):
    try:
        return f"{int(amount):,}".replace(",", ".") + " VNĐ"
    except:
        return str(amount)

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

class InvoiceTab:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_invoices()

    def create_widgets(self):
        filter_frame = ttk.Frame(self.frame)
        filter_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(filter_frame, text='Lọc theo khách hàng:', font=('Segoe UI', 11)).pack(side='left')
        self.customer_entry = ttk.Entry(filter_frame, font=('Segoe UI', 11), width=20)
        self.customer_entry.pack(side='left', padx=5)
        ttk.Label(filter_frame, text='Lọc theo ngày:', font=('Segoe UI', 11)).pack(side='left')
        self.date_entry = ttk.Entry(filter_frame, font=('Segoe UI', 11), width=15)
        self.date_entry.pack(side='left', padx=5)
        self.filter_btn = ttk.Button(filter_frame, text='Lọc', style='Accent.TButton', command=self.filter_invoices)
        self.filter_btn.pack(side='left', padx=5)
        self.reload_btn = ttk.Button(filter_frame, text='Tải lại', command=self.load_invoices)
        self.reload_btn.pack(side='left', padx=5)

        columns = ('ID', 'Khách hàng', 'Ngày', 'Tổng tiền', 'Trạng thái')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=12, style='Custom.Treeview')
        for col in columns:
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
            cursor.execute('''SELECT i.InvoiceId, info.FullName, i.CreateAt, i.Amount, i.Status \
                              FROM Invoices i JOIN Informations info ON i.UserId = info.UserId''')
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_date_vn(row[2])  # Ngày
                row[3] = format_currency_vnd(row[3])  # Tổng tiền
                row[4] = 'Chưa thanh toán' if row[4] == 0 else 'Đã thanh toán'
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải hóa đơn: {e}')

    def filter_invoices(self):
        customer = self.customer_entry.get().strip()
        date = self.date_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = '''SELECT i.InvoiceId, info.FullName, i.CreateAt, i.Amount, i.Status \
                       FROM Invoices i JOIN Informations info ON i.UserId = info.UserId \
                       WHERE (info.FullName LIKE %s OR %s = '') AND (i.CreateAt LIKE %s OR %s = '')'''
            like_cust = f'%{customer}%'
            like_date = f'%{date}%'
            cursor.execute(query, (like_cust, customer, like_date, date))
            for row in cursor.fetchall():
                row = list(row)
                row[2] = format_date_vn(row[2])  # Ngày
                row[3] = format_currency_vnd(row[3])  # Tổng tiền
                row[4] = 'Chưa thanh toán' if row[4] == 0 else 'Đã thanh toán'
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi lọc hóa đơn: {e}')

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
            columns = ('Tên sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền')
            tree = ttk.Treeview(top, columns=columns, show='tree headings', height=6, style='Detail.Treeview')
            tree.heading('#0', text='Ảnh')
            tree.column('#0', width=80, anchor='center')
            for col, w in zip(columns, [220, 80, 100, 120]):
                tree.heading(col, text=col)
                tree.column(col, width=w, anchor='center')
            tree.pack(fill='both', expand=True, padx=10, pady=10)
            from utils.image_utils import load_image_from_url
            images = []
            total = 0
            for d in details:
                thanh_tien = d[3] * d[4]
                total += thanh_tien
                type_map = {1: 'daisy', 2: 'dandelion', 3: 'rose', 4: 'sunflower', 5: 'tulip'}
                folder = type_map.get(d[7], 'rose')
                img_url = d[6]
                img_path = None
                for ext in ['.jpg', '.png']:
                    temp_path = f'flowers_shop/{folder}/{img_url}{ext}'
                    if os.path.exists(temp_path):
                        img_path = temp_path
                        break
                if img_path is None:
                    img_path = f'flowers_shop/{folder}/{img_url}.jpg'
                img = load_image_from_url(img_path, size=(60, 60), master=top)
                images.append(img)
                tree.insert('', 'end', text='', image=img, values=(d[5], d[3], f'{d[4]:,.0f}', f'{thanh_tien:,.0f}'))
            top.images = images
            # XÓA đoạn này vì gây lỗi:
            # for i, img in enumerate(images):
            #     if img:
            #         tree.set(tree.get_children()[i], column='Ảnh', value='')
            #         tree.item(tree.get_children()[i], image=img)
            # Tổng cộng
            total_lbl = tk.Label(top, text=f'Tổng cộng: {total:,.0f} VNĐ', font=('Segoe UI', 12, 'bold'), fg='#d2691e')
            total_lbl.pack(pady=(0, 10))
            tk.Button(top, text='Đóng', command=top.destroy, font=('Segoe UI', 11)).pack(pady=5)
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi lấy chi tiết hóa đơn: {e}')
