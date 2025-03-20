from data_management import inicializar_dataframes, ARCHIVO_ANIMALACO, ARCHIVO_MAMASOTA
from streamlit_ui import setup_streamlit_ui

# Inicializar DataFrames
df_animalaco, df_mamasota = inicializar_dataframes()

# Configurar la interfaz de usuario
setup_streamlit_ui(df_animalaco, df_mamasota, ARCHIVO_ANIMALACO, ARCHIVO_MAMASOTA)