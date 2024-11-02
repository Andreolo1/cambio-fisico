import streamlit as st
import pandas as pd

st.title("🚀 PRIMING")

tab1, tab2 = st.tabs(["Datos", "Dashboard"])

with tab1:
    boton = False
    nuevos_datos = {}
    st.header("📂 ENTRADA DE DATOS:")



    uploaded_file = st.file_uploader("Carga tu archivo", type="csv",
                                     label_visibility="hidden")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file, sep=";", index_col="id")
        st.write(df.head())


    check1 = st.checkbox("Registrar nueva entrada")
    check2 = st.checkbox("Modificar objetivo")
    if check1 == True:
        fecha = st.date_input("Fecha")
        col1, col2, col3 = st.columns(3)
        with col1:
            peso = st.number_input("Peso en kg")
            cuello = st.number_input("Cuello en cm")
            pecho = st.number_input("Pecho en cm")
        with col2:
            altura = st.number_input("Altura en cm")
            cintura = st.number_input("Cintura en cm")
            caderas = st.number_input("Caderas en cm")

        with col3:
            biceps = st.number_input("Bíceps en cm")
            muslos = st.number_input("Muslos en cm")
            gemelo = st.number_input("Gemelo en cm")

        nuevos_datos["fecha"] = fecha
        nuevos_datos["peso"] = peso
        nuevos_datos["altura"] = altura
        nuevos_datos["cuello"] = cuello
        nuevos_datos["pecho"] = pecho
        nuevos_datos["cintura"] = cintura
        nuevos_datos["caderas"] = caderas
        nuevos_datos["biceps"] = biceps
        nuevos_datos["muslos"] = muslos
        nuevos_datos["gemelo"] = gemelo
        
        boton = st.button("Cargar Datos")
        if boton == True:
            st.caption(":green-background[Datos registrados con éxito!]")
    
        

    
with tab2:
    st.header("📊 PROGRESO:")
    
