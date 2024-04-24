import altair as alt
import streamlit as st
import pandas as pd

colores = ["#ce2340","#605c4e","#294380","#8db986","#eaafd5"]

def filtrar(dataframe, años_seleccionados, sexo_seleccionado, rol_seleccionado, tipo_victima_seleccionada):
    # Filtrar por años
    dataframe_filtrado = dataframe[dataframe['Año'].between(años_seleccionados[0], años_seleccionados[1])]
    
    # Filtrar por tipos de vía
    if len(sexo_seleccionado) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['Sexo'].isin(sexo_seleccionado)]
    if len(rol_seleccionado) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['Rol'].isin(rol_seleccionado)]
    if len(tipo_victima_seleccionada) > 0:
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['Victima'].isin(tipo_victima_seleccionada)]
    return dataframe_filtrado

def graficar_victimas_por_rol(victimas):
    # Obtener el conteo de valores de la columna 'Rol'
    conteo_roles = victimas['Rol'].value_counts().reset_index()
    conteo_roles.columns = ['Rol', 'Cantidad']

    # Crear el gráfico de barras horizontales con Altair
    bars = alt.Chart(conteo_roles).mark_bar().encode(
        y=alt.Y('Rol:N', title='Rol'),
        x=alt.X('Cantidad:Q', title='Cantidad'),
        color=alt.Color('Rol:N', scale=alt.Scale(range=colores), legend=None)  # Apply custom colors
    ).properties(
        title='Cantidad de víctimas por rol'
    )

    return st.altair_chart(bars, use_container_width=True)


def graficar_victimas_por_sexo(victimas):
    colores = ["#FFC0CB","#00008B","#40E0D0"]
    # Agrupamos los datos por sexo y contamos el número de víctimas en cada grupo
    victimas_por_sexo = victimas['Sexo'].value_counts().reset_index()
    victimas_por_sexo.columns = ['Sexo', 'count']

    # Creamos el gráfico de torta (pie chart)
    pie_chart = alt.Chart(victimas_por_sexo).mark_arc().encode(
        color=alt.Color('Sexo:N', scale=alt.Scale(range=colores), legend=None),  # Apply custom colors
        tooltip=['Sexo', 'count'],
        theta='count'
    ).properties(
        width=300,
        height=300,
         title='Cantidad de víctimas por Sexo'
    )

    return st.altair_chart(pie_chart, use_container_width=True)

def Graficar_Por_Rango_de_edad(victimas):
    bins = list(range(0, 101, 10))  # Rangos de 10 en 10 hasta 100 años
    labels = [f"{i}-{i+9}" for i in range(0, 100, 10)]  # Etiquetas para los rangos

    # Agregar una nueva columna al DataFrame con los rangos de edad
    victimas['Grupo_Etario'] = pd.cut(victimas['Edad'], bins=bins, labels=labels, right=False)

    # Contar el número de personas en cada grupo etario
    edad_counts = victimas['Grupo_Etario'].value_counts().reset_index()
    edad_counts.columns = ['Grupo_Etario', 'Count']

    # Crear el gráfico
    chart = alt.Chart(edad_counts).mark_bar().encode(
        x=alt.X('Grupo_Etario:O', title='Rango de Edad'),
        y=alt.Y('Count:Q', title='Número de Personas'),
        color=alt.Color('Grupo_Etario:O', scale=alt.Scale(range=colores), legend=None) , # Apply custom colors
        tooltip=['Grupo_Etario', 'Count']
    ).properties(
        title='Distribución de Edades por Rango de 10 años'
    )
    return st.altair_chart(chart, use_container_width=True)