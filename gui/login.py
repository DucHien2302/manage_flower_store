import tkinter as tk
from tkinter import messagebox
from db import get_connection

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg='#f8f8ff', bd=2, relief='groove')
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(self.frame, text='ĐĂNG NHẬP HỆ THỐNG', font=('Segoe UI', 18, 'bold'), fg='#b22222', bg='#f8f8ff').grid(row=0, column=0, columnspan=2, pady=(10, 20))
        tk.Label(self.frame, text='Email:', font=('Segoe UI', 12), bg='#f8f8ff').grid(row=1, column=0, sticky='e', padx=10, pady=5)
        tk.Label(self.frame, text='Mật khẩu:', font=('Segoe UI', 12), bg='#f8f8ff').grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.email_entry = tk.Entry(self.frame, font=('Segoe UI', 12), width=28)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', font=('Segoe UI', 12), width=28)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.login_btn = tk.Button(self.frame, text='Đăng nhập', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', width=20, command=self.login)
        self.login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not email or not password:
            messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ Email và Mật khẩu!')
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT u.id, u.Email, u.Password, r.Name FROM SysUser u 
                              JOIN SysUserRole ur ON u.id = ur.UserId 
                              JOIN SysRole r ON ur.RoleId = r.id 
                              WHERE u.Email=%s''', (email,))
            user = cursor.fetchone()
            if user and user[2] == password:
                messagebox.showinfo('Thành công', 'Đăng nhập thành công!')
                self.frame.destroy()
                if user[3] == 'Admin':
                    from gui.admin_main import AdminMainWindow
                    AdminMainWindow(self.master)
                else:
                    from gui.customer_main import CustomerMainWindow
                    CustomerMainWindow(self.master, user[0])
            else:
                messagebox.showerror('Lỗi', 'Email hoặc mật khẩu không đúng!')
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Không thể kết nối database: {e}')
