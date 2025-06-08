import tkinter as tk
from tkinter import ttk
from gui.product_tab import ProductTab
from gui.category_tab import CategoryTab
from gui.flowertype_tab import FlowerTypeTab
from gui.customer_tab import CustomerTab
from gui.invoice_tab import InvoiceTab
from gui.statistic_tab import StatisticTab

class AdminMainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Quản trị cửa hàng hoa - Admin')
        self.master.configure(bg='#f8f8ff')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f8f8ff', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'), padding=[20, 10], background='#e6e6fa', foreground='#b22222')
        style.map('TNotebook.Tab', background=[('selected', '#b22222')], foreground=[('selected', 'white')])
        self.notebook = ttk.Notebook(master, style='TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        # Tab Sản phẩm
        self.product_tab = ProductTab(self.notebook)
        self.notebook.add(self.product_tab.frame, text='Sản phẩm')
        self.category_tab = CategoryTab(self.notebook)
        self.notebook.add(self.category_tab.frame, text='Danh mục')
        self.flowertype_tab = FlowerTypeTab(self.notebook)
        self.notebook.add(self.flowertype_tab.frame, text='Loại hoa')
        self.customer_tab = CustomerTab(self.notebook)
        self.notebook.add(self.customer_tab.frame, text='Khách hàng')
        self.invoice_tab = InvoiceTab(self.notebook)
        self.notebook.add(self.invoice_tab.frame, text='Hóa đơn')
        # Tab Thống kê
        self.statistic_tab = StatisticTab(self.notebook)
        self.notebook.add(self.statistic_tab.frame, text='Thống kê')
