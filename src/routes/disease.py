from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re

# Definição do blueprint
disease_bp = Blueprint('disease', __name__)

_DOENCAS_CACHE_FILE = 'doencas_cache.json'
_DOENCAS_UPDATE_INTERVAL = 24 * 60 * 60  # 24 horas
_doencas_last_update = 0

def carregar_doencas_local():
    global _doencas_last_update
    if os.path.exists(_DOENCAS_CACHE_FILE):
        try:
            with open(_DOENCAS_CACHE_FILE, encoding='utf-8') as f:
                data = json.load(f)
                _doencas_last_update = data.get('last_update', 0)
                return data.get('doencas', [])
        except Exception:
            return []
    return []

def salvar_doencas_local(doencas):
    global _doencas_last_update
    _doencas_last_update = int(time.time())
    with open(_DOENCAS_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'doencas': doencas, 'last_update': _doencas_last_update}, f, ensure_ascii=False)

def scraping_doencas():
    """Faz scraping das doenças do Datasus - Tabela 2"""
    url = "http://tabnet.datasus.gov.br/cgi/sih/mxcid10lm.htm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        print("Iniciando scraping do Datasus...")
        response = requests.get(url, timeout=30, headers=headers)
        response.encoding = 'latin1'
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        
        print(f'Encontradas {len(tables)} tabelas no HTML do Datasus')
        
        # Usar a Tabela 2 (índice 1) que contém as doenças
        if len(tables) > 1:
            table = tables[1]  # Tabela 2
            rows = table.find_all('tr')
            print(f'Tabela 2 tem {len(rows)} linhas')
            
            doencas = []
            for i, row in enumerate(rows[1:], 1):  # Pular cabeçalho
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Extrair código sequencial, nome da doença e CID
                    codigo_seq = cols[0].get_text(strip=True)
                    nome_doenca = cols[1].get_text(strip=True)
                    cid = cols[2].get_text(strip=True)
                    
                    # Limpar e validar dados
                    if codigo_seq and nome_doenca and cid:
                        # Determinar categoria baseada no CID
                        categoria = "Não especificada"
                        if cid.startswith('A') or cid.startswith('B'):
                            categoria = "Doenças infecciosas e parasitárias"
                        elif cid.startswith('C') or cid.startswith('D'):
                            categoria = "Neoplasias"
                        elif cid.startswith('E'):
                            categoria = "Doenças endócrinas, nutricionais e metabólicas"
                        elif cid.startswith('F'):
                            categoria = "Transtornos mentais e comportamentais"
                        elif cid.startswith('G'):
                            categoria = "Doenças do sistema nervoso"
                        elif cid.startswith('H'):
                            categoria = "Doenças do olho e anexos"
                        elif cid.startswith('I'):
                            categoria = "Doenças do aparelho circulatório"
                        elif cid.startswith('J'):
                            categoria = "Doenças do aparelho respiratório"
                        elif cid.startswith('K'):
                            categoria = "Doenças do aparelho digestivo"
                        elif cid.startswith('L'):
                            categoria = "Doenças da pele e tecido subcutâneo"
                        elif cid.startswith('M'):
                            categoria = "Doenças do sistema osteomuscular"
                        elif cid.startswith('N'):
                            categoria = "Doenças do aparelho geniturinário"
                        elif cid.startswith('O'):
                            categoria = "Condições originadas no período perinatal"
                        elif cid.startswith('P'):
                            categoria = "Condições originadas no período perinatal"
                        elif cid.startswith('Q'):
                            categoria = "Malformações congênitas"
                        elif cid.startswith('R'):
                            categoria = "Sintomas, sinais e achados anormais"
                        elif cid.startswith('S') or cid.startswith('T'):
                            categoria = "Lesões, envenenamentos e outras consequências"
                        elif cid.startswith('V') or cid.startswith('W') or cid.startswith('X') or cid.startswith('Y'):
                            categoria = "Causas externas de morbidade"
                        elif cid.startswith('Z'):
                            categoria = "Fatores que influenciam o estado de saúde"
                        
                        doenca = {
                            'codigo_seq': codigo_seq,
                            'nome': nome_doenca,
                            'cid': cid,
                            'categoria': categoria
                        }
                        doencas.append(doenca)
                        
                        if i <= 10:  # Mostrar apenas as primeiras 10 para debug
                            print(f"Linha {i}: {codigo_seq} - {nome_doenca} ({cid}) - {categoria}")
            
            print(f"Total de doenças extraídas: {len(doencas)}")
            
            if doencas:
                # Salvar no cache
                salvar_doencas_local(doencas)
                print(f"Cache salvo com {len(doencas)} doenças")
                return doencas
            else:
                print("Nenhuma doença foi extraída")
                return None
        else:
            print("Tabela 2 não encontrada")
            return None
            
    except Exception as e:
        print(f'Erro ao fazer scraping do Datasus: {e}')
        return None

def atualizar_doencas_automaticamente():
    global _doencas_last_update
    agora = int(time.time())
    if (agora - _doencas_last_update) > _DOENCAS_UPDATE_INTERVAL:
        scraping_doencas()

@disease_bp.route('/doencas', methods=['GET'])
def get_doencas():
    atualizar_doencas_automaticamente()
    doencas = carregar_doencas_local()
    if doencas:
        return jsonify(doencas)
    else:
        return jsonify({"erro": "Lista de doenças não encontrada. Tente novamente mais tarde."}), 404