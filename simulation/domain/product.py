from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    barcode: str
    name: str
    category: str
    cost_price: float
    sell_price: float
    stock: int
    damaged_barcode_prob: float = 0.03
