import sys
from airflow.models import BaseOperator
from airflow_pipeline.hook.cep_hook import CepHook
from typing import List, Dict, Any, Optional
import csv
from os.path import join

class CepOperator(BaseOperator):
    
    def __init__(self, ceps: List[str], file_path: Optional[str] = None, **kwargs):
        self.ceps = ceps
        self.file_path = file_path 
        super().__init__(**kwargs)
        
    def execute(self, context): 
        
        if not self.file_path:
             raise ValueError("O parâmetro 'file_path' (caminho de saída do CSV) deve ser fornecido.")
             
        self.log.info(f"Iniciando extração do ViaCEP para o arquivo: {self.file_path}")

        hook_result = CepHook(ceps=self.ceps).run()
        

        dados_extraidos: List[Dict[str, Any]] = hook_result[0] if hook_result and hook_result[0] else []
        
        if not dados_extraidos:
            self.log.warning("Nenhum dado válido foi extraído da API ViaCEP.")

            campos = ['cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'ibge', 'gia'] 
            with open(self.file_path, 'w', newline='', encoding='utf-8') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=campos)
                writer.writeheader()
            return
            

        

        campos = list(dados_extraidos[0].keys())
        
        self.log.info(f"Escrevendo {len(dados_extraidos)} registros no arquivo: {self.file_path}")
        
   
        import os
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=campos)
            writer.writeheader()  
            writer.writerows(dados_extraidos) 
            
        self.log.info(f"Extração do ViaCEP concluída. Dados salvos em: {self.file_path}")



if __name__ == "__main__":
    from datetime import datetime
    
    CEPS_PARA_TESTE = ["01001000", "70040906"] 
    test_file_path = join("temp", f"ceps_extraidos_test_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    
    print(f"--- Executando CepOperator para teste local. Saída em: {test_file_path} ---")

    cep_op = CepOperator(
        task_id="teste_cep_run",
        ceps=CEPS_PARA_TESTE,
        file_path=test_file_path
    )
    
    try:
        cep_op.execute(context={}) 
        print(f"--- Teste do CepOperator concluído. Arquivo criado em: {test_file_path} ---")
    except Exception as e:
        print(f"❌ Falha no teste do CepOperator: {e}")