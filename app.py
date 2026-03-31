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
costo_biomasa_inv = st.sidebar.number_input("Costo Planta Biomasa (COP)", value=18000000)

# --- SECCIÓN 1: ENTRADA DE DATOS TÉCNICOS ---
col1, col2 = st.columns(2)

with col1:
    st.header("🚜 Sistema de Biomasa")
    kilos_mes = st.number_input("Cascarilla disponible al mes (kg)", value=2000)
    # Cálculo: 1.2 kWh por kilo
    energia_bio = kilos_mes * 1.2
    ahorro_bio = energia_bio * precio_kwh
    roi_bio = costo_biomasa_inv / ahorro_bio if ahorro_bio > 0 else 0

with col2:
    st.header("☀️ Sistema Solar")
    num_paneles = st.number_input("Cantidad de Paneles (450W)", value=10)
    # 5.8 HSP para El Copey, Cesar | 0.8 de eficiencia
    energia_solar_mes = ((num_paneles * 450 * 5.8 * 0.8) / 1000) * 30
    ahorro_solar = energia_solar_mes * precio_kwh
    inv_solar = num_paneles * costo_panel
    roi_solar = inv_solar / ahorro_solar if ahorro_solar > 0 else 0

st.divider()

# --- SECCIÓN 2: RESULTADOS POR SEPARADO ---
st.header("📊 Resultado del Análisis Individual")
r1, r2 = st.columns(2)

with r1:
    st.subheader("🟢 Informe Biomasa")
    st.metric("Energía Generada", f"{energia_bio:,.1f} kWh/mes")
    st.metric("Ahorro Biomasa", f"$ {ahorro_bio:,.0f}")
    st.metric("Retorno Biomasa", f"{roi_bio:.1f} Meses")

with r2:
    st.subheader("🟡 Informe Solar")
    st.metric("Energía Generada", f"{energia_solar_mes:,.1f} kWh/mes")
    st.metric("Ahorro Solar", f"$ {ahorro_solar:,.0f}")
    st.metric("Retorno Solar", f"{roi_solar:.1f} Meses")

# --- SECCIÓN 3: BALANCE TOTAL ---
st.divider()
st.header("📈 Balance General del Proyecto")
inversion_total = inv_solar + costo_biomasa_inv
ahorro_total_mes = ahorro_bio + ahorro_solar
meses_retorno_total = inversion_total / ahorro_total_mes if ahorro_total_mes > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("INVERSIÓN TOTAL", f"$ {inversion_total:,.0f}", delta_color="inverse")
c2.metric("AHORRO TOTAL MES", f"$ {ahorro_total_mes:,.0f}", delta=f"$ {ahorro_total_mes:,.0f}")
c3.metric("RETORNO GLOBAL", f"{meses_retorno_total:.1f} Meses")

# Gráfica Comparativa de Ahorro
datos_grafica = pd.DataFrame({
    "Fuente": ["Biomasa", "Solar"],
    "Ahorro ($)": [ahorro_bio, ahorro_solar]
})
st.bar_chart(datos_grafica, x="Fuente", y="Ahorro ($)", color="#2E7D32")

# --- SECCIÓN 4: GUÍA TÉCNICA ---
st.divider()
st.header("📍 Guía de Instalación Profesional")
t1, t2 = st.columns(2)
with t1:
    st.info("🧭 **Orientación:** Los paneles DEBEN mirar hacia el **SUR** geográfico.")
with t2:
    st.success("📐 **Inclinación:** Ajustar entre **10° y 12°** para El Copey, Cesar.")

# --- SECCIÓN 5: REGISTRO DE REPORTES ---
st.divider()
st.header("📝 Registro de Clientes (Fincas)")
with st.form("registro_finca"):
    nombre_finca = st.text_input("Nombre de la Finca o Cliente")
    guardar = st.form_submit_button("Guardar Reporte")

if guardar:
    datos_nuevo = pd.DataFrame({
        "Finca": [nombre_finca],
        "Inversión Total": [inversion_total],
        "Ahorro/Mes": [ahorro_total_mes],
        "ROI Global": [round(meses_retorno_total, 1)]
    })
    
    archivo = "reportes_fincas.csv"
    if os.path.exists(archivo):
        df_historico = pd.read_csv(archivo)
        df_final = pd.concat([df_historico, datos_nuevo], ignore_index=True)
    else:
        df_final = datos_nuevo
        
    df_final.to_csv(archivo, index=False)
    st.balloons()
    st.success(f"¡Reporte de {nombre_finca} guardado con éxito!")

if st.checkbox("📂 Ver Historial de Reportes"):
    if os.path.exists("reportes_fincas.csv"):
        st.table(pd.read_csv("reportes_fincas.csv"))
    else:
        st.write("Aún no hay datos registrados.")

st.markdown("---")
st.caption("Desarrollado por Dentalmovilr4 | Agro-Tech Innovación")

