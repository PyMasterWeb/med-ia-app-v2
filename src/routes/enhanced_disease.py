from flask import Blueprint, jsonify, request
import json
import os
from datetime import datetime, timedelta
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .disease import scraping_doencas, salvar_doencas_local

enhanced_disease_bp = Blueprint('enhanced_disease', __name__)

# Cache para doenças
doencas_cache = []
last_update = None

def load_doencas_cache():
    """Carrega o cache de doenças do arquivo JSON. Se não existir, faz scraping e salva."""
    global doencas_cache, last_update
    try:
        if os.path.exists('doencas_cache.json'):
            with open('doencas_cache.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                doencas_cache = data.get('doencas', [])
                last_update = data.get('last_update')
                
                # Verificar se precisa atualizar (a cada 24 horas)
                agora = int(time.time())
                if last_update and (agora - last_update) > (24 * 60 * 60):
                    print("Cache expirado. Atualizando dados do Datasus...")
                    doencas = scraping_doencas()
                    if doencas:
                        salvar_doencas_local(doencas)
                        doencas_cache = doencas
                        last_update = agora
        else:
            # Se não existe, faz scraping e salva
            print('Arquivo doencas_cache.json não encontrado. Fazendo scraping do Datasus...')
            doencas = scraping_doencas()
            if doencas:
                salvar_doencas_local(doencas)
                doencas_cache = doencas
                last_update = int(time.time())
            else:
                doencas_cache = []
                last_update = None
    except Exception as e:
        print(f"Erro ao carregar cache: {e}")
        doencas_cache = []
        last_update = None

@enhanced_disease_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Med-IA API v2 está funcionando!",
        "timestamp": datetime.now().isoformat()
    })

@enhanced_disease_bp.route('/search/name', methods=['POST'])
def search_disease_by_name():
    """Busca doenças por nome"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip().lower()
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query não fornecida"
            }), 400
        
        # Carregar cache se necessário
        load_doencas_cache()
        
        # Buscar doenças que correspondem à query
        results = []
        for doenca in doencas_cache:
            nome_doenca = doenca.get('nome', '').lower()
            if query in nome_doenca:
                # Calcular relevância baseada na similaridade
                relevance = 100 if query == nome_doenca else 80
                if nome_doenca.startswith(query):
                    relevance = 90
                
                results.append({
                    "code": doenca.get('cid', ''),
                    "description": doenca.get('nome', ''),
                    "relevance": relevance,
                    "subcategory": {
                        "category": doenca.get('categoria', 'Não especificada')
                    }
                })
        
        # Ordenar por relevância
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return jsonify({
            "success": True,
            "total_found": len(results),
            "results": results[:20]  # Limitar a 20 resultados
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro na busca: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/disease/<code>/details', methods=['GET'])
def get_disease_details(code):
    """Obtém detalhes de uma doença específica"""
    try:
        # Carregar cache se necessário
        load_doencas_cache()
        
        # Buscar doença pelo código
        doenca = None
        for d in doencas_cache:
            if d.get('cid', '').upper() == code.upper():
                doenca = d
                break
        
        if not doenca:
            return jsonify({
                "success": False,
                "message": "Doença não encontrada"
            }), 404
        
        # Simular detalhes baseados no nome da doença
        nome = doenca.get('nome', '').lower()
        
        # Determinar gravidade baseada em palavras-chave
        severity = "Leve"
        if any(word in nome for word in ['câncer', 'tumor', 'maligno', 'grave', 'crítico', 'infarto', 'acidente vascular']):
            severity = "Grave"
        elif any(word in nome for word in ['moderado', 'crônico', 'agudo', 'insuficiência']):
            severity = "Moderada"
        
        # Determinar se tem tratamento
        has_treatment = True
        treatment_type = "Medicamentoso"
        
        # Medicamentos comuns baseados no tipo de doença
        medications = []
        if 'diabetes' in nome:
            medications = ['Metformina', 'Insulina', 'Glimepirida']
        elif 'hipertensão' in nome:
            medications = ['Captopril', 'Losartana', 'Amlodipina']
        elif 'asma' in nome:
            medications = ['Salbutamol', 'Budesonida', 'Formoterol']
        elif 'câncer' in nome:
            medications = ['Quimioterapia', 'Radioterapia', 'Terapia alvo']
        elif 'depressão' in nome:
            medications = ['Sertralina', 'Fluoxetina', 'Escitalopram']
        
        # Sintomas típicos
        symptoms = []
        if 'diabetes' in nome:
            symptoms = ['Sede excessiva', 'Fome excessiva', 'Micção frequente']
        elif 'hipertensão' in nome:
            symptoms = ['Dor de cabeça', 'Tontura', 'Náusea']
        elif 'asma' in nome:
            symptoms = ['Falta de ar', 'Tosse', 'Chiado no peito']
        elif 'câncer' in nome:
            symptoms = ['Perda de peso', 'Fadiga', 'Dor']
        elif 'depressão' in nome:
            symptoms = ['Tristeza', 'Perda de interesse', 'Alterações do sono']
        
        # Prognóstico
        prognosis = "Bom com tratamento adequado"
        if severity == "Grave":
            prognosis = "Requer acompanhamento médico intensivo"
        
        return jsonify({
            "success": True,
            "disease_details": {
                "severity": severity,
                "has_treatment": has_treatment,
                "treatment_type": treatment_type,
                "medications": medications,
                "non_medication_treatment": ["Dieta", "Exercícios", "Controle de peso"],
                "symptoms": symptoms,
                "prognosis": prognosis
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao obter detalhes: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/categories', methods=['GET'])
def get_categories():
    """Obtém categorias CID-10"""
    try:
        # Carregar cache se necessário
        load_doencas_cache()
        
        # Agrupar doenças por categoria
        categories = {}
        for doenca in doencas_cache:
            categoria = doenca.get('categoria', 'Não especificada')
            if categoria not in categories:
                categories[categoria] = []
            categories[categoria].append(doenca)
        
        # Criar lista de categorias
        category_list = []
        for categoria, doencas in categories.items():
            category_list.append({
                "letter": categoria[:1] if categoria else "?",
                "title": categoria,
                "description": f"{len(doencas)} doenças nesta categoria"
            })
        
        return jsonify({
            "success": True,
            "total_categories": len(category_list),
            "categories": category_list
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao obter categorias: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/categories/<letter>/diseases', methods=['GET'])
def get_diseases_by_category(letter):
    """Obtém doenças de uma categoria específica"""
    try:
        # Carregar cache se necessário
        load_doencas_cache()
        
        # Filtrar doenças pela categoria
        category_diseases = []
        for doenca in doencas_cache:
            categoria = doenca.get('categoria', '')
            if categoria and categoria.upper().startswith(letter.upper()):
                category_diseases.append({
                    "code": doenca.get('cid', ''),
                    "description": doenca.get('nome', ''),
                    "severity": "Leve",  # Simulado
                    "has_treatment": True,
                    "treatment_type": "Medicamentoso"
                })
        
        return jsonify({
            "success": True,
            "category": letter.upper(),
            "total_diseases": len(category_diseases),
            "diseases": category_diseases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao obter doenças da categoria: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/symptoms/categories', methods=['GET'])
def get_symptom_categories():
    """Obtém categorias de sintomas"""
    categories = {
        "Sistema Respiratório": [
            "Tosse", "Falta de ar", "Chiado no peito", "Dor no peito",
            "Nariz entupido", "Espirros", "Rouquidão"
        ],
        "Sistema Digestivo": [
            "Náusea", "Vômito", "Dor abdominal", "Diarréia",
            "Constipação", "Azia", "Perda de apetite"
        ],
        "Sistema Cardiovascular": [
            "Dor no peito", "Palpitações", "Falta de ar",
            "Tontura", "Desmaio", "Inchaço nas pernas"
        ],
        "Sistema Nervoso": [
            "Dor de cabeça", "Tontura", "Convulsões", "Paralisia",
            "Formigamento", "Perda de memória", "Confusão"
        ],
        "Sistema Urinário": [
            "Dor ao urinar", "Urgência urinária", "Incontinência",
            "Sangue na urina", "Inchaço", "Dor lombar"
        ]
    }
    
    return jsonify({
        "success": True,
        "categories": categories
    })

@enhanced_disease_bp.route('/diagnose/symptoms', methods=['POST'])
def diagnose_symptoms():
    """Diagnóstico por sintomas (texto livre)"""
    try:
        data = request.get_json()
        symptoms_report = data.get('symptoms_report', '').strip()
        include_report = data.get('include_report', False)
        
        if not symptoms_report:
            return jsonify({
                "success": False,
                "message": "Relatório de sintomas não fornecido"
            }), 400
        
        # Simular diagnóstico baseado em palavras-chave
        symptoms_lower = symptoms_report.lower()
        diagnoses = []
        
        if any(word in symptoms_lower for word in ['diabetes', 'açúcar', 'sede']):
            diagnoses.append({
                "disease_name": "Diabetes Mellitus",
                "cid_code": "E11",
                "probability": 85,
                "confidence_level": "Alta",
                "matching_symptoms": ["Sede excessiva", "Fome excessiva", "Micção frequente"]
            })
        
        if any(word in symptoms_lower for word in ['hipertensão', 'pressão', 'cabeça']):
            diagnoses.append({
                "disease_name": "Hipertensão Arterial",
                "cid_code": "I10",
                "probability": 80,
                "confidence_level": "Alta",
                "matching_symptoms": ["Dor de cabeça", "Tontura", "Náusea"]
            })
        
        if any(word in symptoms_lower for word in ['asma', 'respirar', 'chiado']):
            diagnoses.append({
                "disease_name": "Asma",
                "cid_code": "J45",
                "probability": 75,
                "confidence_level": "Média",
                "matching_symptoms": ["Falta de ar", "Chiado no peito", "Tosse"]
            })
        
        if not diagnoses:
            diagnoses.append({
                "disease_name": "Sintomas Inespecíficos",
                "cid_code": "R68",
                "probability": 50,
                "confidence_level": "Baixa",
                "matching_symptoms": ["Sintomas gerais"]
            })
        
        response = {
            "success": True,
            "total_diagnoses": len(diagnoses),
            "diagnostic_results": diagnoses
        }
        
        if include_report:
            response["medical_report"] = f"""
RELATÓRIO MÉDICO

Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

SINTOMAS RELATADOS:
{symptoms_report}

DIAGNÓSTICOS POSSÍVEIS:
{chr(10).join([f"- {d['disease_name']} ({d['cid_code']}) - Probabilidade: {d['probability']}%" for d in diagnoses])}

RECOMENDAÇÕES:
- Consulte um médico para confirmação diagnóstica
- Mantenha registro dos sintomas
- Evite automedicação
- Procure atendimento de emergência se sintomas graves

Este é um diagnóstico preliminar baseado em IA. Consulte sempre um profissional de saúde.
"""
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro no diagnóstico: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/diagnose/objective_symptoms', methods=['POST'])
def diagnose_objective_symptoms():
    """Diagnóstico por sintomas objetivos"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        include_report = data.get('include_report', False)
        
        if not symptoms:
            return jsonify({
                "success": False,
                "message": "Sintomas não fornecidos"
            }), 400
        
        # Simular validação de sintomas
        symptom_validation = []
        for symptom in symptoms:
            confidence = 70  # Simulado
            if any(word in symptom.lower() for word in ['dor', 'febre', 'tosse']):
                confidence = 85
            symptom_validation.append({
                "condition": f"Condição relacionada a {symptom}",
                "confidence": confidence,
                "matching_symptoms": 1,
                "total_symptoms": len(symptoms)
            })
        
        # Simular diagnósticos
        diagnoses = []
        symptoms_lower = [s.lower() for s in symptoms]
        
        if any(word in symptoms_lower for word in ['diabetes', 'sede']):
            diagnoses.append({
                "disease_name": "Diabetes Mellitus",
                "cid_code": "E11",
                "probability": 85,
                "confidence_level": "Alta",
                "matching_symptoms": ["Sede excessiva", "Fome excessiva"]
            })
        
        if any(word in symptoms_lower for word in ['hipertensão', 'cabeça']):
            diagnoses.append({
                "disease_name": "Hipertensão Arterial",
                "cid_code": "I10",
                "probability": 80,
                "confidence_level": "Alta",
                "matching_symptoms": ["Dor de cabeça", "Tontura"]
            })
        
        if not diagnoses:
            diagnoses.append({
                "disease_name": "Sintomas Inespecíficos",
                "cid_code": "R68",
                "probability": 50,
                "confidence_level": "Baixa",
                "matching_symptoms": symptoms
            })
        
        response = {
            "success": True,
            "total_diagnoses": len(diagnoses),
            "symptom_validation": symptom_validation,
            "diagnostic_results": diagnoses
        }
        
        if include_report:
            response["medical_report"] = f"""
RELATÓRIO MÉDICO - SINTOMAS OBJETIVOS

Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

SINTOMAS SELECIONADOS:
{chr(10).join([f"- {symptom}" for symptom in symptoms])}

DIAGNÓSTICOS POSSÍVEIS:
{chr(10).join([f"- {d['disease_name']} ({d['cid_code']}) - Probabilidade: {d['probability']}%" for d in diagnoses])}

RECOMENDAÇÕES:
- Consulte um médico para confirmação diagnóstica
- Mantenha registro dos sintomas
- Evite automedicação
- Procure atendimento de emergência se sintomas graves

Este é um diagnóstico preliminar baseado em IA. Consulte sempre um profissional de saúde.
"""
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro no diagnóstico: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/interactions/check', methods=['POST'])
def check_interactions():
    """Verifica interações medicamentosas"""
    try:
        data = request.get_json()
        medications = data.get('medications', [])
        include_report = data.get('include_report', False)
        
        if len(medications) < 2:
            return jsonify({
                "success": False,
                "message": "Adicione pelo menos 2 medicamentos"
            }), 400
        
        # Simular verificação de interações
        interactions = []
        severity_levels = ["Leve", "Moderada", "Grave", "Contraindicada"]
        
        # Verificar interações conhecidas
        for i in range(len(medications)):
            for j in range(i + 1, len(medications)):
                med1, med2 = medications[i], medications[j]
                
                # Simular algumas interações conhecidas
                if any(word in med1.lower() for word in ['aspirina', 'aas']) and any(word in med2.lower() for word in ['varfarina', 'coumadin']):
                    interactions.append({
                        "drug1": med1,
                        "drug2": med2,
                        "severity": "Grave",
                        "mechanism": "Aumento do risco de sangramento",
                        "clinical_effects": ["Sangramento", "Hemorragia", "Hematomas"]
                    })
                elif any(word in med1.lower() for word in ['omeprazol', 'pantoprazol']) and any(word in med2.lower() for word in ['clopidogrel', 'plavix']):
                    interactions.append({
                        "drug1": med1,
                        "drug2": med2,
                        "severity": "Moderada",
                        "mechanism": "Redução da eficácia do clopidogrel",
                        "clinical_effects": ["Redução da proteção cardiovascular", "Aumento do risco de eventos cardíacos"]
                    })
                else:
                    # Interação genérica
                    interactions.append({
                        "drug1": med1,
                        "drug2": med2,
                        "severity": "Leve",
                        "mechanism": "Interação farmacocinética potencial",
                        "clinical_effects": ["Monitoramento necessário", "Ajuste de dose pode ser necessário"]
                    })
        
        # Resumo
        summary = {
            "total_interactions": len(interactions),
            "highest_severity": max([i["severity"] for i in interactions]) if interactions else "Nenhuma",
            "interactions": interactions
        }
        
        response = {
            "success": True,
            "summary": summary
        }
        
        if include_report:
            response["detailed_report"] = f"""
RELATÓRIO DE INTERAÇÕES MEDICAMENTOSAS

Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

MEDICAMENTOS ANALISADOS:
{chr(10).join([f"- {med}" for med in medications])}

INTERAÇÕES ENCONTRADAS: {len(interactions)}

{chr(10).join([f"""
INTERAÇÃO {idx + 1}:
- Medicamentos: {interaction['drug1']} + {interaction['drug2']}
- Gravidade: {interaction['severity']}
- Mecanismo: {interaction['mechanism']}
- Efeitos Clínicos: {', '.join(interaction['clinical_effects'])}
""" for idx, interaction in enumerate(interactions)])}

RECOMENDAÇÕES:
- Consulte sempre um médico ou farmacêutico
- Não interrompa medicamentos sem orientação médica
- Mantenha lista atualizada de todos os medicamentos
- Informe sobre suplementos e fitoterápicos

Este relatório é informativo. Sempre consulte um profissional de saúde.
"""
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro na verificação de interações: {str(e)}"
        }), 500

@enhanced_disease_bp.route('/enhanced_disease/test', methods=['GET'])
def test_enhanced_disease():
    return jsonify({"message": "Rota /api/v2/enhanced_disease/test funcionando!"}) 