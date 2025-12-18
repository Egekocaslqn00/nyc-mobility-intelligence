# NYC Urban Mobility Intelligence Platform 🚖

**Kapsamlı NYC Taksi ve Rideshare Veri Analizi & Tahmin Sistemi**

> **[Click here for English README](README.md)**

Bu proje, New York City'nin karmaşık ulaşım ağını anlamak, tahminlemek ve optimize etmek için geliştirilmiş uçtan uca bir veri bilimi projesidir. **~1 Milyon satırlık** gerçek dünya verisini (NYC TLC) kullanarak, talep tahmini, pazar analizi ve sürücü optimizasyonu yapan yapay zeka modelleri içerir.

---

## 🌟 Detaylı Proje Kapsamı ve Özellikler

Bu proje, modern bir ulaşım zekası platformunun sahip olması gereken tüm yetenekleri kapsar:

*   **Saatlik/Günlük Talep Tahmini:** Makine öğrenmesi (Random Forest) ile gelecekteki araç ihtiyacını %90 doğrulukla öngörür.
*   **Dış Faktör Analizi:** Hava durumu, tatil günleri ve özel etkinliklerin taksi talebi üzerindeki etkisini analiz eder.
*   **Dinamik Fiyatlandırma Simülasyonu:** Talebin yoğun olduğu saatlerde fiyat değişimlerinin etkisini simüle eder.
*   **Pazar Payı Analizi:** Sarı Taksi ve FHV (Uber/Lyft) arasındaki rekabeti ve pazar payı değişimlerini görselleştirir.
*   **Bölgesel Tercih Haritası:** Hangi mahallelerde Uber'in, hangilerinde Sarı Taksi'nin tercih edildiğini ortaya çıkarır.
*   **Sürücü Gelir Optimizasyonu:** Sürücüler için en karlı bekleme noktalarını (hotspots) ve saatleri belirler.
*   **Rota Optimizasyonu:** Trafik verilerine dayanarak en hızlı ve verimli rotaları önerir.
*   **Gerçek Zamanlı Trafik Tahmini:** Geçmiş verilerden yola çıkarak anlık trafik yoğunluğunu tahmin eder.
*   **Hassas Süre Tahmini:** A noktasından B noktasına varış süresini 3 dakika hata payıyla hesaplar.
*   **Congestion Pricing Analizi:** Şehir merkezine giriş ücretlerinin (2025 vizyonu) trafiğe olası etkilerini modeller.
*   **Havalimanı Transfer Stratejisi:** Uçuş saatlerine göre havalimanı yolcu talebini tahmin eder ve fiyat optimizasyonu yapar.
*   **Sosyoekonomik Analiz:** Gelir seviyesi ve turizm yoğunluğu ile taksi kullanımı arasındaki korelasyonu inceler.
*   **Gece Hayatı Analizi:** Gece saatlerinde (22:00-04:00) eğlence merkezlerindeki hareketliliği haritalandırır.
*   **Hafta İçi vs Hafta Sonu:** İş ve eğlence amaçlı yolculukların karakteristik farklarını ortaya koyar.
*   **Bahşiş Tahmin Modeli:** Mesafe, saat, bölge ve ödeme tipine göre bahşiş miktarını tahmin eder (Sürücü dostu özellik).
*   **Etkinlik Bazlı Talep:** Konser, maç gibi büyük etkinliklerin taksi talebinde yarattığı ani artışları (spike) öngörür.

---

## 🌟 Projenin Temel İşlevleri (Adım Adım)

Bu proje, bir ulaşım şirketinin veya şehir planlamacısının ihtiyaç duyacağı şu kritik yeteneklere sahiptir:

### 1. Geleceği Görme (Talep Tahmini)
*   **Ne Yapar?** Yarın, gelecek hafta veya belirli bir saatte Manhattan'da kaç taksiye ihtiyaç olacağını tahmin eder.
*   **Nasıl Çalışır?** Geçmiş verileri analiz ederek saatlik, günlük ve mevsimsel trendleri öğrenir.
*   **Fayda:** Araçların boş gezmesini önler, tam ihtiyaç olan yere yönlendirir. (%90 Doğruluk)

### 2. Kazancı Artırma (Sürücü Optimizasyonu)
*   **Ne Yapar?** Sürücülere "Şu an havalimanına git" veya "Bu bölgedeki yolcular %15 daha fazla bahşiş veriyor" gibi akıllı öneriler sunar.
*   **Nasıl Çalışır?** Bahşiş verilerini ve bölgesel yoğunluğu analiz eder.
*   **Fayda:** Sürücülerin gelirini %20'ye kadar artırma potansiyeli sunar.

### 3. Süre Hesaplama (Müşteri Memnuniyeti)
*   **Ne Yapar?** Bir yolculuğun trafik ve mesafeye göre tam olarak kaç dakika süreceğini hesaplar.
*   **Nasıl Çalışır?** Trafik yoğunluğunu ve yolculuk mesafesini XGBoost algoritması ile işler.
*   **Fayda:** Müşterilere "25 dakika sonra oradasınız" gibi kesin bilgi verir (Hata payı sadece ~3 dakika).

### 4. Otomatik Veri İndirme (Smart Downloader)
*   **Ne Yapar?** 1GB'lık devasa veri setini sizin yerinize indirir ve kurar.
*   **Nasıl Çalışır?** Kodu çalıştırdığınızda eksik dosyaları tespit eder ve NYC.gov sunucularından çeker.
*   **Fayda:** Manuel dosya indirme derdini ortadan kaldırır, tek tuşla çalışır.

---

## 🏆 Somut İş Sonuçları (Business Impact)

*   **Talep Tahmini Doğruluğu:** %90 (R²: 0.899)
*   **Gelir Artış Potansiyeli:** ~%20 (Optimize edilmiş rotalarla)
*   **Süre Tahmini Hatası:** Sadece ~3 dakika (MAE)
*   **Havalimanı Stratejisi:** Ortalama ücreti 18$'dan 53$'a çıkarma fırsatı.

---

## 📚 Kullanılan Kütüphaneler ve Amaçları

Bu projede her bir kütüphane, belirli bir teknik ihtiyacı karşılamak için özenle seçilmiştir:

| Kütüphane | Ne İçin Kullanıldı? | Neden Seçildi? |
| :--- | :--- | :--- |
| **Pandas** | Veri Manipülasyonu | 1 milyon satırlık veriyi filtrelemek, temizlemek ve dönüştürmek için endüstri standardı olduğu için. |
| **PyArrow** | Veri Okuma (Parquet) | Büyük veri setlerini (Parquet formatı) CSV'ye göre 10 kat daha hızlı ve bellek dostu okumak için. |
| **Scikit-learn** | Makine Öğrenmesi | Veriyi eğitim/test olarak bölmek (train_test_split) ve Random Forest algoritmasını uygulamak için. |
| **XGBoost** | İleri Seviye ML | Bahşiş ve süre tahmini gibi karmaşık problemlerde, yüksek hız ve doğruluk (Gradient Boosting) sağladığı için. |
| **Joblib** | Model Kaydetme | Eğitilen modelleri diske kaydetmek ve tekrar tekrar eğitmek zorunda kalmadan kullanabilmek için. |
| **Requests** | Veri İndirme | 1GB'lık veri setlerini kod içinden otomatik olarak indirmek (Smart Downloader) için. |

---

## 🛠️ Adım Adım Nasıl Çalıştırılır?

Projeyi kendi bilgisayarınızda çalıştırmak için şu 3 adımı izleyin:

**Adım 1: Projeyi İndirin**
Terminal veya komut satırını açın:
```bash
git clone https://github.com/Egekocaslqn00/nyc-mobility-intelligence.git
cd nyc-mobility-intelligence
```

**Adım 2: Gerekli Kütüphaneleri Yükleyin**
```bash
pip install -r requirements.txt
```

**Adım 3: Analizi Başlatın (Tek Komut)**
Aşağıdaki komutu yazın ve arkanıza yaslanın. Kod verileri indirecek, modelleri eğitecek ve sonuçları üretecektir.
```bash
python src/main_analysis.py
```

---

## 📊 Görseller

![Hourly Demand Analysis](visualizations/images/hourly_demand.png)
![Market Share](visualizations/images/market_share.png)
