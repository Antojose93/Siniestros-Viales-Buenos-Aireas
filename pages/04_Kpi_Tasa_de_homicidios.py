import streamlit as st
import pandas as pd
import altair as alt

victimas_agrupadas = pd.read_parquet("./Data/victimas_agrupadas.parquet")
st.markdown("""
<h1><span style="text-align: start; color: rgb(13, 13, 13); background-color: rgb(255, 255, 255); font-size: 26px; font-family: &quot;Palatino Linotype&quot;, &quot;Book Antiqua&quot;, Palatino, serif;" id="isPasted">Indicador Clave de Desempeño (KPI)</span></h1><p><span style="" id="isPasted">​</span><br></p><p><span style="font-family: &quot;Palatino Linotype&quot;, &quot;Book Antiqua&quot;, Palatino, serif; font-size: 20px;">Reducir en un 10% la tasa de homicidios en siniestros viales de los últimos seis meses, en CABA, en comparación con la tasa de homicidios en siniestros viales del semestre anterior</span></p>

            """,unsafe_allow_html=True)


chart = alt.Chart(victimas_agrupadas).mark_line().encode(
    x='Fecha:T',
    y='Tasa_Homicidios:Q'
).properties(
    title='Tasa de Homicidios en Siniestros Viales (por cada 100,000 habitantes)',
    width=600,
    height=400
)

# Mostrar la gráfica
st.altair_chart(chart, use_container_width=True)

st.markdown("""
<p><span style="font-family: &quot;Palatino Linotype&quot;, &quot;Book Antiqua&quot;, Palatino, serif; font-size: 20px;">A partir de la grafica anterior podemos notar que la tendencia es a bajar la tasa de homicidios</span></p>
            """,unsafe_allow_html=True)


victimas_agrupadas['Incremento_Tasa_Homicidios'] = victimas_agrupadas['Tasa_Homicidios'].diff()

# Calcular el porcentaje de incremento
victimas_agrupadas['Porcentaje_Incremento'] = (victimas_agrupadas['Incremento_Tasa_Homicidios'] / victimas_agrupadas['Tasa_Homicidios'].shift(1)) * 100

st.write(victimas_agrupadas)