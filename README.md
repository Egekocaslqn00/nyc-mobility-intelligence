# NYC Urban Mobility Intelligence Platform 🚖

**[English Below]**

## 🇹🇷 Proje Hakkında (Turkish)

**Kapsamlı NYC Taksi ve Rideshare Veri Analizi & Tahmin Sistemi**

Bu proje, New York City'nin karmaşık ulaşım ağını anlamak, tahminlemek ve optimize etmek için geliştirilmiş uçtan uca bir veri bilimi projesidir. **~1 Milyon satırlık** gerçek dünya verisini (NYC TLC) kullanarak, talep tahmini, pazar analizi ve sürücü optimizasyonu yapan yapay zeka modelleri içerir.

### 🌟 Projenin Temel Özellikleri (Ne İşe Yarar?)

Bu proje 3 temel problemi çözer:

1.  **Geleceği Görür (Talep Tahmini):**
    *   "Yarın saat 18:00'de Manhattan'da kaç araca ihtiyaç olacak?" sorusuna **%90 doğrulukla** cevap verir.
    *   Şirketlerin araçlarını boş gezdirmesini önler, tam ihtiyaç olan yere yönlendirir.

2.  **Kazancı Artırır (Sürücü Optimizasyonu):**
    *   Sürücülere "Şu an havalimanına gidersen %20 daha fazla kazanırsın" veya "Bu bölgedeki yolcular daha yüksek bahşiş veriyor" gibi akıllı öneriler sunar.
    *   Bahşiş tahmin modeli ile geliri maksimize eder.

3.  **Süreyi Hesaplar (Müşteri Memnuniyeti):**
    *   Trafik ve mesafe verilerine bakarak bir yolculuğun tam olarak kaç dakika süreceğini hassas bir şekilde (**2.98 dakika hata payıyla**) hesaplar.

### 🚀 Otomatik Veri İndirme Sistemi (Smart Downloader)

Bu proje, kullanım kolaylığı için **"Akıllı İndirici"** özelliğine sahiptir.
GitHub deposunda 1GB'lık veri dosyalarını göremezsiniz (GitHub limitleri nedeniyle). Ancak endişelenmeyin!

*   **Nasıl Çalışır?** Siz sadece kodu çalıştırırsınız (`python src/main_analysis.py`).
*   **Ne Yapar?** Kod, gerekli veri dosyalarının eksik olduğunu fark eder ve **otomatik olarak** resmi kaynaklardan (NYC.gov) 1GB veriyi indirip kurar.
*   **Sizin Yapmanız Gereken:** Sadece "Başlat" tuşuna basmak! Manuel dosya indirme derdi yoktur.

### 📚 Kullanılan Kütüphaneler ve Amaçları

Bu projede her bir kütüphane, belirli bir teknik ihtiyacı karşılamak için özenle seçilmiştir:

| Kütüphane | Ne İçin Kullanıldı? | Neden Seçildi? |
| :--- | :--- | :--- |
| **Pandas** | Veri Manipülasyonu | 1 milyon satırlık veriyi filtrelemek, temizlemek ve dönüştürmek için endüstri standardı olduğu için. |
| **PyArrow** | Veri Okuma (Parquet) | Büyük veri setlerini (Parquet formatı) CSV'ye göre 10 kat daha hızlı ve bellek dostu okumak için. |
| **Scikit-learn** | Makine Öğrenmesi | Veriyi eğitim/test olarak bölmek (train_test_split) ve Random Forest algoritmasını uygulamak için. |
| **XGBoost** | İleri Seviye ML | Bahşiş ve süre tahmini gibi karmaşık problemlerde, yüksek hız ve doğruluk (Gradient Boosting) sağladığı için. |
| **Joblib** | Model Kaydetme | Eğitilen modelleri diske kaydetmek ve tekrar tekrar eğitmek zorunda kalmadan kullanabilmek için. |
| **Requests** | Veri İndirme | 1GB'lık veri setlerini kod içinden otomatik olarak indirmek (Smart Downloader) için. |

### 🛠️ Adım Adım Nasıl Çalıştırılır?

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

## 🇬🇧 About the Project (English)

**Comprehensive NYC Taxi & Rideshare Data Analysis & Prediction System**

This is an end-to-end data science project designed to understand, predict, and optimize New York City's complex transportation network. Using **~1 Million rows** of real-world data (NYC TLC), it features AI models for demand prediction, market analysis, and driver optimization.

### 🌟 Key Features (What does it do?)

This project solves 3 main problems:

1.  **Predicts the Future (Demand Prediction):**
    *   Answers "How many cars will be needed in Manhattan tomorrow at 6:00 PM?" with **90% accuracy**.
    *   Prevents empty cruising and directs fleets exactly where they are needed.

2.  **Maximizes Revenue (Driver Optimization):**
    *   Provides smart suggestions like "Go to the airport now to earn 20% more" or "Passengers in this zone tip higher."
    *   Optimizes income via the Tip Prediction Model.

3.  **Estimates Duration (Customer Satisfaction):**
    *   Calculates exactly how many minutes a trip will take based on traffic and distance with high precision (**2.98 minutes margin of error**).

### 🚀 Automatic Data Download System (Smart Downloader)

This project features a **"Smart Downloader"** for ease of use.
You won't see the 1GB data files in the GitHub repo (due to limits). But don't worry!

*   **How it works:** You simply run the code (`python src/main_analysis.py`).
*   **What it does:** The code detects missing data files and **automatically downloads** the 1GB dataset from official sources (NYC.gov) and sets it up.
*   **What you need to do:** Just press "Start"! No manual file downloading required.

### 📚 Libraries Used & Their Purpose

Each library in this project was carefully selected to meet specific technical needs:

| Library | Used For | Why Selected? |
| :--- | :--- | :--- |
| **Pandas** | Data Manipulation | Industry standard for filtering, cleaning, and transforming 1 million rows of data. |
| **PyArrow** | Data Reading (Parquet) | To read large datasets (Parquet format) 10x faster and more memory-efficiently than CSV. |
| **Scikit-learn** | Machine Learning | For splitting data (train_test_split) and implementing the Random Forest algorithm. |
| **XGBoost** | Advanced ML | For high speed and accuracy (Gradient Boosting) in complex problems like tip and duration prediction. |
| **Joblib** | Model Saving | To save trained models to disk so they can be reused without retraining. |
| **Requests** | Data Downloading | To automatically download 1GB datasets within the code (Smart Downloader). |

### 🛠️ Step-by-Step: How to Run?

Follow these 3 steps to run the project on your machine:

**Step 1: Clone the Project**
Open your terminal or command line:
```bash
git clone https://github.com/Egekocaslqn00/nyc-mobility-intelligence.git
cd nyc-mobility-intelligence
```

**Step 2: Install Requirements**
```bash
pip install -r requirements.txt
```

**Step 3: Start Analysis (One Command)**
Run the following command and sit back. The code will download data, train models, and generate results automatically.
```bash
python src/main_analysis.py
```

---

## 📊 Business Impact & Results

*   **Demand Prediction Accuracy:** 90% (R²: 0.899)
*   **Revenue Increase Potential:** ~20% via optimized routing
*   **Duration Prediction Error:** Only ~3 minutes (MAE)
