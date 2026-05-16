CLOTHING_KEYWORDS = [
    "giyim", "kıyafet", "elbise", "ceket", "pantolon", "etek",
    "gömlek", "tişört", "t-shirt", "mont", "kaban", "triko",
    "kazak", "forma", "ayakkabı", "sneaker", "bot", "çanta",
    "tote bag", "aksesuar", "tekstil", "kumaş", "defile", "podyum",
    "koleksiyon", "tasarım", "tasarımcı", "stil", "kombin",
    "streetwear", "oversize", "haute couture", "cruise",
    "kırmızı halı", "mango", "zara", "h&m", "trendyolmilla",
    "lc waikiki", "vans", "chanel", "dior", "gucci", "prada",
    "balenciaga"
]
COMMERCE_KEYWORDS = [
    "kargo",
    "lojistik",
    "teslimat",
    "dağıtım",
    "dağıtım ağı",
    "kurye",
    "son kilometre",
    "last mile",
    "depolama",
    "fulfillment",
    "iade",
    "teslimat süresi",
    "kargo ücreti",
    "kargo ücretleri",
    "e-ticaret",
    "eticaret",
    "marketplace",
    "pazaryeri",
    "trendyol",
    "hepsiburada",
    "amazon",
    "n11",
    "çiçeksepeti",
    "satıcı",
    "satıcı paneli",
    "komisyon",
    "ödeme sistemi",
    "dijital ticaret",
    "online satış",
    "internet satışı",
    "e-ihracat",
    "ihracat",
    "ithalat",
    "gümrük",
    "vergi",
    "kdv",
    "stopaj",
    "e-fatura",
    "e-arşiv",
    "fatura",
    "lojistik",
    "kargo",
    "depo",
    "fba",
    "fulfillment",
    "seller",
    "seller policy",
    "fee",
    "fees",
    "policy",
    "regulation",
    "düzenleme"
]


COMMERCE_BLOCKED_KEYWORDS = [
    "spor",
    "magazin",
    "cinayet",
    "deprem",
    "siyaset",
    "seçim",
    "futbol",
    "sağlık",
    "uzman yardımcılığı",
    "sözlü sınav",
    "personel",
    "atama",
    "aday",
    "biyometrik fotoğraf",
    "adli sicil",
    "askerlik",
    "kamu görevlileri"
]

BLOCKED_KEYWORDS = [
    "sofra", "tabak", "bardak", "karaca", "paşabahçe", "mutfak",
    "dekorasyon", "mobilya", "kozmetik", "parfüm", "makyaj",
    "cilt bakım", "lancôme"
]


def is_commerce_related(title: str, description: str | None = None) -> bool:
    text = f"{title or ''} {description or ''}".lower()

    if any(blocked in text for blocked in COMMERCE_BLOCKED_KEYWORDS):
        return False

    return any(keyword in text for keyword in COMMERCE_KEYWORDS)



def is_clothing_related(title: str, description: str | None = None) -> bool:
    text = f"{title or ''} {description or ''}".lower()

    if any(blocked in text for blocked in BLOCKED_KEYWORDS):
        return False

    return any(keyword in text for keyword in CLOTHING_KEYWORDS)