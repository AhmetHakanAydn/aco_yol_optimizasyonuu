# 🚚 Kargo Rota Optimizasyonu - Karınca Kolonisi Algoritması (ACO)

## 📋 Proje Hakkında

Bu proje, Antalya'nın Muratpaşa ilçesindeki bir kargo firmasının 20 farklı mağazaya günde 1 kez uğraması gereken durumda, en kısa rotayı bulmak için **Karınca Kolonisi Optimizasyonu (Ant Colony Optimization - ACO)** algoritmasını kullanmaktadır.

Proje, **Streamlit** web arayüzü ve **Google Maps API** kullanılarak geliştirilmiştir.

## 👤 Öğrenci Bilgileri

- **Ad Soyad:** Ahmet Hakan AYDIN
- **Okul Numarası:** 2012721044
- **GitHub:** [AhmetHakanAydn](https://github.com/AhmetHakanAydn)

## 🎯 Proje Özellikleri

- ✅ Google Maps API ile gerçek mesafe hesaplama
- ✅ Ant Colony Optimization (ACO) algoritması implementasyonu
- ✅ Streamlit ile interaktif web arayüzü
- ✅ Harita üzerinde rota görselleştirmesi
- ✅ Algoritma yakınsama grafiği
- ✅ Kullanıcı tarafından ayarlanabilir parametreler
- ✅ Güvenli API anahtarı yönetimi

## 📁 Proje Yapısı

```
aco_ilac_rutasi/
├── main.py                 # Streamlit ana uygulama dosyası
├── config.py              # ACO parametre ayarları
├── requirements.txt        # Gerekli kütüphaneler
├── .env                   # API anahtarı (opsiyonel)
├── README.md              # Proje dokümantasyonu
├── data/
│   └── coordinates.py     # Mağaza lokasyon verileri
├── core/
│   ├── haversine.py       # Haversine mesafe hesaplama
│   ├── matrix_utils.py    # Mesafe matrisi oluşturma
│   └── ant_algorithm.py  # ACO algoritması
├── visual/
│   └── plotting.py        # Görselleştirme fonksiyonları
└── .streamlit/
    └── secrets.toml       # Streamlit API anahtarı (gizli)
```

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.8 veya üzeri
- Google Maps API anahtarı ([Nasıl alınır?](https://developers.google.com/maps/documentation/distance-matrix/get-api-key))

### 2. Projeyi İndirin

```bash
git clone https://github.com/AhmetHakanAydn/aco_ilac_rutasi.git
cd aco_ilac_rutasi
```

### 3. Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 4. Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 5. API Anahtarını Yapılandırın

**Seçenek 1: Streamlit secrets.toml (Önerilen)**

`.streamlit/secrets.toml.example` dosyasını `.streamlit/secrets.toml` olarak kopyalayın:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Ardından `secrets.toml` dosyasını düzenleyip API anahtarınızı ekleyin:

```toml
GOOGLE_MAPS_API_KEY = "BURAYA_API_ANAHTARINIZI_YAZIN"
```

**Seçenek 2: .env dosyası**

Proje kök dizininde `.env` dosyası oluşturun:

```
GOOGLE_MAPS_API_KEY=BURAYA_API_ANAHTARINIZI_YAZIN
```

## 🎮 Kullanım

### Uygulamayı Başlatın

```bash
streamlit run main.py
```

Tarayıcınızda otomatik olarak açılacaktır (genellikle `http://localhost:8501`).

### Arayüz Kullanımı

1. **Parametreleri Ayarlayın:** Sol taraftaki sidebar'dan ACO algoritması parametrelerini ayarlayın:
   - Karınca Sayısı
   - İterasyon Sayısı
   - α (Feromon Önemi)
   - β (Mesafe Önemi)
   - Buharlaşma Oranı
   - Feromon Sabiti (Q)

2. **Optimizasyonu Başlatın:** "🚀 Optimizasyonu Başlat" butonuna tıklayın.

3. **Sonuçları İnceleyin:**
   - En kısa mesafe ve istatistikler
   - Rota detayları (mağaza sırası)
   - Harita üzerinde görselleştirilmiş rota
   - Algoritma yakınsama grafiği
   - Adım adım mesafe bilgileri

## 🔧 ACO Algoritması Parametreleri

- **Karınca Sayısı (num_ants):** Algoritmada kullanılan karınca sayısı. Daha fazla karınca, daha iyi sonuçlar verebilir ancak hesaplama süresini artırır.
- **İterasyon Sayısı (num_iterations):** Algoritmanın kaç kez çalıştırılacağı. Daha fazla iterasyon, daha iyi sonuçlar verebilir.
- **α (Alpha):** Feromon önemi parametresi. Yüksek değerler, feromon izlerine daha fazla önem verir.
- **β (Beta):** Mesafe önemi parametresi. Yüksek değerler, kısa mesafelere daha fazla önem verir.
- **Buharlaşma Oranı (evaporation_rate):** Feromonların ne kadar hızlı buharlaşacağı. Yüksek değerler, eski izlerin daha hızlı kaybolmasına neden olur.
- **Feromon Sabiti (Q):** Her karıncanın bıraktığı feromon miktarını belirler.

## 🗺️ Mağaza Lokasyonları

Proje, Muratpaşa, Antalya'daki 20 farklı mağaza lokasyonunu içermektedir. Bu lokasyonlar `data/coordinates.py` dosyasında tanımlanmıştır ve kolayca güncellenebilir.

## 🔒 Güvenlik

- API anahtarları `.gitignore` dosyasına eklenmiştir ve GitHub'a yüklenmez.
- Hassas bilgiler `.env` veya `.streamlit/secrets.toml` dosyalarında saklanmalıdır.
- Bu dosyalar asla gerçek API anahtarlarıyla commit edilmemelidir.

## 📊 Algoritma Açıklaması

**Ant Colony Optimization (ACO)**, doğadaki karıncaların yiyecek arama davranışından esinlenen bir meta-sezgisel optimizasyon algoritmasıdır. Algoritma şu adımları takip eder:

1. **Başlangıç:** Her karınca rastgele bir başlangıç noktasından başlar.
2. **Rota Oluşturma:** Her karınca, feromon izleri ve mesafe bilgisine dayanarak bir sonraki şehri seçer.
3. **Feromon Güncelleme:** Karıncalar, buldukları rotaya göre feromon bırakır. Daha kısa rotalar daha fazla feromon alır.
4. **Buharlaşma:** Feromonlar zamanla buharlaşır, böylece eski çözümler unutulur.
5. **Yakınsama:** Algoritma, belirli bir iterasyon sayısına ulaşana kadar devam eder.

## 🛠️ Teknolojiler

- **Python 3.8+**
- **Streamlit:** Web arayüzü
- **Google Maps API:** Mesafe hesaplama
- **NumPy:** Matematiksel işlemler
- **Plotly:** Görselleştirme
- **Pandas:** Veri işleme

## 📝 Lisans

Bu proje eğitim amaçlıdır ve öğrenci ödevi kapsamında geliştirilmiştir.

## 🙏 Teşekkürler

- Google Maps API dokümantasyonu
- Streamlit topluluğu
- ACO algoritması literatürü

---

**Not:** Bu proje, akademik bir ödev kapsamında geliştirilmiştir. Kodlar öğrenci tarafından özgün olarak yazılmıştır.

