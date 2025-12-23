"""
Mesafe Matrisi Yardımcı Fonksiyonları
Google Maps API kullanarak mesafe matrisi oluşturma
"""

import googlemaps
import numpy as np
from typing import List, Dict, Tuple, Optional


class DistanceMatrix:
    """Google Maps API kullanarak mesafe matrisi oluşturan sınıf"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: Google Maps API anahtarı
        """
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
    
    def get_distance_matrix(self, stores: List[Dict]) -> Tuple[Optional[np.ndarray], List[Tuple[float, float]]]:
        """
        Mağazalar arası mesafe matrisini oluşturur.
        
        Args:
            stores: Mağaza bilgilerini içeren liste (her eleman 'lat' ve 'lng' içermeli)
        
        Returns:
            Tuple: (mesafe_matrisi, lokasyon_listesi)
                - mesafe_matrisi: numpy array (km cinsinden)
                - lokasyon_listesi: (lat, lng) tuple'larından oluşan liste
        """
        n = len(stores)
        locations = [(store['lat'], store['lng']) for store in stores]
        distance_matrix = np.zeros((n, n))
        
        try:
            # Google Maps Distance Matrix API kullan
            origins = [f"{loc[0]},{loc[1]}" for loc in locations]
            destinations = origins.copy()
            
            # API çağrısı (tek seferde tüm matrisi al)
            result = self.gmaps.distance_matrix(
                origins=origins,
                destinations=destinations,
                mode="driving",
                units="metric"
            )
            
            # Sonuçları matrise dönüştür
            for i, row in enumerate(result['rows']):
                for j, element in enumerate(row['elements']):
                    if element['status'] == 'OK':
                        # Mesafeyi km cinsinden al
                        distance_km = element['distance']['value'] / 1000.0
                        distance_matrix[i][j] = distance_km
                    else:
                        # Hata durumunda Haversine formülü kullan
                        distance_matrix[i][j] = self._haversine_distance(
                            locations[i], locations[j]
                        )
            
            return distance_matrix, locations
            
        except Exception as e:
            # API hatası durumunda Haversine formülü kullan
            print(f"API hatası: {e}. Haversine formülü kullanılıyor...")
            for i in range(n):
                for j in range(n):
                    if i == j:
                        distance_matrix[i][j] = 0
                    else:
                        distance_matrix[i][j] = self._haversine_distance(
                            locations[i], locations[j]
                        )
            
            return distance_matrix, locations
    
    def _haversine_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        İki nokta arasındaki Haversine mesafesini hesaplar (km).
        Bu, düz çizgi mesafesidir, gerçek yol mesafesi değildir.
        
        Args:
            point1: (lat, lng) tuple
            point2: (lat, lng) tuple
        
        Returns:
            Mesafe (km)
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Dünya yarıçapı (km)
        
        lat1, lon1 = radians(point1[0]), radians(point1[1])
        lat2, lon2 = radians(point2[0]), radians(point2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        distance = R * c
        return distance

