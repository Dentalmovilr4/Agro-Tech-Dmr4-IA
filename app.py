import streamlit as st
import pandas as pd
import os

# Configuración de página profesional
st.set_page_config(page_title="Agro-Tech DMR4 IA", page_icon="🌾", layout="wide")

st.title("🌾 Agro-Tech-Dmr4-IA: Central de Negocios")
st.markdown("---")

# --- BARRA LATERAL: CONFIGURACIÓN FINANCIERA ---
st.sidebar.header("💰 Parámetros de Inversión")
precio_kwh = st.sidebar.number_input("Precio kWh actual (COP)", value=850)
costo_panel = st.sidebar.number_input("Costo Panel Instalado (COP)", value=1250000)
costo_biomasa = st.sidebar.number_input("Costo Planta Biomasa (COP)", value=18000000)

# --- SECCIÓN 1: ENTRADA DE DATOS TÉCNICOS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🚜 Sistema de Biomasa")
    kilos_mes = st.number_input("Cascarilla disponible al mes (kg)", value=2000)
    energia_bio = kilos_mes * 1.2
    ahorro_bio = energia_bio * precio_kwh

with col2:
    st.header("☀️ Sistema Solar")
    num_paneles = st.number_input("Cantidad de Paneles (450W)", value=10)
    # 5.8 HSP para El Copey, Cesar
    energia_solar_mes = ((num_paneles * 450 * 5.8 * 0.8) / 1000) * 30
    ahorro_solar = energia_solar_mes * precio_kwh

st.divider()

# --- SECCIÓN 2: ANÁLISIS ECONÓMICO Y GRÁFICAS ---
inversion_total = (num_paneles * costo_panel) + costo_biomasa
ahorro_total_mes = ahorro_bio + ahorro_solar
meses_retorno = inversion_total / ahorro_total_mes if ahorro_total_mes > 0 else 0

st.header("📊 Resultado del Análisis")
c1, c2, c3 = st.columns(3)
c1.metric("Inversión Total", f"$ {inversion_total:,.0f}")
c2.metric("Ahorro Mensual", f"$ {ahorro_total_mes:,.0f}")
c3.metric("Retorno de Inversión", f"{meses_retorno:.1f} Meses")

# Gráfica Comparativa
datos_grafica = pd.DataFrame({
    "Fuente": ["Biomasa", "Solar"],
    "Ahorro ($)": [ahorro_bio, ahorro_solar]
})
st.bar_chart(datos_grafica, x="Fuente", y="Ahorro ($)", color="#2E7D32")

# --- SECCIÓN 3: UBICACIÓN Y CONSEJOS ---
st.divider()
st.header("📍 Guía de Instalación Profesional")
t1, t2 = st.columns(2)
with t1:
    st.info("🧭 **Orientación:** Los paneles DEBEN mirar hacia el **SUR** geográfico.")
with t2:
    st.success("📐 **Inclinación:** Ajustar entre **10° y 12°** para El Copey, Cesar.")

# --- SECCIÓN 4: BASE DE DATOS DE REPORTES ---
st.divider()
st.header("📝 Registro de Clientes (Fincas)")
with st.form("registro_finca"):
    nombre_finca = st.text_input("Nombre de la Finca o Cliente")
    guardar = st.form_submit_button("Guardar Reporte")

if guardar:
    datos_nuevo = pd.DataFrame({
        "Finca": [nombre_finca],
        "Inversión": [inversion_total],
        "Ahorro/Mes": [ahorro_total_mes],
        "Meses_ROI": [round(meses_retorno, 1)]
    })
    
    archivo = "reportes_fincas.csv"
    if os.path.exists(archivo):
        df_historico = pd.read_csv(archivo)
        df_final = pd.concat([df_historico, datos_nuevo], ignore_index=True)
    else:
        df_final = datos_nuevo
        
    df_final.to_csv(archivo, index=False)
    st.balloons()
    st.success(f"¡Reporte de {nombre_finca} guardado en la base de datos!")

if st.checkbox("📂 Ver Historial de Reportes"):
    if os.path.exists("reportes_fincas.csv"):
        st.table(pd.read_csv("reportes_fincas.csv"))
    else:
        st.write("Aún no hay datos registrados.")

st.markdown("---")
st.caption("Desarrollado por Dentalmovilr4 | Agro-Tech Innovación")
