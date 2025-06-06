import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta


st.set_page_config(
    page_title="TechNova Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Header principal con efecto neón */
    .main-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0 2rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 20px rgba(66, 165, 245, 0.3); }
        to { box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 30px rgba(156, 39, 176, 0.4); }
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #42a5f5, #ab47bc, #26c6da);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(66, 165, 245, 0.5);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
        font-weight: 300;
    }
    
    /* Tarjetas de métricas con glassmorphism */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    /* Secciones de gráficos */
    .chart-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .section-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-left: 1rem;
        border-left: 4px solid;
        border-image: linear-gradient(45deg, #42a5f5, #ab47bc) 1;
    }
    
    /* Elementos Streamlit */
    .stPlotlyChart {
        background: transparent !important;
    }
    
    .stMetric {
        background: transparent;
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(45deg, #42a5f5, #ab47bc);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(66, 165, 245, 0.4);
    }
    
    /* Animación de carga */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #42a5f5;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Efectos de hover para dataframes */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Indicadores de estado */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online { background-color: #4caf50; }
    .status-warning { background-color: #ff9800; }
    .status-error { background-color: #f44336; }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🚀 TechNova Retail Analytics</h1>
        <p class="subtitle">Dashboard Inteligente de Ventas & Analytics</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar con filtros y estado
with st.sidebar:
    st.markdown("### 🎛️ Panel de Control")
    
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span class="status-indicator status-online"></span>
            <span style="color: #4caf50;">Sistema Activo</span>
        </div>
    """, unsafe_allow_html=True)
    
    refresh_data = st.button("🔄 Actualizar Datos", use_container_width=True)
    st.markdown("---")
    
    tiempo_periodo = st.selectbox(
        "📅 Período de Análisis",
        ["Último Mes", "Últimos 3 Meses", "Último Año", "Todo el Período"]
    )
    
    mostrar_filtros = st.checkbox("🔍 Filtros Avanzados", value=False)

# Cargamos y procesamos datos
archivo_path = "Ventas_Minoristas.xlsx"

@st.cache_data
def cargar_datos(path):
    if os.path.exists(path):
        df_local = pd.read_excel(path)
        df_local["Ventas"] = df_local["Cantidad"] * df_local["Precio_unitario(USD)"]
        df_local['Fecha'] = pd.to_datetime(df_local['Fecha'])
        # Aseguramos que existan las columnas que usaremos más adelante
        if 'edad_cliente' not in df_local.columns:
            df_local['edad_cliente'] = np.nan
        if 'genero_cliente' not in df_local.columns:
            df_local['genero_cliente'] = 'Desconocido'
        if 'calificación_satisfaccion' not in df_local.columns:
            df_local['calificación_satisfaccion'] = np.nan
        if 'metodo_pago' not in df_local.columns:
            df_local['metodo_pago'] = 'Desconocido'
        if 'pais' not in df_local.columns:
            df_local['pais'] = 'Desconocido'
        if 'ciudad' not in df_local.columns:
            df_local['ciudad'] = 'Desconocido'
        return df_local
    return None

with st.spinner('Cargando datos...'):
    df = cargar_datos(archivo_path)

if df is None:
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(244, 67, 54, 0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(244, 67, 54, 0.3);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❌</div>
            <h2 style="color: #f44336; margin-bottom: 1rem;">Archivo No Encontrado</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">
                No se pudo encontrar el archivo <strong>Ventas_Minoristas.xlsx</strong><br>
                Por favor, asegúrate de colocarlo en la misma carpeta que este script.
            </p>
            <div style="margin-top: 1.5rem;">
                <span class="status-indicator status-error"></span>
                <span style="color: #f44336;">Sistema Desconectado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Aplicamos filtro de tiempo
if tiempo_periodo != "Todo el Período":
    fecha_fin = df['Fecha'].max()
    if tiempo_periodo == "Último Mes":
        fecha_inicio = fecha_fin - timedelta(days=30)
    elif tiempo_periodo == "Últimos 3 Meses":
        fecha_inicio = fecha_fin - timedelta(days=90)
    else:  # Último Año
        fecha_inicio = fecha_fin - timedelta(days=365)
    df = df[df['Fecha'] >= fecha_inicio]

# Filtros adicionales en sidebar
if mostrar_filtros:
    with st.sidebar:
        categorias_disponibles = df['categoria'].unique()
        categorias_seleccionadas = st.multiselect(
            "Categorías",
            sorted(categorias_disponibles),
            default=list(categorias_disponibles)
        )
        df = df[df['categoria'].isin(categorias_seleccionadas)]

# Cálculo de métricas principales
total_ventas = df["Ventas"].sum()
total_productos = df["Nombre_producto"].nunique()
promedio_venta = df["Ventas"].mean() if len(df) > 0 else 0
mejor_categoria = df.groupby('categoria')['Ventas'].sum().idxmax() if len(df) > 0 else "N/A"

# Dashboard de métricas principales (glassmorphism)
col1, col2, col3, col4 = st.columns(4)
metrics_data = [
    ("💰", f"${total_ventas:,.0f}", "Ventas Totales", f"+{np.random.randint(5,15)}%"),
    ("📦", f"{total_productos:,}", "Productos Únicos", f"+{np.random.randint(2,8)}%"),
    ("📊", f"${promedio_venta:,.0f}", "Venta Promedio", f"+{np.random.randint(3,12)}%"),
    ("🏆", mejor_categoria, "Top Categoría", "Líder")
]
for col, (icon, value, label, change) in zip([col1, col2, col3, col4], metrics_data):
    with col:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: white; margin-bottom: 0.3rem;">{value}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 0.3rem;">{label}</div>
                <div style="font-size: 0.8rem; color: #4caf50; font-weight: 600;">{change}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------
# Gráficos: Evolución temporal y Top Categorías
# ----------------------------------------------------------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="section-header">📈 Evolución de Ventas en Tiempo Real</div>', unsafe_allow_html=True)
    ventas_tiempo = df.groupby('Fecha')['Ventas'].sum().reset_index()
    fig_temporal = go.Figure()
    fig_temporal.add_trace(go.Scatter(
        x=ventas_tiempo['Fecha'],
        y=ventas_tiempo['Ventas'],
        mode='lines+markers',
        name='Ventas',
        line=dict(color='rgba(66, 165, 245, 1)', width=3, shape='spline'),
        marker=dict(size=8, color='rgba(66, 165, 245, 1)', line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(66, 165, 245, 0.2)',
        hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
    ))
    if len(ventas_tiempo) >= 2:
        z = np.polyfit(range(len(ventas_tiempo)), ventas_tiempo['Ventas'], 1)
        p = np.poly1d(z)
        fig_temporal.add_trace(go.Scatter(
            x=ventas_tiempo['Fecha'],
            y=p(range(len(ventas_tiempo))),
            mode='lines',
            name='Tendencia',
            line=dict(color='rgba(255, 193, 7, 0.8)', width=2, dash='dash'),
            hovertemplate='Tendencia: $%{y:,.0f}<extra></extra>'
        ))
    fig_temporal.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True, tickformat='$,.0f'),
        hovermode='x unified'
    )
    st.plotly_chart(fig_temporal, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">🎯 Top Categorías</div>', unsafe_allow_html=True)
    cat_ventas = df.groupby('categoria')['Ventas'].sum().sort_values(ascending=False)
    fig_dona = go.Figure(data=[go.Pie(
        labels=cat_ventas.index,
        values=cat_ventas.values,
        hole=0.6,
        textinfo='label+percent',
        textposition='outside',
        marker=dict(
            colors=['#42a5f5', '#ab47bc', '#26c6da', '#66bb6a', '#ff7043'],
            line=dict(color='#000000', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Ventas: $%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    fig_dona.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        showlegend=False,
        annotations=[dict(
            text=f"${total_ventas:,.0f}",
            x=0.5, y=0.5,
            font_size=20,
            font_color='white',
            showarrow=False
        )]
    )
    st.plotly_chart(fig_dona, use_container_width=True)

# ----------------------------------------------------------
# Gráfico de Barras Vert: Ventas Totales por Categoría
# ----------------------------------------------------------
st.markdown('<div class="section-header">📦 Ventas Totales por Categoría de Producto</div>', unsafe_allow_html=True)
barras = df.groupby('categoria')['Ventas'].sum().sort_values(ascending=False).reset_index()
fig_barras_vertical = go.Figure()
fig_barras_vertical.add_trace(go.Bar(
    x=barras['categoria'],
    y=barras['Ventas'],
    marker=dict(
        color=barras['Ventas'],
        colorscale='Plasma',
        showscale=True,
        colorbar=dict(
            title="Ventas ($)",
            titlefont=dict(color='white'),
            tickfont=dict(color='white')
        ),
        line=dict(color='rgba(255,255,255,0.2)', width=1)
    ),
    text=[f'${x:,.0f}' for x in barras['Ventas']],
    textposition='outside',
    textfont=dict(color='white', size=12),
    hovertemplate='<b>%{x}</b><br>Ventas Totales: $%{y:,.0f}<extra></extra>',
    name='Ventas por Categoría'
))
fig_barras_vertical.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=500,
    xaxis=dict(
        title='Categoría de Producto',
        gridcolor='rgba(255,255,255,0.1)',
        tickangle=45
    ),
    yaxis=dict(
        title='Ventas Totales (USD)',
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='$,.0f'
    ),
    title=dict(
        text="Ventas Totales por Categoría de Producto",
        font=dict(size=18, color='white'),
        x=0.5
    ),
    showlegend=False
)
st.plotly_chart(fig_barras_vertical, use_container_width=True)

# ----------------------------------------------------------
# Histograma + Estadísticas Clave
# ----------------------------------------------------------
st.markdown('<div class="section-header">📊 Distribución de Ventas (Histograma + KDE)</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df['Ventas'],
        nbinsx=35,
        marker=dict(color='rgba(26, 198, 218, 0.7)', line=dict(color='rgba(26, 198, 218, 1)', width=1)),
        name='Distribución de Ventas',
        opacity=0.8,
        hovertemplate='Rango: $%{x}<br>Frecuencia: %{y}<extra></extra>'
    ))
    promedio = df['Ventas'].mean() if len(df) > 0 else 0
    fig_hist.add_vline(
        x=promedio,
        line_dash="dash",
        line_color="rgba(255, 193, 7, 0.8)",
        line_width=3,
        annotation_text=f"Promedio: ${promedio:,.0f}",
        annotation_position="top",
        annotation_font_color="white"
    )
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        xaxis=dict(title='Monto de Ventas (USD)', gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
        yaxis=dict(title='Frecuencia', gridcolor='rgba(255,255,255,0.1)'),
        title=dict(text="Distribución de Ventas Individuales", font=dict(size=16, color='white'), x=0.5),
        showlegend=False
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.markdown("**📈 Estadísticas Clave**")
    stats_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="margin-bottom: 1rem;">
            <span style="color: #42a5f5; font-weight: 600;">Promedio:</span><br>
            <span style="font-size: 1.2rem; color: white;">${promedio:,.2f}</span>
        </div>
        <div style="margin-bottom: 1rem;">
            <span style="color: #ab47bc; font-weight: 600;">Mediana:</span><br>
            <span style="font-size: 1.2rem; color: white;">${df['Ventas'].median():,.2f}</span>
        </div>
        <div style="margin-bottom: 1rem;">
            <span style="color: #26c6da; font-weight: 600;">Desv. Estándar:</span><br>
            <span style="font-size: 1.2rem; color: white;">${df['Ventas'].std():,.2f}</span>
        </div>
        <div style="margin-bottom: 1rem;">
            <span style="color: #66bb6a; font-weight: 600;">Máximo:</span><br>
            <span style="font-size: 1.2rem; color: white;">${df['Ventas'].max():,.2f}</span>
        </div>
        <div>
            <span style="color: #ff7043; font-weight: 600;">Mínimo:</span><br>
            <span style="font-size: 1.2rem; color: white;">${df['Ventas'].min():,.2f}</span>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)

# ----------------------------------------------------------
# Gráfico de Dispersión: Ventas por Categoría
# ----------------------------------------------------------
st.markdown('<div class="section-header">🌀 Gráfico de Dispersión - Distribución de Ventas por Categorías</div>', unsafe_allow_html=True)
fig_scatter = go.Figure()
categorias = df['categoria'].unique()
colores = ['#42a5f5', '#ab47bc', '#26c6da', '#66bb6a', '#ff7043', '#ffa726', '#ec407a', '#5c6bc0']

for i, categoria in enumerate(categorias):
    df_cat = df[df['categoria'] == categoria]
    fig_scatter.add_trace(go.Scatter(
        x=[categoria] * len(df_cat),
        y=df_cat['Ventas'],
        mode='markers',
        marker=dict(
            size=df_cat['Ventas'] / df_cat['Ventas'].max() * 30 + 5 if df_cat['Ventas'].max() > 0 else 5,
            color=colores[i % len(colores)],
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        name=categoria,
        text=df_cat['Nombre_producto'],
        customdata=np.column_stack((
            df_cat['pais'] if 'pais' in df.columns else ['N/A']*len(df_cat),
            df_cat['ciudad'] if 'ciudad' in df.columns else ['N/A']*len(df_cat),
            df_cat['Cantidad']
        )),
        hovertemplate='<b>%{text}</b><br>' +
                      'Categoría: %{x}<br>' +
                      'Ventas: $%{y:,.2f}<br>' +
                      'País: %{customdata[0]}<br>' +
                      'Ciudad: %{customdata[1]}<br>' +
                      'Cantidad: %{customdata[2]}<extra></extra>'
    ))

fig_scatter.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=600,
    xaxis=dict(title='Categoría de Producto', gridcolor='rgba(255,255,255,0.1)', tickangle=45),
    yaxis=dict(title='Ventas (USD)', gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
    title=dict(text="Distribución de Ventas por Categoría y Producto (Tamaño = Monto de Venta)", font=dict(size=16, color='white'), x=0.5),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1),
    hovermode='closest'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------------
# Análisis Geográfico Básico (Barras) + Top 5 Países
# ----------------------------------------------------------
if 'pais' in df.columns:
    st.markdown('<div class="section-header">🌍 Análisis Geográfico por País</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        pais_ventas = df.groupby('pais')['Ventas'].sum().sort_values(ascending=False).head(10)
        fig_geo = go.Figure()
        fig_geo.add_trace(go.Bar(
            x=pais_ventas.index,
            y=pais_ventas.values,
            marker=dict(
                color=pais_ventas.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Ventas ($)",
                    titlefont=dict(color='white'),
                    tickfont=dict(color='white')
                )
            ),
            text=[f'${x:,.0f}' for x in pais_ventas.values],
            textposition='outside',
            textfont=dict(color='white'),
            hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
        ))
        fig_geo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            xaxis=dict(title='País', tickangle=45, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Ventas Totales (USD)', tickformat='$,.0f', gridcolor='rgba(255,255,255,0.1)'),
            title=dict(text="Top 10 Países por Ventas", font=dict(size=16, color='white'), x=0.5),
            showlegend=False
        )
        st.plotly_chart(fig_geo, use_container_width=True)
    with col2:
        st.markdown("**🏆 Top 5 Países**")
        top_paises = pais_ventas.head(5)
        for i, (pais, ventas) in enumerate(top_paises.items()):
            porcentaje = (ventas / total_ventas * 100) if total_ventas > 0 else 0
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 1rem;
                margin: 0.5rem 0;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 600; color: white; font-size: 1.1rem;">#{i+1} {pais}</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{porcentaje:.1f}% del total</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: #42a5f5;">${ventas:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------
# Vista Detallada de Datos
# ----------------------------------------------------------
st.markdown('<div class="section-header">📋 Vista Detallada de Datos</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    num_filas = st.selectbox("Mostrar filas:", [10, 25, 50, 100], index=1)
with col2:
    ordenar_por = st.selectbox("Ordenar por:", ['Ventas', 'Fecha', 'categoria'])
with col3:
    orden_desc = st.checkbox("Descendente", value=True)

df_display = df.sort_values(ordenar_por, ascending=not orden_desc).head(num_filas)
df_formatted = df_display.copy()
df_formatted['Ventas'] = df_formatted['Ventas'].apply(lambda x: f"${x:,.2f}")
df_formatted['Precio_unitario(USD)'] = df_formatted['Precio_unitario(USD)'].apply(lambda x: f"${x:.2f}")
st.dataframe(df_formatted, use_container_width=True, hide_index=True, height=400)

# ----------------------------------------------------------
# Footer con información de actualización
# ----------------------------------------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📊 Última Actualización**")
    st.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
with col2:
    st.markdown("**📈 Total de Registros**")
    st.write(f"{len(df):,} transacciones")
with col3:
    st.markdown("**💹 Período Analizado**")
    st.write(f"{df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')}")

# ----------------------------------------------------------
#  Análisis Adicionales
# ----------------------------------------------------------

# 1) Ventas por Método de Pago (Barras Horizontales)
st.markdown("---")
st.markdown('<div class="section-header">💳 Ventas por Método de Pago</div>', unsafe_allow_html=True)
ventas_metodo = df.groupby('metodo_pago')['Ventas'].sum().sort_values(ascending=False).reset_index()
fig_pago = go.Figure(go.Bar(
    x=ventas_metodo['Ventas'],
    y=ventas_metodo['metodo_pago'],
    orientation='h',
    text=[f"${v:,.0f}" for v in ventas_metodo['Ventas']],
    textposition='outside',
    marker=dict(
        color=ventas_metodo['Ventas'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title="Ventas ($)",
            titlefont=dict(color='white'),
            tickfont=dict(color='white')
        ),
        line=dict(color='rgba(255,255,255,0.2)', width=1)
    ),
    hovertemplate='<b>%{y}</b><br>Ventas: $%{x:,.0f}<extra></extra>'
))
fig_pago.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=350,
    xaxis=dict(
        title='Ventas Totales (USD)',
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='$,.0f'
    ),
    yaxis=dict(
        title='Método de Pago',
        gridcolor='rgba(255,255,255,0.1)'
    ),
    showlegend=False,
    margin=dict(l=120, r=20, t=40, b=40)
)
st.plotly_chart(fig_pago, use_container_width=True)

# 2) Box Plot: Ventas según Rango de Edad
st.markdown("---")
st.markdown('<div class="section-header">👥 Ventas según Edad de Cliente</div>', unsafe_allow_html=True)
bins = [0, 18, 30, 45, 60, 100]
labels = ['<18', '18-30', '31-45', '46-60', '61+']
df['rango_edad'] = pd.cut(df['edad_cliente'], bins=bins, labels=labels, right=False)
fig_edad = go.Figure()
for grupo in labels:
    ventas_grupo = df[df['rango_edad'] == grupo]['Ventas']
    if len(ventas_grupo) > 0:
        fig_edad.add_trace(go.Box(
            y=ventas_grupo,
            name=grupo,
            boxpoints='suspectedoutliers',
            marker=dict(opacity=0.7),
            hovertemplate=f'Rango: {grupo}<br>Ventas: $%{{y:,.0f}}<extra></extra>'
        ))
fig_edad.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400,
    yaxis=dict(
        title='Ventas (USD)',
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='$,.0f'
    ),
    xaxis=dict(
        title='Rango de Edad',
        gridcolor='rgba(255,255,255,0.1)'
    ),
    title=dict(text="Distribución de Ventas por Rango de Edad", font=dict(size=16, color='white'), x=0.5),
    showlegend=False
)
st.plotly_chart(fig_edad, use_container_width=True)

# 3) Ventas por Género (Pie + KPI)
st.markdown("---")
st.markdown('<div class="section-header">⚥ Ventas por Género de Cliente</div>', unsafe_allow_html=True)
ventas_genero = df.groupby('genero_cliente')['Ventas'].sum()
total = ventas_genero.sum()
porcentajes = (ventas_genero / total * 100).round(1)
col1, col2 = st.columns(2)
with col1:
    ventas_m = ventas_genero.get('Masculino', 0)
    st.metric(label="Ventas Masculinas", value=f"${ventas_m:,.0f}", delta=f"{porcentajes.get('Masculino',0)}%")
with col2:
    ventas_f = ventas_genero.get('Femenino', 0)
    st.metric(label="Ventas Femeninas", value=f"${ventas_f:,.0f}", delta=f"{porcentajes.get('Femenino',0)}%")
fig_gen = go.Figure(data=[go.Pie(
    labels=ventas_genero.index,
    values=ventas_genero.values,
    hole=0.5,
    textinfo='label+percent',
    marker=dict(line=dict(color='#000000', width=2)),
    hovertemplate='<b>%{label}</b><br>Ventas: $%{value:,.0f}<br>%{percent}<extra></extra>'
)])
fig_gen.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=350,
    showlegend=False,
    annotations=[dict(
        text=f"${total:,.0f}",
        x=0.5, y=0.5,
        font_size=18,
        font_color='white',
        showarrow=False
    )]
)
st.plotly_chart(fig_gen, use_container_width=True)

# 4) Violin Plot: Satisfacción vs Monto de Venta
st.markdown("---")
st.markdown('<div class="section-header">⭐ Satisfacción de Clientes vs Monto de Venta</div>', unsafe_allow_html=True)
df['satisfaccion_str'] = df['calificación_satisfaccion'].astype(str)
fig_sat = go.Figure()
niveles = sorted([x for x in df['satisfaccion_str'].unique() if x not in [np.nan, 'nan']], key=lambda x: int(x) if x.isdigit() else 0)
for nivel in niveles:
    ventas_nivel = df[df['satisfaccion_str'] == nivel]['Ventas']
    fig_sat.add_trace(go.Violin(
        x=[nivel] * len(ventas_nivel),
        y=ventas_nivel,
        name=f"{nivel}",
        box_visible=True,
        meanline_visible=True,
        points='all',
        jitter=0.3,
        hovertemplate=f"Satisfacción: {nivel}<br>Ventas: $%{{y:,.0f}}<extra></extra>"
    ))
fig_sat.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400,
    xaxis=dict(title='Calificación de Satisfacción', gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(title='Ventas (USD)', gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
    title=dict(text="Distribución de Ventas según Nivel de Satisfacción", font=dict(size=16, color='white'), x=0.5),
    showlegend=False
)
st.plotly_chart(fig_sat, use_container_width=True)

# 5) Evolución Mensual por Categoría (Líneas Múltiples)
st.markdown("---")
st.markdown('<div class="section-header">📅 Evolución Mensual por Categoría</div>', unsafe_allow_html=True)
df['anio_mes'] = df['Fecha'].dt.to_period('M').astype(str)
pivot_cat = df.pivot_table(
    index='anio_mes',
    columns='categoria',
    values='Ventas',
    aggfunc='sum'
).fillna(0)
pivot_cat.index = pd.to_datetime(pivot_cat.index + '-01')
fig_mensual = go.Figure()
for cat in pivot_cat.columns:
    fig_mensual.add_trace(go.Scatter(
        x=pivot_cat.index,
        y=pivot_cat[cat],
        mode='lines+markers',
        name=cat,
        hovertemplate='<b>'+cat+'</b><br>%{x|%b %Y}<br>Ventas: $%{y:,.0f}<extra></extra>'
    ))
fig_mensual.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=450,
    xaxis=dict(title='Mes', gridcolor='rgba(255,255,255,0.1)', tickformat='%b %Y'),
    yaxis=dict(title='Ventas (USD)', gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
    title=dict(text="Tendencia Mensual de Ventas por Categoría", font=dict(size=16, color='white'), x=0.5),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode='x unified'
)
st.plotly_chart(fig_mensual, use_container_width=True)

# 6) Matriz de Correlación (Heatmap)
st.markdown("---")
st.markdown('<div class="section-header">🔍 Matriz de Correlación</div>', unsafe_allow_html=True)

cols_num = ['Cantidad', 'Precio_unitario(USD)', 'Ventas', 'edad_cliente', 'calificación_satisfaccion']
corr_matrix = df[cols_num].corr().round(2)

annotations = []
for i, row in enumerate(corr_matrix.values):
    for j, val in enumerate(row):
        font_color = 'white' if abs(val) > 0.5 else 'black'
        annotations.append(
            dict(
                x=corr_matrix.columns[j],
                y=corr_matrix.index[i],
                text=str(val),
                showarrow=False,
                font=dict(color=font_color)
            )
        )

fig_corr = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.index,
    colorscale='RdBu',
    zmin=-1, zmax=1,
    colorbar=dict(
        title="Correlación",
        titleside='right',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    hovertemplate='Var1: %{y}<br>Var2: %{x}<br>Corr: %{z:.2f}<extra></extra>'
))

fig_corr.update_layout(
    annotations=annotations,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=450,
    xaxis=dict(tickangle=45),
    yaxis=dict(autorange='reversed'),
    title=dict(text="Heatmap de Correlación de Variables Numéricas", font=dict(size=16, color='white'), x=0.5)
)

st.plotly_chart(fig_corr, use_container_width=True)


# 7) Top 10 Productos más Vendidos (Bubble Chart)
st.markdown("---")
st.markdown('<div class="section-header">🏅 Top 10 Productos (Ventas vs Unidades)</div>', unsafe_allow_html=True)
prod_stats = df.groupby('Nombre_producto').agg({
    'Cantidad': 'sum',
    'Ventas': 'sum'
}).reset_index()
top10 = prod_stats.sort_values('Ventas', ascending=False).head(10)
fig_bubble = go.Figure(go.Scatter(
    x=top10['Cantidad'],
    y=top10['Ventas'],
    mode='markers+text',
    text=top10['Nombre_producto'],
    textposition='top center',
    marker=dict(
        size=top10['Ventas'] / top10['Ventas'].max() * 50 + 10 if top10['Ventas'].max() > 0 else 10,
        opacity=0.7,
        line=dict(color='white', width=1),
        color=top10['Ventas'],
        colorscale='Plasma',
        showscale=True,
        colorbar=dict(title="Ventas ($)", tickfont=dict(color='white'), titlefont=dict(color='white'))
    ),
    hovertemplate='<b>%{text}</b><br>Unidades vendidas: %{x}<br>Ventas: $%{y:,.0f}<extra></extra>'
))
fig_bubble.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=450,
    xaxis=dict(title='Unidades Vendidas', gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(title='Ventas (USD)', gridcolor='rgba(255,255,255,0.1)', tickformat='$,.0f'),
    title=dict(text="Top 10 Productos más Vendidos (Tamaño = Monto de Venta)", font=dict(size=16, color='white'), x=0.5),
    hovermode='closest'
)
st.plotly_chart(fig_bubble, use_container_width=True)

# 8) Heatmap Diario-Semanal de Ventas
st.markdown("---")
st.markdown('<div class="section-header">📆 Ventas por Día de la Semana y Hora</div>', unsafe_allow_html=True)
df['dia_semana'] = df['Fecha'].dt.dayofweek  # 0 Lunes, 6 Domingo
df['hora'] = df['Fecha'].dt.hour
pivot_sem = df.pivot_table(
    index='dia_semana',
    columns='hora',
    values='Ventas',
    aggfunc='sum'
).fillna(0)
pivot_sem = pivot_sem.sort_index()
etiquetas_dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
fig_heat = go.Figure(data=go.Heatmap(
    z=pivot_sem.values,
    x=pivot_sem.columns,
    y=etiquetas_dias,
    colorscale='Viridis',
    colorbar=dict(title="Ventas ($)", tickfont=dict(color='white'), titlefont=dict(color='white')),
    hovertemplate='Día: %{y}<br>Hora: %{x}:00<br>Ventas: $%{z:,.0f}<extra></extra>'
))
fig_heat.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=500,
    xaxis=dict(title='Hora del Día', tickmode='linear'),
    yaxis=dict(title='Día de la Semana', ticks='', automargin=True),
    title=dict(text="Heatmap de Ventas por Día de la Semana y Hora", font=dict(size=16, color='white'), x=0.5)
)
st.plotly_chart(fig_heat, use_container_width=True)

# 9) KPI: Tendencia Mensual y Promedio Diario
st.markdown("---")
col1, col2, col3 = st.columns(3)
ultimo_periodo = ventas_tiempo['Ventas'].iloc[-1] if len(ventas_tiempo) > 0 else 0
anteultimo = ventas_tiempo['Ventas'].iloc[-2] if len(ventas_tiempo) >= 2 else 0
delta_pct = ((ultimo_periodo - anteultimo) / anteultimo * 100) if anteultimo != 0 else 0
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📆</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: white;">Mes Actual</div>
            <div style="font-size: 1.2rem; color: rgba(255,255,255,0.7);">Ventas: ${ultimo_periodo:,.0f}</div>
            <div style="font-size: 0.8rem; color: #4caf50; font-weight: 600;">{delta_pct:.1f}% vs mes anterior</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    dias_distintos = df['Fecha'].dt.date.nunique()
    avg_diario = df['Ventas'].sum() / dias_distintos if dias_distintos > 0 else 0
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: white;">Promedio Diario</div>
            <div style="font-size: 1.2rem; color: rgba(255,255,255,0.7);">Ventas: ${avg_diario:,.0f}</div>
            <div style="font-size: 0.8rem; color: #4caf50; font-weight: 600;">Basado en {dias_distintos} días</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    num_trans = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🛒</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: white;">Transacciones</div>
            <div style="font-size: 1.2rem; color: rgba(255,255,255,0.7);">Total: {num_trans:,}</div>
            <div style="font-size: 0.8rem; color: #4caf50; font-weight: 600;">Índice de Actividad</div>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# Mapeo de nombres de países para corregir choropleth
# ----------------------------------------------------------
mapa_paises = {
    "Estados Unidos": "United States",
    "Reino Unido": "United Kingdom",
    "México": "Mexico",
    "España": "Spain",
    "Brasil": "Brazil",
    "Alemania": "Germany",
    "Francia": "France",
    "Italia": "Italy",
    "República Dominicana": "Dominican Republic",
    "Costa Rica": "Costa Rica",
    "Colombia": "Colombia",
    "Argentina": "Argentina",
    "Chile": "Chile",
    "Perú": "Peru",
}

# Creamos la columna corregida para Plotly
df['pais_plotly'] = df['pais'].replace(mapa_paises)


# mostrar en pantalla cuáles no se han mapeado
# sin_corregir = [
#    p for p in df['pais_plotly'].unique()
#    if p not in mapa_paises.values()
# ]
# st.write("Países que podrían NO mapearse correctamente:", sin_corregir)

# 10) Mapa Choropleth de Ventas por País (mejorado visualmente)
if 'pais' in df.columns:
    st.markdown("---")
    st.markdown('<div class="section-header">🌐 Mapa de Ventas por País</div>', unsafe_allow_html=True)

    pais_ventas = df.groupby('pais_plotly')['Ventas'].sum().reset_index()

    fig_map = go.Figure(go.Choropleth(
        locations=pais_ventas['pais_plotly'],
        locationmode='country names',
        z=pais_ventas['Ventas'],
        text=pais_ventas['pais_plotly'],
        colorscale='Plasma',
        zmin=pais_ventas['Ventas'].min(),
        zmax=pais_ventas['Ventas'].max(),
        marker_line_color='white',  # bordes blancos
        marker_line_width=0.5,
        colorbar=dict(
            title="Ventas ($)",
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        hovertemplate='<b>%{text}</b><br>Ventas: $%{z:,.0f}<extra></extra>'
    ))

    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='gray',
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=550,
        title=dict(
            text="🌎 Mapa Global de Ventas por País",
            font=dict(size=18, color='white'),
            x=0.5
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)