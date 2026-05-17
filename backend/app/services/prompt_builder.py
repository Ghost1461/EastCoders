import json



def to_pretty_json(data: dict) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )


def build_report_summary_prompt(report_data: dict) -> str:
    return f"""
Sen bir e-ticaret satıcı danışmanısın.

Aşağıdaki dashboard verilerine göre kısa, net ve aksiyon odaklı Türkçe rapor üret.


Kurallar:
- Cevap maksimum 5 bölüm olsun.
- Gereksiz selamlama yapma.
- Dashboard’da zaten görünen tüm sayıları tekrar etme.
- En önemli 3 problemi önceliklendir.
- En iyi 3 fırsatı belirt.
- Platform, ürün, stok, yorum ve cinsiyet kırılımlarını dikkate al.
- Eğer aylık veri karşılaştırıyorsan, ay tamamlanmadıysa kesin düşüş yorumu yapma; "şu ana kadar" diye belirt.
- Her aksiyon maddesi uygulanabilir ve net olsun.
- Belirsiz veri varsa tahmin yapma.
- Cevap şu formatta olsun:

## Genel Durum
2-3 cümlelik özet.

## Kritik Bulgular
- Madde 1
- Madde 2
- Madde 3

## Fırsatlar
- Madde 1
- Madde 2
- Madde 3

## Riskler
- Madde 1
- Madde 2
- Madde 3

## Öncelikli Aksiyon Planı
1. İlk yapılacak aksiyon
2. İkinci aksiyon
3. Üçüncü aksiyon

VERİ:
{to_pretty_json(report_data)}
"""

def build_ai_recommendations_prompt(report_data: dict) -> str:
    return f"""
Sen deneyimli bir e-ticaret satış danışmanısın.

Aşağıdaki dashboard verilerine göre satıcıya uygulanabilir, veri odaklı ve aksiyon alınabilir öneriler üret.

Sadece öneri üret. Genel özet yazma.

Çıktı formatı:

🔥 Öncelikli Aksiyonlar
- En yüksek etki oluşturacak kritik problemler
- Maksimum 3-4 madde

📈 Satış Artırma Önerileri
- Satışı artırabilecek fırsatlar
- Ürün, platform, kategori ve gender verilerini birlikte yorumla

⚠️ Riskli Alanlar
- Operasyonel veya müşteri memnuniyeti riskleri
- İptal, iade, düşük rating, düşük teslimat oranı gibi metrikleri değerlendir

🚀 Hızlı Kazanımlar
- Kısa sürede uygulanabilecek pratik öneriler
- Özellikle yüksek yorumlu / yüksek puanlı ürünleri değerlendir

Kurallar:
- Her öneri mutlaka veriye dayansın.
- Çok genel tavsiyeler verme.
- Dashboard’da zaten görünen tüm sayıları tekrar etme.
- Gereksiz resmi dil kullanma.
- Ürün, stok, yorum, satış, platform ve gender verilerini birlikte yorumla.
- Düşük puanlı ürünlerde yorum konularını dikkate al.
- Yüksek puanlı ürünlerde satış fırsatı üret.
- Düşük stok varsa bunu risk/fırsat olarak değerlendir.
- Veri azsa veya dönem tamamlanmadıysa kesin yargılar kurma.
- "Alarm verici", "kritik başarısızlık" gibi aşırı sert ifadeleri dikkatli kullan.
- Gereksiz uzun yazma.
- Türkçe yaz.
- Maksimum 600-700 kelime üret.
- Her bölüm aksiyon odaklı olsun.
- Belirsiz veri varsa tahmin yapma.

VERİ:
{to_pretty_json(report_data)}
"""


def build_stock_analysis_prompt(product_data: dict) -> str:
    return f"""
Sen bir e-ticaret stok ve ürün performansı danışmanısın.

Aşağıdaki ürün verilerine göre kısa, uygulanabilir ve veri odaklı stok analizi üret.

Çıktı formatı:

## Stok Öncelikleri
- En fazla 5 ürün seç.
- Her ürün için: Ürün adı, platform, stok durumu, önerilen aksiyon.

## Güçlü Ürünler
- Yüksek rating + yüksek yorum + yeterli stok kombinasyonuna sahip ürünleri belirt.
- Bu ürünler için satış artırıcı öneri ver.

## Dikkat Gereken Ürünler
- Düşük rating, yüksek yorum veya düşük stok kombinasyonlarını değerlendir.
- Stok artırmadan önce kalite/yorum kontrolü gereken ürünleri ayır.

## Kısa Aksiyon Planı
1. İlk yapılacak stok aksiyonu
2. İkinci aksiyon
3. Üçüncü aksiyon

Kurallar:
- Gereksiz uzun yazma.
- Maksimum 500-600 kelime üret.
- Dashboard’da görünen tüm sayıları tekrar etme.
- low_stock listesi boşsa "kritik stok var" deme, uyarıda bulun sadece.
- Yorum sayısını kesin talep/satış hızı olarak yorumlama; "ilgi sinyali" olarak ifade et.
- Satış hızı verisi yoksa "hızla tükenir" gibi kesin tahmin yapma.
- Düşük ratingli ürünlerde stok artırmadan önce yorum/kalite kontrolü öner.
- Ürün, platform, kategori ve gender verilerini birlikte değerlendir.
- Belirsiz veri varsa tahmin yapma.
- Türkçe yaz.

VERİ:
{to_pretty_json(product_data)}
"""


def build_review_analysis_prompt(review_data: dict) -> str:
    return f"""
Sen deneyimli bir müşteri deneyimi ve e-ticaret yorum analizi uzmanısın.

Aşağıdaki review verilerine göre müşteri memnuniyeti analizi yap.

Çıktı formatı:

🔥 En Kritik Problem
- En önemli müşteri memnuniyetsizliği konusu
- Kısa ve net açıklama

😊 Pozitif İçgörüler
- Güçlü yönleri belirt
- Özellikle yüksek puan alan konuları öne çıkar

⚠️ Riskli Konular
- Düşük puanlı veya tekrar eden problemleri belirt
- Kargo, beden, kalite, renk gibi konuları analiz et
- Sorunların olası etkisini açıkla

💬 En Çok Geçen Konular
- En fazla konuşulan konuları sırala
- Her konu için kısa yorum yap

🛠️ İyileştirme Önerileri
- Her öneri uygulanabilir olsun
- Müşteri şikayetlerinden aksiyon çıkar
- Gereksiz uzun yazma

Kurallar:
- Sentiment, rating distribution ve topic summary verilerini birlikte kullan.
- Dashboard’da görünen tüm sayıları tekrar etme.
- Çok resmi rapor dili kullanma.
- Veride olmayan şeyi uydurma.
- Az sayıda yorum varsa kesin yargılar kurma.
- Tek bir kötü yoruma dayanarak aşırı sert yorum yapma.
- “Kritik başarısızlık”, “alarm verici” gibi aşırı sert ifadeleri dikkatli kullan.
- Güçlü yönleri ve problemleri dengeli değerlendir.
- Yorum konularını ürün, kategori veya gender bağlamında değerlendirmeye çalış.
- Maksimum 500 kelime üret.
- Türkçe yaz.
- Çıktı kısa, okunabilir ve aksiyon odaklı olsun.

REVIEW VERİSİ:
{to_pretty_json(review_data)}
"""


def build_period_summary_prompt(period: str, value: str, data: dict) -> str:
    return f"""
Sen bir e-ticaret performans analisti ve satıcı danışmanısın.

Aşağıdaki tek dönem verisine göre kısa performans raporu üret.

Dönem tipi: {period}
Dönem değeri: {value}

Veri:
{to_pretty_json(data)}

Format:

## Dönem Özeti
2-3 cümlelik kısa özet.

## Öne Çıkan Bulgular
- En fazla 3 madde.

## Dikkat Gerekenler
- En fazla 2 madde.

## Aksiyon Önerileri
1. En önemli aksiyon
2. İkinci aksiyon
3. Üçüncü aksiyon

Kurallar:
- Sadece verilen tek dönem verisini yorumla.
- Veride olmayan şeyi uydurma.
- Sipariş sayısı çok düşükse kesin yargı kurma.
- 1-2 siparişlik dönemlerde "genel performans kötü/iyi" gibi büyük çıkarımlar yapma.
- Gelir 0 ise bunun sebebini tahmin etme; sadece başarılı sipariş olmadığını söyle.
- İade/iptal nedenini bilmiyorsan neden belirtme, yalnızca araştırılmasını öner.
- Weekly/monthly dönemlerde de dönem tamamlanmamış olabilir; kesin trend yorumu yapma.
- Gereksiz selamlama yapma.
- Çok resmi rapor dili kullanma.
- Dashboard’da görünen tüm sayıları tekrar etme.
- Maksimum 300-400 kelime üret.
- Türkçe yaz.
"""