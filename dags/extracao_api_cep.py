from datetime import datetime, timedelta
from airflow.models import DAG
from os.path import join
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_dir)


if project_root not in sys.path:
    sys.path.insert(0, project_root) 


from airflow_pipeline.operators.cep_operator import CepOperator


CEPS_DE_TESTE = [
    # ============== Ceps Originais / Existentes ==============
    "01001000", # SP - Praça da Sé (Região 0)
    "20010000", # RJ - Rua Primeiro de Março (Região 2)
    "70040906", # DF - Setor de Autarquias Sul (Região 7)
    "40020000", # BA - Rua Carlos Gomes (Região 4)
    "57020000", # AL - Centro de Maceió (Região 5)
    "49050170", # SE - Bairro Ponto Novo (Região 4)
    "99999999", # CEP Inválido/Não Encontrado

    # ============== NOVOS CEPS (Expandindo a Cobertura) ==============

    # REGIÃO 0 - Grande São Paulo
    "05423000", # SP - Pinheiros, São Paulo (capital)
    "09720000", # SP - São Bernardo do Campo (região metropolitana)

    # REGIÃO 1 - Interior de São Paulo
    "13013002", # SP - Campinas
    "14010000", # SP - Ribeirão Preto
    "17500000", # SP - Marília (CEP geral para a cidade)

    # REGIÃO 2 - Rio de Janeiro e Espírito Santo
    "29050910", # ES - Vitória, Enseada do Suá
    "28010000", # RJ - Campos dos Goytacazes (interior)
    "27253005", # RJ - Volta Redonda (interior)

    # REGIÃO 3 - Minas Gerais
    "30180060", # MG - Belo Horizonte (capital)
    "38400000", # MG - Uberlândia (interior)
    "35700000", # MG - Sete Lagoas (interior)

    # REGIÃO 4 - Bahia e Sergipe
    "41830460", # BA - Salvador, Pituba (capital)
    "44001000", # BA - Feira de Santana (interior)

    # REGIÃO 5 - Nordeste Central (PE, AL, PB, RN)
    "50030260", # PE - Recife (capital)
    "58010000", # PB - João Pessoa (capital)
    "59010000", # RN - Natal (capital)
    "55000000", # PE - Caruaru (interior)

    # REGIÃO 6 - Nordeste Setentrional e Região Norte (CE, PI, MA, PA, AM, AC, AP, RR)
    "60125040", # CE - Fortaleza (capital)
    "64000000", # PI - Teresina (capital)
    "65000000", # MA - São Luís (capital)
    "66025050", # PA - Belém (capital)
    "69005000", # AM - Manaus (capital)
    "69301020", # RR - Boa Vista (capital)
    "68900000", # AP - Macapá (capital)
    "69900000", # AC - Rio Branco (capital)

    # REGIÃO 7 - Centro-Oeste e Norte (DF, GO, TO, MT, MS, RO)
    "74000000", # GO - Goiânia (capital)
    "77001000", # TO - Palmas (capital)
    "78005400", # MT - Cuiabá (capital)
    "79000000", # MS - Campo Grande (capital)
    "76801380", # RO - Porto Velho (capital)
    "73800000", # GO - Formosa (interior)
    "78700000", # MT - Rondonópolis (interior)

    # REGIÃO 8 - Sul (PR e SC)
    "80010000", # PR - Curitiba (capital)
    "88010000", # SC - Florianópolis (capital)
    "80000000", # PR - CEP genérico de Curitiba
    "89000000", # SC - Blumenau (interior)

    # REGIÃO 9 - Rio Grande do Sul
    "90010000", # RS - Porto Alegre (capital)
    "95000000", # RS - Caxias do Sul (interior)
    "96000000", # RS - Pelotas (interior)
    "90010902", # RS - Porto Alegre, Caixa Postal Comunitária

    # ============== Casos Especiais / Fronteira ==============
    "29999999", # ES - Último CEP da faixa (limite de região)
    "30000000", # MG - Primeiro CEP da faixa (limite de região)
    "70000000", # DF - CEP genérico de Brasília (Região 7)
    "72000000", # DF - Taguatinga, área administrativa
    "68925000", # AP - Santana (CEP único por município)
    "83490000", # PR - Adrianópolis (CEP único por município)
    "01311000", # SP - Av. Paulista (CEP com variação par/ímpar)

    # Ceps de Aeroportos (grandes centros logísticos)
    "07190100", # SP - Aeroporto de Guarulhos
    "21941900", # RJ - Aeroporto do Galeão
    "83010900"  # PR - Aeroporto Afonso Pena (Curitiba)
]

with DAG(
    dag_id="extracao_dados_viacep",
    start_date=datetime(2025, 1, 1), 
    schedule_interval=None,         
    catchup=False,                   
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
) as dag:
    
    
    extraction_date = '{{ ds }}' 
    
    file_output_path = join(
        "datalake/viacep/raw", 
        f"extract_date={extraction_date}", 
        f"ceps_extraidos_{extraction_date}.csv"
    )
    

    extracao_cep = CepOperator(
        task_id="extrair_ceps_brasil",
   
        ceps=CEPS_DE_TESTE,

        file_path=file_output_path
    )