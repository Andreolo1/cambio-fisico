import streamlit as st
from datetime import datetime
from data_management import guardar_entrenamiento
from data_management import existe_entrenamiento_en_fecha
from stats_analysis import mostrar_analisis_fuerza  # Importa la función de análisis
import os
from PIL import Image
from drive_utils import mostrar_imagen_desde_drive  # Importar la función para mostrar imágenes desde Drive


def obtener_ultima_imagen(carpeta_imagenes):
    """Obtiene la última imagen numerada en la carpeta especificada."""
    try:
        # Listar archivos en la carpeta
        archivos = [f for f in os.listdir(carpeta_imagenes) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        # Ordenar archivos por nombre (asumiendo que están numerados)
        archivos.sort(key=lambda x: int(x.split('.')[0]))
        
        # Obtener la última imagen
        ultima_imagen = archivos[-1] if archivos else None
        
        return os.path.join(carpeta_imagenes, ultima_imagen) if ultima_imagen else None
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
        return None


from data_management import inicializar_dataframes

def setup_streamlit_ui():
    """Configura la interfaz de usuario de Streamlit."""
    st.title("🏋️ DOS BUENORROS ENTRENANDO")

    # Inicializar DataFrames desde Google Sheets
    df_animalaco, df_mamasota = inicializar_dataframes()
    
    # Creación de las pestañas
    tab1, tab2, tab3 = st.tabs(["🏠 Principal", "Animalaco", "Mamasota"])

    with tab1:
        st.header("ESTADÍSTICAS DE AMBOS")
        
        # Crear dos columnas
        col1, col2 = st.columns(2)
        
        # Gráfico de Animalaco (hombre)
        with col1:
            st.subheader("Animalaco")
            mostrar_analisis_fuerza(df_animalaco, "hombre")
        
        # Gráfico de Mamasota (mujer)
        with col2:
            st.subheader("Mamasota")
            mostrar_analisis_fuerza(df_mamasota, "mujer")
        
        # Mostrar la última imagen desde Google Drive
        mostrar_imagen_desde_drive()

    # Resto de las pestañas (Animalaco y Mamasota)
    with tab2:
        st.header("Pestaña Animalaco")
        st.write("Registra tu entrenamiento aquí.")
        df_animalaco = mostrar_formulario_entrenamiento(df_animalaco, "Animalaco")

    with tab3:
        st.header("Pestaña Mamasota")
        st.write("Registra tu entrenamiento aquí.")
        df_mamasota = mostrar_formulario_entrenamiento(df_mamasota, "Mamasota")
        
        
        
def mostrar_formulario_entrenamiento(df, tab_name):
    """
    Muestra el formulario para registrar un entrenamiento.
    """
    # Paso 1: Selección del focus y ejercicios
    st.subheader("Paso 1: Selecciona el focus y los ejercicios")
    focus = st.multiselect(
        "Focus del entrenamiento",
        options=["pata", "espalda", "pechito", "hombro", "biceps", "triceps", "core"],
        key=f"{tab_name}_focus"
    )

    # Ejercicios disponibles por focus
    ejercicios_por_focus = {
        "pata": [
            "sentadilla frontal", "sentadilla trasera", "peso muerto", "peso muerto unilateral",
            "femoral máquina sentado", "femoral máquina tumbado", "puente de glúteo",
            "abductor", "adductor", "prensa", "jaca", "gemelos máquina"
        ],
        "espalda": [
            "dominada", "jalón al pecho", "remo polea", "remo libre", "trapecio barra inclinada",
            "trapecio máquina", "trapecio en máquina de aperturas", "pajaritos"
        ],
        "biceps": [
            "biceps libre unilateral", "biceps libre doble", "biceps máquina", "biceps polea"
        ],
        "pechito": [
            "press banca", "press inclinado", "aperturas"
        ],
        "hombro": [
            "press militar"
        ],
        "triceps": [
            "triceps polea", "triceps libre", "triceps máquina fondos", "fondos"
        ],
        "core": [
            "plancha"
        ]
    }

    # Selección de ejercicios realizados
    ejercicios_seleccionados = {}
    for f in focus:
        ejercicios_seleccionados[f] = st.multiselect(
            f"Selecciona los ejercicios de {f} que realizaste",
            options=ejercicios_por_focus[f],
            key=f"{tab_name}_{f}_ejercicios"
        )

    # Botón para continuar al Paso 2
    if st.button("Continuar al Paso 2", key=f"{tab_name}_continuar_paso_2"):
        st.session_state["ejercicios_seleccionados"] = ejercicios_seleccionados
        st.session_state["focus"] = focus
        st.session_state["mostrar_paso_2"] = True

    # Paso 2: Registro de pesos y detalles
    if st.session_state.get("mostrar_paso_2", False):
        st.subheader("Paso 2: Registra los pesos y detalles del entrenamiento")
        with st.form(key=f"registro_entrenamiento_{tab_name}"):
            # Fecha del entrenamiento
            fecha_hora = st.date_input("Día del entrenamiento", datetime.today(), key=f"{tab_name}_fecha")

            # Verificar si ya existe un entrenamiento en esa fecha
            if existe_entrenamiento_en_fecha(df, fecha_hora):
                st.error(f"Ya tienes un entrenamiento registrado el día {fecha_hora.strftime('%d/%m/%Y')}.")
            else:
                # Input para el tiempo entrenado (en formato horas:minutos:segundos)
                tiempo_entrenado = st.text_input(
                    "Tiempo entrenado (HH:MM:SS):",
                    placeholder="Ejemplo: 1:34:00",
                    key=f"{tab_name}_tiempo"
                )

                # Validación del formato del tiempo entrenado
                def validar_tiempo(tiempo):
                    try:
                        horas, minutos, segundos = map(int, tiempo.split(":"))
                        if 0 <= horas < 24 and 0 <= minutos < 60 and 0 <= segundos < 60:
                            return True
                        return False
                    except:
                        return False

                if tiempo_entrenado and not validar_tiempo(tiempo_entrenado):
                    st.error("Formato de tiempo incorrecto. Usa el formato HH:MM:SS (por ejemplo, 1:34:00).")

                # Diccionario para almacenar los ejercicios y sus pesos
                ejercicios_realizados = {}

                # Registro de pesos para los ejercicios seleccionados
                for f, ejercicios in st.session_state["ejercicios_seleccionados"].items():
                    st.subheader(f"Ejercicios de {f}")
                    for ejercicio in ejercicios:
                        if f == "core" and ejercicio == "plancha":
                            ejercicios_realizados[ejercicio] = st.number_input(
                                f"{ejercicio} (segundos)", min_value=0, key=f"{tab_name}_{ejercicio}_segundos"
                            )
                        else:
                            ejercicios_realizados[ejercicio] = st.number_input(
                                f"{ejercicio} (kg)", min_value=0, key=f"{tab_name}_{ejercicio}_kg"
                            )

                # Sensación del entrenamiento
                sensacion = st.selectbox(
                    "Sensación", options=["mala", "normal", "buena"], key=f"{tab_name}_sensacion"
                )

                # Botón para enviar el formulario
                if st.form_submit_button("Registrar entrenamiento") and validar_tiempo(tiempo_entrenado):
                    # Crear un diccionario con los datos del entrenamiento
                    registro = {
                        "Fecha": fecha_hora.strftime("%d-%m-%Y"),
                        "Tiempo entrenado": tiempo_entrenado,
                        "Sensación": sensacion,
                        **ejercicios_realizados
                    }

                    # Guardar el registro en Google Sheets
                    nombre_hoja = "data_animalaco" if tab_name == "Animalaco" else "data_mamasota"
                    df = guardar_entrenamiento(df, registro, nombre_hoja)

                    # Reiniciar la página
                    st.rerun()

    return df




