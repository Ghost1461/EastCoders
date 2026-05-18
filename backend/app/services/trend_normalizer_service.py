import re
import unicodedata


CATEGORY_MAP = {
    "kadın giyim": "kadin_giyim",
    "kadın": "kadin_giyim",
    "erkek giyim": "erkek_giyim",
    "ayakkabı": "ayakkabi",
    "çanta": "canta",
    "aksesuar": "aksesuar",
    "gömlek": "gomlek",
    "elbise": "elbise",
    "pantolon": "pantolon",
}


PLATFORM_MAP = {
    "trendyol": "trendyol",
    "hepsiburada": "hepsiburada",
    "amazon": "amazon",
}


STOPWORDS = {
    "kadin", "erkek", "cocuk", "beyaz", "siyah", "mavi",
    "yeni", "sezon", "model", "beden"
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_product_name(name: str) -> str:
    text = normalize_text(name)
    words = text.split()

    words = [word for word in words if word not in STOPWORDS]

    important_words = []

    for word in words:
        if word in [
            "oversize", "keten", "gomlek", "elbise", "trenckot",
            "jean", "pantolon", "tshirt", "sweatshirt", "takim",
            "blazer", "crop", "abiye"
        ]:
            important_words.append(word)

    if important_words:
        return " ".join(important_words)

    return " ".join(words[:3])


def normalize_category(category: str) -> str:
    text = normalize_text(category)

    for key, value in CATEGORY_MAP.items():
        if normalize_text(key) in text:
            return value

    return text.replace(" ", "_")


def normalize_platform(platform: str) -> str:
    text = normalize_text(platform)
    return PLATFORM_MAP.get(text, text)