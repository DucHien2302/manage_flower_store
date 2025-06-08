# Mô hình dữ liệu sản phẩm
class Product:
    def __init__(self, id, name, description, price, discounted_price, stock_quantity, image_url, is_freeship, category_id, flower_type_id):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.discounted_price = discounted_price
        self.stock_quantity = stock_quantity
        self.image_url = image_url
        self.is_freeship = is_freeship
        self.category_id = category_id
        self.flower_type_id = flower_type_id
