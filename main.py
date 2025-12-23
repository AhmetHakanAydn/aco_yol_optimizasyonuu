"""
Streamlit Ana Uygulama Dosyası
Ant Colony Optimization ile Kargo Rota Optimizasyonu
"""

import streamlit as st
import os
from pathlib import Path
import sys

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.ant_algorithm import AntColonyOptimizer
from core.matrix_utils import DistanceMatrix
from data.coordinates import get_store_locations
from visual.plotting import plot_route_on_map, plot_convergence
from config import Config

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kargo Rota Optimizasyonu - ACO",
    page_icon="🚚",
    layout="wide"
)

# Başlık
st.title("🚚 Kargo Rota Optimizasyonu - Karınca Kolonisi Algoritması")
st.markdown("---")

# Sidebar - Parametreler
st.sidebar.header("⚙️ Algoritma Parametreleri")

# API Key kontrolü
api_key = None

# Önce Streamlit secrets'tan dene
try:
    api_key = st.secrets.get("GOOGLE_MAPS_API_KEY", "")
except:
    pass

# Eğer secrets'ta yoksa .env dosyasından dene
if not api_key:
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")

if not api_key:
    st.error("⚠️ Google Maps API anahtarı bulunamadı! Lütfen .streamlit/secrets.toml veya .env dosyasına API anahtarınızı ekleyin.")
    st.stop()

# Kullanıcı parametreleri
num_ants = st.sidebar.slider("Karınca Sayısı", min_value=10, max_value=100, value=Config.NUM_ANTS, step=10)
num_iterations = st.sidebar.slider("İterasyon Sayısı", min_value=50, max_value=500, value=Config.NUM_ITERATIONS, step=50)
alpha = st.sidebar.slider("α (Feromon Önemi)", min_value=0.1, max_value=5.0, value=Config.ALPHA, step=0.1)
beta = st.sidebar.slider("β (Mesafe Önemi)", min_value=0.1, max_value=5.0, value=Config.BETA, step=0.1)
evaporation_rate = st.sidebar.slider("Buharlaşma Oranı", min_value=0.1, max_value=0.9, value=Config.EVAPORATION_RATE, step=0.05)
pheromone_constant = st.sidebar.slider("Feromon Sabiti (Q)", min_value=1, max_value=1000, value=Config.Q, step=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Bilgiler")
st.sidebar.info(f"""
**Öğrenci:** Ahmet Hakan AYDIN  
**Okul No:** 2012721044  
**GitHub:** [AhmetHakanAydn](https://github.com/AhmetHakanAydn)
""")

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Mağaza Lokasyonları")
    
    # Mağaza lokasyonlarını al
    stores = get_store_locations()
    
    # Mağaza listesini göster
    store_names = [store['name'] for store in stores]
    st.write(f"**Toplam Mağaza Sayısı:** {len(stores)}")
    
    # Mağazaları tablo olarak göster
    import pandas as pd
    df_stores = pd.DataFrame(stores)
    st.dataframe(df_stores[['name', 'address']], use_container_width=True, hide_index=True)

with col2:
    st.subheader("🎯 Optimizasyon")
    
    if st.button("🚀 Optimizasyonu Başlat", type="primary", use_container_width=True):
        with st.spinner("Mesafe matrisi hesaplanıyor..."):
            # Mesafe matrisini oluştur
            distance_matrix = DistanceMatrix(api_key)
            matrix, locations = distance_matrix.get_distance_matrix(stores)
            
            if matrix is None:
                st.error("Mesafe matrisi oluşturulamadı. API anahtarınızı kontrol edin.")
                st.stop()
        
        with st.spinner("ACO algoritması çalıştırılıyor..."):
            # ACO parametrelerini güncelle
            config = Config()
            config.NUM_ANTS = num_ants
            config.NUM_ITERATIONS = num_iterations
            config.ALPHA = alpha
            config.BETA = beta
            config.EVAPORATION_RATE = evaporation_rate
            config.Q = pheromone_constant
            
            # ACO algoritmasını çalıştır
            aco = AntColonyOptimizer(
                distance_matrix=matrix,
                num_ants=config.NUM_ANTS,
                num_iterations=config.NUM_ITERATIONS,
                alpha=config.ALPHA,
                beta=config.BETA,
                evaporation_rate=config.EVAPORATION_RATE,
                q=config.Q
            )
            
            best_route, best_distance, convergence_data = aco.solve()
            
            # Sonuçları session state'e kaydet
            st.session_state['best_route'] = best_route
            st.session_state['best_distance'] = best_distance
            st.session_state['convergence_data'] = convergence_data
            st.session_state['locations'] = locations
            st.session_state['stores'] = stores

# Sonuçları göster
if 'best_route' in st.session_state:
    st.markdown("---")
    st.subheader("📈 Optimizasyon Sonuçları")
    
    best_route = st.session_state['best_route']
    best_distance = st.session_state['best_distance']
    convergence_data = st.session_state['convergence_data']
    locations = st.session_state['locations']
    stores = st.session_state['stores']
    
    # İstatistikler
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("En Kısa Mesafe", f"{best_distance:.2f} km")
    with col2:
        st.metric("Ziyaret Edilen Mağaza", f"{len(best_route)}")
    with col3:
        st.metric("Ortalama Mesafe/Mağaza", f"{best_distance/len(best_route):.2f} km")
    
    # Rota detayları
    st.markdown("### 🗺️ En Kısa Rota")
    route_names = [stores[i]['name'] for i in best_route]
    route_df = pd.DataFrame({
        'Sıra': range(1, len(route_names) + 1),
        'Mağaza Adı': route_names,
        'Adres': [stores[i]['address'] for i in best_route]
    })
    st.dataframe(route_df, use_container_width=True, hide_index=True)
    
    # Harita görselleştirmesi
    st.markdown("### 🗺️ Rota Haritası")
    fig_map = plot_route_on_map(locations, best_route, stores)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Yakınsama grafiği
    st.markdown("### 📊 Algoritma Yakınsama Grafiği")
    fig_conv = plot_convergence(convergence_data)
    st.plotly_chart(fig_conv, use_container_width=True)
    
    # Rota mesafeleri
    st.markdown("### 📏 Adım Adım Mesafeler")
    route_distances = []
    for i in range(len(best_route) - 1):
        from_idx = best_route[i]
        to_idx = best_route[i + 1]
        distance = matrix[from_idx][to_idx]
        route_distances.append({
            'Başlangıç': stores[from_idx]['name'],
            'Varış': stores[to_idx]['name'],
            'Mesafe (km)': f"{distance:.2f}"
        })
    
    # Son noktadan başlangıca dönüş
    from_idx = best_route[-1]
    to_idx = best_route[0]
    distance = matrix[from_idx][to_idx]
    route_distances.append({
        'Başlangıç': stores[from_idx]['name'],
        'Varış': stores[to_idx]['name'] + " (Başlangıç)",
        'Mesafe (km)': f"{distance:.2f}"
    })
    
    st.dataframe(pd.DataFrame(route_distances), use_container_width=True, hide_index=True)

