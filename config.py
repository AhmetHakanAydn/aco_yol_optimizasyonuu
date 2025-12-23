"""
ACO Parametre Ayarları
"""

class Config:
    """Ant Colony Optimization algoritması için varsayılan parametreler"""
    
    # Algoritma parametreleri
    NUM_ANTS = 50  # Karınca sayısı
    NUM_ITERATIONS = 100  # İterasyon sayısı
    ALPHA = 1.0  # Feromon önemi (pheromone importance)
    BETA = 2.0  # Mesafe önemi (distance importance)
    EVAPORATION_RATE = 0.5  # Feromon buharlaşma oranı
    Q = 100  # Feromon sabiti (pheromone constant)
    
    # Başlangıç feromon değeri
    INITIAL_PHEROMONE = 1.0
    
    # Rastgele sayı üreteci seed (tekrarlanabilirlik için)
    RANDOM_SEED = None  # None ise her çalıştırmada farklı sonuçlar

