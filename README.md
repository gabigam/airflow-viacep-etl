# 🇧🇷 Airflow ETL: Extração e Orquestração de Dados Postais (ViaCEP)

Este projeto demonstra a construção de um pipeline de ETL utilizando o Apache Airflow. O objetivo é consumir dados públicos de Endereçamento Postal (CEP) do Brasil através do webservice ViaCEP.

## ⚙️ Arquitetura e Componentes Técnicos

A pipeline é totalmente orquestrada pelo Airflow e utiliza o conceito de Hooks e Operators customizados, seguindo o padrão de projeto para componentes de terceiros.

### 1. Custom Hook (`airflow_pipeline/hook/cep_hook.py`)

**`CepHook`**:  Gerencia a conexão HTTP com a API ViaCEP e trata erros de API. 

### 2. Custom Operator (`airflow_pipeline/operators/cep_operator.py`)

**`CepOperator`**: Executa a lógica de extração e persistência dos dados. Utiliza o `CepHook` para coletar dados de +50 CEPs e salva o resultado final em formato CSV. 

### 3. DAG (`dags/extracao_dados_viacep_dag.py`)

A DAG orquestra a execução da tarefa de extração e configura o caminho de saída no disco.

