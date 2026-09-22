from typing import List, Dict
from .models import Product


class CatalogRepository:
    def __init__(self):
        self._products: List[Product] = self._initialize_catalog()
        self._affinities: Dict[str, List[str]] = self._initialize_affinities()

    def get_all(self) -> List[Product]:
        return [Product(**p.__dict__) for p in self._products]

    def get_by_sku(self, sku: str) -> Product:
        for product in self._products:
            if product.sku == sku:
                return Product(**product.__dict__)
        return Product(
            sku=sku,
            barcode="0000000000000",
            name="UNKNOWN PRODUCT",
            category="UNKNOWN",
            cost_price=0.0,
            sell_price=0.0,
            stock=0,
            damaged_barcode_prob=0.0,
        )

    def get_affinities(self, sku: str) -> List[str]:
        return self._affinities.get(sku, [])

    def _initialize_catalog(self) -> List[Product]:
        return [
            Product("SKU-1001", "8992753110014", "Beras Pandan Wangi 5kg", "Groceries", 68000.0, 78500.0, 120, 0.02),
            Product("SKU-1002", "8992753110021", "Minyak Goreng Bimoli 2L", "Groceries", 32000.0, 37500.0, 150, 0.03),
            Product("SKU-1003", "8992753110038", "Gula Pasir Gulaku 1kg", "Groceries", 14500.0, 17500.0, 200, 0.01),
            Product("SKU-1004", "8992753110045", "Tepung Terigu Segitiga Biru 1kg", "Groceries", 11000.0, 13500.0, 100, 0.02),
            Product("SKU-1005", "8992753110052", "Garam Dapur Cap Kapal 250g", "Groceries", 3500.0, 5000.0, 150, 0.01),
            Product("SKU-1006", "8992753110069", "Kecap Manis Bango 520ml", "Groceries", 21000.0, 25500.0, 140, 0.02),
            Product("SKU-1007", "8992753110076", "Saus Sambal ABC 335ml", "Groceries", 14000.0, 17500.0, 130, 0.02),
            Product("SKU-1008", "8992753110083", "Indomie Goreng Spesial 85g", "Groceries", 2800.0, 3500.0, 600, 0.04),
            Product("SKU-1009", "8992753110090", "Indomie Kuah Ayam Bawang 69g", "Groceries", 2700.0, 3400.0, 450, 0.04),
            Product("SKU-1010", "8992753110106", "Sedaap Mie Goreng 90g", "Groceries", 2700.0, 3400.0, 350, 0.03),
            Product("SKU-1011", "8992753110113", "Sarden ABC Saus Tomat 155g", "Groceries", 9500.0, 12000.0, 90, 0.02),
            Product("SKU-1012", "8992753110120", "Kornet Sapi Pronas 198g", "Groceries", 21000.0, 26000.0, 80, 0.02),

            Product("SKU-2001", "8992753220010", "Telur Ayam Negeri 1kg", "Fresh & Dairy", 26000.0, 31000.0, 80, 0.05),
            Product("SKU-2002", "8992753220027", "Susu Ultra Milk Full Cream 1L", "Fresh & Dairy", 17500.0, 21500.0, 110, 0.02),
            Product("SKU-2003", "8992753220034", "Susu Ultra Milk Cokelat 1L", "Fresh & Dairy", 17500.0, 21500.0, 100, 0.02),
            Product("SKU-2004", "8992753220041", "Yakult Pack isi 5", "Fresh & Dairy", 9200.0, 11500.0, 90, 0.01),
            Product("SKU-2005", "8992753220058", "Keju Kraft Cheddar 165g", "Fresh & Dairy", 19000.0, 24000.0, 75, 0.02),
            Product("SKU-2006", "8992753220065", "Mentega Blue Band 200g", "Fresh & Dairy", 9500.0, 12500.0, 85, 0.02),
            Product("SKU-2007", "8992753220072", "Sari Roti Tawar Spesial", "Fresh & Dairy", 13500.0, 16500.0, 60, 0.04),
            Product("SKU-2008", "8992753220089", "Sari Roti Sobek Cokelat", "Fresh & Dairy", 16000.0, 19500.0, 50, 0.03),

            Product("SKU-3001", "8992753330016", "Air Mineral Aqua 600ml", "Snacks & Drinks", 3000.0, 4000.0, 400, 0.02),
            Product("SKU-3002", "8992753330023", "Air Mineral Le Minerale 600ml", "Snacks & Drinks", 2900.0, 3800.0, 350, 0.02),
            Product("SKU-3003", "8992753330030", "Teh Pucuk Harum 350ml", "Snacks & Drinks", 3200.0, 4500.0, 300, 0.03),
            Product("SKU-3004", "8992753330047", "Kopi Kapal Api Spesial Mix 10s", "Snacks & Drinks", 12500.0, 15500.0, 120, 0.02),
            Product("SKU-3005", "8992753330054", "Good Day Moccacino 250ml", "Snacks & Drinks", 6000.0, 8000.0, 150, 0.02),
            Product("SKU-3006", "8992753330061", "Coca Cola 390ml", "Snacks & Drinks", 5500.0, 7500.0, 160, 0.02),
            Product("SKU-3007", "8992753330078", "Chitato Sapi Panggang 68g", "Snacks & Drinks", 9800.0, 12500.0, 140, 0.04),
            Product("SKU-3008", "8992753330085", "Taro Net Seaweed 65g", "Snacks & Drinks", 7500.0, 9800.0, 130, 0.03),
            Product("SKU-3009", "8992753330092", "Oreo Original Roll 133g", "Snacks & Drinks", 8500.0, 11000.0, 110, 0.02),
            Product("SKU-3010", "8992753330108", "SilverQueen Cokelat Mede 58g", "Snacks & Drinks", 13000.0, 17000.0, 90, 0.03),

            Product("SKU-4001", "8992753440012", "Sabun Mandi Lifebuoy Total 10 450ml", "Personal Care", 22000.0, 27500.0, 80, 0.02),
            Product("SKU-4002", "8992753440029", "Shampoo Sunsilk Black Shine 160ml", "Personal Care", 21000.0, 26000.0, 70, 0.02),
            Product("SKU-4003", "8992753440036", "Pasta Gigi Pepsodent 190g", "Personal Care", 13500.0, 17000.0, 95, 0.02),
            Product("SKU-4004", "8992753440043", "Sikat Gigi Formula Double Action 3s", "Personal Care", 12000.0, 15500.0, 60, 0.01),
            Product("SKU-4005", "8992753440050", "Rexona Deodorant Roll On 45ml", "Personal Care", 16000.0, 20500.0, 50, 0.02),
            Product("SKU-4006", "8992753440067", "Paseo Facial Tissue 250 Sheets", "Personal Care", 13000.0, 16500.0, 120, 0.03),
            Product("SKU-4007", "8992753440074", "Minyak Telon My Baby 90ml", "Personal Care", 22500.0, 28000.0, 45, 0.01),

            Product("SKU-5001", "8992753550018", "Deterjen Rinso Anti Noda 770g", "Household", 18500.0, 23000.0, 85, 0.02),
            Product("SKU-5002", "8992753550025", "Pewangi Pakaian Molto All in 1 720ml", "Household", 19000.0, 24000.0, 75, 0.02),
            Product("SKU-5003", "8992753550032", "Sabun Cuci Piring Sunlight 650ml", "Household", 12500.0, 15500.0, 110, 0.02),
            Product("SKU-5004", "8992753550049", "Pembersih Lantai Super Pell 770ml", "Household", 11500.0, 14500.0, 80, 0.02),
            Product("SKU-5005", "8992753550056", "Baygon Obat Nyamuk Semprot 600ml", "Household", 35000.0, 42000.0, 50, 0.02),
            Product("SKU-5006", "8992753550063", "Baterai ABC Alkaline AA 4s", "Household", 16000.0, 21000.0, 70, 0.03),
        ]

    def _initialize_affinities(self) -> Dict[str, List[str]]:
        return {
            "SKU-1008": ["SKU-2001", "SKU-1007", "SKU-3001"],
            "SKU-1009": ["SKU-2001", "SKU-1007", "SKU-3001"],
            "SKU-1010": ["SKU-2001", "SKU-1007"],
            "SKU-2007": ["SKU-2006", "SKU-2005", "SKU-2002"],
            "SKU-1001": ["SKU-1002", "SKU-1003", "SKU-1005"],
            "SKU-1002": ["SKU-1001", "SKU-1004", "SKU-1006"],
            "SKU-3004": ["SKU-1003", "SKU-2007", "SKU-3009"],
            "SKU-4001": ["SKU-4002", "SKU-4003"],
            "SKU-4002": ["SKU-4001", "SKU-4003"],
            "SKU-4003": ["SKU-4004"],
            "SKU-5001": ["SKU-5002", "SKU-5003"],
            "SKU-5003": ["SKU-5004", "SKU-5001"],
            "SKU-3007": ["SKU-3006", "SKU-3003", "SKU-3010"],
        }
