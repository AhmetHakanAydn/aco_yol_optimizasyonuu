"""
Karınca Kolonisi Optimizasyonu (ACO) Algoritması
Traveling Salesman Problem (TSP) için ACO implementasyonu
"""

import numpy as np
import random
from typing import List, Tuple, Optional
from config import Config


class AntColonyOptimizer:
    """
    Ant Colony Optimization algoritması ile TSP çözücü
    """
    
    def __init__(
        self,
        distance_matrix: np.ndarray,
        num_ants: int = 50,
        num_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation_rate: float = 0.5,
        q: float = 100
    ):
        """
        Args:
            distance_matrix: Mesafe matrisi (n x n numpy array)
            num_ants: Karınca sayısı
            num_iterations: İterasyon sayısı
            alpha: Feromon önemi parametresi
            beta: Mesafe önemi parametresi
            evaporation_rate: Feromon buharlaşma oranı (0-1 arası)
            q: Feromon sabiti
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        
        # Feromon matrisini başlat
        self.pheromone_matrix = np.ones((self.num_cities, self.num_cities)) * Config.INITIAL_PHEROMONE
        
        # Mesafe matrisinde 0 olan değerleri küçük bir sayıyla değiştir (bölme hatası önlemek için)
        self.distance_matrix = np.where(
            self.distance_matrix == 0,
            0.0001,
            self.distance_matrix
        )
        
        # Seed ayarla (tekrarlanabilirlik için)
        if Config.RANDOM_SEED is not None:
            np.random.seed(Config.RANDOM_SEED)
            random.seed(Config.RANDOM_SEED)
    
    def _calculate_probability(self, current_city: int, unvisited_cities: List[int]) -> np.ndarray:
        """
        Bir karıncanın bir sonraki şehri seçme olasılıklarını hesaplar.
        
        Args:
            current_city: Mevcut şehir indeksi
            unvisited_cities: Ziyaret edilmemiş şehirler listesi
        
        Returns:
            Olasılık dizisi
        """
        probabilities = np.zeros(len(unvisited_cities))
        
        for idx, city in enumerate(unvisited_cities):
            # Feromon değeri
            pheromone = self.pheromone_matrix[current_city][city] ** self.alpha
            
            # Mesafe (heuristic değer)
            distance = self.distance_matrix[current_city][city]
            heuristic = (1.0 / distance) ** self.beta
            
            # Toplam olasılık
            probabilities[idx] = pheromone * heuristic
        
        # Normalize et
        total = probabilities.sum()
        if total > 0:
            probabilities = probabilities / total
        else:
            # Eşit olasılık dağılımı
            probabilities = np.ones(len(unvisited_cities)) / len(unvisited_cities)
        
        return probabilities
    
    def _construct_solution(self) -> Tuple[List[int], float]:
        """
        Bir karınca için çözüm (rota) oluşturur.
        
        Returns:
            (rota, toplam_mesafe) tuple
        """
        # Rastgele başlangıç şehri
        start_city = random.randint(0, self.num_cities - 1)
        route = [start_city]
        unvisited = [i for i in range(self.num_cities) if i != start_city]
        
        # Tüm şehirleri ziyaret et
        current_city = start_city
        total_distance = 0.0
        
        while unvisited:
            # Olasılıkları hesapla
            probabilities = self._calculate_probability(current_city, unvisited)
            
            # Olasılıklara göre bir sonraki şehri seç
            next_city_idx = np.random.choice(len(unvisited), p=probabilities)
            next_city = unvisited[next_city_idx]
            
            # Rota ve mesafeyi güncelle
            route.append(next_city)
            total_distance += self.distance_matrix[current_city][next_city]
            
            # Güncellemeler
            current_city = next_city
            unvisited.remove(next_city)
        
        # Başlangıç şehrine dön
        total_distance += self.distance_matrix[route[-1]][route[0]]
        
        return route, total_distance
    
    def _update_pheromone(self, routes: List[List[int]], distances: List[float]):
        """
        Feromon matrisini günceller.
        
        Args:
            routes: Tüm karıncaların rotaları
            distances: Tüm karıncaların mesafeleri
        """
        # Buharlaşma
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        
        # Her karınca için feromon ekle
        for route, distance in zip(routes, distances):
            pheromone_deposit = self.q / distance
            
            for i in range(len(route) - 1):
                from_city = route[i]
                to_city = route[i + 1]
                self.pheromone_matrix[from_city][to_city] += pheromone_deposit
            
            # Son şehirden başlangıca
            self.pheromone_matrix[route[-1]][route[0]] += pheromone_deposit
    
    def solve(self) -> Tuple[List[int], float, List[Tuple[int, float]]]:
        """
        ACO algoritmasını çalıştırır ve en iyi çözümü döndürür.
        
        Returns:
            (en_iyi_rota, en_iyi_mesafe, yakınsama_verisi) tuple
                - en_iyi_rota: En kısa rotayı temsil eden şehir indeksleri listesi
                - en_iyi_mesafe: En kısa mesafe (km)
                - yakınsama_verisi: Her iterasyondaki en iyi mesafe listesi
        """
        best_route = None
        best_distance = float('inf')
        convergence_data = []
        
        # İterasyonlar
        for iteration in range(self.num_iterations):
            routes = []
            distances = []
            
            # Her karınca için çözüm oluştur
            for ant in range(self.num_ants):
                route, distance = self._construct_solution()
                routes.append(route)
                distances.append(distance)
                
                # En iyi çözümü güncelle
                if distance < best_distance:
                    best_distance = distance
                    best_route = route.copy()
            
            # Feromon güncelle
            self._update_pheromone(routes, distances)
            
            # Yakınsama verisini kaydet
            convergence_data.append((iteration + 1, best_distance))
            
            # İlerleme bilgisi (isteğe bağlı)
            if (iteration + 1) % 10 == 0:
                print(f"İterasyon {iteration + 1}/{self.num_iterations}, En iyi mesafe: {best_distance:.2f} km")
        
        return best_route, best_distance, convergence_data

