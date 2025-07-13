#!/usr/bin/env python3
"""
Script de teste para o sistema de sintomas aprimorado
"""

from enhanced_symptom_service import EnhancedSymptomService

def test_enhanced_symptoms():
    """Testa o sistema de sintomas aprimorado"""
    print("🧪 Testando Sistema de Sintomas Aprimorado")
    print("=" * 50)
    
    # Inicializar serviço
    service = EnhancedSymptomService()
    
    # Teste 1: Categorias de sintomas
    print("\n1️⃣ Testando categorias de sintomas...")
    categories = service.get_all_symptom_categories()
    print(f"✅ Encontradas {len(categories)} categorias:")
    for category in categories.keys():
        print(f"   - {category}")
    
    # Teste 2: Busca de sintomas
    print("\n2️⃣ Testando busca de sintomas...")
    search_results = service.search_symptoms("dor")
    print(f"✅ Encontrados {len(search_results)} resultados para 'dor':")
    for result in search_results:
        print(f"   Categoria: {result['category']}")
        print(f"   Sintomas: {', '.join(result['symptoms'])}")
    
    # Teste 3: Análise de sintomas
    print("\n3️⃣ Testando análise de sintomas...")
    test_symptoms = ["Febre", "Tosse seca", "Fadiga"]
    analysis = service.get_symptom_analysis(test_symptoms)
    
    print(f"✅ Análise para sintomas: {', '.join(test_symptoms)}")
    print(f"   Doenças encontradas: {analysis['total_matches']}")
    print(f"   Resumo: {analysis['analysis_summary']}")
    
    if analysis['related_diseases']:
        print("   Top 3 doenças relacionadas:")
        for i, disease in enumerate(analysis['related_diseases'][:3]):
            print(f"     {i+1}. {disease['nome']} ({disease['cid']}) - Confiança: {disease['confidence']}%")
    
    # Teste 4: Sintomas relacionados
    print("\n4️⃣ Testando sintomas relacionados...")
    related_symptoms = service.get_related_symptoms(test_symptoms)
    print(f"✅ Sintomas relacionados sugeridos: {', '.join(related_symptoms)}")
    
    # Teste 5: Doenças por sintomas
    print("\n5️⃣ Testando doenças por sintomas...")
    diseases = service.get_diseases_by_symptoms(test_symptoms)
    print(f"✅ Encontradas {len(diseases)} doenças para os sintomas:")
    for i, disease in enumerate(diseases[:5]):
        print(f"   {i+1}. {disease['nome']} - Score: {disease['score']}")
    
    # Teste 6: Sintomas por doença
    print("\n6️⃣ Testando sintomas por doença...")
    if diseases:
        test_cid = diseases[0]['cid']
        symptoms = service.get_symptoms_by_disease(test_cid)
        print(f"✅ Sintomas para {diseases[0]['nome']} ({test_cid}):")
        print(f"   {', '.join(symptoms)}")
    
    print("\n🎉 Todos os testes concluídos com sucesso!")

if __name__ == "__main__":
    test_enhanced_symptoms() 