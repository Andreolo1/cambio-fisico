import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Configuración de Google Sheets
CREDENCIALES_JSON = "sheets-key.json"  # Ruta al archivo JSON de credenciales
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Columnas base para los DataFrames
COLUMNAS_EJERCICIOS = [
    "sentadilla frontal", "sentadilla trasera", "peso muerto", "peso muerto unilateral",
    "femoral máquina sentado", "femoral máquina tumbado", "puente de glúteo",
    "abductor", "adductor", "prensa", "jaca", "gemelos máquina", "dominada",
    "jalón al pecho", "remo polea", "remo libre", "trapecio barra inclinada",
    "trapecio máquina", "trapecio en máquina de aperturas", "pajaritos",
    "biceps libre unilateral", "biceps libre doble", "biceps máquina", "biceps polea",
    "press banca", "press inclinado", "aperturas", "press militar", "triceps polea",
    "triceps libre", "triceps máquina fondos", "fondos", "plancha"
]
COLUMNAS = ["Fecha", "Tiempo entrenado", "Sensación"] + COLUMNAS_EJERCICIOS

def conectar_google_sheets(nombre_hoja):
    """
    Conecta a Google Sheets y devuelve un DataFrame.
    
    Args:
        nombre_hoja (str): Nombre de la hoja de Google Sheets.
    
    Returns:
        pd.DataFrame: DataFrame con los datos de la hoja.
    """
    try:
        # Autenticación
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, SCOPE)
        client = gspread.authorize(creds)
        
        # Abrir la hoja de cálculo
        hoja = client.open(nombre_hoja).sheet1
        
        # Convertir a DataFrame
        datos = hoja.get_all_records()
        df = pd.DataFrame(datos)
        
        return df
    except Exception as e:
        print(f"Error al conectar con Google Sheets: {e}")
        return pd.DataFrame()

def inicializar_dataframes():
    """
    Inicializa los DataFrames para Animalaco y Mamasota desde Google Sheets.
    Si las hojas están vacías, crea DataFrames con las columnas base.
    """
    # Crear DataFrames base con las columnas definidas
    df_base = pd.DataFrame(columns=COLUMNAS)
    df_base["Fecha"] = pd.to_datetime(df_base["Fecha"])  # Asegurar tipo datetime

    # Cargar datos desde Google Sheets
    df_animalaco = conectar_google_sheets("data_animalaco")
    df_mamasota = conectar_google_sheets("data_mamasota")
    
    # Si las hojas están vacías, usar el DataFrame base
    if df_animalaco.empty:
        df_animalaco = df_base.copy()
    if df_mamasota.empty:
        df_mamasota = df_base.copy()
    
    # Asegurar que los DataFrames tengan las columnas correctas
    df_animalaco = df_animalaco.reindex(columns=COLUMNAS, fill_value=None)
    df_mamasota = df_mamasota.reindex(columns=COLUMNAS, fill_value=None)
    
    return df_animalaco, df_mamasota

def existe_entrenamiento_en_fecha(df, fecha):
    """
    Verifica si ya existe un entrenamiento registrado en la fecha dada.
    """
    if df.empty:
        return False
    # Convertir a string para comparación exacta
    fecha_str = fecha.strftime("%d-%m-%Y")
    return fecha_str in df["Fecha"].astype(str).values

def guardar_entrenamiento(df, registro, nombre_hoja):
    """
    Guarda un nuevo registro en el DataFrame correspondiente y lo guarda en Google Sheets.
    """
    try:
        # Autenticación
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, SCOPE)
        client = gspread.authorize(creds)
        
        # Abrir la hoja de cálculo
        hoja = client.open(nombre_hoja).sheet1
        
        # Si la hoja está vacía, escribir las columnas primero
        if hoja.get_all_records() == []:
            hoja.append_row(COLUMNAS)  # Escribir las columnas
        
        # Convertir el registro a lista (en el orden de COLUMNAS)
        nuevo_registro = [registro.get(col, "") for col in COLUMNAS]
        
        # Añadir el registro a la hoja
        hoja.append_row(nuevo_registro)
        
        # Actualizar el DataFrame local
        df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
        return df
    except Exception as e:
        print(f"Error al guardar en Google Sheets: {e}")
        return df