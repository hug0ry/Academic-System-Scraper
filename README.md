# 🚀 SIGAA Extension Scraper: Automação de Inteligência Acadêmica

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-informational.svg)](https://pandas.pydata.org/)

## 📋 Sobre o Projeto

Este projeto foi desenvolvido para automatizar a coleta e o levantamento de dados dos projetos de extensão universitária no sistema SIGAA. 

### 💡 O Problema
Anteriormente, o levantamento de dados era feito **manualmente** por toda a equipe do setor de extensão. Milhares de projetos eram divididos entre funcionários que entravam um a um no sistema para extrair informações. Esse processo era:
* **Lento:** Levava dias ou semanas para ser concluído, comprometendo a mão de obra dos servidores.
* **Suscetível a erros:** A coleta manual aumentava o risco de dados inconsistentes.
* **Custo operacional alto:** Desviava a equipe de tarefas analíticas para tarefas repetitivas.
 
Lembrando que essa é uma versão refatorada do projeto, preservando dados sensiveis do sistema da UFPB, apenas para demonstração dos métodos utilizados na realização do projeto, podendo ser personalizado para outros sistemas.
### ✨ A Solução
Com este scraper, o processo foi transformado em uma **operação de minutos**. O bot realiza o login, navega pelos menus acadêmicos e extrai automaticamente dados como:
* Título do Projeto e Edital.
* Nome do Coordenador.
* **Locais de Realização (Cidades e Estados, bairros, departamentos e etc):** Principal foco para análise de capilaridade e alcance da extensão.



---

## 📊 Impacto e Resultados
Os dados estruturados permitem que a gestão universitária:
1.  **Mapeie o Alcance:** Identificar quantas cidades e estados diferentes são atendidos.
2.  **Dashboards de Gestão:** Alimentar relatórios visuais e Power BI para identificar gargalos.
3.  **Identificação de Pontos Cegos:** Visualizar áreas geográficas com baixa concentração de projetos para expansão estratégica.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem base.
* **Selenium WebDriver:** Automação da navegação e interação com o sistema.
* **Pandas:** Estruturação e limpeza dos dados coletados.
* **Python-dotenv:** Gerenciamento seguro de credenciais e variáveis de ambiente.

---

## ⚙️ Configuração e Instalação

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Google Chrome instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/Academic-System-Scraper.git](https://github.com/seu-usuario/Academic-System-Scraper.git)
    cd Academic-System-Scraper
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as credenciais:**
    * Renomeie o arquivo `.env.example` para `.env`.
    * Insira seu usuário e senha do SIGAA no arquivo `.env`.
    > **Nota:** O arquivo `.env` está no `.gitignore` e nunca será enviado para o repositório por questões de segurança.

4.  **Execute o script:**
    ```bash
    python academic_scrapper.py
    ```

---

## 🏗️ Estrutura do Projeto

* `academic_scrapper.py`: Script principal de automação.
* `.env`: Armazenamento seguro de credenciais (local).
* `.gitignore`: Proteção de arquivos sensíveis e temporários.
* `local_survey_2025.xlsx`: Arquivo gerado com os dados consolidados.

---

## 👨‍💻 Desenvolvedor
* **Hugo Ryan** - https://www.linkedin.com/in/hugo-ryan-9b5621201/
