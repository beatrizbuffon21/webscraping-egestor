# ==================== Bibliotecas utilizadas ========================= #

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys #chaves
from selenium.webdriver.common.by import By #encontrar algo na página html
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC #ExpectedCondition
import pandas as pd #manipulação e tratamento dos dados extraídos
import re 

# ==================== Web scraping ========================= #

driver = webdriver.Chrome()

driver.get('https://www.exactsales.com.br/prelogin.html')

email_input = driver.find_element(by='xpath', value='//*[@id="email"]')
email_input.send_keys('email')

avancar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div[4]/div/button'))
)
avancar_button.click()

password_input = driver.find_element(by='xpath', value='//*[@id="Password"]')
password_input.send_keys('senha')

password_input.send_keys(Keys.RETURN)
primeiro_botao = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="page-content-wrapper"]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[2]'))
)
primeiro_botao.click()

segundo_botao = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[3]/ul/li[3]'))
)
segundo_botao.click()

elements = []

for i in range(1, 35):
    xpath = '//*[@id="desempenhoPreVendedoresDataTable"]/tbody/tr[{}]'.format(i)
    element = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
    )
    elements.append(element)

spotter = []

for i in range(1, 35):
    elements = locals()["elements" + str(i)]
    for element in elements:                                                                                                                                                                                                                                    
        numero = element.text
        spotter.append(numero)

dados = []
for elemento in spotter:
    partes = elemento.split('\n')
    print(partes)
    nome = partes[0]
    print(nome)
    numeros = []
    for part in partes[1:]:
        if part.isdigit():
            numeros.append(int(part))
    dados.append([nome] + numeros)

colunas = ['nome', 'cadastro', 'aplicacao_filtro2', 'agendamentos', 'feedbacks', 'vendas',
           'tempo_ligacao', 'reagendamentos', 'cancelamentos']

df = pd.DataFrame(dados, columns=colunas)
df = df[['nome', 'agendamentos', 'vendas']]
duplicadas = df.duplicated(subset='nome', keep=False)
df = df[~(duplicadas & duplicadas.shift())]

def limpar_nome(nome):
    padrao = r'^\W*'
    return re.sub(padrao, '', nome)
df['nome'] = df['nome'].apply(limpar_nome)
prefixos = ['Ca', 'Gu', 'Li', 'Na', 'Fer', 'Rod', 'Al', 'We']

def remover_prefixo(nome):
    padrao = r'^(' + '|'.join(prefixos) + r')\s'
    return re.sub(padrao, '', nome)

df['nome'] = df['nome'].apply(remover_prefixo)
df_spotter = df
