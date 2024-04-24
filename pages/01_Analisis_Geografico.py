import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium
from utils.Graficas1 import plot_map , filtrar ,plot_bar_chart, plot_bar_chart2

st.set_option('deprecation.showfileUploaderEncoding', False)
# Cargar datos
df = pd.read_parquet("./Data/hechosGeograficos.parquet")

dfiltrado = df.copy()



# Opciones del Filtro
st.sidebar.title('Opciones de Filtrado')
años_seleccionados = st.sidebar.slider('1.Selecciona el rango de años:', 2016, 2021, (2016, 2021))
tipo_via_seleccionado = st.sidebar.multiselect('2.Selecciona el tipo de vía:',dfiltrado['TIPO_DE_CALLE'].unique())
tipo_victima_seleccionado = st.sidebar.multiselect('3.Selecciona el tipo de victima:', dfiltrado['VICTIMA'].unique())
comuna_seleccionada = st.sidebar.multiselect('4.Seleccione la comuna' , sorted(dfiltrado['COMUNA'].unique()))
# Título del análisis geográfico
titulo = f"Análisis geográfico de fatalidad - Buenos Aires ({años_seleccionados[0]}-{años_seleccionados[1]})"
st.markdown(f"### {titulo}", unsafe_allow_html=True)
# Encabezado con el total de homicidios

st.markdown("""
<p><span style='text-align: start; color: rgb(13, 13, 13); background-color: rgb(255, 255, 255); font-size: 20px; font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;'>Este analisis es con el fin de comprender mejor la distribuci&oacute;n espacial de eventos o siniestros viales y c&oacute;mo est&aacute;n relacionados entre si en la ciudad de buenos aires</span></p>

            """,unsafe_allow_html=True)


# Verificar si hay valores seleccionados en las variables de selección
if len(años_seleccionados) > 0 or len(tipo_via_seleccionado) > 0 or len(tipo_victima_seleccionado) > 0 or len(comuna_seleccionada) > 0:
    dfiltrado = filtrar(dfiltrado,años_seleccionados,tipo_via_seleccionado,tipo_victima_seleccionado,comuna_seleccionada)
st.write(f"**Total Homicidios:** {len(dfiltrado)}")

#st.write(dfiltrado) 

plot_map(dfiltrado)    

# Divide la pantalla en dos columnas
col1, col2 = st.columns(2)

# Genera el primer gráfico en la primera columna
with col1:
    if len(dfiltrado['TIPO_DE_CALLE'].unique()) > 2:
        plot_bar_chart(dfiltrado)

# Genera el segundo gráfico en la segunda columna
with col2:
    if len(dfiltrado['COMUNA'].unique()) > 2:
     plot_bar_chart2(dfiltrado)


