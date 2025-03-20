import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import streamlit as st

# Configuración de categorías y máximos
CATEGORIAS = {
    "pata": ["sentadilla frontal", "sentadilla trasera", "peso muerto"],
    "culaso": ["puente de glúteo"],
    "espalda": ["dominada", "remo polea", "jalón al pecho"],
    "pechito": ["press banca"],
    "hombro": ["press militar"],
    "biceps": ["biceps máquina", "biceps libre unilateral"],
    "triceps": ["triceps polea"],
    "core": ["plancha"]
}

MAXIMOS = {
    "mujer": {
        "pata": {"sentadilla frontal": 60, "sentadilla trasera": 80, "peso muerto": 90},
        "culaso": {"puente de glúteo": 80},
        "espalda": {"dominada": 50, "remo polea": 60, "jalón al pecho": 55},
        "pechito": {"press banca": 50},
        "hombro": {"press militar": 40},
        "biceps": {"biceps máquina": 25, "biceps libre unilateral": 20},
        "triceps": {"triceps polea": 25},
        "core": {"plancha": 90}
    },
    "hombre": {
        "pata": {"sentadilla frontal": 120, "sentadilla trasera": 140, "peso muerto": 180},
        "culaso": {"puente de glúteo": 140},
        "espalda": {"dominada": 70, "remo polea": 90, "jalón al pecho": 80},
        "pechito": {"press banca": 100},
        "hombro": {"press militar": 70},
        "biceps": {"biceps máquina": 35, "biceps libre unilateral": 30},
        "triceps": {"triceps polea": 40},
        "core": {"plancha": 120}
    }
}

def calcular_puntuacion_grupo(df, categoria, genero):
    """Calcula la puntuación para una categoría específica."""
    ejercicios = CATEGORIAS[categoria]
    total = 0
    peso_total = 0
    
    for ejercicio in ejercicios:
        peso = df[ejercicio].iloc[-1] if ejercicio in df.columns else 0
        
        # Convertir peso a número
        try:
            peso = float(peso)
        except (ValueError, TypeError):
            peso = 0.0
            
        if peso == 0:
            continue
            
        # Obtener ponderación y máximo
        maximo = MAXIMOS[genero][categoria][ejercicio]
        
        # Calcular contribución
        contribucion = (peso / maximo) * 10
        total += contribucion
        peso_total += 1
    
    return min(total / peso_total, 10) if peso_total > 0 else 0

def generar_radar_chart(puntuaciones):
    """Genera un gráfico de araña con las puntuaciones."""
    categorias = list(puntuaciones.keys())
    valores = list(puntuaciones.values())
    
    # Cerrar el círculo del radar
    valores += valores[:1]
    angulos = [n / len(categorias) * 2 * pi for n in range(len(categorias))]
    angulos += angulos[:1]
    
    # Configurar gráfico
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    ax.plot(angulos, valores, linewidth=1, linestyle='solid')
    ax.fill(angulos, valores, alpha=0.25)
    
    # Ajustar ejes
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], fontsize=10)
    plt.ylim(0, 10)
    
    return fig

def mostrar_analisis_fuerza(df, genero):
    """Muestra el análisis en la interfaz de Streamlit."""
    st.header("🏋️ Análisis de Fuerza por Grupo Muscular")
    
    if df.empty:
        st.warning("No hay datos para analizar")
        return
    
    # Calcular puntuaciones
    puntuaciones = {
        categoria: calcular_puntuacion_grupo(df, categoria, genero)
        for categoria in CATEGORIAS.keys()
    }
    
    # Mostrar resultados
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Puntuaciones")
        for cat, score in puntuaciones.items():
            st.metric(label=cat.capitalize(), value=f"{score:.1f}/10")
    
    with col2:
        st.subheader("Gráfico de Progreso")
        fig = generar_radar_chart(puntuaciones)
        st.pyplot(fig)