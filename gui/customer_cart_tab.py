import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection, get_cart_id

class CustomerCartTab:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_cart()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Tên', 'Giá', 'Số lượng', 'Chọn mua'), show='headings', height=12, style='Custom.Treeview')
        for col in ('ID', 'Tên', 'Giá', 'Số lượng', 'Chọn mua'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.update_btn = ttk.Button(btn_frame, text='Cập nhật số lượng', style='Accent.TButton', command=self.update_quantity)
        self.update_btn.pack(side='left', padx=5)
        self.delete_btn = ttk.Button(btn_frame, text='Xóa sản phẩm', command=self.delete_item)
        self.delete_btn.pack(side='left', padx=5)
        self.check_btn = ttk.Button(btn_frame, text='Chọn mua', style='Accent.TButton', command=self.check_item)
        self.check_btn.pack(side='left', padx=5)
        self.pay_btn = ttk.Button(btn_frame, text='Thanh toán', style='Accent.TButton', command=self.pay)
        self.pay_btn.pack(side='left', padx=5)

    def load_cart(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            cart_id = get_cart_id(self.user_id)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc('GetCartsById', (cart_id,))
            for result in cursor.stored_results():
                for row in result.fetchall():
                    self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải giỏ hàng: {e}')

    def update_quantity(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để cập nhật!')
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
                cursor.execute('UPDATE Carts SET Quantity=%s WHERE CartId=%s AND ProductId=%s', (qty, cart_id, prod_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Cập nhật số lượng thành công!')
                top.destroy()
                self.load_cart()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi cập nhật: {e}')
        top = tk.Toplevel(self.master)
        top.title('Cập nhật số lượng')
        tk.Label(top, text='Số lượng:').grid(row=0, column=0, padx=10, pady=5)
        qty_entry = tk.Entry(top)
        qty_entry.insert(0, str(item['values'][3]))
        qty_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(top, text='Xác nhận', command=save).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để xóa!')
            return
        item = self.tree.item(selected[0])
        prod_id = item['values'][0]
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa sản phẩm này khỏi giỏ?'):
            try:
                cart_id = get_cart_id(self.user_id)
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Carts WHERE CartId=%s AND ProductId=%s', (cart_id, prod_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Đã xóa sản phẩm khỏi giỏ!')
                self.load_cart()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi xóa: {e}')

    def check_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sản phẩm để đánh dấu mua!')
            return
        item = self.tree.item(selected[0])
        prod_id = item['values'][0]
        try:
            cart_id = get_cart_id(self.user_id)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE Carts SET IsChecked=1 WHERE CartId=%s AND ProductId=%s', (cart_id, prod_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo('Thành công', 'Đã chọn sản phẩm để mua!')
            self.load_cart()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi đánh dấu: {e}')

    def pay(self):
        try:
            cart_id = get_cart_id(self.user_id)
            conn = get_connection()
            cursor = conn.cursor()
            # Sinh mã hóa đơn mới
            import uuid
            invoice_id = uuid.uuid4().hex
            amount = 0
            cursor.callproc('AddInvoice', (cart_id, self.user_id, invoice_id, amount))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo('Thành công', 'Thanh toán thành công!')
            self.load_cart()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi thanh toán: {e}')
