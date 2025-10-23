from airflow.providers.http.hooks.http import HttpHook
from airflow.exceptions import AirflowException
import requests
import json
import time
from typing import List, Dict, Any, Generator, Tuple 
import logging 



class CepHook(HttpHook):

    def __init__(self, ceps: List[str], conn_id: str = "viacep_default"):
        self.ceps = ceps
        self.http_conn_id = conn_id 
        
        super().__init__(method="GET", http_conn_id=conn_id)

        self.fallback_base_url = "https://viacep.com.br"
        self.sleep_time = 0.1
        self.timeout = 1.0 

    def get_conn(self) -> requests.Session:
        return super().get_conn() 

    def connect_to_endpoint(self, endpoint: str, session: requests.Session) -> requests.Response:
        req = requests.Request(self.method, endpoint)
        
        prep = session.prepare_request(req)
        
        self.log.info(f"Endpoint: {endpoint}")
        
    
        return self.run_and_check(
            session=session,
            prepped_request=prep,
    
            extra_options={"timeout": self.timeout} 
        )
    
    def run(self) -> List[List[Dict[str, Any]]]:
        dados_extraidos: List[Dict[str, Any]] = []
        
        session = self.get_conn() 
        
   
        base_url = self.base_url 
        
       
        if not base_url:
            base_url = self.fallback_base_url
            self.log.warning(f"self.base_url não encontrado. Usando fallback: {base_url}")
            
      
        if base_url.endswith('/'):
            base_url = base_url[:-1]
            
        self.log.info(f"Iniciando extração para {len(self.ceps)} CEPs. Base URL: {base_url}")

        for cep in self.ceps:
          
            endpoint = f"{base_url}/ws/{cep}/json/" 
            
            try:
                response = self.connect_to_endpoint(endpoint, session)
                
                try:
                    json_response = response.json()
                except json.JSONDecodeError:
                    self.log.error(f"Resposta inválida para o CEP {cep}. Conteúdo: {response.text[:100]}")
                    raise AirflowException(f"Falha ao decodificar JSON para o CEP {cep}.")
                
                if json_response.get('erro'):
                    self.log.warning(f"CEP {cep} inválido ou não encontrado. Pulando. URL: {endpoint}")
                    continue
                
                self.log.info(f"CEP {cep} extraído com sucesso.")
                dados_extraidos.append(json_response)

            except AirflowException as e:
                self.log.error(f"ERRO DE REQUISIÇÃO/PROXY/STATUS ao buscar CEP {cep}: {e}")
                raise 
                
            except Exception as e:
                self.log.error(f"Erro inesperado ao processar CEP {cep}: {e}")
                raise AirflowException(f"Erro inesperado no Hook: {e}")
            
            time.sleep(self.sleep_time) 
            
        self.log.info(f"Extração concluída. Total de {len(dados_extraidos)} registros válidos.")
   
        return [dados_extraidos]



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    CEPS_PARA_TESTE = ["01001000", "70040906", "99999999"] 
    print("--- Testando CepHook (Simulação Airflow) ---")
    try:
      
        hook = CepHook(ceps=CEPS_PARA_TESTE, conn_id="viacep_default")
        resultados_encapsulados = hook.run() 
        resultados = resultados_encapsulados[0] if resultados_encapsulados and resultados_encapsulados[0] else []
        print("\n--- Resultados Finais ---")
        print(f"Total de CEPs válidos extraídos: {len(resultados)}")
        print(json.dumps(resultados, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Falha fatal no Hook: {e}")