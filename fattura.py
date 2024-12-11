# ==================== Bibliotecas utilizadas ========================= #

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

# ==================== Web scraping - selenium ========================= #

driver = webdriver.Chrome()
driver.get('http://zipline.fattura.com.br/corrida/')

user_input = driver.find_element(by='xpath', value='//*[@id="loginfat"]')
user_input.send_keys('usuario')

password_input = driver.find_element(by='xpath', value='//*[@id="senhafat"]')
password_input.send_keys('senha')

avancar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="botaoentrar"]'))
)
avancar_button.click()

WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
current_url = driver.current_url

if current_url == 'https://zipline.fattura.com.br/inicio/':
    driver.get('http://zipline.fattura.com.br/corrida/') 
    
avancar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/a'))
)
avancar_button.click()

elements = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '/html/body/table[2]/tbody'))
)

# ==================== Extração e tratamento dos dados ========================= #

fattura = []
for element in elements:
    numero = element.text
    fattura.append(numero)
    print(fattura)

linhas = []
for elemento in fattura:
    linhas.extend(elemento.split('\n')) 

linhas2 = [linhas[i:i+7] for i in range(0, len(linhas), 7)]

colunas = ['nome', 'crescimento', 'saida_nos_6meses', 'saida_apos_6meses', 'total_potencia_receita', 'planos', 'pontuacao']

df = pd.DataFrame(columns=colunas)

for lista in linhas2:
    if len(lista) == len(colunas): 
        df.loc[len(df)] = lista
    else: 
        df.loc[len(df)] = [''] * len(colunas)
print(df)

def extrair_info(coluna):
    return coluna.str.extract(r':\s*(.*?)\s*❦')
colunas_extrair = ['crescimento', 'saida_nos_6meses', 'saida_apos_6meses']
for coluna in colunas_extrair:
    df[coluna] = extrair_info(df[coluna])
def extrair_info(coluna):
    return coluna.str.extract(r':\s*(.*)')
colunas_extrair = ['planos', 'pontuacao', 'total_potencia_receita']
for coluna in colunas_extrair:
    df[coluna] = extrair_info(df[coluna])colunas_nome = ['nome']

def limpar_numeros_caracteres(df, colunas):
    for coluna in colunas:
        # r'\d' = qualquer dígito numérico.
        df[coluna] = df[coluna].str.replace(r'\d', '', regex=True)
        # r'\W' = qualquer caractere não alfanumérico.
        df[coluna] = df[coluna].str.replace(r'\W', '', regex=True)

limpar_numeros_caracteres(df, colunas_nome)

def split_nome(df, coluna):
    df[coluna] = df[coluna].str.replace(r'([a-z])([A-Z])', r'\1 \2', regex=True)

coluna_nome = 'nome'
split_nome(df, coluna_nome)

# ==================== Setores válidos ========================= #

def atribuir_setor(row):
    if row ['nome'] in ['nome-das-pessoas']:
        return 'Trials'
    elif row['nome'] in ['nome-das-pessoas']:
        return 'NfeMais'
    elif row['nome'] in ['nome-das-pessoas']:
        return 'Canais IB'
    elif row['nome'] in ['nome-das-pessoas']:
         return 'Canais OB'
    elif row['nome'] in ['nome-das-pessoas']:
         return 'Farmers'
    elif row['nome'] in ['nome-das-pessoas']:
         return 'Financeiro'
    elif row['nome'] in ['nome-das-pessoas']:
         return 'Administrativo'
        
df['setor'] = df.apply(atribuir_setor, axis=1)

setores_validos = ['Trials', 'NfeMais', 'Canais IB', 'Canais OB', 'Farmers', 'Financeiro'] 
df = df[df['setor'].isin(setores_validos)] 
