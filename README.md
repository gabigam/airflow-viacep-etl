# Airflow ETL: Extração e Orquestração de Dados Postais (ViaCEP)

Este projeto demonstra a construção de um pipeline de ETL utilizando o Apache Airflow. O objetivo é consumir dados públicos de Endereçamento Postal (CEP) do Brasil através do webservice ViaCEP.

## ⚙️ Arquitetura e Componentes Técnicos

A pipeline é totalmente orquestrada pelo Airflow e utiliza o conceito de Hooks e Operators.

### 1. Custom Hook (`airflow_pipeline/hook/cep_hook.py`)

**`CepHook`**:  Gerencia a conexão HTTP com a API ViaCEP e trata erros de API. 

### 2. Custom Operator (`airflow_pipeline/operators/cep_operator.py`)

**`CepOperator`**: Executa a lógica de extração e persistência dos dados. Utiliza o `CepHook` para coletar dados de +50 CEPs e salva o resultado final em formato CSV. 

### 3. DAG (`dags/extracao_dados_viacep_dag.py`)

A DAG orquestra a execução da tarefa de extração e configura o caminho de saída no disco.



Entendido. Para quem está revisando seu projeto no GitHub, ou para você mesmo, o que é mais útil é o passo a passo de como rodar o ETL completo no Airflow, desde o `git clone` até a verificação do resultado final.

Aqui está o passo a passo completo, do início ao fim, focando no terminal e na execução da sua DAG.

## 🚀 Guia Rápido: Execução Completa do ETL Airflow

Este guia assume que você já tem o Git instalado e o Python 3.8+ configurado.

### 1. Preparação e Configuração do Projeto

| Comando | Descrição |
| :--- | :--- |
| `git clone https://github.com/gabigam/airflow-viacep-etl.git` | Clona o seu projeto do GitHub. |
| `cd airflow-viacep-etl` | Entra no diretório raiz do projeto. |
| `python3 -m venv venv` | Cria um ambiente virtual Python. |
| `source venv/bin/activate` | **Ativa** o ambiente virtual (necessário para os comandos `pip` e `airflow`). |
| `pip install -r requirements.txt` | Instala todas as dependências, incluindo o Airflow. |

### 2. Inicialização do Airflow Standalone

Usaremos o modo *standalone* para inicializar o banco de dados e rodar os componentes essenciais rapidamente.

| Comando | Descrição |
| :--- | :--- |
| `airflow standalone` | Inicializa o Airflow (Webserver e Scheduler). O sistema cria a pasta `airflow.cfg` e o banco de dados. |
| *(Após a inicialização, pressione `Ctrl + C`)* | Para o Webserver e Scheduler, permitindo rodá-los separadamente. |

### 3. Rodar Componentes (Em Terminais Separados)

**Importante:** Repita o comando `source venv/bin/activate` em CADA NOVO terminal.

| Terminal 1: Webserver | Terminal 2: Scheduler |
| :--- | :--- |
| `source venv/bin/activate` | `source venv/bin/activate` |
| `airflow webserver --port 8080` | `airflow scheduler` |

### 4. Configuração da Conexão e Deploy

Com o Webserver rodando (`http://localhost:8080`), você deve configurar a conexão e garantir que as DAGs sejam lidas.

1.  **Deploy dos Arquivos:** O `scheduler` deve reconhecer automaticamente as DAGs e Hooks/Operators, pois eles estão no diretório do Airflow.
2.  **Configurar Conexão:**
    * Acesse a UI (`http://localhost:8080`), faça login (`airflow`/`airflow`).
    * Crie uma **Conexão HTTP** com **ID** `viacep_default` e **Host** `https://viacep.com.br`.

### 5. Execução da DAG (O ETL)

1.  Na UI do Airflow, ligue a DAG `extracao_dados_viacep`.
2.  Dispare a DAG manualmente (clique no botão **Play**).
3.  Aguarde o status da tarefa `extracao_ceps_viacep` mudar para **Sucesso (Success)**.

### 6. Verificação do Resultado (O Arquivo CSV)

Verifique se o arquivo CSV com o resultado do seu ETL foi criado no diretório esperado.

| Comando | Descrição |
| :--- | :--- |
| `ls -R datalake/` | Lista o conteúdo da pasta `datalake` de forma recursiva. |
| `cat datalake/viacep/raw/extract_date=[DATA_HOJE]/ceps_extraidos_[DATA_HOJE].csv` | Exibe o conteúdo do CSV extraído. |
