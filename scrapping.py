from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/ibov?language=pt-br'

chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--log-level=3")  # Reduz a verbosidade dos logs do Chrome



def extract_table_data(soup):
    table = soup.find('table', {'class': 'table table-responsive-sm table-responsive-md'})

    if table:
        headers = [header.text.strip() for header in table.find_all('th')]

        headers = [header for header in headers if header != '%Setor']

        rows = []
        for row in table.find_all('tr')[1:]:  # Pular o cabeçalho
            cells = row.find_all('td')
            if cells:
                row_data = [cell.text.strip() for cell in cells]

                if row_data[0] not in ['Quantidade Teórica Total', 'Redutor']:
                    row_data = [data for data in row_data if data != '%Setor']
                    rows.append(row_data)
        return headers, rows
    return [], []


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get(url)

    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "segment"))
    )

    select = Select(select_element)
    select.select_by_visible_text("Setor de Atuação")  # Altere o texto conforme necessário

    # Aguarde alguns segundos para a página carregar os novos dados (ajuste conforme necessário)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-responsive-md"))
    )

    all_data = []
    headers = []
    page_number = 1

    while True:
        # Extrair o conteúdo da página
        page_content = driver.page_source

        soup = BeautifulSoup(page_content, 'html.parser')

        current_headers, rows = extract_table_data(soup)

        if current_headers:
            if not headers:
                headers = current_headers
            else:

                if len(current_headers) == len(headers):
                    all_data.extend(rows)
                else:
                    print(
                        f'Número de colunas inconsistentes: {len(current_headers)} colunas na página, '
                        f'{len(headers)} colunas esperadas.')

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='pagination-next']/a"))
            )
            next_button.click()

            time.sleep(1)

            new_page_content = driver.page_source
            if new_page_content == page_content:
                break
            page_number += 1
        except Exception:
            break

    df = pd.DataFrame(all_data, columns=headers)

    df.to_csv('dados_tabela.csv', index=False)

finally:
    driver.quit()
