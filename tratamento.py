#importação de bibliotecas para ETL: manipulação, limpesa e anonimização dos dados 
import pandas as pd

# PASSO 1: CARREGAR A BASE DE DADOS
caminho_arquivo = "dados/inscricoes_formulario.csv"
df = pd.read_csv(caminho_arquivo)
# Guardamos o número total de linhas iniciais para comparar depois
total_inicial = len(df)
print("--- RELATÓRIO DE LIMPEZA ---")
print(f"1. Total de registros iniciais: {total_inicial}")

# PASSO 2: PADRONIZAR OS NOMES (Letras Maiúsculas e sem Espaços Sobrando)
# .str.strip() limpa os espaços invisíveis antes ou depois do nome
# .str.upper() deixa todo mundo igual em CAIXA ALTA
df['Nome_Completo'] = df['Nome_Completo'].str.strip().str.upper()
# Exibe apenas as primeiras linhas após a transformação para conferência
#print("--- NOMES PADRONIZADOS (CAIXA ALTA) ---")
#print(df['Nome_Completo'].head(5))
#print("-" * 40)

# PASSO 3: IDENTIFICAR E REMOVER DUPLICATAS
# O keep='last' garante que vamos manter a última inscrição que a pessoa fez (a mais recente)
df_limpo = df.drop_duplicates(subset=['Nome_Completo'], keep='last').copy()
# Pegamos a nova quantidade de linhas para calcular a diferença
total_final = len(df_limpo)
linhas_excluidas = total_inicial - total_final

print("--- RELATÓRIO DE DUPLICATAS ---")
print(f"1. Total de registros antes: {total_inicial}")
print(f"2. Total de registros após a limpeza: {total_final}")
print(f"3. Resultado: Foram removidos {linhas_excluidas} cadastros duplicados!")
print("-" * 40)

# PASSO 4: GERAR ID ANÔNIMO E DELETAR NOME (LGPD)
# 1. Reorganiza a numeração das linhas para não ficar buracos após a exclusão das duplicatas
df_limpo = df_limpo.reset_index(drop=True)

# 2. Criamos o ID no formato desejado: FY2026-001, FY2026-002...
# .str.zfill(3) garante que o número tenha sempre 3 dígitos (001, 010, 100)
df_limpo['ID_Aluno'] = "FY2026-" + (df_limpo.index + 1).astype(str).str.zfill(3)
# VERIFICAÇÃO 1: IDS GERADOS E ALINHADOS (Antes de deletar)
#print("--- CONFERÊNCIA: IDS GERADOS E ALINHADOS ---")
#print(df_limpo[['ID_Aluno', 'Nome_Completo']].head(5))
#print("-" * 40)

# 3. Deletamos a coluna de nomes para garantir a anonimização total
df_final = df_limpo.drop(columns=['Nome_Completo'])

# 4. Colocamos a coluna ID_Aluno como a primeira coluna do DataFrame
colunas = ['ID_Aluno'] + [col for col in df_final.columns if col != 'ID_Aluno']
df_final = df_final[colunas]
# VERIFICAÇÃO 2: ESTRUTURA FINAL (ID na primeira coluna)
print("--- CONFERÊNCIA 2: ESTRUTURA FINAL DO DATAFRAME ---")
print(df_final.head(5))
print("-" * 40)

# 5. Exportamos o arquivo oficial tratado para a pasta dados
caminho_salvamento = "dados/inscricoes_tratadas.csv"
df_final.to_csv(caminho_salvamento, index=False)

print("--- STATUS DA ANONIMIZAÇÃO (LGPD) ---")
print(f"1. Nova chave primária no padrão 'FY2026-XXX' gerada com sucesso.")
print(f"2. Coluna 'Nome_Completo' removida permanentemente da base de análise.")
print(f"3. Arquivo de portfólio salvo em: {caminho_salvamento}")
print("-" * 40)