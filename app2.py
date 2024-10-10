import streamlit as st
import pandas as pd
import plotly.express as px

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas
colunas = ['NM_VOTAVEL', 'SG_PARTIDO', 'NR_VOTAVEL', 'NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO']  # Adicione 'ENDERECO'

# Carregando arquivo com dados
df = pd.read_csv('maragogipe.csv', delimiter=';', encoding='latin1')

# Carregando arquivo com endereços
df_enderecos = pd.read_csv('local.csv', delimiter=';', encoding='latin1')  # Altere o nome do arquivo conforme necessário

# Supondo que o df_enderecos tenha as colunas NR_SECAO e ENDERECO
# Exibir as primeiras linhas para garantir que as colunas estão corretas
# st.write(df_enderecos.head())

st.write("""
    # Eleições Municipais de 2024 Bahia
    Dados das eleições municipais de 2024 no estado da Bahia fornecido pelo TSE
""")

# Menu que seleciona o nome do votável na tela
st.sidebar.title('Filtrar dados')

municipio = st.sidebar.selectbox('Município', df['NM_MUNICIPIO'].unique())
df_municipio = df[df['NM_MUNICIPIO'] == municipio]

cargo = st.sidebar.selectbox('Cargo', df_municipio['DS_CARGO_PERGUNTA'].unique())
df_cargo = df_municipio[df_municipio['DS_CARGO_PERGUNTA'] == cargo]

# Alteração: Usar multiselect para selecionar vários candidatos
votaveis = st.sidebar.multiselect('Nome do votável (Candidato)', df_cargo['NM_VOTAVEL'].unique())

# Filtro para os candidatos selecionados
if votaveis:
    df_votavel = df_cargo[df_cargo['NM_VOTAVEL'].isin(votaveis)]
else:
    df_votavel = df_cargo

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

# Merge com os endereços
df_votavel = df_votavel.merge(df_enderecos[['NR_SECAO', 'NM_LOCAL_VOTACAO']], on='NR_SECAO', how='left')

# Exibe na tela o dataframe filtrado
st.dataframe(df_votavel[colunas], hide_index=True, use_container_width=True)

# Agrupar os votos por candidato e ordenar em ordem decrescente
df_votos_por_candidato = df_votavel.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
df_votos_por_candidato = df_votos_por_candidato.sort_values(by='QT_VOTOS', ascending=False)

# Criar o gráfico de barras vertical para comparar candidatos
fig = px.bar(df_votos_por_candidato, 
             x='NM_VOTAVEL', 
             y='QT_VOTOS', 
             labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
             title=f'Comparação de Votos para {cargo}')

# Ajustar o layout para melhorar a exibição
fig.update_layout(xaxis_tickangle=-45)  # Inclinar os nomes dos candidatos

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
