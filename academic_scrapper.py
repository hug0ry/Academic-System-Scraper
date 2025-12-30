import os 
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Carrega credenciais e URL de um arquivo .env (opcional para segurança)
load_dotenv()

class SigaaExtensaoBot:
    def __init__(self):
        self.driver = self._configurar_browser()
        self.wait = WebDriverWait(self.driver, 25)
        self.short_wait = WebDriverWait(self.driver, 8)
        self.projetos_geral = []

    def _configurar_browser(self):
        options = ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def login(self, url, user, password):
        print(f"Acessando portal...")
        self.driver.get(url)
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "form:login"))).send_keys(user)
            self.driver.find_element(By.ID, "form:senha").send_keys(password)
            self.driver.find_element(By.ID, "form:entrar").click()
            print("Login realizado.")
            return True
        except Exception as e:
            print(f"Erro no login: {e}")
            return False

    def navegar_ate_busca(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//strong[contains(., 'Servidor')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Módulos"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Extensão']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "menuExtensao:buscarAcoes"))).click()
            return True
        except Exception as e:
            print(f"Erro na navegação: {e}")
            return False

    def extrair_dados_locais(self):
        """Extrai TODAS as informações da tabela de locais de realização."""
        dados_locais = {
            'estados': "Tabela ausente", 
            'municipios': "Tabela ausente",
            'bairros': "Tabela ausente", 
            'locais_realizacao': "Tabela ausente"
        }
        
        try:
            # Tenta localizar a tabela e as linhas de dados (dentro do tbody)
            tabela = self.short_wait.until(EC.presence_of_element_located((By.ID, "tbLocaisRealizacao")))
            linhas = tabela.find_elements(By.XPATH, ".//tbody/tr")
            
            l_est, l_mun, l_bai, l_esp = [], [], [], []

            for linha in linhas:
                cols = linha.find_elements(By.TAG_NAME, "td")
                
                # Verifica se a linha tem as 4 colunas esperadas
                if len(cols) >= 4:
                    # Captura o texto e limpa espaços extras
                    estado = cols[0].text.strip()
                    municipio = cols[1].text.strip()
                    bairro = cols[2].text.strip()
                    espaco = cols[3].text.strip()

                    # Só adiciona se o campo "Espaço" (o principal) não estiver vazio
                    if espaco:
                        l_est.append(estado if estado else "N/I")
                        l_mun.append(municipio if municipio else "N/I")
                        l_bai.append(bairro if bairro else "N/I")
                        l_esp.append(espaco)

            # Se encontrámos dados, juntamos tudo com " | "
            if l_esp:
                dados_locais['estados'] = " | ".join(l_est)
                dados_locais['municipios'] = " | ".join(l_mun)
                dados_locais['bairros'] = " | ".join(l_bai)
                dados_locais['locais_realizacao'] = " | ".join(l_esp)
                
        except TimeoutException:
            # Se a tabela não existir para este projeto específico
            pass
        except Exception as e:
            print(f"Erro ao extrair locais: {e}")
            
        return dados_locais

    def processar_edital(self, edital_val, edital_nome, status_lista, d_inicio, d_fim):
        print(f"\n--- Iniciando Edital: {edital_nome} ---")
        
        self.navegar_ate_busca()
        
        Select(self.wait.until(EC.visibility_of_element_located((By.ID, "formBuscaAtividade:buscaEdital")))).select_by_value(edital_val)
        
        # Datas
        f_ini = self.driver.find_element(By.ID, "formBuscaAtividade:dataInicio")
        f_ini.clear()
        f_ini.send_keys(d_inicio)
        f_fim = self.driver.find_element(By.ID, "formBuscaAtividade:dataFim")
        f_fim.clear()
        f_fim.send_keys(d_fim)

        # Status Múltiplo
        sel_status = Select(self.driver.find_element(By.ID, "formBuscaAtividade:buscaSituacao"))
        sel_status.deselect_all()
        for s in status_lista:
            sel_status.select_by_value(s)

        self.driver.find_element(By.ID, "formBuscaAtividade:btBuscar").click()

        try:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Visualizar Ação']")))
            total = len(self.driver.find_elements(By.CSS_SELECTOR, "a[title='Visualizar Ação']"))
            
            for i in range(2):
                # Recarregar elementos para evitar Stale Exception
                botoes = self.driver.find_elements(By.CSS_SELECTOR, "a[title='Visualizar Ação']")
                nomes = self.driver.find_elements(By.XPATH, "//td[i[contains(text(), 'Coordenador')]]")
                stats = self.driver.find_elements(By.XPATH, "//td[i[contains(text(), 'Coordenador')]]/following-sibling::td[2]")

                nome_proj = nomes[i].text.split('\n')[0].strip()
                status_atual = stats[i].text.strip()
                
                print(f"Extraindo [{i+1}/{total}]: {nome_proj[:40]}...")
                botoes[i].click()

                # Coleta Detalhada
                coord_xpath = "//th[contains(text(), 'Coordenação')]/following-sibling::td"
                coord = self.wait.until(EC.visibility_of_element_located((By.XPATH, coord_xpath))).text.strip()
                
                locais = self.extrair_dados_locais()
                
                # Montagem do dicionário conforme colunas originais
                projeto_data = {
                    'edital': edital_nome,
                    'projeto': nome_proj,
                    'coordenador': coord,
                    'status': status_atual,
                    **locais
                }
                
                self.projetos_geral.append(projeto_data)
                self.driver.back()
                self.wait.until(EC.visibility_of_element_located((By.ID, "formBuscaAtividade:btBuscar")))

        except TimeoutException:
            print("Nenhum resultado encontrado para este filtro.")

    def exportar(self, nome_arq):
        if self.projetos_geral:
            df = pd.DataFrame(self.projetos_geral)
            colunas = ['edital', 'projeto', 'coordenador', 'status', 'estados', 'municipios', 'bairros', 'locais_realizacao']
            df = df[[c for c in colunas if c in df.columns]]
            df.to_excel(nome_arq, index=False)
            print(f"\nSucesso! {len(df)} registros salvos em {nome_arq}")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    URL = os.getenv("URL_SISTEMA")
    USUARIO = os.getenv("SIGAA_USER")
    SENHA = os.getenv("SIGAA_PASS")

    EDITAIS = [('92', 'Edital 92/2025'), ('93', 'Edital 93/2025')] # Exemplo de tuplas (id, nome)
    STATUS = ['117', '103', '105']

    bot = SigaaExtensaoBot()
    if bot.login(URL, USUARIO, SENHA):
        for id_ed, nome_ed in EDITAIS:
            bot.processar_edital(id_ed, nome_ed, STATUS, "01/01/2025", "31/12/2025")
        
        bot.exportar("Levantamento_Completo_2025.xlsx")
    bot.driver.quit()