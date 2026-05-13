import json
import random
import os
from faker import Faker

fake = Faker()

# Konfigürasyon
CATEGORIES = ["Hoodie", "T-Shirt", "Pants", "Hat", "Dress", "Jacket"]
COLORS = ["Black", "White", "Beige", "Navy Blue", "Grey", "Yellow", "Pink", "Purple"]
PLATFORMS = ["trendyol", "hepsiburada", "amazon"]
BRANDS = ["ModaNova", "TrendStyle", "UrbanWear", "BasicLine", "EastCoders"]
SIZES = ["S", "M", "L", "XL", "XXL"]

def generate_platform_pools(num_products_per_platform=50):
    """Platformların başlangıç ham havuzlarını (Raw Data) oluşturur."""
    for plat in PLATFORMS:
        products_pool = []
        for i in range(num_products_per_platform):
            color = random.choice(COLORS)
            cat = random.choice(CATEGORIES)
            
            products_pool.append({
                "external_id": f"{plat.upper()}-{random.randint(10000, 99999)}",
                "name": f"{color} {cat}",
                "brand": random.choice(BRANDS),
                "category": cat,
                "color": color,
                "size": random.choice(SIZES),
                "price": random.randint(300, 1500),
                "stock": random.randint(10, 100),
                "sku": f"SKU-{plat[:2].upper()}-{random.randint(1000, 9999)}",
                "image_url": f"https://api.dicebear.com/7.x/identicon/svg?seed={random.randint(1,1000)}"
            })
        
        file_path = f"../data/mock_sources/{plat}_products.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(products_pool, f, indent=4, ensure_ascii=False)
    print("✅ Başlangıç platform havuzları (raw) oluşturuldu.")

def simulate_user_import(user_id, platform, num_to_import=5):
    """
    Platform havuzundan ürünleri seçer ve görsellerdeki modellere 
    tam uyumlu şekilde özellikler ekleyerek kaydeder.
    """
    source_path = f"../data/mock_sources/{platform}_products.json"
    
    with open(source_path, "r", encoding="utf-8") as f:
        raw_products = json.load(f)
    
    product_samples = random.sample(raw_products, k=min(num_to_import, len(raw_products)))
    user_products = []

    for item in product_samples:
        if platform == "hepsiburada":
            ext_id = f"HB-{random.randint(1000, 9999)}"
        elif platform == "trendyol":
            ext_id = f"TR-{random.randint(1000, 9999)}"
        else:
            ext_id = f"AZN-{random.randint(1000, 9999)}"

        # Görsellerdeki (image_2a597b.jpg ve image_2a5997.jpg) sütunları ekliyoruz
        user_products.append({
            "internal_product_id": f"INT-P-{random.randint(10000, 99999)}", 
            "product_id": ext_id, 
            "user_id": user_id,
            "platform": platform,
            "external_product_id": item["external_id"], 
            "seller_sku": item["sku"], 
            "name": item["name"],
            "brand": item["brand"], 
            "category": item["category"],
            "color": item["color"], 
            "size": item["size"], 
            "price": item["price"],
            "stock": item["stock"],
            "commission_rate": round(random.uniform(0.05, 0.20), 2), 
            "rating": round(random.uniform(3.5, 5.0), 1), 
            "review_count": random.randint(0, 500), 
            "status": "active", 
            "tags": [item["category"].lower(), item["color"].lower(), "fashion"], 
            "image_url": item["image_url"], 
            "last_updated": fake.date_time_between(start_date='-1d', end_date='now').isoformat() 
        })

    with open(source_path, "w", encoding="utf-8") as f:
        json.dump(user_products, f, indent=4, ensure_ascii=False)
    
    print(f"✅ {platform.upper()} ürünleri zenginleştirilmiş verilerle {user_id} için kaydedildi.")

def generate_mock_orders(user_id, platform, num_orders=20):
    """Siparişleri oluşturur ve platformun sipariş dosyasına kaydeder."""
    products_path = f"../data/mock_sources/{platform}_products.json"
    output_path = f"../data/mock_sources/{platform}_orders.json"

    with open(products_path, "r", encoding="utf-8") as f:
        user_prods = json.load(f)

    all_orders = []
    for i in range(num_orders):
        selected_prods = random.sample(user_prods, k=random.randint(1, min(2, len(user_prods))))
        order_items = []
        for p in selected_prods:
            order_items.append({
                "listing_id": f"L-{random.randint(100, 999)}",
                "internal_product_id": p["internal_product_id"], 
                "quantity": random.randint(1, 2),
                "unit_price": p["price"]
            })

        all_orders.append({
            "order_id": f"O-{random.randint(10000, 99999)}",
            "user_id": user_id,
            "platform": platform.capitalize(),
            "external_order_id": f"{platform[:2].upper()}-ORD-{random.randint(1000, 9999)}",
            "customer_id": f"C-{random.randint(100, 999)}",
            "items": order_items,
            "status": random.choice(["delivered", "shipped", "cancelled", "returned"]),
            "order_date": fake.date_between(start_date='-30d', end_date='today').isoformat()
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_orders, f, indent=4, ensure_ascii=False)
    print(f"✅ {platform.upper()} siparişleri kaydedildi.")

def generate_mock_reviews(user_id, platform, num_reviews=15):
    """Yorumları oluşturur ve platformun yorum dosyasına kaydeder."""
    products_path = f"../data/mock_sources/{platform}_products.json"
    output_path = f"../data/mock_sources/{platform}_reviews.json"

    with open(products_path, "r", encoding="utf-8") as f:
        user_prods = json.load(f)

    review_templates = [
        {"comment": "Ürün çok kaliteli, tam beklediğim gibi.", "rating": 5, "sentiment": "positive", "topic": "quality"},
        {"comment": "Kumaşı güzel ama bedeni çok dar.", "rating": 3, "sentiment": "mixed", "topic": "size"},
        {"comment": "Kargo çok yavaştı.", "rating": 2, "sentiment": "negative", "topic": "shipping"},
        {"comment": "Rengi fotoğraftakinden biraz farklı.", "rating": 4, "sentiment": "mixed", "topic": "color"}
    ]

    all_reviews = []
    for i in range(num_reviews):
        target_prod = random.choice(user_prods)
        template = random.choice(review_templates)
        
        all_reviews.append({
            "review_id": f"REV-{random.randint(10000, 99999)}",
            "customer_id": f"C-{random.randint(100, 999)}",
            "internal_product_id": target_prod["internal_product_id"], 
            "listing_id": f"L-{random.randint(100, 999)}",
            "platform": platform.capitalize(),
            "rating": template["rating"],
            "comment": template["comment"],
            "sentiment": template["sentiment"],
            "topic": template["topic"],
            "created_at": fake.date_between(start_date='-20d', end_date='today').isoformat()
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, indent=4, ensure_ascii=False)
    print(f"✅ {platform.upper()} yorumları kaydedildi.")

def reset_normalized_files():
    """Normalized klasöründeki dosyaları temizler."""
    files_to_reset = [
        "../data/normalized/products.json",
        "../data/normalized/orders.json",
        "../data/normalized/reviews.json"
    ]
    for file_path in files_to_reset:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
    print("🧹 Normalized dosyalar temizlendi.")

if __name__ == "__main__":
    # 1. Önce normalize edilmiş verileri temizle
    reset_normalized_files()

    # 2. Platform havuzlarını temizle ve yeniden oluştur
    generate_platform_pools()
    
    # 3. Ürünleri import et
    simulate_user_import("u_001", "trendyol", num_to_import=20)
    simulate_user_import("u_001", "amazon", num_to_import=25)
    simulate_user_import("u_001", "hepsiburada", num_to_import=30)

    # 4. Siparişleri oluştur
    generate_mock_orders("u_001", "trendyol", num_orders=15)
    generate_mock_orders("u_001", "amazon", num_orders=10)
    generate_mock_orders("u_001", "hepsiburada", num_orders=12)
    
    # 5. Yorum Üretimi
    generate_mock_reviews("u_001", "trendyol", num_reviews=10)
    generate_mock_reviews("u_001", "amazon", num_reviews=8)
    generate_mock_reviews("u_001", "hepsiburada", num_reviews=12)

    print("\n🚀 İşlem tamamlandı. Tüm veriler 'mock_sources' içine ayrıştırıldı.")