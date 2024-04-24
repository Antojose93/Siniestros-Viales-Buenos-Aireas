import folium
from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import altair as alt


def filtrar(dataframe,años_seleccionados,tipos_via_seleccionados,victimas_seleccionados,comunas_seleccionadas):
    # Filtrar por años
    dataframe_filtrado = dataframe[dataframe['Año'].between(años_seleccionados[0], años_seleccionados[1])]
    
    # Filtrar por tipos de vía
    if len(tipos_via_seleccionados) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['TIPO_DE_CALLE'].isin(tipos_via_seleccionados)]
    if len(victimas_seleccionados) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['VICTIMA'].isin(victimas_seleccionados)]
    if len(comunas_seleccionadas) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['COMUNA'].isin(comunas_seleccionadas)]
    return dataframe_filtrado
    


def plot_map(df):
    """
    Genera un mapa usando Folium a partir de un DataFrame con columnas 'pos x' y 'pos y'.

    Parameters:
        df (DataFrame): DataFrame con columnas 'pos x' y 'pos y' que representan las coordenadas del mapa.

    Returns:
        Folium Map: Mapa generado.
    """
    try:
        # Convertir columnas a numéricas y eliminar filas con valores NaN
        df[['pos x', 'pos y']] = df[['pos x', 'pos y']].apply(pd.to_numeric, errors='coerce')
        df = df.dropna(subset=['pos x', 'pos y'])

        # Crear el mapa con la ubicación del primer punto y un nivel de zoom inicial
        mapa = folium.Map(location=[df['pos y'].iloc[0], df['pos x'].iloc[0]], zoom_start=12)

        # Agrupar marcadores si hay más de 50 puntos
        if len(df) > 50:
            marker_cluster = MarkerCluster().add_to(mapa)
        else:
            marker_cluster = None

        # Añadir marcadores al mapa
        for index, row in df.iterrows():
            folium.Marker([row['pos y'], row['pos x']]).add_to(marker_cluster or mapa)

        # Retorna el mapa
        return st_folium(mapa, width=725)

    except Exception as e:
        return st.write("Error al generar el mapa: " + str(e))

def MuertesPorTipoDeCalle(dataframe):
    # Contar el número de accidentes por tipo de calle y ordenar por índice
    accidents_per_street_type = dataframe['TIPO_DE_CALLE'].value_counts().sort_index().reset_index()
    accidents_per_street_type.columns = ['Tipo de Calle', 'Número de Accidentes']
    customColors = ['#2b8186', '#459a9f', '#92e3e8' , '#78cbd0']
    # Crear el gráfico de barras con Altair
    chart = alt.Chart(accidents_per_street_type).mark_bar().encode(
        x=alt.X('Tipo de Calle:N', title='Tipo de Calle'),
        y=alt.Y('Número de Accidentes:Q', title='Número de Accidentes'),
        color=alt.Color('Tipo de Calle:N', scale=alt.Scale(range=customColors))
    ).properties(
        title='Número de Accidentes por Tipo de Calle'
    ).configure_axis(
        labelAngle=45
    )
    
    return st.altair_chart(chart, use_container_width=True) 

def MuertesPorComuna(dataframe):
    # Contar el número de accidentes por comuna
    dataframe['COMUNA'] = dataframe['COMUNA'].map(lambda x: f'Comuna_{x}')
    accidents_per_comuna = dataframe['COMUNA'].value_counts().sort_index().reset_index()
    accidents_per_comuna.columns = ['Comuna', 'Número de Accidentes']
    
    customColors = ['#2b8186', '#459a9f', '#92e3e8', '#78cbd0']
    
    # Crear el gráfico de barras con Altair
    chart = alt.Chart(accidents_per_comuna).mark_bar().encode(
        x=alt.X('Comuna:N', title='Comuna'),
        y=alt.Y('Número de Accidentes:Q', title='Número de Accidentes'),
        color=alt.Color('Comuna:N', scale=alt.Scale(range=customColors))
    ).properties(
        title='Número de Accidentes por Comuna'
    ).configure_axis(
        labelAngle=45
    )
    
    return st.altair_chart(chart, use_container_width=True)
