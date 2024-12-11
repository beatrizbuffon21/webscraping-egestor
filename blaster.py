# ==================== Bibliotecas utilizadas ========================= #

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# ==================== Web scraping ========================= #

driver = webdriver.Chrome()
driver.get('http://blaster.zipline.com.br/implementacoes/')

email_input = driver.find_element(by='xpath', value='//*[@id="login_user"]')
email_input.send_keys('usuario')

password_input = driver.find_element(by='xpath', value='//*[@id="login_pass"]')
password_input.send_keys('senha')

avancar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="login_btnIn"]'))
)
avancar_button.click()

colunas = ['nome', 'concluidas', 'reagendadas', 
           'nao_quer', 'no_show', 'em_andamento',
           'cliente_contatara', 'concluidas_agrupado', 'total']

elements1 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[1]'))
)

for element in elements1:                                                                                                                                                                                                                                    
    numero1 = element.text
    dados_separados1 = numero1.split()
    nome1 = ' '.join(dados_separados1[:3])
    dados_finais1 = [nome1] + dados_separados1[3:]

elements2 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[2]'))
)

for element in elements2:                                                                                                                                                                                                                                    
    numero2 = element.text
    dados_separados2 = numero2.split()
    nome2 = ' '.join(dados_separados2[:2])
    dados_finais2 = [nome2] + dados_separados2[2:]

elements3 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[3]'))
)

for element in elements3:                                                                                                                                                                                                                                    
    numero3 = element.text
    dados_separados3 = numero3.split()
    nome3 = ' '.join(dados_separados3[:5])
    dados_finais3 = [nome3] + dados_separados3[5:]

elements4 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[4]'))
)

for element in elements4:                                                                                                                                                                                                                                    
    numero4 = element.text
    dados_separados4 = numero4.split()
    nome4 = ' '.join(dados_separados4[:2])
    dados_finais4 = [nome4] + dados_separados4[2:]

elements5 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[5]'))
)

for element in elements5:                                                                                                                                                                                                                                    
    numero5 = element.text
    dados_separados5 = numero5.split()
    nome5 = ' '.join(dados_separados5[:5])
    dados_finais5 = [nome5] + dados_separados5[5:]

elements6 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[6]'))
)

for element in elements6:                                                                                                                                                                                                                                    
    numero6 = element.text
    dados_separados6 = numero6.split()
    nome6 = ' '.join(dados_separados6[:4])
    dados_finais6 = [nome6] + dados_separados6[4:]

elements7 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[7]'))
)

for element in elements7:                                                                                                                                                                                                                                    
    numero7 = element.text
    dados_separados7 = numero7.split()
    nome7 = ' '.join(dados_separados7[:5])
    dados_finais7 = [nome7] + dados_separados7[5:]

elements8 = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="divLista"]/table/tbody/tr[8]'))
)

for element in elements8:                                                                                                                                                                                                                                    
    numero8 = element.text
    dados_separados8 = numero8.split()
    nome8 = ' '.join(dados_separados8[:4])
    dados_finais8 = [nome8] + dados_separados8[4:]


df_blaster = pd.DataFrame([dados_finais1, dados_finais2, dados_finais3,dados_finais4,
                           dados_finais5, dados_finais6, dados_finais7, dados_finais8],
                           columns=['nome', 'concluidas', 'reagendadas','nao_quer',
                                    'no_show', 'em_andamento', 'cliente_contatara', 'concluidas_agrupado', 'total'])

print(df_blaster)
