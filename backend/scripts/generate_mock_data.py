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
    """
    Platformların başlangıç ham havuzlarını (Raw Data) oluşturur.
    Her platform için benzersiz (unique) external_id üretilmesini garanti eder.
    """
    for plat in PLATFORMS:
        products_pool = []
        used_external_ids = set()  # Her platform için ayrı bir küme ile ID takibi yapıyoruz
        
        while len(products_pool) < num_products_per_platform:
            # Pazar yeri bazında benzersiz sayı üretimi
            ext_id_num = random.randint(10000, 99999)
            # Platform ismini ekleyerek platformlar arası çakışmayı da önlüyoruz
            ext_id = f"{plat.upper()}-{ext_id_num}"
            
            # Eğer bu ID bu platformda daha önce üretilmediyse havuza ekle
            if ext_id not in used_external_ids:
                used_external_ids.add(ext_id)
                color = random.choice(COLORS)
                cat = random.choice(CATEGORIES)
                
                products_pool.append({
                    "external_id": ext_id,
                    "name": f"{color} {cat}",
                    "brand": random.choice(BRANDS),
                    "category": cat,
                    "color": color,
                    "size": random.choice(SIZES),
                    "price": random.randint(300, 1500),
                    "stock": random.randint(10, 100),
                    "sku": f"SKU-{ext_id}",
                    "image_url": f"https://api.dicebear.com/7.x/identicon/svg?seed={ext_id_num}"
                })
        
        file_path = f"data/mock_sources/{plat}_products.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(products_pool, f, indent=4, ensure_ascii=False)
    print("✅ Platform havuzları pazar yeri bazında UNIQUE ID'lerle oluşturuldu.")

def simulate_user_import(user_id, platform, num_to_import=5):
    """
    Platform havuzundan ürünleri seçer ve 'product_id = external_product_id' 
    mantığıyla sisteme aktarır. internal_product_id veritabanı aşamasına bırakılmıştır.
    """
    source_path = f"data/mock_sources/{platform}_products.json"
    
    with open(source_path, "r", encoding="utf-8") as f:
        raw_products = json.load(f)
    
    # Havuzdaki ürünlerden istenen sayıda örnek al
    product_samples = random.sample(raw_products, k=min(num_to_import, len(raw_products)))
    user_products = []

    for item in product_samples:
        # Ana mantık: product_id ve external_product_id artık aynı (external_id) değerini taşıyor
        unique_id = item["external_id"]

        user_products.append({
            "product_id": unique_id,           # Sistem içi geçici ana kimlik
            "user_id": user_id,
            "platform": platform,
            "external_product_id": unique_id,  # Pazar yerindeki orijinal kimlik
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

    # Güncellenen veriyi platformun JSON dosyasına geri yazıyoruz
    with open(source_path, "w", encoding="utf-8") as f:
        json.dump(user_products, f, indent=4, ensure_ascii=False)
    
    print(f"✅ {platform.upper()} ürünleri ({len(user_products)} adet) başarıyla içe aktarıldı.")

def generate_mock_orders(user_id, platform, num_orders=20):
    """Siparişleri oluşturur ve platformun sipariş dosyasına kaydeder."""
    products_path = f"data/mock_sources/{platform}_products.json"
    output_path = f"data/mock_sources/{platform}_orders.json"

    with open(products_path, "r", encoding="utf-8") as f:
        user_prods = json.load(f)

    all_orders = []
    for i in range(num_orders):
        selected_prods = random.sample(user_prods, k=random.randint(1, min(2, len(user_prods))))
        order_items = []
        for p in selected_prods:
            order_items.append({
                "listing_id": f"L-{random.randint(100, 999)}",
                "product_id": p["product_id"], 
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
    products_path = f"data/mock_sources/{platform}_products.json"
    output_path = f"data/mock_sources/{platform}_reviews.json"

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
            "product_id": target_prod["product_id"],
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



# generate_mock_data.py içine eklenecek kısım
def generate_mock_api_keys(user_ids=["u_001", "u_002"], platforms=["trendyol", "amazon", "hepsiburada"]):
    api_keys = []
    for uid in user_ids:
        for plat in platforms:
            # Her kullanıcı ve platform kombinasyonu için eşsiz bir key
            key = f"{plat[:2].upper()}-{uid}-{random.randint(100, 999)}"
            api_keys.append({
                "user_id": uid,
                "platform": plat,
                "api_key": key
            })
    
    file_path = os.path.join(os.getcwd(), "data", "mock_sources", "api_keys.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(api_keys, f, indent=4)
        f.flush()            # Veriyi hemen diske it
        os.fsync(f.fileno()) # İşletim sistemini zorla
    print(f"✅ Mock API Key'ler '{file_path}' dosyasına yazıldı. Toplam: {len(api_keys)}")


def reset_normalized_files():
    """Normalized klasöründeki dosyaları temizler."""
    files_to_reset = [
        "data/normalized/products.json",
        "data/normalized/orders.json",
        "data/normalized/reviews.json"
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
    
    # 3. API Key'leri üret (Ürünlerden önce üretmek daha mantıklı)
    generate_mock_api_keys(user_ids=["u_001", "u_002"], platforms=PLATFORMS)
    
    # 4. Ürünleri import et
    simulate_user_import("u_001", "trendyol", num_to_import=20)
    simulate_user_import("u_001", "amazon", num_to_import=25)
    simulate_user_import("u_001", "hepsiburada", num_to_import=30)

    # 5. Siparişleri oluştur
    generate_mock_orders("u_001", "trendyol", num_orders=15)
    generate_mock_orders("u_001", "amazon", num_orders=10)
    generate_mock_orders("u_001", "hepsiburada", num_orders=12)
    
    # 6. Yorum Üretimi
    generate_mock_reviews("u_001", "trendyol", num_reviews=10)
    generate_mock_reviews("u_001", "amazon", num_reviews=8)
    generate_mock_reviews("u_001", "hepsiburada", num_reviews=12)

    print("\n🚀 İşlem tamamlandı. Tüm veriler 'mock_sources' içine ayrıştırıldı.")