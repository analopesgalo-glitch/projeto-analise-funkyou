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
# ==========================================
print("=" * 50)
print("       RELATÓRIO DE DIAGNÓSTICO INICIAL (BLOCOS)       ")
print("=" * 50)
print(f"1. Total de alunos na base tratada: {total_registros}")
print(f"2. Respostas vazias (Nunca desfilaram): {total_vazios} ({ (total_vazios/total_registros)*100:.1f}%)")
print(f"3. Respostas preenchidas (Já desfilaram): {total_respondidos} ({ (total_respondidos/total_registros)*100:.1f}%)")
print(f"4. Alunos retidos/recorrentes (Mencionaram Funk You): {total_recorrentes_funk_you}")
print("-" * 50)

# 4. Amostra bruta de conferência visual das 10 primeiras respostas preenchidas
print("AMOSTRA VISUAL DAS RESPOSTAS PREENCHIDAS:")
print(df[df[coluna_bloco].notna()][coluna_bloco].head(10))
print("=" * 50)