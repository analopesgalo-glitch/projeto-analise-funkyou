import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import unicodedata
# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")

# PASSO 1: CARGA E DIAGNÓSTICO DE VOLUMETRIA
# 1. Carrega a base tratada e anônima
caminho_dados = "dados/inscricoes_tratadas.csv"
df = pd.read_csv(caminho_dados)

# --- DIAGNÓSTICO TEMPORÁRIO DE COLUNAS ---
#print("--- NOMES REAIS DAS COLUNAS DETECTADOS PELO PANDAS ---")
#print(list(df.columns))
#print("-" * 50)

# Copie o nome exato que aparecer no terminal e cole entre as aspas abaixo:
coluna_bloco = 'Se_sim_qual_bloco'

# 2. Cálculos para o Relatório de Diagnóstico
total_registros = len(df)
total_vazios = df[coluna_bloco].isna().sum()
total_respondidos = df[coluna_bloco].notna().sum()

# 3. Identificação de fidelidade (Menções ao próprio bloco)
padrao_funk_you = r'(FUNK\s*YOU|FUNKU|FUNK\s*U)'
com_filtro_funk_you = df[coluna_bloco].str.contains(padrao_funk_you, case=False, na=False)
total_recorrentes_funk_you = com_filtro_funk_you.sum()

# EMISSÃO DO RELATÓRIO DE VOLUMETRIA
print("=" * 50)
print("       RELATÓRIO DE DIAGNÓSTICO INICIAL (BLOCOS)       ")
print("=" * 50)
print(f"1. Total de alunos na base tratada: {total_registros}")
print(f"2. Respostas vazias (Nunca desfilaram): {total_vazios} ({ (total_vazios/total_registros)*100:.1f}%)")
print(f"3. Respostas preenchidas (Já desfilaram): {total_respondidos} ({ (total_respondidos/total_registros)*100:.1f}%)")
print(f"4. Alunos retidos/recorrentes (Mencionaram Funk You): {total_recorrentes_funk_you}")
print("-" * 50)

# GRÁFICO DE DIAGNÓSTICO (PIZZA)
labels = ['Nunca desfilou', 'Apenas Funk You', 'Outros Blocos']
# Lógica simples para categorizar:
# 1. Nunca desfilou = NaN
# 2. Apenas Funk You = Contém Funk You e nada mais
# 3. Outros blocos = Contém outros blocos (com ou sem Funk You)
# (Vamos simplificar para o gráfico de pizza inicial)

total = len(df)

# LÓGICA DE CLASSIFICAÇÃO EXCLUSIVA PARA O GRÁFICO

# 1. Nunca desfilou (NaN)
nunca_desfilou = df[coluna_bloco].isna().sum()

# 2. Criamos máscaras booleanas para identificar o conteúdo
contem_funk = df[coluna_bloco].str.contains(r'(FUNK\s*YOU|FUNKU|FUNK\s*U|FY)', case=False, na=False)
contem_outros = df[coluna_bloco].str.contains(r'[^FUNKYOUS\s,]+', case=False, na=True)

# 3. Classificação Exclusiva:
# Apenas Funk You: Contém Funk E NÃO contém outros
apenas_funk_you = df[contem_funk & ~contem_outros].shape[0]

# Com outros: Contém outros blocos (com ou sem Funk You)
com_outros = df[contem_outros & df[coluna_bloco].notna()].shape[0]

# 4. Definição dos tamanhos para o gráfico
sizes = [nunca_desfilou, apenas_funk_you, com_outros]

colors = ['#ff9999', '#66b3ff', '#99ff99']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title('Distribuição do Perfil de Experiência dos Alunos')

import os

# Cria a pasta 'graficos' se ela não existir
if not os.path.exists('graficos'):
    os.makedirs('graficos')

plt.savefig('graficos/diagnostico_inicial.png') # Salva para o portfólio!
plt.show()