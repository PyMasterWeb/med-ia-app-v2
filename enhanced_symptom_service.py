import json
from typing import List, Dict, Any

class EnhancedSymptomService:
    def __init__(self):
        self.diseases_cache = self._load_diseases_cache()
        self.symptom_disease_map = self._create_symptom_disease_mapping()
        self.symptom_categories = self._load_enhanced_symptom_categories()
    
    def _load_diseases_cache(self):
        """Carrega o cache de doenças"""
        try:
            with open('doencas_cache.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"doencas": []}
    
    def _create_symptom_disease_mapping(self):
        """Cria mapeamento entre sintomas e doenças específicas"""
        return {
            # Sintomas Gerais
            "Febre": ["A15", "A16", "A90", "B15", "B16", "B17", "B50", "B55", "B57", "B65"],
            "Fadiga": ["E10", "E11", "D50", "D51", "D60", "F32", "F41"],
            "Perda de peso": ["E10", "E11", "C50", "C61", "C34", "B20", "B57"],
            "Ganho de peso": ["E11", "E66"],
            "Sudorese": ["E10", "E11", "F32", "F41", "I10"],
            "Calafrios": ["A15", "A16", "A90", "B50", "B55"],
            "Mal-estar geral": ["A15", "A16", "A90", "B15", "B16", "B17", "B50"],
            "Fraqueza": ["D50", "D51", "D60", "E10", "E11", "F32", "F41"],
            
            # Sistema Cardiovascular
            "Dor no peito": ["I21", "I22", "I23", "I24", "I25", "I50"],
            "Palpitações": ["I49", "I10", "E10", "E11", "F41"],
            "Falta de ar": ["I50", "J45", "J18", "J42", "J43", "I21", "I22"],
            "Inchaço nas pernas": ["I50", "I81", "I82", "I83"],
            "Tontura": ["I10", "I49", "F32", "F41", "D50", "D51"],
            "Desmaio": ["I49", "I10", "F32", "F41"],
            "Pressão alta": ["I10", "I11", "I12", "I13"],
            "Pressão baixa": ["I95", "D50", "D51"],
            
            # Sistema Respiratório
            "Tosse seca": ["J45", "J18", "A15", "A16", "C34"],
            "Tosse com catarro": ["J18", "J42", "J43", "A15", "A16"],
            "Chiado no peito": ["J45", "J42", "J43"],
            "Dor ao respirar": ["J18", "J45", "I21", "I22", "C34"],
            "Respiração rápida": ["J45", "J18", "I50", "I21", "I22"],
            "Congestão nasal": ["J00", "J01", "J02", "J03", "J04"],
            "Espirros": ["J00", "J01", "J30"],
            
            # Sistema Digestivo
            "Dor abdominal": ["K25", "K26", "K27", "K28", "K29", "K35", "K36", "K37"],
            "Náuseas": ["K25", "K26", "K27", "K28", "K29", "I21", "I22", "F32"],
            "Vômitos": ["K25", "K26", "K27", "K28", "K29", "I21", "I22"],
            "Diarreia": ["A09", "A06", "A07", "K52"],
            "Constipação": ["K59.0", "K59.1"],
            "Azia": ["K21", "K25", "K26", "K27", "K28"],
            "Queimação no estômago": ["K21", "K25", "K26", "K27", "K28"],
            "Perda de apetite": ["C50", "C61", "C34", "F32", "F41"],
            "Inchaço abdominal": ["K59.1", "K66", "K67"],
            
            # Sistema Urinário
            "Dor ao urinar": ["N30", "N34", "N39.0", "N39.1"],
            "Urgência urinária": ["N30", "N34", "N39.0", "N39.1"],
            "Micção frequente": ["E10", "E11", "N30", "N34", "N39.0", "N39.1"],
            "Sangue na urina": ["N30", "N34", "N20", "N21", "N22"],
            "Urina turva": ["N30", "N34", "N39.0", "N39.1"],
            "Dor lombar": ["N20", "N21", "N22", "N30", "N34"],
            "Incontinência urinária": ["N39.3", "N39.4"],
            "Retenção urinária": ["N39.0", "N39.1"],
            
            # Sistema Neurológico
            "Dor de cabeça": ["I10", "F32", "F41", "G44", "G43"],
            "Confusão mental": ["F32", "F41", "F20", "F31"],
            "Perda de memória": ["F32", "F41", "F20", "F31"],
            "Convulsões": ["G40", "G41"],
            "Tremores": ["G25", "F32", "F41", "E10", "E11"],
            "Formigamento": ["G60", "G61", "G62", "E10", "E11"],
            "Perda de coordenação": ["G60", "G61", "G62"],
            
            # Sistema Musculoesquelético
            "Dor nas articulações": ["M06", "M05", "M08", "M09"],
            "Dor muscular": ["M79", "M60", "M61", "M62"],
            "Rigidez matinal": ["M06", "M05", "M08", "M09"],
            "Inchaço articular": ["M06", "M05", "M08", "M09"],
            "Limitação de movimento": ["M06", "M05", "M08", "M09", "M81"],
            "Dor nas costas": ["M54", "M51", "M52", "M53"],
            "Dor no pescoço": ["M54", "M50", "M51", "M52", "M53"],
            "Cãibras": ["M79", "E10", "E11", "D50", "D51"],
            
            # Pele e Anexos
            "Erupção cutânea": ["L20", "L21", "L22", "L23", "L24", "L25"],
            "Coceira": ["L20", "L21", "L22", "L23", "L24", "L25"],
            "Vermelhidão": ["L20", "L21", "L22", "L23", "L24", "L25"],
            "Descamação": ["L20", "L21", "L22", "L23", "L24", "L25"],
            "Feridas que não cicatrizam": ["C44", "E10", "E11", "D50", "D51"],
            "Mudança na cor da pele": ["C44", "L20", "L21", "L22", "L23", "L24", "L25"],
            "Queda de cabelo": ["L63", "L64", "L65"],
            "Unhas frágeis": ["L60", "D50", "D51"],
            
            # Sistema Endócrino
            "Sede excessiva": ["E10", "E11", "E86"],
            "Fome excessiva": ["E10", "E11", "E66"],
            "Micção excessiva": ["E10", "E11", "N39.0", "N39.1"],
            "Intolerância ao calor": ["E05", "E06"],
            "Intolerância ao frio": ["E03", "E04"],
            "Alterações menstruais": ["N91", "N92", "N93", "N94", "N95"],
            "Crescimento anormal": ["E22", "E23", "E24", "E25"],
            "Mudanças de humor": ["F31", "F32", "F33", "F34"],
            
            # Saúde Mental
            "Tristeza persistente": ["F32", "F33", "F34"],
            "Ansiedade": ["F41", "F42", "F43"],
            "Irritabilidade": ["F31", "F32", "F33", "F34", "F41"],
            "Perda de interesse": ["F32", "F33", "F34"],
            "Alterações do sono": ["F32", "F33", "F34", "F41", "F42"],
            "Pensamentos negativos": ["F32", "F33", "F34", "F41"],
            "Dificuldade de concentração": ["F32", "F33", "F34", "F41", "F42"],
            "Isolamento social": ["F20", "F21", "F22", "F23", "F24", "F25"]
        }
    
    def _load_enhanced_symptom_categories(self):
        """Carrega categorias de sintomas aprimoradas"""
        return {
            "Sintomas Gerais": [
                "Febre", "Fadiga", "Perda de peso", "Ganho de peso", 
                "Sudorese", "Calafrios", "Mal-estar geral", "Fraqueza"
            ],
            "Sistema Cardiovascular": [
                "Dor no peito", "Palpitações", "Falta de ar", "Inchaço nas pernas",
                "Tontura", "Desmaio", "Pressão alta", "Pressão baixa"
            ],
            "Sistema Respiratório": [
                "Tosse seca", "Tosse com catarro", "Falta de ar", "Chiado no peito",
                "Dor ao respirar", "Respiração rápida", "Congestão nasal", "Espirros"
            ],
            "Sistema Digestivo": [
                "Dor abdominal", "Náuseas", "Vômitos", "Diarreia", "Constipação",
                "Azia", "Queimação no estômago", "Perda de apetite", "Inchaço abdominal"
            ],
            "Sistema Urinário": [
                "Dor ao urinar", "Urgência urinária", "Micção frequente", "Sangue na urina",
                "Urina turva", "Dor lombar", "Incontinência urinária", "Retenção urinária"
            ],
            "Sistema Neurológico": [
                "Dor de cabeça", "Tontura", "Confusão mental", "Perda de memória",
                "Convulsões", "Tremores", "Formigamento", "Perda de coordenação"
            ],
            "Sistema Musculoesquelético": [
                "Dor nas articulações", "Dor muscular", "Rigidez matinal", "Inchaço articular",
                "Limitação de movimento", "Dor nas costas", "Dor no pescoço", "Cãibras"
            ],
            "Pele e Anexos": [
                "Erupção cutânea", "Coceira", "Vermelhidão", "Descamação",
                "Feridas que não cicatrizam", "Mudança na cor da pele", "Queda de cabelo", "Unhas frágeis"
            ],
            "Sistema Endócrino": [
                "Sede excessiva", "Fome excessiva", "Micção excessiva", "Intolerância ao calor",
                "Intolerância ao frio", "Alterações menstruais", "Crescimento anormal", "Mudanças de humor"
            ],
            "Saúde Mental": [
                "Tristeza persistente", "Ansiedade", "Irritabilidade", "Perda de interesse",
                "Alterações do sono", "Pensamentos negativos", "Dificuldade de concentração", "Isolamento social"
            ]
        }
    
    def get_diseases_by_symptoms(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """Retorna doenças relacionadas aos sintomas selecionados"""
        disease_scores = {}
        
        for symptom in symptoms:
            if symptom in self.symptom_disease_map:
                cid_codes = self.symptom_disease_map[symptom]
                for cid in cid_codes:
                    if cid not in disease_scores:
                        disease_scores[cid] = {"score": 0, "matching_symptoms": []}
                    disease_scores[cid]["score"] += 1
                    disease_scores[cid]["matching_symptoms"].append(symptom)
        
        # Encontrar doenças correspondentes no cache
        matched_diseases = []
        for cid, score_data in disease_scores.items():
            for disease in self.diseases_cache["doencas"]:
                if disease["cid"] == cid:
                    matched_diseases.append({
                        "codigo_seq": disease["codigo_seq"],
                        "nome": disease["nome"],
                        "cid": disease["cid"],
                        "categoria": disease["categoria"],
                        "score": score_data["score"],
                        "matching_symptoms": score_data["matching_symptoms"],
                        "confidence": min(score_data["score"] * 25, 100)  # Máximo 100%
                    })
                    break
        
        # Ordenar por score (maior primeiro)
        matched_diseases.sort(key=lambda x: x["score"], reverse=True)
        
        return matched_diseases
    
    def get_symptoms_by_disease(self, disease_cid: str) -> List[str]:
        """Retorna sintomas relacionados a uma doença específica"""
        symptoms = []
        for symptom, cid_codes in self.symptom_disease_map.items():
            if disease_cid in cid_codes:
                symptoms.append(symptom)
        return symptoms
    
    def get_related_symptoms(self, selected_symptoms: List[str]) -> List[str]:
        """Sugere sintomas relacionados baseados nos já selecionados"""
        related_symptoms = set()
        
        # Encontrar doenças relacionadas aos sintomas selecionados
        related_diseases = self.get_diseases_by_symptoms(selected_symptoms)
        
        # Para cada doença relacionada, sugerir sintomas adicionais
        for disease in related_diseases[:5]:  # Top 5 doenças
            disease_symptoms = self.get_symptoms_by_disease(disease["cid"])
            for symptom in disease_symptoms:
                if symptom not in selected_symptoms:
                    related_symptoms.add(symptom)
        
        return list(related_symptoms)[:10]  # Máximo 10 sugestões
    
    def get_symptom_analysis(self, symptoms: List[str]) -> Dict[str, Any]:
        """Análise completa dos sintomas selecionados"""
        if not symptoms:
            return {"error": "Nenhum sintoma selecionado"}
        
        # Encontrar doenças relacionadas
        related_diseases = self.get_diseases_by_symptoms(symptoms)
        
        # Análise por categoria
        category_analysis = {}
        for disease in related_diseases:
            category = disease["categoria"]
            if category not in category_analysis:
                category_analysis[category] = []
            category_analysis[category].append(disease)
        
        # Sintomas relacionados
        related_symptoms = self.get_related_symptoms(symptoms)
        
        return {
            "selected_symptoms": symptoms,
            "related_diseases": related_diseases[:10],  # Top 10
            "category_analysis": category_analysis,
            "suggested_symptoms": related_symptoms,
            "total_matches": len(related_diseases),
            "analysis_summary": self._generate_analysis_summary(symptoms, related_diseases)
        }
    
    def _generate_analysis_summary(self, symptoms: List[str], diseases: List[Dict]) -> str:
        """Gera um resumo da análise dos sintomas"""
        if not diseases:
            return "Nenhuma doença específica encontrada para os sintomas selecionados."
        
        top_disease = diseases[0]
        confidence = top_disease["confidence"]
        
        if confidence >= 75:
            severity = "alta"
        elif confidence >= 50:
            severity = "moderada"
        else:
            severity = "baixa"
        
        summary = f"Com base nos sintomas selecionados, foi encontrada uma correspondência de {severity} confiança "
        summary += f"com '{top_disease['nome']}' ({top_disease['cid']}). "
        summary += f"Esta doença está na categoria '{top_disease['categoria']}' e "
        summary += f"apresenta {len(top_disease['matching_symptoms'])} sintomas compatíveis."
        
        return summary
    
    def get_all_symptom_categories(self):
        """Retorna todas as categorias de sintomas"""
        return self.symptom_categories
    
    def search_symptoms(self, query: str) -> List[Dict[str, Any]]:
        """Busca sintomas que contenham o termo pesquisado"""
        results = []
        query_lower = query.lower()
        
        for category, symptoms in self.symptom_categories.items():
            matching_symptoms = [s for s in symptoms if query_lower in s.lower()]
            if matching_symptoms:
                results.append({
                    'category': category,
                    'symptoms': matching_symptoms
                })
        
        return results 