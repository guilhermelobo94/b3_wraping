from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd  # Importa a biblioteca pandas para criar o DataFrame


url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/ibov?language=pt-br'

chrome_options = Options()
chrome_options.add_argument('--headless')  # Executa o Chrome em modo headless
chrome_options.add_argument('--no-sandbox')  # Para ambientes sem GUI
chrome_options.add_argument('--disable-dev-shm-usage')  # Desativa o uso compartilhado da memória para evitar problemas em alguns ambientes


def extract_table_data(soup):
    # Encontrar a tabela pela classe
    table = soup.find('table', {'class': 'table table-responsive-sm table-responsive-md'})

    # Verificar se a tabela foi encontrada
    if table:
        # Extrair os cabeçalhos da tabela
        headers = [header.text.strip() for header in table.find_all('th')]

        # Filtrar o texto '%Setor' dos cabeçalhos se estiver presente
        headers = [header for header in headers if header != '%Setor']

        # Extrair as linhas de dados da tabela
        rows = []
        for row in table.find_all('tr')[1:]:  # Pular o cabeçalho
            cells = row.find_all('td')
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                # Verificar se a primeira célula da linha contém textos a serem ignorados
                if row_data[0] not in ['Quantidade Teórica Total', 'Redutor']:
                    # Remover '%Setor' dos dados, se estiver presente
                    row_data = [data for data in row_data if data != '%Setor']
                    rows.append(row_data)
        return headers, rows
    return [], []


driver = webdriver.Chrome()

try:
    # Abrir a página
    driver.get(url)

    # Esperar até que o select esteja presente
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "segment"))
    )

    # Selecionar o setor de atuação desejado
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

        # Usar BeautifulSoup para parsear o HTML
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extrair dados da tabela
        current_headers, rows = extract_table_data(soup)

        # Se os cabeçalhos forem encontrados e válidos
        if current_headers:
            if not headers:
                headers = current_headers  # Captura os cabeçalhos da primeira página
            else:
                # Verifica se os cabeçalhos são consistentes com os dados extraídos
                if len(current_headers) == len(headers):
                    all_data.extend(rows)
                else:
                    print(
                        f'Número de colunas inconsistentes: {len(current_headers)} colunas na página, '
                        f'{len(headers)} colunas esperadas.')

        # Tentar encontrar o botão de próxima página
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='pagination-next']/a"))
            )
            next_button.click()

            # Aguardar até que a nova página seja carregada
            time.sleep(1)

            # Verificar se a página mudou
            new_page_content = driver.page_source
            if new_page_content == page_content:
                break
            page_number += 1
        except Exception as e:
            break


    # Criar um DataFrame com os dados da tabela
    df = pd.DataFrame(all_data, columns=headers)

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv('dados_tabela.csv', index=False)

finally:
    driver.quit()


