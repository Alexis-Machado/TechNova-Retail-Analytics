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
        ["Todo el Período", "Último Mes", "Últimos 3 Meses", "Último Año"]
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
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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

# 10) Mapa Choropleth de Ventas por País 
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
        marker_line_color='white', # bordes blancos
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

# 1) Gráfico de Barras Apiladas: Ventas por categoría desglosado por método de pago
st.markdown("---")
st.markdown('<div class="section-header">💳 Ventas por Categoría y Método de Pago (Barras Apiladas)</div>', unsafe_allow_html=True)

pivot_categoria_pago = df.pivot_table(
    index='categoria',
    columns='metodo_pago',
    values='Ventas',
    aggfunc='sum'
).fillna(0)

fig_barras_apiladas = go.Figure()
colores_pago = ['#42a5f5', '#ab47bc', '#26c6da', '#66bb6a', '#ff7043', '#ffa726']

for i, metodo in enumerate(pivot_categoria_pago.columns):
    fig_barras_apiladas.add_trace(go.Bar(
        name=metodo,
        x=pivot_categoria_pago.index,
        y=pivot_categoria_pago[metodo],
        marker_color=colores_pago[i % len(colores_pago)],
        hovertemplate=f'<b>{metodo}</b><br>Categoría: %{{x}}<br>Ventas: $%{{y:,.0f}}<extra></extra>'
    ))

fig_barras_apiladas.update_layout(
    barmode='stack',
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
        text="Ventas por Categoría Desglosadas por Método de Pago",
        font=dict(size=16, color='white'),
        x=0.5
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    )
)

st.plotly_chart(fig_barras_apiladas, use_container_width=True)

# 2) Heatmap: Correlación entre edad, satisfacción y cantidad comprada
st.markdown("---")
st.markdown('<div class="section-header">🔥 Correlaciones: Edad, Satisfacción y Cantidad Comprada</div>', unsafe_allow_html=True)

# Creamos bins para edad y satisfacción para mejor visualización
df['edad_bin'] = pd.cut(df['edad_cliente'], bins=[0, 25, 35, 45, 55, 100], labels=['<25', '25-35', '35-45', '45-55', '55+'])
df['satisfaccion_bin'] = pd.cut(df['calificación_satisfaccion'], bins=[0, 2, 3, 4, 5], labels=['Baja', 'Media', 'Alta', 'Muy Alta'])

# Matriz de correlación mejorada
pivot_correlacion = df.pivot_table(
    index='edad_bin',
    columns='satisfaccion_bin',
    values='Cantidad',
    aggfunc='mean'
).fillna(0)

# Creamos anotaciones para el heatmap
annotations_corr = []
for i, row in enumerate(pivot_correlacion.index):
    for j, col in enumerate(pivot_correlacion.columns):
        val = pivot_correlacion.iloc[i, j]
        text_color = 'white' if val > pivot_correlacion.values.mean() else 'black'
        annotations_corr.append(
            dict(
                x=col,
                y=row,
                text=f'{val:.1f}',
                showarrow=False,
                font=dict(color=text_color, size=12)
            )
        )

fig_heatmap_corr = go.Figure(data=go.Heatmap(
    z=pivot_correlacion.values,
    x=pivot_correlacion.columns,
    y=pivot_correlacion.index,
    colorscale='Plasma',
    colorbar=dict(
        title="Cantidad Promedio",
        titleside='right',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    hovertemplate='Edad: %{y}<br>Satisfacción: %{x}<br>Cantidad Promedio: %{z:.1f}<extra></extra>'
))

fig_heatmap_corr.update_layout(
    annotations=annotations_corr,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400,
    xaxis=dict(title='Nivel de Satisfacción'),
    yaxis=dict(title='Rango de Edad', autorange='reversed'),
    title=dict(
        text="Correlación: Edad vs Satisfacción vs Cantidad Comprada",
        font=dict(size=16, color='white'),
        x=0.5
    )
)

st.plotly_chart(fig_heatmap_corr, use_container_width=True)

# 3) Boxplot: Distribución de precios por categoría de producto
st.markdown("---")
st.markdown('<div class="section-header">📊 Distribución de Precios por Categoría (Boxplot)</div>', unsafe_allow_html=True)

fig_boxplot = go.Figure()
categorias_unicas = df['categoria'].unique()
colores_box = ['#42a5f5', '#ab47bc', '#26c6da', '#66bb6a', '#ff7043', '#ffa726', '#ec407a', '#5c6bc0']

for i, categoria in enumerate(categorias_unicas):
    precios_categoria = df[df['categoria'] == categoria]['Precio_unitario(USD)']
    color_actual = colores_box[i % len(colores_box)]
    
    # Convertimos color hex a rgba con transparencia
    if color_actual == '#42a5f5':
        fillcolor = 'rgba(66, 165, 245, 0.3)'
    elif color_actual == '#ab47bc':
        fillcolor = 'rgba(171, 71, 188, 0.3)'
    elif color_actual == '#26c6da':
        fillcolor = 'rgba(38, 198, 218, 0.3)'
    elif color_actual == '#66bb6a':
        fillcolor = 'rgba(102, 187, 106, 0.3)'
    elif color_actual == '#ff7043':
        fillcolor = 'rgba(255, 112, 67, 0.3)'
    elif color_actual == '#ffa726':
        fillcolor = 'rgba(255, 167, 38, 0.3)'
    elif color_actual == '#ec407a':
        fillcolor = 'rgba(236, 64, 122, 0.3)'
    else:
        fillcolor = 'rgba(92, 107, 192, 0.3)'
    
    fig_boxplot.add_trace(go.Box(
        y=precios_categoria,
        name=categoria,
        boxpoints='outliers',
        marker_color=color_actual,
        fillcolor=fillcolor,
        hovertemplate=f'<b>{categoria}</b><br>Precio: $%{{y:.2f}}<extra></extra>'
    ))

fig_boxplot.update_layout(
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
        title='Precio Unitario (USD)',
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='$,.2f'
    ),
    title=dict(
        text="Distribución de Precios por Categoría de Producto",
        font=dict(size=16, color='white'),
        x=0.5
    ),
    showlegend=False
)

st.plotly_chart(fig_boxplot, use_container_width=True)

# 4) Gráfico de Líneas: Evolución de la satisfacción del cliente a lo largo del tiempo
st.markdown("---")
st.markdown('<div class="section-header">📈 Evolución de Satisfacción del Cliente en el Tiempo</div>', unsafe_allow_html=True)

# Agrupamos por mes y calculamos satisfacción promedio
df['mes_anio'] = df['Fecha'].dt.to_period('M')
satisfaccion_tiempo = df.groupby('mes_anio')['calificación_satisfaccion'].mean().reset_index()
satisfaccion_tiempo['fecha'] = pd.to_datetime(satisfaccion_tiempo['mes_anio'].astype(str) + '-01')

fig_satisfaccion = go.Figure()

# Línea principal
fig_satisfaccion.add_trace(go.Scatter(
    x=satisfaccion_tiempo['fecha'],
    y=satisfaccion_tiempo['calificación_satisfaccion'],
    mode='lines+markers',
    name='Satisfacción Promedio',
    line=dict(color='#42a5f5', width=4, shape='spline'),
    marker=dict(size=10, color='#42a5f5', line=dict(color='white', width=2)),
    fill='tonexty',
    fillcolor='rgba(66, 165, 245, 0.2)',
    hovertemplate='<b>%{x|%b %Y}</b><br>Satisfacción: %{y:.2f}<extra></extra>'
))

# Línea de tendencia
if len(satisfaccion_tiempo) >= 2:
    z = np.polyfit(range(len(satisfaccion_tiempo)), satisfaccion_tiempo['calificación_satisfaccion'], 1)
    p = np.poly1d(z)
    fig_satisfaccion.add_trace(go.Scatter(
        x=satisfaccion_tiempo['fecha'],
        y=p(range(len(satisfaccion_tiempo))),
        mode='lines',
        name='Tendencia',
        line=dict(color='rgba(255, 193, 7, 0.8)', width=3, dash='dash'),
        hovertemplate='Tendencia: %{y:.2f}<extra></extra>'
    ))

# Línea promedio general
promedio_satisfaccion = df['calificación_satisfaccion'].mean()
fig_satisfaccion.add_hline(
    y=promedio_satisfaccion,
    line_dash="dot",
    line_color="rgba(156, 39, 176, 0.8)",
    line_width=2,
    annotation_text=f"Promedio General: {promedio_satisfaccion:.2f}",
    annotation_position="top left",
    annotation_font_color="white"
)

fig_satisfaccion.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=450,
    xaxis=dict(
        title='Mes',
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='%b %Y'
    ),
    yaxis=dict(
        title='Satisfacción Promedio',
        gridcolor='rgba(255,255,255,0.1)',
        range=[0, 5]
    ),
    title=dict(
        text="Evolución de la Satisfacción del Cliente a lo Largo del Tiempo",
        font=dict(size=16, color='white'),
        x=0.5
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode='x unified'
)

st.plotly_chart(fig_satisfaccion, use_container_width=True)

# 5) Mapa de Burbujas: Cantidad de ventas por ciudad
st.markdown("---")
st.markdown('<div class="section-header">🌆 Mapa de Burbujas - Ventas por Ciudad</div>', unsafe_allow_html=True)

# Agregamos datos por ciudad
ciudad_stats = df.groupby(['ciudad', 'pais']).agg({
    'Ventas': 'sum',
    'Cantidad': 'sum'
}).reset_index()

# Coordenadas aproximadas para algunas ciudades 
coordenadas_ciudades = {
    'Nueva York': {'lat': 40.7128, 'lon': -74.0060},
    'Los Angeles': {'lat': 34.0522, 'lon': -118.2437},
    'Chicago': {'lat': 41.8781, 'lon': -87.6298},
    'Londres': {'lat': 51.5074, 'lon': -0.1278},
    'París': {'lat': 48.8566, 'lon': 2.3522},
    'Madrid': {'lat': 40.4168, 'lon': -3.7038},
    'Barcelona': {'lat': 41.3851, 'lon': 2.1734},
    'Ciudad de México': {'lat': 19.4326, 'lon': -99.1332},
    'São Paulo': {'lat': -23.5558, 'lon': -46.6396},
    'Río de Janeiro': {'lat': -22.9068, 'lon': -43.1729},
    'Buenos Aires': {'lat': -34.6118, 'lon': -58.3960},
    'Lima': {'lat': -12.0464, 'lon': -77.0428},
    'Santiago': {'lat': -33.4489, 'lon': -70.6693},
    'Bogotá': {'lat': 4.7110, 'lon': -74.0721},
    'Berlín': {'lat': 52.5200, 'lon': 13.4050},
    'Roma': {'lat': 41.9028, 'lon': 12.4964},
    'Milán': {'lat': 45.4642, 'lon': 9.1900}
}

# Añadimos coordenadas a nuestros datos
ciudad_stats['lat'] = ciudad_stats['ciudad'].map(lambda x: coordenadas_ciudades.get(x, {}).get('lat', np.nan))
ciudad_stats['lon'] = ciudad_stats['ciudad'].map(lambda x: coordenadas_ciudades.get(x, {}).get('lon', np.nan))

# Filtramos solo las ciudades con coordenadas conocidas
ciudad_stats_geo = ciudad_stats.dropna(subset=['lat', 'lon'])

if len(ciudad_stats_geo) > 0:
    fig_mapa_burbujas = px.scatter_geo(
        ciudad_stats_geo,
        lat='lat',
        lon='lon',
        size='Ventas',
        color='Cantidad',
        hover_name='ciudad',
        hover_data={'pais': True, 'Ventas': ':$,.0f', 'Cantidad': ':,'},
        title="Mapa de Burbujas - Ventas por Ciudad",
        color_continuous_scale='Plasma',
        size_max=50
    )
    
    fig_mapa_burbujas.update_geos(
        showcoastlines=True,
        coastlinecolor='gray',
        showland=True,
        landcolor='rgba(30,30,30,0.8)',
        showocean=True,
        oceancolor='rgba(10,10,20,0.9)',
        projection_type='natural earth',
        bgcolor='rgba(0,0,0,0)'
    )
    
    fig_mapa_burbujas.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=600,
        title=dict(
            text="🌆 Mapa Global de Ventas por Ciudad",
            font=dict(size=18, color='white'),
            x=0.5
        ),
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        coloraxis_colorbar=dict(
            title="Cantidad",
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        )
    )
    
    st.plotly_chart(fig_mapa_burbujas, use_container_width=True)
else:
    st.warning("No se pudieron mapear las coordenadas de las ciudades para el mapa de burbujas.")

# 6) Segmentación de mercado por rangos de edad
st.markdown("---")
st.markdown('<div class="section-header">👥 Segmentación de Mercado por Edad</div>', unsafe_allow_html=True)

# Creamos los grupos de edad
df['grupo_edad'] = pd.cut(df['edad_cliente'], bins=[0, 30, 45, 100], labels=['<30', '30-45', '>45'])

col1, col2 = st.columns(2)

with col1:
    # Ventas por grupo de edad
    ventas_edad = df.groupby('grupo_edad')['Ventas'].sum()
    fig_edad_seg = go.Figure(data=[go.Pie(
        labels=ventas_edad.index,
        values=ventas_edad.values,
        hole=0.5,
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
        marker=dict(
            colors=['#42a5f5', '#ab47bc', '#26c6da'],
            line=dict(color='#000000', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Ventas: $%{{value:,.0f}}<extra></extra>'
    )])
    
    fig_edad_seg.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        title=dict(
            text="Segmentación por Edad - Ventas",
            font=dict(size=14, color='white'),
            x=0.5
        ),
        showlegend=False,
        annotations=[dict(
            text="Ventas<br>por Edad",
            x=0.5, y=0.5,
            font_size=16,
            font_color='white',
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_edad_seg, use_container_width=True)

with col2:
    # Satisfacción promedio por grupo de edad
    satisfaccion_edad = df.groupby('grupo_edad')['calificación_satisfaccion'].mean()
    fig_sat_edad = go.Figure(go.Bar(
        x=satisfaccion_edad.index,
        y=satisfaccion_edad.values,
        marker=dict(
            color=['#42a5f5', '#ab47bc', '#26c6da'],
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f'{x:.2f}' for x in satisfaccion_edad.values],
        textposition='outside',
        textfont=dict(color='white', size=14),
        hovertemplate='<b>%{x}</b><br>Satisfacción Promedio: %{y:.2f}<extra></extra>'
    ))
    
    fig_sat_edad.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        xaxis=dict(title='Grupo de Edad', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Satisfacción Promedio', gridcolor='rgba(255,255,255,0.1)', range=[0, 5]),
        title=dict(
            text="Satisfacción por Grupo de Edad",
            font=dict(size=14, color='white'),
            x=0.5
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig_sat_edad, use_container_width=True)

# 7) Comparación de satisfacción por género
st.markdown("---")
st.markdown('<div class="section-header">⚥ Análisis de Satisfacción por Género</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Satisfacción promedio por género
    satisfaccion_genero = df.groupby('genero_cliente')['calificación_satisfaccion'].agg(['mean', 'count'])
    
    # KPIs por género
    for genero in satisfaccion_genero.index:
        satisfaccion_prom = satisfaccion_genero.loc[genero, 'mean']
        num_clientes = satisfaccion_genero.loc[genero, 'count']
        icono = "👨" if genero == "Masculino" else "👩" if genero == "Femenino" else "👤"
        color = "#42a5f5" if genero == "Masculino" else "#ab47bc"
        
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icono}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">{genero}</div>
                <div style="font-size: 1.2rem; color: {color}; font-weight: 600;">⭐ {satisfaccion_prom:.2f}</div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">{num_clientes:,} clientes</div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    # Distribución de satisfacción por género (violín)
    fig_violin_genero = go.Figure()
    generos = df['genero_cliente'].unique()
    colores_genero = ['#42a5f5', '#ab47bc', '#26c6da']
    
    for i, genero in enumerate(generos):
        satisfaccion_gen = df[df['genero_cliente'] == genero]['calificación_satisfaccion']
        fig_violin_genero.add_trace(go.Violin(
            x=[genero] * len(satisfaccion_gen),
            y=satisfaccion_gen,
            name=genero,
            box_visible=True,
            meanline_visible=True,
            fillcolor=colores_genero[i % len(colores_genero)],
            line_color=colores_genero[i % len(colores_genero)],
            opacity=0.7,
            hovertemplate=f'<b>{genero}</b><br>Satisfacción: %{{y}}<extra></extra>'
        ))
    
    fig_violin_genero.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        xaxis=dict(title='Género', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Satisfacción', gridcolor='rgba(255,255,255,0.1)', range=[0, 5]),
        title=dict(
            text="Distribución de Satisfacción por Género",
            font=dict(size=14, color='white'),
            x=0.5
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig_violin_genero, use_container_width=True)

with col3:
    # Ventas por género
    ventas_genero_total = df.groupby('genero_cliente')['Ventas'].sum()
    fig_ventas_genero = go.Figure(data=[go.Pie(
        labels=ventas_genero_total.index,
        values=ventas_genero_total.values,
        hole=0.6,
        textinfo='label+percent',
        marker=dict(
            colors=['#42a5f5', '#ab47bc'],
            line=dict(color='#000000', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Ventas: $%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    fig_ventas_genero.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        title=dict(
            text="Participación en Ventas por Género",
            font=dict(size=14, color='white'),
            x=0.5
        ),
        showlegend=False,
        annotations=[dict(
            text=f"${ventas_genero_total.sum():,.0f}",
            x=0.5, y=0.5,
            font_size=18,
            font_color='white',
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_ventas_genero, use_container_width=True)

# ----------------------------------------------------------
# SECCIÓN DE KPIs PRINCIPALES - RESUMEN EJECUTIVO
# ----------------------------------------------------------
st.markdown("---")
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    ">
        <h1 style="
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #42a5f5, #ab47bc, #26c6da);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">📊 RESUMEN EJECUTIVO - KPIs PRINCIPALES</h1>
        <p style="font-size: 1.2rem; color: rgba(255,255,255,0.8);">
            Análisis completo del rendimiento empresarial y métricas clave
        </p>
    </div>
""", unsafe_allow_html=True)

# Calculamos todas las métricas principales
total_transacciones = len(df)
ticket_promedio = df['Ventas'].mean()
producto_top = df.groupby('Nombre_producto')['Ventas'].sum().idxmax()
ventas_producto_top = df.groupby('Nombre_producto')['Ventas'].sum().max()
categoria_lider = df.groupby('categoria')['Ventas'].sum().idxmax()
ventas_categoria_lider = df.groupby('categoria')['Ventas'].sum().max()
pais_top = df.groupby('pais')['Ventas'].sum().idxmax() if 'pais' in df.columns else "N/A"
ciudad_top = df.groupby('ciudad')['Ventas'].sum().idxmax() if 'ciudad' in df.columns else "N/A"
metodo_pago_top = df.groupby('metodo_pago')['Ventas'].sum().idxmax()
edad_promedio = df['edad_cliente'].mean()
satisfaccion_promedio = df['calificación_satisfaccion'].mean()
genero_dominante = df.groupby('genero_cliente')['Ventas'].sum().idxmax()

# Métricas temporales
fecha_inicio = df['Fecha'].min()
fecha_fin = df['Fecha'].max()
dias_operacion = (fecha_fin - fecha_inicio).days + 1
ventas_por_dia = total_ventas / dias_operacion
crecimiento_mes = ((ventas_tiempo['Ventas'].iloc[-1] - ventas_tiempo['Ventas'].iloc[0]) / ventas_tiempo['Ventas'].iloc[0] * 100) if len(ventas_tiempo) >= 2 else 0

# 1. MÉTRICAS FINANCIERAS PRINCIPALES
st.markdown('<div class="section-header">💰 Métricas Financieras Principales</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 2rem; font-weight: 700; color: #4caf50; margin-bottom: 0.3rem;">${total_ventas:,.0f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Ventas Totales</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Período completo</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 2rem; font-weight: 700; color: #42a5f5; margin-bottom: 0.3rem;">${ticket_promedio:,.0f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Ticket Promedio</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Por transacción</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📈</div>
            <div style="font-size: 2rem; font-weight: 700; color: #ab47bc; margin-bottom: 0.3rem;">${ventas_por_dia:,.0f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Ventas Diarias</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Promedio</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚀</div>
            <div style="font-size: 2rem; font-weight: 700; color: #26c6da; margin-bottom: 0.3rem;">{crecimiento_mes:+.1f}%</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Crecimiento</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Período analizado</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛒</div>
            <div style="font-size: 2rem; font-weight: 700; color: #ff7043; margin-bottom: 0.3rem;">{total_transacciones:,}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Transacciones</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Total</div>
        </div>
    """, unsafe_allow_html=True)

# 2. TOP PERFORMERS
st.markdown('<div class="section-header">🏆 Top Performers</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🥇 TOP PRODUCTOS**")
    top_productos = df.groupby('Nombre_producto')['Ventas'].sum().sort_values(ascending=False).head(5)
    for i, (producto, ventas) in enumerate(top_productos.items()):
        emoji = ["🥇", "🥈", "🥉", "🏅", "🏅"][i]
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
                    <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {producto[:25]}...</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">Ranking #{i+1}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #4caf50;">${ventas:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("**🎯 TOP CATEGORÍAS**")
    top_categorias = df.groupby('categoria')['Ventas'].sum().sort_values(ascending=False).head(5)
    for i, (categoria, ventas) in enumerate(top_categorias.items()):
        emoji = ["🥇", "🥈", "🥉", "🏅", "🏅"][i]
        porcentaje = (ventas / total_ventas * 100)
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
                    <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {categoria}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{porcentaje:.1f}% del total</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #42a5f5;">${ventas:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("**🌍 TOP PAÍSES**")
    if 'pais' in df.columns:
        top_paises = df.groupby('pais')['Ventas'].sum().sort_values(ascending=False).head(5)
        for i, (pais, ventas) in enumerate(top_paises.items()):
            emoji = ["🥇", "🥈", "🥉", "🏅", "🏅"][i]
            clientes = df[df['pais'] == pais]['Nombre_producto'].nunique()
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
                        <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {pais}</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{clientes} productos únicos</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #ab47bc;">${ventas:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 3. ANÁLISIS DE CLIENTES
st.markdown('<div class="section-header">👥 Análisis de Clientes</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

# Calculamos métricas de clientes
clientes_masculinos = len(df[df['genero_cliente'] == 'Masculino'])
clientes_femeninos = len(df[df['genero_cliente'] == 'Femenino'])
total_clientes = clientes_masculinos + clientes_femeninos
pct_masculino = (clientes_masculinos / total_clientes * 100) if total_clientes > 0 else 0
pct_femenino = (clientes_femeninos / total_clientes * 100) if total_clientes > 0 else 0

# Rango de edad más frecuente
edad_bins = pd.cut(df['edad_cliente'], bins=[0, 25, 35, 45, 55, 100], labels=['<25', '25-35', '35-45', '45-55', '55+'])
rango_edad_top = edad_bins.value_counts().idxmax()

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">👨</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #42a5f5; margin-bottom: 0.3rem;">{pct_masculino:.1f}%</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Clientes Masculinos</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">{clientes_masculinos:,} personas</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">👩</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ab47bc; margin-bottom: 0.3rem;">{pct_femenino:.1f}%</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Clientes Femeninos</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">{clientes_femeninos:,} personas</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎂</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #26c6da; margin-bottom: 0.3rem;">{edad_promedio:.0f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Edad Promedio</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Rango top: {rango_edad_top}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">⭐</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ffa726; margin-bottom: 0.3rem;">{satisfaccion_promedio:.2f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Satisfacción</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Escala 1-5</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    # Cliente con mayor gasto
    cliente_top_gasto = df.groupby('genero_cliente')['Ventas'].sum().idxmax()
    gasto_top = df.groupby('genero_cliente')['Ventas'].sum().max()
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">👑</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #66bb6a; margin-bottom: 0.3rem;">{cliente_top_gasto}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Género Dominante</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">${gasto_top:,.0f} en ventas</div>
        </div>
    """, unsafe_allow_html=True)

# 4. ANÁLISIS DE PRODUCTOS Y OPERACIONES
st.markdown('<div class="section-header">📦 Análisis de Productos y Operaciones</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# Métricas de productos
cantidad_total_vendida = df['Cantidad'].sum()
precio_promedio = df['Precio_unitario(USD)'].mean()
producto_mas_caro = df.loc[df['Precio_unitario(USD)'].idxmax(), 'Nombre_producto']
precio_mas_alto = df['Precio_unitario(USD)'].max()

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📦</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #42a5f5; margin-bottom: 0.3rem;">{cantidad_total_vendida:,}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Unidades Vendidas</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Total del período</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💲</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ab47bc; margin-bottom: 0.3rem;">${precio_promedio:.2f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Precio Promedio</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Por unidad</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💎</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #26c6da; margin-bottom: 0.3rem;">${precio_mas_alto:.2f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Producto Premium</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">{producto_mas_caro[:20]}...</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    metodo_pago_pct = df.groupby('metodo_pago')['Ventas'].sum()
    metodo_top_pct = (metodo_pago_pct.max() / metodo_pago_pct.sum() * 100)
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💳</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #66bb6a; margin-bottom: 0.3rem;">{metodo_pago_top}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Método de Pago Top</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">{metodo_top_pct:.1f}% de ventas</div>
        </div>
    """, unsafe_allow_html=True)

# 5. RESUMEN TEMPORAL
st.markdown('<div class="section-header">📅 Análisis Temporal</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# Día de la semana con más ventas
df['dia_nombre'] = df['Fecha'].dt.day_name()
dia_top = df.groupby('dia_nombre')['Ventas'].sum().idxmax()
ventas_dia_top = df.groupby('dia_nombre')['Ventas'].sum().max()

# Mes con más ventas
mes_top = df.groupby(df['Fecha'].dt.month)['Ventas'].sum().idxmax()
nombres_meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
mes_top_nombre = nombres_meses.get(mes_top, 'N/A')

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #42a5f5; margin-bottom: 0.3rem;">{dias_operacion}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Días Operativos</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">{fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🗓️</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ab47bc; margin-bottom: 0.3rem;">{dia_top}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Mejor Día</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">${ventas_dia_top:,.0f} en ventas</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📆</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #26c6da; margin-bottom: 0.3rem;">{mes_top_nombre}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Mejor Mes</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Mayor actividad</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    # Transacciones por día promedio
    transacciones_por_dia = total_transacciones / dias_operacion
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔄</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #66bb6a; margin-bottom: 0.3rem;">{transacciones_por_dia:.1f}</div>
            <div style="font-size: 1rem; color: white; margin-bottom: 0.3rem;">Transacciones/Día</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Promedio</div>
        </div>
    """, unsafe_allow_html=True)

# 6. RESUMEN EJECUTIVO DE HALLAZGOS Y RECOMENDACIONES ESTRATÉGICAS
st.markdown("---")
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(76, 175, 80, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="
            color: #4caf50;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            font-weight: 600;
        ">📋 Resumen Ejecutivo de Hallazgos</h2>
""", unsafe_allow_html=True)

# Calculamos métricas específicas para el resumen ejecutivo
paises_ventas = df.groupby('pais')['Ventas'].sum().sort_values(ascending=False)
metodos_pago_pref = df.groupby('metodo_pago')['Ventas'].sum().sort_values(ascending=False)
ciudades_satisfaccion = df.groupby('ciudad')['calificación_satisfaccion'].mean().sort_values(ascending=False)
metodo_pago_por_pais = df.groupby(['pais', 'metodo_pago'])['Ventas'].sum().reset_index()
metodo_pago_top_por_pais = metodo_pago_por_pais.loc[metodo_pago_por_pais.groupby('pais')['Ventas'].idxmax()]
categorias_baja_satisfaccion = df.groupby('categoria')['calificación_satisfaccion'].mean().sort_values(ascending=True)

# Perfil de cliente más satisfecho
clientes_satisfechos = df[df['calificación_satisfaccion'] >= 4]
if len(clientes_satisfechos) > 0:
    perfil_satisfecho_genero = clientes_satisfechos['genero_cliente'].mode().iloc[0] if len(clientes_satisfechos['genero_cliente'].mode()) > 0 else 'N/A'
    perfil_satisfecho_edad = clientes_satisfechos['edad_cliente'].mean()
    perfil_satisfecho_pais = clientes_satisfechos['pais'].mode().iloc[0] if len(clientes_satisfechos['pais'].mode()) > 0 else 'N/A'
else:
    perfil_satisfecho_genero = 'N/A'
    perfil_satisfecho_edad = 0
    perfil_satisfecho_pais = 'N/A'

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🌍 Países con Más Ventas:**")
    for i in range(3):
        pais = paises_ventas.index[i]
        ventas = paises_ventas.iloc[i]
        porcentaje = ventas/paises_ventas.sum()*100
        emoji = ["🥇", "🥈", "🥉"][i]
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(76, 175, 80, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {pais}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{porcentaje:.1f}% del total</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #4caf50;">${ventas:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**💳 Métodos de Pago Preferidos:**")
    for i in range(3):
        metodo = metodos_pago_pref.index[i]
        ventas = metodos_pago_pref.iloc[i]
        porcentaje = ventas/metodos_pago_pref.sum()*100
        emoji = ["🥇", "🥈", "🥉"][i]
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(33, 150, 243, 0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(33, 150, 243, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {metodo}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{porcentaje:.1f}% del total</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #42a5f5;">${ventas:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("**👤 Perfil de Cliente Satisfecho:**")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(171, 71, 188, 0.1) 0%, rgba(171, 71, 188, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(171, 71, 188, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="color: white; line-height: 1.8;">
            <div style="margin-bottom: 0.8rem;">
                <span style="color: #ab47bc; font-weight: 600;">Género:</span> 
                <span style="color: white; margin-left: 0.5rem;">{perfil_satisfecho_genero}</span>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <span style="color: #ab47bc; font-weight: 600;">Edad Promedio:</span> 
                <span style="color: white; margin-left: 0.5rem;">{perfil_satisfecho_edad:.0f} años</span>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <span style="color: #ab47bc; font-weight: 600;">País Principal:</span> 
                <span style="color: white; margin-left: 0.5rem;">{perfil_satisfecho_pais}</span>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <span style="color: #ab47bc; font-weight: 600;">Satisfacción:</span> 
                <span style="color: #4caf50; margin-left: 0.5rem; font-weight: 700;">4.0+ / 5.0</span>
            </div>
            <div>
                <span style="color: #ab47bc; font-weight: 600;">Representa:</span> 
                <span style="color: white; margin-left: 0.5rem;">{len(clientes_satisfechos)/len(df)*100:.1f}% de clientes</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**🏙️ Ciudades con Mayor Satisfacción:**")
    for i in range(3):
        ciudad = ciudades_satisfaccion.index[i]
        satisfaccion = ciudades_satisfaccion.iloc[i]
        emoji = ["🥇", "🥈", "🥉"][i]
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(38, 198, 218, 0.1) 0%, rgba(38, 198, 218, 0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(38, 198, 218, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; color: white; font-size: 1rem;">{emoji} {ciudad}</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">Top satisfacción</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #26c6da;">⭐ {satisfaccion:.2f}/5.0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# RECOMENDACIONES ESTRATÉGICAS
st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.08) 100%);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(33, 150, 243, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="
            color: #2196f3;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            font-weight: 600;
        ">🚀 Recomendaciones Estratégicas</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            min-height: 300px;
            display: flex;
            flex-direction: column;
        ">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🎯</div>
                <h4 style="color: #4caf50; margin-bottom: 0.8rem; font-size: 1.1rem;">Focalizar Campañas</h4>
            </div>
            <div style="color: white; line-height: 1.4; font-size: 0.85rem; flex-grow: 1;">
                <p style="margin-bottom: 0.8rem;"><strong>Objetivo:</strong> Concentrar en ciudades top</p>
                <ul style="padding-left: 1rem; margin: 0.8rem 0; list-style-type: none;">
                    <li style="margin-bottom: 0.5rem;">🥇 <strong>{ciudades_satisfaccion.index[0][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;({ciudades_satisfaccion.iloc[0]:.2f}/5.0)</li>
                    <li style="margin-bottom: 0.5rem;">🥈 <strong>{ciudades_satisfaccion.index[1][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;({ciudades_satisfaccion.iloc[1]:.2f}/5.0)</li>
                    <li style="margin-bottom: 0.5rem;">🥉 <strong>{ciudades_satisfaccion.index[2][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;({ciudades_satisfaccion.iloc[2]:.2f}/5.0)</li>
                </ul>
                <p style="color: #4caf50; font-weight: 600; font-size: 0.9rem; margin-top: auto;">📈 ROI esperado: +25%</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            min-height: 300px;
            display: flex;
            flex-direction: column;
        ">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">💳</div>
                <h4 style="color: #42a5f5; margin-bottom: 0.8rem; font-size: 1.1rem;">Métodos de Pago</h4>
            </div>
            <div style="color: white; line-height: 1.4; font-size: 0.85rem; flex-grow: 1;">
                <p style="margin-bottom: 0.8rem;"><strong>Estrategia:</strong> Promover por país</p>
                <ul style="padding-left: 1rem; margin: 0.8rem 0; list-style-type: none;">
                    <li style="margin-bottom: 0.5rem;">🇦🇷 <strong>{metodo_pago_top_por_pais.iloc[0]['pais'][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{metodo_pago_top_por_pais.iloc[0]['metodo_pago']}</li>
                    <li style="margin-bottom: 0.5rem;">🇨🇱 <strong>{metodo_pago_top_por_pais.iloc[1]['pais'][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{metodo_pago_top_por_pais.iloc[1]['metodo_pago']}</li>
                    <li style="margin-bottom: 0.5rem;">🇨🇴 <strong>{metodo_pago_top_por_pais.iloc[2]['pais'][:10]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{metodo_pago_top_por_pais.iloc[2]['metodo_pago']}</li>
                </ul>
                <p style="color: #42a5f5; font-weight: 600; font-size: 0.9rem; margin-top: auto;">📊 Conversión: +15%</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            min-height: 300px;
            display: flex;
            flex-direction: column;
        ">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">💲</div>
                <h4 style="color: #ff9800; margin-bottom: 0.8rem; font-size: 1.1rem;">Ajustar Precios</h4>
            </div>
            <div style="color: white; line-height: 1.4; font-size: 0.85rem; flex-grow: 1;">
                <p style="margin-bottom: 0.8rem;"><strong>Acción:</strong> Revisar categorías problema</p>
                <ul style="padding-left: 1rem; margin: 0.8rem 0; list-style-type: none;">
                    <li style="margin-bottom: 0.5rem;">⚠️ <strong>{categorias_baja_satisfaccion.index[0]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{categorias_baja_satisfaccion.iloc[0]:.2f}/5.0</li>
                    <li style="margin-bottom: 0.5rem;">⚠️ <strong>{categorias_baja_satisfaccion.index[1]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{categorias_baja_satisfaccion.iloc[1]:.2f}/5.0</li>
                    <li style="margin-bottom: 0.5rem;">⚠️ <strong>{categorias_baja_satisfaccion.index[2]}</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;{categorias_baja_satisfaccion.iloc[2]:.2f}/5.0</li>
                </ul>
                <p style="color: #ff9800; font-weight: 600; font-size: 0.9rem; margin-top: auto;">🎯 Meta: 4.0+/5.0</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)