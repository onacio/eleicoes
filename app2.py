import streamlit as st
import pandas as pd
import plotly.express as px

# Ocupa a largura total da tela
st.set_page_config(layout='wide')

# Colunas que serão exibidas
colunas = ['NM_VOTAVEL', 'SG_PARTIDO', 'NR_SECAO', 'QT_VOTOS', 'NM_LOCAL_VOTACAO']

# Carregando arquivos com dados
df_votacao = pd.read_csv('maragogipe.csv', delimiter=';', encoding='latin1')
df_secao = pd.read_csv('local.csv', delimiter=';', encoding='latin1')  # Carrega o arquivo com os endereços das seções

# Fazendo o merge com base no número da seção (NR_SECAO)
df_combinado = pd.merge(df_votacao, df_secao, on='NR_SECAO', how='left')

st.write("""
    # Eleições Municipais de 2024 Bahia
    Dados das eleições municipais de 2024 no estado da Bahia fornecido pelo TSE
""")

# Menu que seleciona o nome do votável na tela
st.sidebar.title('Filtrar dados')

# municipio = st.sidebar.selectbox('Município', df_combinado['NM_MUNICIPIO'].unique())
# df_municipio = df_combinado[df_combinado['NM_MUNICIPIO'] == municipio]

cargo = st.sidebar.selectbox('Cargo', df_combinado['DS_CARGO_PERGUNTA'].unique())
df_cargo = df_combinado[df_combinado['DS_CARGO_PERGUNTA'] == cargo]

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

# Exibe na tela o dataframe filtrado com as localidades e endereços
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
