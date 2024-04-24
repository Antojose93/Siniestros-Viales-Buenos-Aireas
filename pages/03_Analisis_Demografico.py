
import pandas as pd
import streamlit as st
from utils.Graficas2 import filtrar , graficar_victimas_por_rol, graficar_victimas_por_sexo , Graficar_Por_Rango_de_edad


df = pd.read_parquet("./Data/victimas.parquet")

dfiltrado = df.copy()



# Opciones del Filtro
st.sidebar.title('Opciones de Filtrado')
años_seleccionados = st.sidebar.slider('1.Selecciona el rango de años:', 2016, 2021, (2016, 2021))
sexo_seleccionado = st.sidebar.multiselect('2.Selecciona el Sexo:',dfiltrado['Sexo'].unique())
rol_seleccionado = st.sidebar.multiselect('3.Selecciona el Rol:', dfiltrado['Rol'].unique())
tipo_victima_seleccionada = st.sidebar.multiselect('4.Seleccione el tipo de Victima' , sorted(dfiltrado['Victima'].unique()))
# Título del análisis geográfico
titulo = f"Análisis demografico de fatalidad - Buenos Aires ({años_seleccionados[0]}-{años_seleccionados[1]})"
st.markdown(f"### {titulo}", unsafe_allow_html=True)
# Encabezado con el total de homicidios


st.markdown("""
<p><span style="text-align: left; color: rgb(13, 13, 13); background-color: rgb(255, 255, 255); font-size: 20px; font-family: &quot;Palatino Linotype&quot;, &quot;Book Antiqua&quot;, Palatino, serif;" id="isPasted">Este analisis tiene el propocito de proporcionar insights sobre los grupos de población más vulnerables a los accidentes de tráfico y ayudar a diseñar medidas de prevención específicas para estos grupos.</span></p>
            """,unsafe_allow_html=True)

# Verificar si hay valores seleccionados en las variables de selección
if len(años_seleccionados) > 0 or len(sexo_seleccionado) > 0 or len(rol_seleccionado) > 0 or len(tipo_victima_seleccionada) > 0:
    dfiltrado = filtrar(dfiltrado,años_seleccionados,sexo_seleccionado,rol_seleccionado,tipo_victima_seleccionada)
st.write(f"**Total de Victimas:** <h2><font color='red'>{len(dfiltrado)}</font></h2>", unsafe_allow_html=True)




if len(dfiltrado['Sexo']) > 1:
    graficar_victimas_por_sexo(dfiltrado)
if len(dfiltrado['Rol']) > 2:
    graficar_victimas_por_rol(dfiltrado)

Graficar_Por_Rango_de_edad(dfiltrado)