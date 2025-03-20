import pandas as pd
from datetime import datetime
import os

# Rutas de los archivos CSV
ARCHIVO_ANIMALACO = "data_animalaco.csv"
ARCHIVO_MAMASOTA = "data_mamasota.csv"

def inicializar_dataframes():
    """
    Inicializa los DataFrames para Animalaco y Mamasota.
    Si los archivos CSV existen, carga los datos desde allí.
    """
    columnas_ejercicios = [
        "sentadilla frontal", "sentadilla trasera", "peso muerto", "peso muerto unilateral",
        "femoral máquina sentado", "femoral máquina tumbado", "puente de glúteo",
        "abductor", "adductor", "prensa", "jaca", "gemelos máquina", "dominada",
        "jalón al pecho", "remo polea", "remo libre", "trapecio barra inclinada",
        "trapecio máquina", "trapecio en máquina de aperturas", "pajaritos",
        "biceps libre unilateral", "biceps libre doble", "biceps máquina", "biceps polea",
        "press banca", "press inclinado", "aperturas", "press militar", "triceps polea",
        "triceps libre", "triceps máquina fondos", "fondos", "plancha"
    ]
    columnas = ["Fecha", "Tiempo entrenado", "Sensación"] + columnas_ejercicios

    # Cargar DataFrames desde archivos CSV si existen
    if os.path.exists(ARCHIVO_ANIMALACO):
        df_animalaco = pd.read_csv(ARCHIVO_ANIMALACO, parse_dates=["Fecha"])
    else:
        df_animalaco = pd.DataFrame(columns=columnas)

    if os.path.exists(ARCHIVO_MAMASOTA):
        df_mamasota = pd.read_csv(ARCHIVO_MAMASOTA, parse_dates=["Fecha"])
    else:
        df_mamasota = pd.DataFrame(columns=columnas)

    return df_animalaco, df_mamasota

def guardar_entrenamiento(df, registro, archivo):
    """
    Guarda un nuevo registro en el DataFrame correspondiente y lo guarda en un archivo CSV.
    """
    nuevo_registro = pd.DataFrame([registro])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_csv(archivo, index=False)  # Guardar el DataFrame en un archivo CSV
    return df

def existe_entrenamiento_en_fecha(df, fecha):
    """
    Verifica si ya existe un entrenamiento registrado en la fecha dada.
    """
    return fecha in df["Fecha"].values