import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
from tkinter import filedialog
import os

class CategoryTab:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_categories()

    def create_widgets(self):
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(search_frame, text='Tìm kiếm:', font=('Segoe UI', 11)).pack(side='left')
        self.search_entry = ttk.Entry(search_frame, font=('Segoe UI', 11), width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_btn = ttk.Button(search_frame, text='Tìm', style='Accent.TButton', command=self.search_categories)
        self.search_btn.pack(side='left', padx=5)
        self.reload_btn = ttk.Button(search_frame, text='Tải lại', command=self.load_categories)
        self.reload_btn.pack(side='left', padx=5)

        columns = ('ID', 'Tên', 'Mô tả')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=12, style='Custom.Treeview')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        self.add_btn = ttk.Button(btn_frame, text='Thêm', style='Accent.TButton', command=self.add_category)
        self.add_btn.pack(side='left', padx=5)
        self.edit_btn = ttk.Button(btn_frame, text='Sửa', command=self.edit_category)
        self.edit_btn.pack(side='left', padx=5)
        self.delete_btn = ttk.Button(btn_frame, text='Xóa', command=self.delete_category)
        self.delete_btn.pack(side='left', padx=5)

    def load_categories(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, Name, Description FROM Categories')
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tải danh mục: {e}')

    def search_categories(self):
        keyword = self.search_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = 'SELECT id, Name, Description FROM Categories WHERE Name LIKE %s'
            like_kw = f'%{keyword}%'
            cursor.execute(query, (like_kw,))
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi tìm kiếm: {e}')

    def add_category(self):
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name:
                messagebox.showerror('Lỗi', 'Tên danh mục không được để trống!')
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Categories (Name, Description) VALUES (%s, %s)', (name, desc))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Thêm danh mục thành công!')
                top.destroy()
                self.load_categories()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi thêm danh mục: {e}')
        top = tk.Toplevel(self.master)
        top.title('Thêm danh mục')
        top.configure(bg='#f8f8ff')
        for i in range(3):
            top.grid_rowconfigure(i, pad=6)
        for i in range(2):
            top.grid_columnconfigure(i, pad=8)
        tk.Label(top, text='Tên danh mục:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        name_entry.grid(row=0, column=1)
        tk.Label(top, text='Mô tả:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=1, column=0, sticky='e')
        desc_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        desc_entry.grid(row=1, column=1)
        save_btn = tk.Button(top, text='Lưu', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', command=save)
        save_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def edit_category(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn danh mục để sửa!')
            return
        item = self.tree.item(selected[0])
        cat_id, old_name, old_desc = item['values']
        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name:
                messagebox.showerror('Lỗi', 'Tên danh mục không được để trống!')
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE Categories SET Name=%s, Description=%s WHERE id=%s', (name, desc, cat_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Cập nhật danh mục thành công!')
                top.destroy()
                self.load_categories()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi cập nhật: {e}')
        top = tk.Toplevel(self.master)
        top.title('Sửa danh mục')
        top.configure(bg='#f8f8ff')
        for i in range(3):
            top.grid_rowconfigure(i, pad=6)
        for i in range(2):
            top.grid_columnconfigure(i, pad=8)
        tk.Label(top, text='Tên danh mục:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        name_entry.insert(0, old_name)
        name_entry.grid(row=0, column=1)
        tk.Label(top, text='Mô tả:', font=('Segoe UI', 12, 'bold'), bg='#f8f8ff').grid(row=1, column=0, sticky='e')
        desc_entry = tk.Entry(top, font=('Segoe UI', 12), width=30)
        desc_entry.insert(0, old_desc)
        desc_entry.grid(row=1, column=1)
        save_btn = tk.Button(top, text='Lưu', font=('Segoe UI', 12, 'bold'), bg='#b22222', fg='white', command=save)
        save_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def delete_category(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn danh mục để xóa!')
            return
        item = self.tree.item(selected[0])
        cat_id = item['values'][0]
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn xóa danh mục này?'):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Categories WHERE id=%s', (cat_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo('Thành công', 'Xóa danh mục thành công!')
                self.load_categories()
            except Exception as e:
                messagebox.showerror('Lỗi', f'Lỗi xóa danh mục: {e}')
