import folium
from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import matplotlib.pyplot as plt


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
    
def asignar_color(victima):
    if "MOTO" in victima:
        return "red"
    elif "AUTO" in victima:
        return "blue"
    elif "PEATON" in victima:
        return "yellow"
    elif "CARGA" in victima:
        return "orange"
    elif "BICICLETA" in victima:
        return "green"
    elif "PASAJEROS" in victima:
        return "brown"
    else:
        return "lightgray"

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

def plot_bar_chart(dataframe):
    # Contar el número de accidentes por año
    accidents_per_street_type = dataframe['TIPO_DE_CALLE'].value_counts().sort_index()
    
    # Graficar
    fig, ax = plt.subplots()
    ax.bar(accidents_per_street_type.index, accidents_per_street_type.values)
    ax.set_xlabel('Tipo de Calle')
    ax.set_ylabel('Número de Accidentes')
    ax.set_title('Número de Accidentes por Tipo de Calle')
    plt.xticks(rotation=45, ha='right')
    return st.pyplot(fig)

def plot_bar_chart2(dataframe):
    # Contar el número de accidentes por tipo de calle
    dataframe['COMUNA'] = dataframe['COMUNA'].map(lambda x: f'Comuna_{x}')
    accidents_per_street_type = dataframe['COMUNA'].value_counts().sort_index()
    
    # Graficar
    fig, ax = plt.subplots()
    ax.bar(accidents_per_street_type.index, accidents_per_street_type.values)
    ax.set_xlabel('Comuna')
    ax.set_ylabel('Número de Accidentes')
    ax.set_title('Número de Accidentes por Comuna')
    plt.xticks(rotation=45, ha='right')
    return st.pyplot(fig)
