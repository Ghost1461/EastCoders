#mock dataları buradan miktarını seçerek oluşturabilirsiniz bu komutla:
#"docker compose exec backend python scripts/generate_mock_data.py"
#uygulama açıldıktan sonra, ekstra terminal açıp yukardaki komutu girin.


import json
import hashlib
import base64
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker


class MockDataGenerator:
    PLATFORMS = ["trendyol", "hepsiburada", "amazon"]
    CATEGORIES = ["Kapüşonlu", "T-Shirt", "Pantolon", "Şapka", "Elbise", "Ceket","Çorap"]
    COLORS = ["Siyah", "Beyaz", "Bej", "Lacivert", "Gri", "Sarı", "Pembe", "Mor"]
    BRANDS = ["ModaNova", "TrendStyle", "UrbanWear", "BasicLine", "EastCoders"] 
    SIZES = ["S", "M", "L", "XL", "XXL"] 
    GENDERS = ["Unisex", "Erkek", "Kadın"]
    STATUSES = ["Aktif", "Stokta Yok"]

    PLATFORM_PREFIXES = {
        "trendyol": "TR",
        "hepsiburada": "HB",
        "amazon": "AMZ"
    }

    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent / "data" / "mock_sources"
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.fake = Faker()

    def _format_user_id(self, user_id: int | str) -> str:
        user_id = str(user_id)

        if user_id.startswith("u_"):
            return user_id

        return f"u_{int(user_id):03d}"

    def _generate_secure_api_key(self, user_id: int, platform: str) -> str:
        raw_string = f"USER_{user_id}_PLATFORM_{platform}_SALT_EASTCODERS_2026"
        hash_bytes = hashlib.sha256(raw_string.encode("utf-8")).digest()
        api_key = base64.b64encode(hash_bytes).decode("utf-8")
        api_key = api_key.replace("+", "").replace("/", "").replace("=", "")
        return f"sk_live_{api_key[:32]}"

    def generate_mock_api_keys(self, number_of_users: int) -> None:
        api_keys_list = []

        for user_number in range(1, number_of_users + 1):
            user_id = self._format_user_id(user_number)

            for platform in self.PLATFORMS:
                api_keys_list.append({
                    "user_id": user_id,
                    "platform": platform,
                    "api_key": self._generate_secure_api_key(user_number, platform)
                })

        file_path = self.base_path / "api_keys.json"

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(api_keys_list, json_file, ensure_ascii=False, indent=4)

        print(f"[SUCCESS] {number_of_users} kullanıcı için API anahtarları '{file_path}' konumuna kaydedildi.")

    def generate_platform_pools(self, number_of_products_per_platform: int = 50) -> None:
        user_count = 5

        for platform in self.PLATFORMS:
            products_list = []
            prefix = self.PLATFORM_PREFIXES[platform]

            for index in range(1, number_of_products_per_platform + 1):
                user_number = ((index - 1) % user_count) + 1
                user_id = self._format_user_id(user_number)

                category = random.choice(self.CATEGORIES)
                brand = random.choice(self.BRANDS)
                color = random.choice(self.COLORS)
                size = random.choice(self.SIZES)
                gender = random.choice(self.GENDERS)
                status = random.choice(self.STATUSES)

                external_product_id = f"{prefix}-{user_number:03d}-{index:06d}"
                seller_sku = f"{prefix}-{user_number:03d}-{index:06d}-SKU"

                product_data = {
                    "user_id": user_id,
                    "platform": platform,
                    "external_product_id": external_product_id,
                    "name": f"{brand} {gender} {color} {category} ({size})",
                    "brand": brand,
                    "gender": gender,
                    "status": status,
                    "price": round(random.uniform(150.0, 2500.0), 2),
                    "stock": random.randint(0, 500) if status != "Out of Stock" else 0,
                    "seller_sku": seller_sku,
                    "category": category,
                    "color": color,
                    "size": size,
                    "review_count": random.randint(0, 1500),
                    "rating": round(random.uniform(1.0, 5.0), 1),
                    "commission_rate": round(random.uniform(0.05, 0.20), 2),
                    "tags": [
                        category.lower(),
                        color.lower(),
                        brand.lower(),
                        "fashion"
                    ],
                    "image_url": f"https://images.eastcoders.com/products/{platform}/{external_product_id}.jpg",
                    "last_updated": self.fake.date_time_between(
                        start_date="-1d",
                        end_date="now"
                    ).isoformat()
                }

                products_list.append(product_data)

            file_path = self.base_path / f"{platform}_products.json"

            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(products_list, json_file, ensure_ascii=False, indent=4)

            print(f"[SUCCESS] '{platform.upper()}' için {number_of_products_per_platform} ürün başarıyla '{file_path}' konumuna kaydedildi.")

    def simulate_user_import(self, platform: str, api_key: str, num_to_import: int = 5) -> list:
        platform_lower = platform.lower()
        api_keys_file = self.base_path / "api_keys.json"

        if not api_keys_file.exists():
            print("[ERROR] api_keys.json bulunamadı.")
            return []

        with open(api_keys_file, "r", encoding="utf-8") as file:
            api_keys_data = json.load(file)

        matched_key = None

        for item in api_keys_data:
            if item["platform"].lower() == platform_lower and item["api_key"] == api_key:
                matched_key = item
                break

        if not matched_key:
            print("[ERROR] Geçersiz API key veya platform.")
            return []

        user_id = matched_key["user_id"]

        products_file = self.base_path / f"{platform_lower}_products.json"

        if not products_file.exists():
            print(f"[ERROR] Ürün dosyası bulunamadı: {products_file}")
            return []

        with open(products_file, "r", encoding="utf-8") as file:
            products = json.load(file)

        user_products = [
            product for product in products
            if product["user_id"] == user_id
        ]

        if not user_products:
            print(f"[WARNING] {platform.upper()} için {user_id} kullanıcısına ait ürün bulunamadı.")
            return []

        num_to_import = min(max(num_to_import, 1), len(user_products))
        selected_products = random.sample(user_products, num_to_import)

        print(f"[SUCCESS] API key doğrulandı. {platform.upper()} / {user_id} için {num_to_import} ürün simüle edildi.")
        return selected_products

    def generate_mock_orders(self, platform: str, num_orders: int = 10) -> None:
        platform_lower = platform.lower()
        products_file = self.base_path / f"{platform_lower}_products.json"

        if not products_file.exists():
            print(f"[ERROR] Sipariş üretilemedi: '{products_file}' bulunamadı.")
            return

        with open(products_file, "r", encoding="utf-8") as file:
            products = json.load(file)

        if not products:
            print("[ERROR] Sipariş üretilemedi: Ürün havuzu boş.")
            return

        orders_list = []
        prefix = self.PLATFORM_PREFIXES.get(platform_lower, "EXT")
        order_statuses = ["delivered", "shipped", "cancelled", "returned"]

        products_by_user = {}

        for product in products:
            products_by_user.setdefault(product["user_id"], []).append(product)

        user_ids = list(products_by_user.keys())

        for index in range(1, num_orders + 1):
            user_id = random.choice(user_ids)
            user_products = products_by_user[user_id]

            item_count = min(random.randint(1, 3), len(user_products))
            selected_products = random.sample(user_products, item_count)

            items_list = []

            for item_index, product in enumerate(selected_products, start=1):
                quantity = random.randint(1, 3)

                items_list.append({
                    "listing_id": f"{platform.capitalize()}-LIST-{index:06d}-{item_index}",
                    "external_product_id": product["external_product_id"],
                    "quantity": quantity,
                    "unit_price": product["price"]
                })

            order_data = {
                "order_id": f"ORD-{prefix}-{index:06d}",
                "user_id": user_id,
                "platform": platform.capitalize(),
                "external_order_id": f"{prefix}-ORD-{index:06d}",
                "customer_id": f"{platform.capitalize()}-CTM-{index:06d}",
                "items": items_list,
                "status": random.choice(order_statuses),
                "order_date": self.fake.date_time_between(
                    start_date="-30d",
                    end_date="now"
                ).strftime("%Y-%m-%d")
            }

            orders_list.append(order_data)

        file_path = self.base_path / f"{platform_lower}_orders.json"

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(orders_list, json_file, ensure_ascii=False, indent=4)

        print(f"[SUCCESS] '{platform.upper()}' için {num_orders} sipariş başarıyla '{file_path}' konumuna kaydedildi.")

    def generate_mock_reviews(self, platform: str, num_reviews: int = 10) -> None:
        platform_lower = platform.lower()
        orders_file = self.base_path / f"{platform_lower}_orders.json"

        if not orders_file.exists():
            print(f"[ERROR] Yorum üretilemedi: '{orders_file}' bulunamadı.")
            return

        with open(orders_file, "r", encoding="utf-8") as file:
            orders = json.load(file)

        if not orders:
            print("[ERROR] Yorum üretilemedi: Sipariş listesi boş.")
            return

        review_templates = [
            {"comment": "Ürün çok kaliteli, tam beklediğim gibi.", "rating": 5, "sentiment": "positive", "topic": "quality"},
            {"comment": "Kumaşı güzel ama bedeni çok dar.", "rating": 3, "sentiment": "mixed", "topic": "size"},
            {"comment": "Kargo çok yavaştı.", "rating": 2, "sentiment": "negative", "topic": "shipping"},
            {"comment": "Rengi fotoğraftakinden biraz farklı.", "rating": 4, "sentiment": "mixed", "topic": "color"},
            {"comment": "Fiyat performans açısından harika bir ürün, tavsiye ederim.", "rating": 5, "sentiment": "positive", "topic": "price"},
            {"comment": "Beklentimi karşılamadı, dikişleri sökük geldi.", "rating": 1, "sentiment": "negative", "topic": "quality"}
        ]

        reviews_list = []

        for index in range(1, num_reviews + 1):
            order = random.choice(orders)
            order_item = random.choice(order["items"])
            template = random.choice(review_templates)

            order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
            review_date = order_date + timedelta(days=random.randint(1, 5))

            if review_date > datetime.now():
                review_date = datetime.now()

            review_data = {
                "user_id": order["user_id"],
                "external_order_id": order["external_order_id"],
                "review_id": f"REV-{self.PLATFORM_PREFIXES.get(platform_lower, 'EXT')}-{index:06d}",
                "customer_id": order["customer_id"],
                "external_product_id": order_item["external_product_id"],
                "listing_id": order_item["listing_id"],
                "platform": order["platform"],
                "rating": template["rating"],
                "comment": template["comment"],
                "sentiment": template["sentiment"],
                "topic": template["topic"],
                "created_at": review_date.strftime("%Y-%m-%d")
            }

            reviews_list.append(review_data)

        file_path = self.base_path / f"{platform_lower}_reviews.json"

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(reviews_list, json_file, ensure_ascii=False, indent=4)

        print(f"[SUCCESS] '{platform.upper()}' için {num_reviews} yorum başarıyla '{file_path}' konumuna kaydedildi.")


if __name__ == "__main__":
    print("=== MOCK DATA SEEDING OPERASYONU BAŞLADI ===\n")

    generator = MockDataGenerator()

    generator.generate_mock_api_keys(number_of_users=5)

    generator.generate_platform_pools(number_of_products_per_platform=50)

    print("\n--- SİPARİŞ VE YORUM ÜRETİM SÜRECİ ---")

    generator.generate_mock_orders(platform="trendyol", num_orders=15)
    generator.generate_mock_orders(platform="amazon", num_orders=12)
    generator.generate_mock_orders(platform="hepsiburada", num_orders=18)

    generator.generate_mock_reviews(platform="trendyol", num_reviews=10)
    generator.generate_mock_reviews(platform="amazon", num_reviews=11)
    generator.generate_mock_reviews(platform="hepsiburada", num_reviews=11)

    print("\n--- FRONTEND ENTEGRASYON TESTİ ---")

    with open(generator.base_path / "api_keys.json", "r", encoding="utf-8") as file:
        keys = json.load(file)
        sample_key = keys[0]["api_key"]
        sample_platform = keys[0]["platform"]

    user_inventory = generator.simulate_user_import(
        platform=sample_platform,
        api_key=sample_key,
        num_to_import=6
    )

    if user_inventory:
        print(json.dumps(user_inventory, indent=4, ensure_ascii=False))

    print("\n=== TÜM MOCK VERİLER HATASIZ ŞEKİLDE ÜRETİLDİ ===")