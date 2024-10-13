import streamlit as st
import pandas as pd
import plotly.express as px

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas
colunas = ['NM_VOTAVEL', 'NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO', 'NM_BAIRRO', 'NM_ZONA']

# Carregando arquivo com dados
df = pd.read_csv('dados.csv', delimiter=';', encoding='latin1')

st.write("""
    # Eleições Municipais de 2024 Bahia
    Dados das eleições municipais de 2024 no estado da Bahia fornecido pelo TSE
""")

# Menu que seleciona o nome do votável na tela
st.sidebar.title('Filtrar dados')

municipio = st.sidebar.selectbox('Município', df['NM_MUNICIPIO_x'].unique())
df_municipio = df[df['NM_MUNICIPIO_x'] == municipio]

cargo = st.sidebar.selectbox('Cargo', df_municipio['DS_CARGO_PERGUNTA'].unique())
df_cargo = df_municipio[df_municipio['DS_CARGO_PERGUNTA'] == cargo]

# Multiselect para selecionar vários candidatos
votaveis = st.sidebar.multiselect('Nome do votável (Candidato)', df_cargo['NM_VOTAVEL'].unique())

# Multiselect para filtrar pelos locais de votação
locais_votacao = st.sidebar.multiselect('Local de Votação', df_cargo['NM_LOCAL_VOTACAO'].unique())

# Filtro para os candidatos selecionados
if votaveis:
    df_votavel = df_cargo[df_cargo['NM_VOTAVEL'].isin(votaveis)]
else:
    df_votavel = df_cargo

# Filtro para os locais de votação selecionados
if locais_votacao:
    df_votavel = df_votavel[df_votavel['NM_LOCAL_VOTACAO'].isin(locais_votacao)]

# Exibindo dados do candidato na barra lateral
if votaveis:
    st.sidebar.write('# Dados dos candidatos selecionados')
    for candidato in votaveis:
        total_votos = df_votavel[df_votavel['NM_VOTAVEL'] == candidato]['QT_VOTOS'].sum()
        numero_votavel = df_votavel[df_votavel['NM_VOTAVEL'] == candidato]['NR_VOTAVEL'].unique()[0]
        st.sidebar.write(f'Nome: {candidato}')
        st.sidebar.write(f'Número: {numero_votavel}')
        st.sidebar.write(f'Total de votos: {total_votos}')               
else:
    st.sidebar.write('Selecione pelo menos um candidato.')

# Exibe na tela o dataframe filtrado
st.dataframe(df_votavel[colunas], hide_index=True, use_container_width=True)

# Agrupar os votos por candidato e ordenar em ordem decrescente
df_votos_por_candidato = df_votavel.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
df_votos_por_candidato = df_votos_por_candidato.sort_values(by='QT_VOTOS', ascending=False)

# Definir a altura do gráfico com base no número de candidatos, com altura mínima
num_candidatos = len(df_votos_por_candidato)
altura_minima = 400  # Define a altura mínima
altura_grafico = max(50 * num_candidatos, altura_minima)  # Altura mínima ou dinâmica, o que for maior

# Criar o gráfico de barras horizontal para comparar candidatos
fig = px.bar(df_votos_por_candidato, 
             x='QT_VOTOS',  # Total de votos no eixo X
             y='NM_VOTAVEL',  # Nome do candidato no eixo Y
             orientation='h',  # Barras horizontais
             labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
             title=f'Comparação de Votos para {cargo}')

# Ajustar o layout para melhorar a exibição
fig.update_layout(
    yaxis=dict(autorange="reversed"),  # Reverter para que o candidato com mais votos fique no topo
    height=altura_grafico,  # Altura dinâmica com um mínimo
    margin=dict(l=200),  # Aumenta a margem à esquerda para nomes longos
    bargap=0.1  # Ajusta o espaço entre as barras
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)