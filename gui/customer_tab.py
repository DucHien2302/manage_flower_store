import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
from tkinter import filedialog
from tkcalendar import DateEntry
import os
import datetime

def format_date_vn(date_val):
    if isinstance(date_val, str):
        try:
            date_val = datetime.datetime.strptime(date_val, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                date_val = datetime.datetime.strptime(date_val, "%Y-%m-%d")
            except:
                return str(date_val)
    return date_val.strftime("%d/%m/%Y")

class CustomerTab:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.setup_treeview_style()
        self.create_widgets()
        self.load_customers()

    def setup_treeview_style(self):
        style = ttk.Style()
        style.configure('Custom.Treeview',
                        font=('Segoe UI', 12),  # Font chữ dòng
                        rowheight=32)           # Chiều cao dòng
        style.configure('Custom.Treeview.Heading',
                        font=('Segoe UI', 13, 'bold'),  # Font header
                        foreground='#b22222',           # Màu chữ header
                        background='#e6e6fa')           # Màu nền header
        style.map('Custom.Treeview.Heading',
                  background=[('active', '#f8f8ff')])

    def create_widgets(self):
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(search_frame, text='Tìm kiếm:', font=('Segoe UI', 11)).pack(side='left')
        self.search_entry = ttk.Entry(search_frame, font=('Segoe UI', 11), width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_btn = ttk.Button(search_frame, text='Tìm', style='Accent.TButton', command=self.search_customers)
        self.search_btn.pack(side='left', padx=5)
        self.reload_btn = ttk.Button(search_frame, text='Tải lại', command=self.load_customers)
        self.reload_btn.pack(side='left', padx=5)

        columns = ('ID', 'Tên', 'Email', 'Địa chỉ', 'Ngày sinh', 'Giới tính')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=12, style='Custom.Treeview')
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col, anchor='center')
            # Đặt lại độ rộng và vị trí cột hợp lý
            if col == 'ID':
                self.tree.column(col, width=60, anchor='center')
            elif col == 'Tên':
                self.tree.column(col, width=180, anchor='w')
            elif col == 'Email':
                self.tree.column(col, width=180, anchor='w')
            elif col == 'Địa chỉ':
                self.tree.column(col, width=200, anchor='w')
            elif col == 'Ngày sinh':
                self.tree.column(col, width=110, anchor='center')
            elif col == 'Giới tính':
                self.tree.column(col, width=90, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.add_btn = ttk.Button(btn_frame, text='Thêm', style='Accent.TButton', command=self.add_customer)
        self.add_btn.pack(side='left', padx=5)
        self.edit_btn = ttk.Button(btn_frame, text='Sửa', command=self.edit_customer)
        self.edit_btn.pack(side='left', padx=5)
        self.delete_btn = ttk.Button(btn_frame, text='Xóa', command=self.delete_customer)
        self.delete_btn.pack(side='left', padx=5)

    def load_customers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT i.id, i.FullName, u.Email, i.Address, i.DateOfBirth, i.Gender \
                              FROM Informations i JOIN SysUser u ON i.UserId = u.id''')
            for row in cursor.fetchall():
                row = list(row)
                row[4] = format_date_vn(row[4])
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải khách hàng: {e}')

    def search_customers(self):
        keyword = self.search_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = '''SELECT i.id, i.FullName, u.Email, i.Address, i.DateOfBirth, i.Gender \
                       FROM Informations i JOIN SysUser u ON i.UserId = u.id \
                       WHERE i.FullName LIKE %s OR u.Email LIKE %s'''
            like_kw = f'%{keyword}%'
            cursor.execute(query, (like_kw, like_kw))
            for row in cursor.fetchall():
                row = list(row)
                row[4] = format_date_vn(row[4])
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tìm kiếm: {e}')

    def add_customer(self):
        def save():
            fullname = fullname_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            dob = dob_entry.get_date().strftime('%Y-%m-%d')
            gender = gender_cb.get().strip()
            password = password_entry.get().strip()
            if not fullname or not email or not address or not dob or not gender or not password:
                messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ thông tin!')
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                parts = fullname.split()
                first_name = parts[0]
                last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
                cursor.execute('INSERT INTO SysUser (Email, Password) VALUES (%s, %s)', (email, password))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO Informations (FirstName, LastName, FullName, DateOfBirth, Gender, Address, UserId) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (first_name, last_name, fullname, dob, gender, address, user_id))
                cursor.execute('SELECT id FROM SysRole WHERE Name=%s', ('Customer',))
                role_id = cursor.fetchone()[0]
                cursor.execute('INSERT INTO SysUserRole (UserId, RoleId) VALUES (%s, %s)', (user_id, role_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Thêm khách hàng thành công!')
                top.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi thêm khách hàng: {e}')
        top = tk.Toplevel(self.master)
        top.title('Thêm khách hàng')
        top.configure(bg='#f8f8ff')
        for i in range(7):
            top.grid_rowconfigure(i, pad=6)
        for i in range(2):
            top.grid_columnconfigure(i, pad=8)
        tk.Label(top, text='Họ và tên:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=0, column=0, sticky='e')
        fullname_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        fullname_entry.grid(row=0, column=1)
        tk.Label(top, text='Email:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=1, column=0, sticky='e')
        email_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        email_entry.grid(row=1, column=1)
        tk.Label(top, text='Mật khẩu:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=2, column=0, sticky='e')
        password_entry = tk.Entry(top, font=('Segoe UI', 12), width=30, show='*')
        password_entry.grid(row=2, column=1)
        tk.Label(top, text='Địa chỉ:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=3, column=0, sticky='e')
        address_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        address_entry.grid(row=3, column=1)
        tk.Label(top, text='Ngày sinh:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=4, column=0, sticky='e')
        dob_entry = DateEntry(top, font=('Segoe UI', 12), width=28, date_pattern='yyyy-mm-dd', background='#e6e6fa', foreground='#b22222', borderwidth=2)
        dob_entry.grid(row=4, column=1)
        tk.Label(top, text='Giới tính:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=5, column=0, sticky='e')
        gender_cb = ttk.Combobox(top, values=['Nam', 'Nữ', 'Khác'], state='readonly', font=('Segoe UI', 12), width=28)
        gender_cb.grid(row=5, column=1)
        save_btn = tk.Button(top, text='Lưu', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', command=save)
        save_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def edit_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn khách hàng để sửa!')
            return
        item = self.tree.item(selected[0])
        cust_id, old_fullname, old_email, old_address, old_dob, old_gender = item['values']
        # Chuyển đổi old_dob về datetime.date nếu là string
        import datetime
        dob_value = old_dob
        if isinstance(dob_value, str):
            try:
                dob_value = datetime.datetime.strptime(dob_value, "%d/%m/%Y").date()
            except:
                try:
                    dob_value = datetime.datetime.strptime(dob_value, "%Y-%m-%d").date()
                except:
                    dob_value = datetime.date.today()
        def save():
            fullname = fullname_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            dob = dob_entry.get_date().strftime('%Y-%m-%d')
            gender = gender_cb.get().strip()
            if not fullname or not email or not address or not dob or not gender:
                messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ thông tin!')
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                parts = fullname.split()
                first_name = parts[0]
                last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
                cursor.execute('UPDATE Informations SET FirstName=%s, LastName=%s, FullName=%s, DateOfBirth=%s, Gender=%s, Address=%s WHERE id=%s',
                    (first_name, last_name, fullname, dob, gender, address, cust_id))
                cursor.execute('SELECT UserId FROM Informations WHERE id=%s', (cust_id,))
                user_id = cursor.fetchone()[0]
                cursor.execute('UPDATE SysUser SET Email=%s WHERE id=%s', (email, user_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Cập nhật khách hàng thành công!')
                top.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi cập nhật: {e}')
        top = tk.Toplevel(self.master)
        top.title('Sửa khách hàng')
        top.configure(bg='#f8f8ff')
        for i in range(6):
            top.grid_rowconfigure(i, pad=6)
        for i in range(2):
            top.grid_columnconfigure(i, pad=8)
        tk.Label(top, text='Họ và tên:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=0, column=0, sticky='e')
        fullname_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        fullname_entry.insert(0, old_fullname)
        fullname_entry.grid(row=0, column=1)
        tk.Label(top, text='Email:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=1, column=0, sticky='e')
        email_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        email_entry.insert(0, old_email)
        email_entry.grid(row=1, column=1)
        tk.Label(top, text='Địa chỉ:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=2, column=0, sticky='e')
        address_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        address_entry.insert(0, old_address)
        address_entry.grid(row=2, column=1)
        tk.Label(top, text='Ngày sinh:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=3, column=0, sticky='e')
        dob_entry = DateEntry(top, font=('Segoe UI', 12), width=28, date_pattern='yyyy-mm-dd', background='#e6e6fa', foreground='#b22222', borderwidth=2)
        dob_entry.set_date(dob_value)
        dob_entry.grid(row=3, column=1)
        tk.Label(top, text='Giới tính:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=4, column=0, sticky='e')
        gender_cb = ttk.Combobox(top, values=['Nam', 'Nữ', 'Khác'], state='readonly', font=('Segoe UI', 12), width=28)
        gender_cb.set(old_gender)
        gender_cb.grid(row=4, column=1)
        save_btn = tk.Button(top, text='Lưu', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', command=save)
        save_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn khách hàng để xóa!')
            return
        item = self.tree.item(selected[0])
        cust_id = item['values'][0]
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa khách hàng này?'):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                # Lấy user_id
                cursor.execute('SELECT UserId FROM Informations WHERE id=%s', (cust_id,))
                user_id = cursor.fetchone()[0]
                cursor.execute('DELETE FROM Informations WHERE id=%s', (cust_id,))
                cursor.execute('DELETE FROM SysUserRole WHERE UserId=%s', (user_id,))
                cursor.execute('DELETE FROM SysUser WHERE id=%s', (user_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Xóa khách hàng thành công!')
                self.load_customers()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi xóa khách hàng: {e}')

    def format_currency_vnd(amount):
        try:
            return f"{int(amount):,}".replace(",", ".") + " VNĐ"
        except:
            return str(amount)

    def format_freeship(value):
        return "Miễn phí" if value == 1 else "Có phí"
