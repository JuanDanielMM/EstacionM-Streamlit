import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.express as px

st.title('Estación Meteorológica')

# Initialize connection

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

data1 = run_query("SELECT * FROM mediciones_medicion;")
data = pd.DataFrame.from_records(data1, columns=['id', 'Temperatura', 'Luz', 'Humedad', 'Fecha', 'posted_by_id'])
data2 = data.astype({'id' : 'int64', 'Temperatura' : 'float64', 'Luz' : 'int64', 'Humedad' : 'int64', 'Fecha' : 'datetime64', 'posted_by_id' : 'int64'}, errors='ignore')
#print(data)
#print(data.dtypes)
#print(data2['Fecha'].unique())

st.sidebar.subheader("Fechas")
fecha_deseada = st.sidebar.selectbox('Selecciona la fecha desdeada', data2['Fecha'].dt.date.unique())
df_fecha = data2[data2['Fecha'].dt.date == fecha_deseada]

st.subheader('Mostrando datos del ' + str(fecha_deseada))

# Create Temperature graph
Temp_graph = px.line(df_fecha, x = "id", y = "Temperatura", title = "Temperatura", labels = {"Temperatura" : "°C", "id" : "Número de muestra"}).update_traces(mode = 'markers+lines', marker = dict(color = "red"), line = dict (color = "red"))
Temp_graph.update_layout(title_text = "Temperatura del ambiente", title_x = 0.5)
st.plotly_chart(Temp_graph)
# Create Humidity chart
Hum_graph = px.line(df_fecha, x = "id", y = "Humedad", title = "Humedad de la tierra", labels = {"Humedad" : "% de Humedad", "id" : "Número de muestra"}).update_traces(mode = 'markers+lines', marker = dict(color = "#1ca1ed"), line = dict (color = "#1ca1ed"))
Hum_graph.update_layout(title_text = "Humedad de la tierra", title_x = 0.5)
st.plotly_chart(Hum_graph)
# Create Light chart
Luz_graph = px.line(df_fecha, x = "id", y = "Luz", title = "Cantidad de luz", labels = {"Luz" : "% de Luz", "id" : "Número de muestra"}).update_traces(mode = 'markers+lines', marker = dict(color = "#ecf01f"), line = dict (color = "#ecf01f"))
Hum_graph.update_layout(title_text = "Humedad de la tierra", title_x = 0.5)
Luz_graph.update_layout(title_text = "Cantidad de luz", title_x = 0.5)
st.plotly_chart(Luz_graph)
