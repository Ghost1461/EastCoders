def calculate_marketplace_rank_signal(rank: int, max_rank: int = 40):
    if not rank:
        return 0

    signal = 1 - ((rank - 1) / max_rank)

    return round(max(signal, 0), 2)


def calculate_keyword_strength(trend_key: str):
    strong_keywords = [
        "keten",
        "oversize",
        "palazzo",
        "blazer",
        "elbise",
        "gomlek",
        "tisort",
        "pantolon",
        "crop",
        "basic",
        "bluz",
        "atlet"
    ]

    words = trend_key.split()
    score = 0

    for word in words:
        if word in strong_keywords:
            score += 0.25

    return round(min(score, 1), 2)


def calculate_trend_score(
    marketplace_signal: float = 0,
    sales_growth: float = 0,
    review_growth: float = 0,
    rating_signal: float = 0,
    stock_signal: float = 0,
    news_signal: float = 0,
    keyword_strength: float = 0
):
    score = (
        marketplace_signal * 0.45
        + sales_growth * 0.20
        + keyword_strength * 0.15
        + rating_signal * 0.10
        + review_growth * 0.05
        + news_signal * 0.05
    )

    return round(score * 100, 2)