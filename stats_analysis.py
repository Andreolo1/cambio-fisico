import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import streamlit as st

# =============================================================================
# CONFIGURACIÓN DE CATEGORÍAS Y MÁXIMOS (ACTUALIZADA CON HOMBRO)
# =============================================================================
CATEGORIAS = {
    "pata": ["sentadilla frontal", "sentadilla trasera", "peso muerto"],
    "culaso": ["puente de glúteo"],
    "espalda": ["dominada", "remo polea", "jalón al pecho"],
    "pechito": ["press banca"],
    "hombro": ["press militar"],  # Nueva categoría
    "biceps": ["biceps máquina", "biceps libre unilateral"],
    "triceps": ["triceps polea"],
    "core": ["plancha"]
}

PESO_EJERCICIOS = {
    "espalda": {"dominada": 2.0, "remo polea": 1.2, "jalón al pecho": 1.0}
}

MAXIMOS = {
    "mujer": {
        "pata": {"sentadilla frontal": 60, "sentadilla trasera": 80, "peso muerto": 90},
        "culaso": {"puente de glúteo": 80},
        "espalda": {"dominada": 50, "remo polea": 60, "jalón al pecho": 55},
        "pechito": {"press banca": 50},
        "hombro": {"press militar": 40},  # Nuevo máximo para hombro
        "biceps": {"biceps máquina": 25, "biceps libre unilateral": 20},
        "triceps": {"triceps polea": 25},
        "core": {"plancha": 90}
    },
    "hombre": {
        "pata": {"sentadilla frontal": 120, "sentadilla trasera": 140, "peso muerto": 180},
        "culaso": {"puente de glúteo": 140},
        "espalda": {"dominada": 70, "remo polea": 90, "jalón al pecho": 80},
        "pechito": {"press banca": 100},
        "hombro": {"press militar": 70},  # Nuevo máximo para hombro
        "biceps": {"biceps máquina": 35, "biceps libre unilateral": 30},
        "triceps": {"triceps polea": 40},
        "core": {"plancha": 120}
    }
}

# =============================================================================
# FUNCIONES DE CÁLCULO (ACTUALIZADAS, CON NOMBRES ORIGINALES)
# =============================================================================
def obtener_ultimo_registro_ejercicio(df, ejercicio):
    """Obtiene el último peso registrado para un ejercicio específico"""
    registros = df[ejercicio].dropna()
    return registros.iloc[-1] if not registros.empty else 0

def calcular_puntuacion_grupo(df, categoria, genero):
    """Calcula la puntuación para una categoría específica"""
    ejercicios = CATEGORIAS[categoria]
    total = 0
    peso_total = 0
    
    # Caso especial para bíceps
    if categoria == "biceps":
        # Obtener el último registro entre las dos opciones
        ultimos_registros = [
            obtener_ultimo_registro_ejercicio(df, ej) 
            for ej in ejercicios
        ]
        ejercicio_usado = ejercicios[np.argmax(ultimos_registros)]  # El que tenga valor más reciente
        peso = max(ultimos_registros)
        maximo = MAXIMOS[genero][categoria][ejercicio_usado]
        
        # Convertir peso a número
        try:
            peso = float(peso)
        except (ValueError, TypeError):
            peso = 0.0
        
        return (peso / maximo) * 10 if maximo != 0 else 0
    
    # Para otras categorías
    for ejercicio in ejercicios:
        peso = obtener_ultimo_registro_ejercicio(df, ejercicio)
        
        # Convertir peso a número
        try:
            peso = float(peso)
        except (ValueError, TypeError):
            peso = 0.0
            
        if peso == 0:
            continue
            
        # Obtener ponderación y máximo
        ponderacion = PESO_EJERCICIOS.get(categoria, {}).get(ejercicio, 1.0)
        maximo = MAXIMOS[genero][categoria][ejercicio]
        
        # Calcular contribución
        contribucion = (peso / maximo) * 10 * ponderacion
        total += contribucion
        peso_total += ponderacion
    
    return min(total / peso_total, 10) if peso_total > 0 else 0

def generar_radar_chart(puntuaciones):
    """Genera el gráfico de araña con Plotly"""
    categorias = list(puntuaciones.keys())
    valores = list(puntuaciones.values()) + [list(puntuaciones.values())[0]]  # Cerrar el círculo
    
    fig = go.Figure(
        data=go.Scatterpolar(
            r=valores,
            theta=categorias + [categorias[0]],
            fill="toself",
            line=dict(color="#FF6B6B", width=2),
            marker=dict(size=8)
        ),
        layout=go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(color="#4ECDC4"),
                    gridcolor="#4ECDC4"
                )
            ),
            paper_bgcolor="#2D3047",
            font=dict(color="#FFFFFF"),
            title="- - - ",
            title_font=dict(size=20)
        )
    )
    return fig

# =============================================================================
# INTEGRACIÓN CON STREAMLIT (CON NOMBRES ORIGINALES)
# =============================================================================
def mostrar_analisis_fuerza(df, genero):
    """Muestra el análisis en Streamlit"""
    
    if df.empty:
        st.warning("No hay datos para analizar")
        return
    
    # Calcular puntuaciones
    puntuaciones = {
        categoria: calcular_puntuacion_grupo(df, categoria, genero)
        for categoria in CATEGORIAS.keys()
    }
    
    fig = generar_radar_chart(puntuaciones)
    st.plotly_chart(fig, use_container_width=True)