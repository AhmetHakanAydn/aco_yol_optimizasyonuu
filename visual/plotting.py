"""
Görselleştirme Fonksiyonları
Rota haritası ve yakınsama grafikleri
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple


def plot_route_on_map(
    locations: List[Tuple[float, float]],
    route: List[int],
    stores: List[dict]
) -> go.Figure:
    """
    Rota haritasını çizer.
    
    Args:
        locations: (lat, lng) tuple'larından oluşan liste
        route: Şehir indekslerinden oluşan rota listesi
        stores: Mağaza bilgileri listesi
    
    Returns:
        Plotly figure objesi
    """
    # Rota koordinatlarını al
    route_lats = [locations[i][0] for i in route]
    route_lngs = [locations[i][1] for i in route]
    
    # Başlangıç noktasına geri dön
    route_lats.append(route_lats[0])
    route_lngs.append(route_lngs[0])
    
    # Tüm noktaların koordinatları
    all_lats = [loc[0] for loc in locations]
    all_lngs = [loc[1] for loc in locations]
    
    # Harita oluştur
    fig = go.Figure()
    
    # Rota çizgisi
    fig.add_trace(go.Scattermapbox(
        mode="lines+markers",
        lon=route_lngs,
        lat=route_lats,
        marker=dict(
            size=10,
            color="red",
            symbol="circle"
        ),
        line=dict(
            width=3,
            color="blue"
        ),
        name="Rota",
        hovertemplate="<b>%{text}</b><br>" +
                      "Koordinat: (%{lat:.4f}, %{lon:.4f})<extra></extra>",
        text=[stores[route[i % len(route)]]['name'] for i in range(len(route_lats))]
    ))
    
    # Tüm mağazaları göster
    store_names = [store['name'] for store in stores]
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=all_lngs,
        lat=all_lats,
        marker=dict(
            size=12,
            color="green",
            symbol="circle"
        ),
        name="Mağazalar",
        text=store_names,
        hovertemplate="<b>%{text}</b><br>" +
                      "Koordinat: (%{lat:.4f}, %{lon:.4f})<extra></extra>"
    ))
    
    # Harita ayarları
    fig.update_layout(
        title="En Kısa Rota Haritası",
        mapbox=dict(
            style="open-street-map",
            center=dict(
                lat=sum(all_lats) / len(all_lats),
                lon=sum(all_lngs) / len(all_lngs)
            ),
            zoom=12
        ),
        height=600,
        showlegend=True,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig


def plot_convergence(convergence_data: List[Tuple[int, float]]) -> go.Figure:
    """
    Algoritmanın yakınsama grafiğini çizer.
    
    Args:
        convergence_data: (iterasyon, mesafe) tuple'larından oluşan liste
    
    Returns:
        Plotly figure objesi
    """
    iterations = [data[0] for data in convergence_data]
    distances = [data[1] for data in convergence_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=iterations,
        y=distances,
        mode='lines+markers',
        name='En İyi Mesafe',
        line=dict(color='blue', width=2),
        marker=dict(size=5)
    ))
    
    fig.update_layout(
        title="Algoritma Yakınsama Grafiği",
        xaxis_title="İterasyon",
        yaxis_title="Mesafe (km)",
        height=400,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

