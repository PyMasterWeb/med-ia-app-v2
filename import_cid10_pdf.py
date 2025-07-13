import json
import time
import re
from pathlib import Path
import PyPDF2
import requests

def extract_from_pdf(pdf_path):
    """Extrai dados do PDF do CID-10"""
    print(f"📖 Extraindo dados do PDF: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            diseases = []
            codigo_seq = 1
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Padrão para encontrar códigos CID-10 e descrições
                # Formato típico: A00.0 - Descrição da doença
                pattern = r'([A-Z]\d{2}(?:\.\d+)?)\s*[-–]\s*([^\n]+)'
                matches = re.findall(pattern, text)
                
                for match in matches:
                    cid_code = match[0].strip()
                    description = match[1].strip()
                    
                    # Determinar categoria baseada no código
                    categoria = get_categoria_by_cid(cid_code)
                    
                    disease = {
                        "codigo_seq": str(codigo_seq),
                        "nome": description,
                        "cid": cid_code,
                        "categoria": categoria
                    }
                    
                    diseases.append(disease)
                    codigo_seq += 1
                    
                    if codigo_seq % 100 == 0:
                        print(f"✅ Processadas {codigo_seq} doenças...")
            
            return diseases
            
    except Exception as e:
        print(f"❌ Erro ao processar PDF: {e}")
        return []

def get_categoria_by_cid(cid_code):
    """Determina a categoria baseada no código CID"""
    categoria_map = {
        'A': 'Doenças infecciosas e parasitárias',
        'B': 'Doenças infecciosas e parasitárias', 
        'C': 'Neoplasias',
        'D': 'Doenças do sangue e órgãos hematopoéticos',
        'E': 'Doenças endócrinas, nutricionais e metabólicas',
        'F': 'Transtornos mentais e comportamentais',
        'G': 'Doenças do sistema nervoso',
        'H': 'Doenças do olho e anexos',
        'I': 'Doenças do aparelho circulatório',
        'J': 'Doenças do aparelho respiratório',
        'K': 'Doenças do aparelho digestivo',
        'L': 'Doenças da pele e tecido subcutâneo',
        'M': 'Doenças do sistema osteomuscular',
        'N': 'Doenças do aparelho geniturinário',
        'O': 'Condições originadas no período perinatal',
        'P': 'Condições originadas no período perinatal',
        'Q': 'Malformações congênitas',
        'R': 'Sintomas, sinais e achados anormais',
        'S': 'Lesões, envenenamentos e outras consequências',
        'T': 'Lesões, envenenamentos e outras consequências',
        'V': 'Causas externas de morbidade',
        'W': 'Causas externas de morbidade',
        'X': 'Causas externas de morbidade',
        'Y': 'Causas externas de morbidade',
        'Z': 'Fatores que influenciam o estado de saúde'
    }
    
    return categoria_map.get(cid_code[0], 'Outras doenças')

def import_to_cache(diseases):
    """Importa as doenças para o cache existente"""
    print("🔄 Importando para o cache...")
    
    # Carregar cache atual
    try:
        with open('doencas_cache.json', 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
    except FileNotFoundError:
        cache_data = {"doencas": [], "last_update": 0}
    
    # Adicionar novas doenças
    codigo_seq = len(cache_data['doencas']) + 1
    
    for disease in diseases:
        disease['codigo_seq'] = str(codigo_seq)
        cache_data['doencas'].append(disease)
        codigo_seq += 1
    
    # Atualizar timestamp
    cache_data['last_update'] = int(time.time())
    
    # Salvar cache atualizado
    with open('doencas_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Cache atualizado com sucesso!")
    print(f"📊 Total de doenças: {len(cache_data['doencas'])}")
    print(f"🆕 Novas doenças adicionadas: {len(diseases)}")

def main():
    downloads_path = Path.home() / "Downloads"
    pdf_path = downloads_path / "CID10_oficial.pdf"
    if not pdf_path.exists():
        print(f"❌ Arquivo {pdf_path} não encontrado.")
        return
    print(f"🎯 Processando: {pdf_path.name}")
    diseases = extract_from_pdf(pdf_path)
    if diseases:
        print(f"📈 Extraídas {len(diseases)} doenças do PDF")
        import_to_cache(diseases)
        print("🎉 Processo concluído com sucesso!")
    else:
        print("❌ Nenhuma doença foi extraída do PDF")

if __name__ == "__main__":
    main() 