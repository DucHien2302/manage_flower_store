# Mô hình chi tiết hóa đơn
class InvoiceDetail:
    def __init__(self, id, product_id, invoice_id, quantity, price, product_name=None, image_url=None):
        self.id = id
        self.product_id = product_id
        self.invoice_id = invoice_id
        self.quantity = quantity
        self.price = price
        self.product_name = product_name
        self.image_url = image_url
