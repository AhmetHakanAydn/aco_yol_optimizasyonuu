"""
Haversine Formülü ile Mesafe Hesaplama
Yedek mesafe hesaplama fonksiyonu
"""

from math import radians, sin, cos, sqrt, atan2
from typing import Tuple


def haversine_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    İki koordinat noktası arasındaki Haversine mesafesini hesaplar.
    
    Args:
        point1: (enlem, boylam) tuple
        point2: (enlem, boylam) tuple
    
    Returns:
        Mesafe (kilometre cinsinden)
    """
    R = 6371  # Dünya yarıçapı (km)
    
    lat1, lon1 = radians(point1[0]), radians(point1[1])
    lat2, lon2 = radians(point2[0]), radians(point2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance

