import pandas as pd


# Carregando arquivos com dados
df_votacao = pd.read_csv('maragogipe.csv', sep=';', encoding='latin1')
df_secao = pd.read_csv('local.csv', sep=';', encoding='latin1')

# # Fazendo o merge com base no número da seção (NR_SECAO)
# df_combinado = pd.merge(df_votacao, df_secao, on='NR_SECAO', how='left')
dataf = df_secao[['NR_SECAO', 'NM_LOCAL_VOTACAO']]
print(dataf)