# ==================== Bibliotecas utilizadas ========================= #

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# ==================== Web scraping ========================= #

driver = webdriver.Chrome()

driver.get('https://app.rdstation.com.br/dashboard')

email_input = driver.find_element(by='xpath', value='//*[@id="email"]')
email_input.send_keys('email')

password_input = driver.find_element(by='xpath', value='//*[@id="password"]')
password_input.send_keys('senha')

password_input.send_keys(Keys.RETURN)
wait = WebDriverWait(driver, 10)

elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "data-block-value"))
)

rdstation = []
for element in elements:
    numero = element.text
    rdstation.append(numero)
    print(rdstation)

login_form = driver.find_element(By.XPATH, '//*[@id="rdsm-dashboard"]/div/div[1]/section[1]/div/div[3]/span')
novos_leads = login_form.text
print(novos_leads)

rdstation = [float(numero) for numero in rdstation]
novos_leads = novos_leads[:5].split()[:5]

dados = {
    'visitantes': (rdstation[0]),
    'leads': (rdstation[1]),
    'vendas': (rdstation[2]),
    'novos_leads': (novos_leads[0])
}

df = pd.DataFrame(dados, index=[0])
