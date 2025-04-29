import streamlit as st
import boto3
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime

dynamodb = boto3.resource('dynamodb', 
                          region_name='eu-west-2',
                          aws_access_key_id='****',
                          aws_secret_access_key='****')

# Nome da tabela de armazenamento dos dados do sensor
table = dynamodb.Table('raspiData_G7_v2')


# Função para obter dados do DynamoDB
def get_data():
    response = table.scan()
    items = response['Items']
    timestamps = []
    values = []

    for item in items:
        timestamp_str = item['timestamp']
        value = float(item['value'])
        timestamp = datetime.strptime(timestamp_str, "%d/%m/%Y, %I:%M:%S %p")
        timestamps.append(timestamp)
        values.append(value)

    # Combinar timestamps e values em uma lista de tuplas e ordenar
    data = list(zip(timestamps, values))
    data.sort()  # Ordenar os timestamps

    # Separar de volta em listas de timestamps e values
    sorted_timestamps, sorted_values = zip(*data)
    
    return sorted_timestamps, sorted_values

# Obter os dados
timestamps, values = get_data()

# Criar o gráfico de evolução temporal
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(timestamps, values, marker='o', linestyle='-', color='b') 

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M:%S %p'))
plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.25)

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator()) 
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

ax.set_ylabel('Value')
ax.set_title('Evolução Temporal dos Dados do Sensor')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig)
