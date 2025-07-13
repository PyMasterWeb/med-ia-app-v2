#!/usr/bin/env python3
"""
Script para atualização automática do cache de doenças do Datasus
Pode ser executado diariamente via cron/task scheduler
"""

import os
import sys
import time
from datetime import datetime

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from routes.disease import scraping_doencas, salvar_doencas_local

def main():
    """Função principal para atualizar o cache"""
    print(f"Iniciando atualização do cache de doenças - {datetime.now()}")
    
    try:
        # Fazer scraping das doenças
        doencas = scraping_doencas()
        
        if doencas:
            # Salvar no cache
            salvar_doencas_local(doencas)
            print(f"Cache atualizado com sucesso! {len(doencas)} doenças salvas.")
        else:
            print("Erro: Nenhuma doença foi extraída do Datasus")
            return 1
            
    except Exception as e:
        print(f"Erro durante a atualização: {e}")
        return 1
    
    print("Atualização concluída com sucesso!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 