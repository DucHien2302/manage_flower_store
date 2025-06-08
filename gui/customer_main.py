import tkinter as tk
from tkinter import ttk
from gui.customer_product_tab import CustomerProductTab
from gui.customer_cart_tab import CustomerCartTab
from gui.customer_invoice_tab import CustomerInvoiceTab

class CustomerMainWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.master.title('Cửa hàng hoa - Khách hàng')
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        self.product_tab = CustomerProductTab(self.notebook, user_id)
        self.notebook.add(self.product_tab.frame, text='Sản phẩm')
        self.cart_tab = CustomerCartTab(self.notebook, user_id)
        self.notebook.add(self.cart_tab.frame, text='Giỏ hàng')
        self.invoice_tab = CustomerInvoiceTab(self.notebook, user_id)
        self.notebook.add(self.invoice_tab.frame, text='Hóa đơn của tôi')
