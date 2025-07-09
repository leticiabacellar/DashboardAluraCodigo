# DASHBOARD ALURA
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard Alura", layout="wide")

# Simular dados para Alura
today = datetime.today()
dates = pd.date_range(today - timedelta(days=30), today)

alura_data = pd.DataFrame({
    'Data': np.random.choice(dates, 300),
    'Curso': np.random.choice(['Python', 'Power BI', 'SQL', 'UX Design'], 300),
    'Instrutor': np.random.choice(['João', 'Maria', 'Ana', 'Carlos'], 300),
    'Categoria': np.random.choice(['Programação', 'Dados', 'Design'], 300),
    'Nível': np.random.choice(['Iniciante', 'Intermediário', 'Avançado'], 300),
    'Receita': np.random.uniform(99, 499, 300)
})

st.title("Dashboard Alura")

st.sidebar.header("Filtros")
curso = st.sidebar.multiselect("Curso", options=alura_data['Curso'].unique(), default=alura_data['Curso'].unique())
categoria = st.sidebar.multiselect("Categoria", options=alura_data['Categoria'].unique(), default=alura_data['Categoria'].unique())
instrutor = st.sidebar.multiselect("Instrutor", options=alura_data['Instrutor'].unique(), default=alura_data['Instrutor'].unique())
nivel = st.sidebar.multiselect("Nível", options=alura_data['Nível'].unique(), default=alura_data['Nível'].unique())
data = st.sidebar.date_input("Período", [alura_data['Data'].min(), alura_data['Data'].max()])

filtro_df = alura_data[(alura_data['Curso'].isin(curso)) &
                       (alura_data['Categoria'].isin(categoria)) &
                       (alura_data['Instrutor'].isin(instrutor)) &
                       (alura_data['Nível'].isin(nivel)) &
                       (alura_data['Data'] >= pd.to_datetime(data[0])) &
                       (alura_data['Data'] <= pd.to_datetime(data[1]))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Alunos Ativos (simulado)", len(filtro_df))
col2.metric("Receita Total", f"R${filtro_df['Receita'].sum():,.2f}")
col3.metric("Curso Top", filtro_df['Curso'].value_counts().idxmax())
col4.metric("Instrutor Top", filtro_df['Instrutor'].value_counts().idxmax())

# Receita diária
receita_diaria = filtro_df.groupby('Data')['Receita'].sum().reset_index()
fig1 = px.line(receita_diaria, x='Data', y='Receita', title='Receita Diária', color_discrete_sequence=['#3E92CC'])
st.plotly_chart(fig1, use_container_width=True)

# Top 5 cursos
top_cursos = filtro_df['Curso'].value_counts().nlargest(5).reset_index()
top_cursos.columns = ['Curso', 'Qtd']

fig2 = px.bar(top_cursos, x='Curso', y='Qtd', title='Top 5 Cursos', color_discrete_sequence=['#132D46'])


st.plotly_chart(fig2, use_container_width=True)

# Receita por categoria
receita_categoria = filtro_df.groupby('Categoria')['Receita'].sum().reset_index()
fig3 = px.bar(receita_categoria, x='Categoria', y='Receita', title='Receita por Categoria', color_discrete_sequence=['#663399'])
st.plotly_chart(fig3, use_container_width=True)

# Tabela
st.dataframe(filtro_df)
