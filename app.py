import streamlit as st
import pandas as pd


# Encabezado del proyecto
st.title("🥛 Simulador de Conservación y Vida Útil de Alimentos")
st.caption("Curso de Programación | FCQ UACH | Docente: José Manuel Nápoles Duarte")
st.write("**Equipo 4:** Diana Soto, Daniela Trevizo, Andrea Ochoa, Ximena Garfio, Sofia Ontiveroz")

st.markdown("---")

# Controles interactivos en la barra lateral
st.sidebar.header("⚙️ Parámetros de Almacenamiento")

# 1. Widget st.radio para seleccionar la categoría del alimento
categoria = st.sidebar.radio(
    "Selecciona la categoría del alimento:",
    ["Carnes y Pescados", "Lácteos y Huevos", "Comida Preparada / Guisados"]
)

# 2. Widget st.slider para ajustar la temperatura (-20 a 45 °C)
temperatura = st.sidebar.slider("Temperatura (°C):", min_value=-20, max_value=45, value=7)

# Slider para los días de almacenamiento
dias = st.sidebar.slider("Días almacenado:", min_value=0.0, max_value=10.0, value=2.0, step=0.5)

# Definir la vida útil base (a 4°C) según el alimento seleccionado
if categoria == "Carnes y Pescados":
    vida_base = 3
elif categoria == "Lácteos y Huevos":
    vida_base = 7
else:
    vida_base = 4

# Cálculo de vida útil en función de la temperatura
if temperatura <= 0:
    vida_estimada = vida_base * 3
elif temperatura <= 4:
    vida_estimada = vida_base
else:
    vida_estimada = max(0.5, vida_base - (temperatura - 4) * 0.25)

# Cálculo para el tiempo límite antes de la aparición de moho
# A mayor temperatura (arriba de 0°C), el moho se desarrolla más rápido
dias_limite_moho = vida_estimada + 1.0

# Panel principal en dos columnas
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📌 Estado y Diagnóstico")
    st.write(f"**Categoría:** {categoria}")
    st.write(f"**Temperatura actual:** {temperatura} °C")
    st.write(f"**Vida útil estimada:** {vida_estimada:.1f} días")
    st.write(f"**Tiempo evaluado:** {dias} días")

    st.markdown("---")

    # 3. Widget st.warning / Alertas de conservación e inocuidad
    if 4 <= temperatura <= 60:
        st.warning("⚠️ **Zona Peligrosa (4°C a 60°C):** La temperatura favorece la proliferación de microorganismos.")
    else:
        st.success("❄️ **Temperatura Segura:** El crecimiento microbiano se encuentra bajo control.")

    # Alerta de caducidad regular
    if dias > vida_estimada and dias < dias_limite_moho:
        st.error("🚨 **¡Alerta!** El alimento superó su vida útil recomendada.")

    # NUEVA ALERTA: Detección de Moho / Hongos
    if dias >= dias_limite_moho and temperatura > 0:
        st.error("🍞 **ALERTA DE MOHO DETECTADO:** A esta temperatura y tiempo transcurrido, se presenta crecimiento visible de moho y descomposición fúngica. **¡No consumir!**")
    elif dias < vida_estimada:
        st.info(f"💡 A {temperatura}°C el alimento se conserva seguro por un máximo de {vida_estimada*24:.0f} horas.")

with col2:
    # 4. Widget st.tabs para organizar las gráficas
    tab1, tab2 = st.tabs(["📈 Vida Útil", "🧫 Crecimiento Microbiano y Moho"])

    with tab1:
        # Generar datos simples para la curva de vida útil
        lista_temps = list(range(-20, 46, 5))
        lista_vidas = []

        for t in lista_temps:
            if t <= 0:
                lista_vidas.append(vida_base * 3)
            elif t <= 4:
                lista_vidas.append(vida_base)
            else:
                lista_vidas.append(max(0.5, vida_base - (t - 4) * 0.25))

        df_vida = pd.DataFrame({"Temperatura (°C)": lista_temps, "Días de vida útil": lista_vidas})
        fig1 = px.line(df_vida, x="Temperatura (°C)", y="Días de vida útil", title=f"Vida Útil vs Temp ({categoria})")

        # 5. Widget st.plotly_chart para desplegar la gráfica
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        # Generar datos simples para el crecimiento microbiano y moho
        lista_dias = [0, 2, 4, 6, 8, 10]
        factor_crecimiento = 1.6 if temperatura > 4 else 1.08
        lista_bacterias = [100 * (factor_crecimiento ** d) for d in lista_dias]

        df_micro = pd.DataFrame({"Días": lista_dias, "Población Microbiana": lista_bacterias})
        fig2 = px.line(df_micro, x="Días", y="Población Microbiana", title="Estimación de Proliferación de Bacterias y Moho")
        st.plotly_chart(fig2, use_container_width=True)
