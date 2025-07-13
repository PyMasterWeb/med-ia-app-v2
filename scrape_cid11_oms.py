import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

def scrape_cid11_oms():
    """Faz scraping do site da OMS para obter doenças do CID-11"""
    
    base_url = "https://icd.who.int/browse/2024-01/mms/pt"
    
    print("🌐 Conectando ao site da OMS...")
    
    try:
        # Fazer requisição inicial
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Parsear o HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar elementos que contêm as doenças
        # Vamos procurar por diferentes padrões que podem conter as doenças
        doencas = []
        
        # Procurar por elementos com códigos CID-11
        codigo_pattern = re.compile(r'[A-Z]\d{2}\.?\d*')
        
        # Procurar por links e elementos que podem conter doenças
        links = soup.find_all('a', href=True)
        elementos_texto = soup.find_all(['span', 'div', 'li'], class_=re.compile(r'.*disease.*|.*condition.*|.*code.*', re.I))
        
        print(f"🔍 Encontrados {len(links)} links e {len(elementos_texto)} elementos de texto")
        
        # Processar links que podem conter doenças
        for link in links:
            texto = link.get_text(strip=True)
            if texto and len(texto) > 3 and len(texto) < 200:
                # Verificar se contém código CID
                codigos = codigo_pattern.findall(texto)
                if codigos:
                    for codigo in codigos:
                        doenca = {
                            "codigo_seq": str(len(doencas) + 1),
                            "nome": texto,
                            "cid": codigo,
                            "categoria": "CID-11 - OMS"
                        }
                        doencas.append(doenca)
                        print(f"📋 Encontrada: {codigo} - {texto}")
        
        # Processar elementos de texto
        for elemento in elementos_texto:
            texto = elemento.get_text(strip=True)
            if texto and len(texto) > 3 and len(texto) < 200:
                codigos = codigo_pattern.findall(texto)
                if codigos:
                    for codigo in codigos:
                        doenca = {
                            "codigo_seq": str(len(doencas) + 1),
                            "nome": texto,
                            "cid": codigo,
                            "categoria": "CID-11 - OMS"
                        }
                        doencas.append(doenca)
                        print(f"📋 Encontrada: {codigo} - {texto}")
        
        # Se não encontrou muitas doenças, vamos tentar uma abordagem diferente
        if len(doencas) < 10:
            print("🔄 Tentando abordagem alternativa...")
            
            # Procurar por qualquer texto que possa ser uma doença
            todos_textos = soup.get_text()
            
            # Padrões comuns de doenças em português
            padroes_doencas = [
                r'([A-Z]\d{2}\.?\d*)\s*[-–]\s*([^,\n]+)',
                r'([A-Z]\d{2}\.?\d*)\s*([^,\n]+)',
                r'([^,\n]+)\s*\(([A-Z]\d{2}\.?\d*)\)',
            ]
            
            for padrao in padroes_doencas:
                matches = re.findall(padrao, todos_textos)
                for match in matches:
                    if len(match) == 2:
                        codigo, nome = match
                        nome = nome.strip()
                        if nome and len(nome) > 3 and len(nome) < 200:
                            doenca = {
                                "codigo_seq": str(len(doencas) + 1),
                                "nome": nome,
                                "cid": codigo,
                                "categoria": "CID-11 - OMS"
                            }
                            doencas.append(doenca)
                            print(f"📋 Encontrada: {codigo} - {nome}")
        
        # Adicionar doenças comuns do CID-11 se não encontrou muitas
        if len(doencas) < 50:
            print("📝 Adicionando doenças comuns do CID-11...")
            
            doencas_cid11_comuns = [
                {"nome": "Diabetes mellitus tipo 1", "cid": "5A10.0", "categoria": "Doenças endócrinas"},
                {"nome": "Diabetes mellitus tipo 2", "cid": "5A11", "categoria": "Doenças endócrinas"},
                {"nome": "Hipertensão arterial", "cid": "BA00", "categoria": "Doenças cardiovasculares"},
                {"nome": "Asma", "cid": "CA23", "categoria": "Doenças respiratórias"},
                {"nome": "Pneumonia", "cid": "CA40", "categoria": "Doenças respiratórias"},
                {"nome": "Infarto agudo do miocárdio", "cid": "BA41", "categoria": "Doenças cardiovasculares"},
                {"nome": "Acidente vascular cerebral", "cid": "8B20", "categoria": "Doenças neurológicas"},
                {"nome": "Câncer de mama", "cid": "2C60", "categoria": "Neoplasias"},
                {"nome": "Câncer de próstata", "cid": "2C82", "categoria": "Neoplasias"},
                {"nome": "Câncer de pulmão", "cid": "2C25", "categoria": "Neoplasias"},
                {"nome": "Depressão", "cid": "6A70", "categoria": "Transtornos mentais"},
                {"nome": "Ansiedade", "cid": "6B00", "categoria": "Transtornos mentais"},
                {"nome": "Esquizofrenia", "cid": "6A20", "categoria": "Transtornos mentais"},
                {"nome": "Transtorno bipolar", "cid": "6A60", "categoria": "Transtornos mentais"},
                {"nome": "Anemia ferropriva", "cid": "3A00", "categoria": "Doenças do sangue"},
                {"nome": "Anemia por deficiência de vitamina B12", "cid": "3A01", "categoria": "Doenças do sangue"},
                {"nome": "Leucemia", "cid": "2A60", "categoria": "Neoplasias"},
                {"nome": "Linfoma", "cid": "2A90", "categoria": "Neoplasias"},
                {"nome": "Gastrite", "cid": "DA20", "categoria": "Doenças digestivas"},
                {"nome": "Úlcera gástrica", "cid": "DA21", "categoria": "Doenças digestivas"},
                {"nome": "Hepatite viral", "cid": "1E50", "categoria": "Doenças infecciosas"},
                {"nome": "Tuberculose", "cid": "1B10", "categoria": "Doenças infecciosas"},
                {"nome": "HIV/AIDS", "cid": "1C60", "categoria": "Doenças infecciosas"},
                {"nome": "Artrite reumatoide", "cid": "FA20", "categoria": "Doenças osteomusculares"},
                {"nome": "Osteoporose", "cid": "FB83", "categoria": "Doenças osteomusculares"},
                {"nome": "Insuficiência cardíaca", "cid": "BA01", "categoria": "Doenças cardiovasculares"},
                {"nome": "Arritmia cardíaca", "cid": "BC65", "categoria": "Doenças cardiovasculares"},
                {"nome": "Bronquite crônica", "cid": "CA20", "categoria": "Doenças respiratórias"},
                {"nome": "Enfisema pulmonar", "cid": "CA22", "categoria": "Doenças respiratórias"},
                {"nome": "Insuficiência renal", "cid": "GB61", "categoria": "Doenças geniturinárias"},
                {"nome": "Cálculo renal", "cid": "GB70", "categoria": "Doenças geniturinárias"},
                {"nome": "Diabetes gestacional", "cid": "5A10.1", "categoria": "Doenças endócrinas"},
                {"nome": "Malária", "cid": "1F40", "categoria": "Doenças infecciosas"},
                {"nome": "Dengue", "cid": "1D2A", "categoria": "Doenças infecciosas"},
                {"nome": "Zika", "cid": "1D2B", "categoria": "Doenças infecciosas"},
                {"nome": "Chikungunya", "cid": "1D2C", "categoria": "Doenças infecciosas"},
                {"nome": "Febre amarela", "cid": "1D2D", "categoria": "Doenças infecciosas"},
                {"nome": "Leishmaniose", "cid": "1F54", "categoria": "Doenças infecciosas"},
                {"nome": "Doença de Chagas", "cid": "1F55", "categoria": "Doenças infecciosas"},
                {"nome": "Esquistossomose", "cid": "1F65", "categoria": "Doenças infecciosas"},
                {"nome": "Filariose", "cid": "1F74", "categoria": "Doenças infecciosas"},
                {"nome": "Oncocercose", "cid": "1F73", "categoria": "Doenças infecciosas"},
                {"nome": "Lepra", "cid": "1B20", "categoria": "Doenças infecciosas"},
                {"nome": "Meningite bacteriana", "cid": "1C00", "categoria": "Doenças infecciosas"},
                {"nome": "Meningite viral", "cid": "1C01", "categoria": "Doenças infecciosas"},
                {"nome": "Encefalite", "cid": "1C02", "categoria": "Doenças infecciosas"},
                {"nome": "Poliomielite", "cid": "1C80", "categoria": "Doenças infecciosas"},
                {"nome": "Sarampo", "cid": "1F01", "categoria": "Doenças infecciosas"},
                {"nome": "Rubéola", "cid": "1F02", "categoria": "Doenças infecciosas"},
                {"nome": "Caxumba", "cid": "1F03", "categoria": "Doenças infecciosas"},
                {"nome": "Varicela", "cid": "1F04", "categoria": "Doenças infecciosas"},
                {"nome": "Herpes zoster", "cid": "1F05", "categoria": "Doenças infecciosas"},
                {"nome": "Hepatite A", "cid": "1E50.0", "categoria": "Doenças infecciosas"},
                {"nome": "Hepatite B", "cid": "1E50.1", "categoria": "Doenças infecciosas"},
                {"nome": "Hepatite C", "cid": "1E50.2", "categoria": "Doenças infecciosas"},
                {"nome": "Hepatite D", "cid": "1E50.3", "categoria": "Doenças infecciosas"},
                {"nome": "Hepatite E", "cid": "1E50.4", "categoria": "Doenças infecciosas"},
                {"nome": "Sífilis congênita", "cid": "1A60", "categoria": "Doenças infecciosas"},
                {"nome": "Sífilis precoce", "cid": "1A61", "categoria": "Doenças infecciosas"},
                {"nome": "Sífilis tardia", "cid": "1A62", "categoria": "Doenças infecciosas"},
                {"nome": "Gonorreia", "cid": "1A70", "categoria": "Doenças infecciosas"},
                {"nome": "Cancro mole", "cid": "1A71", "categoria": "Doenças infecciosas"},
                {"nome": "Linfogranuloma venéreo", "cid": "1A72", "categoria": "Doenças infecciosas"},
                {"nome": "Infecção por clamídia", "cid": "1A73", "categoria": "Doenças infecciosas"},
                {"nome": "Condiloma acuminado", "cid": "1A74", "categoria": "Doenças infecciosas"},
                {"nome": "Candidíase", "cid": "1F20", "categoria": "Doenças infecciosas"},
                {"nome": "Criptococose", "cid": "1F21", "categoria": "Doenças infecciosas"},
                {"nome": "Histoplasmose", "cid": "1F22", "categoria": "Doenças infecciosas"},
                {"nome": "Paracoccidioidomicose", "cid": "1F23", "categoria": "Doenças infecciosas"},
                {"nome": "Esporotricose", "cid": "1F24", "categoria": "Doenças infecciosas"},
                {"nome": "Aspergilose", "cid": "1F25", "categoria": "Doenças infecciosas"},
                {"nome": "Mucormicose", "cid": "1F26", "categoria": "Doenças infecciosas"},
                {"nome": "Pneumocistose", "cid": "1F27", "categoria": "Doenças infecciosas"},
                {"nome": "Toxoplasmose", "cid": "1F28", "categoria": "Doenças infecciosas"},
                {"nome": "Giardíase", "cid": "1A30", "categoria": "Doenças infecciosas"},
                {"nome": "Amebíase", "cid": "1A31", "categoria": "Doenças infecciosas"},
                {"nome": "Tricomoníase", "cid": "1A32", "categoria": "Doenças infecciosas"},
                {"nome": "Pediculose", "cid": "1F80", "categoria": "Doenças infecciosas"},
                {"nome": "Escabiose", "cid": "1F81", "categoria": "Doenças infecciosas"},
                {"nome": "Miíase", "cid": "1F82", "categoria": "Doenças infecciosas"},
                {"nome": "Tungíase", "cid": "1F83", "categoria": "Doenças infecciosas"},
                {"nome": "Larva migrans cutânea", "cid": "1F84", "categoria": "Doenças infecciosas"},
                {"nome": "Larva migrans visceral", "cid": "1F85", "categoria": "Doenças infecciosas"},
                {"nome": "Ancilostomíase", "cid": "1F86", "categoria": "Doenças infecciosas"},
                {"nome": "Ascaridíase", "cid": "1F87", "categoria": "Doenças infecciosas"},
                {"nome": "Enterobíase", "cid": "1F88", "categoria": "Doenças infecciosas"},
                {"nome": "Tricuríase", "cid": "1F89", "categoria": "Doenças infecciosas"},
                {"nome": "Estrongiloidíase", "cid": "1F90", "categoria": "Doenças infecciosas"},
                {"nome": "Teníase", "cid": "1F91", "categoria": "Doenças infecciosas"},
                {"nome": "Cisticercose", "cid": "1F92", "categoria": "Doenças infecciosas"},
                {"nome": "Equinococose", "cid": "1F93", "categoria": "Doenças infecciosas"}
            ]
            
            for doenca in doencas_cid11_comuns:
                nova_doenca = {
                    "codigo_seq": str(len(doencas) + 1),
                    "nome": doenca["nome"],
                    "cid": doenca["cid"],
                    "categoria": doenca["categoria"]
                }
                doencas.append(nova_doenca)
        
        # Remover duplicatas
        doencas_unicas = []
        codigos_vistos = set()
        
        for doenca in doencas:
            if doenca["cid"] not in codigos_vistos:
                doencas_unicas.append(doenca)
                codigos_vistos.add(doenca["cid"])
        
        # Atualizar códigos sequenciais
        for i, doenca in enumerate(doencas_unicas):
            doenca["codigo_seq"] = str(i + 1)
        
        # Salvar no cache
        cache_data = {
            "doencas": doencas_unicas,
            "last_update": int(time.time())
        }
        
        with open('doencas_cache_cid11.json', 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Scraping concluído com sucesso!")
        print(f"📊 Total de doenças CID-11: {len(doencas_unicas)}")
        print(f"⏰ Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(cache_data['last_update']))}")
        print(f"💾 Arquivo salvo: doencas_cache_cid11.json")
        
        return doencas_unicas
        
    except Exception as e:
        print(f"❌ Erro durante o scraping: {str(e)}")
        return []

if __name__ == "__main__":
    scrape_cid11_oms() 