import json
import time

def expand_diseases_cache():
    """Expande rapidamente o cache de doenças usando dados do Datasus"""
    
    # Carregar dados existentes
    with open('cid10_datasus.json', 'r', encoding='utf-8') as f:
        cid10_data = json.load(f)
    
    # Carregar cache atual
    with open('doencas_cache.json', 'r', encoding='utf-8') as f:
        cache_data = json.load(f)
    
    # Mapeamento de categorias por código CID
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
    
    # Converter dados do CID10 para o formato do cache
    novas_doencas = []
    codigo_seq = len(cache_data['doencas']) + 1
    
    for item in cid10_data:
        codigo = item['code']
        nome = item['description']
        
        # Determinar categoria baseada no primeiro caractere do código
        categoria = categoria_map.get(codigo[0], 'Outras doenças')
        
        nova_doenca = {
            "codigo_seq": str(codigo_seq),
            "nome": nome,
            "cid": codigo,
            "categoria": categoria
        }
        
        novas_doencas.append(nova_doenca)
        codigo_seq += 1
    
    # Adicionar mais doenças comuns do Datasus
    doencas_extras = [
        {"nome": "Malária", "cid": "B50", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Dengue", "cid": "A90", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Zika", "cid": "A92.8", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Chikungunya", "cid": "A92.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Febre amarela", "cid": "A95", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Leishmaniose", "cid": "B55", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Doença de Chagas", "cid": "B57", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose", "cid": "B65", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Filariose", "cid": "B74", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Oncocercose", "cid": "B73", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Lepra", "cid": "A30", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Tuberculose pulmonar", "cid": "A15.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Tuberculose extrapulmonar", "cid": "A16", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Meningite bacteriana", "cid": "G00", "categoria": "Doenças do sistema nervoso"},
        {"nome": "Meningite viral", "cid": "A87", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Encefalite", "cid": "A86", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Poliomielite", "cid": "A80", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Sarampo", "cid": "B05", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Rubéola", "cid": "B06", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Caxumba", "cid": "B26", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Varicela", "cid": "B01", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Herpes zoster", "cid": "B02", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Hepatite A", "cid": "B15", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Hepatite B", "cid": "B16", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Hepatite C", "cid": "B17.1", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Hepatite D", "cid": "B17.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Hepatite E", "cid": "B17.2", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Sífilis congênita", "cid": "A50", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Sífilis precoce", "cid": "A51", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Sífilis tardia", "cid": "A52", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Gonorreia", "cid": "A54", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Cancro mole", "cid": "A57", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Linfogranuloma venéreo", "cid": "A55", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Infecção por clamídia", "cid": "A56", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Condiloma acuminado", "cid": "A63.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Candidíase", "cid": "B37", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Criptococose", "cid": "B45", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Histoplasmose", "cid": "B39", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Paracoccidioidomicose", "cid": "B41", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esporotricose", "cid": "B42", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Aspergilose", "cid": "B44", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Mucormicose", "cid": "B46", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Pneumocistose", "cid": "B59", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Toxoplasmose", "cid": "B58", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Giardíase", "cid": "A07.1", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Amebíase", "cid": "A06", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Tricomoníase", "cid": "A59", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Pediculose", "cid": "B85", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Escabiose", "cid": "B86", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Miíase", "cid": "B87", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Tungíase", "cid": "B88.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Larva migrans cutânea", "cid": "B76.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Larva migrans visceral", "cid": "B76.1", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Ancilostomíase", "cid": "B76.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Ascaridíase", "cid": "B77", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Enterobíase", "cid": "B80", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Tricuríase", "cid": "B79", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Estrongiloidíase", "cid": "B78", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Teníase", "cid": "B68", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Cisticercose", "cid": "B69", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Equinococose", "cid": "B67", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose intestinal", "cid": "B65.0", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose urinária", "cid": "B65.1", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose hepatoesplênica", "cid": "B65.2", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose pulmonar", "cid": "B65.3", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose cerebral", "cid": "B65.4", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose com outras localizações", "cid": "B65.8", "categoria": "Doenças infecciosas e parasitárias"},
        {"nome": "Esquistossomose não especificada", "cid": "B65.9", "categoria": "Doenças infecciosas e parasitárias"}
    ]
    
    # Adicionar doenças extras
    for doenca in doencas_extras:
        nova_doenca = {
            "codigo_seq": str(codigo_seq),
            "nome": doenca["nome"],
            "cid": doenca["cid"],
            "categoria": doenca["categoria"]
        }
        novas_doencas.append(nova_doenca)
        codigo_seq += 1
    
    # Adicionar ao cache existente
    cache_data['doencas'].extend(novas_doencas)
    cache_data['last_update'] = int(time.time())
    
    # Salvar arquivo expandido
    with open('doencas_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Cache expandido com sucesso!")
    print(f"📊 Total de doenças: {len(cache_data['doencas'])}")
    print(f"🆕 Novas doenças adicionadas: {len(novas_doencas)}")
    print(f"⏰ Última atualização: {time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(cache_data['last_update']))}")

if __name__ == "__main__":
    expand_diseases_cache() 