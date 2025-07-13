from flask import Blueprint, request, jsonify
from enhanced_symptom_service import EnhancedSymptomService

symptoms_bp = Blueprint('symptoms', __name__)
symptom_service = EnhancedSymptomService()

@symptoms_bp.route('/symptoms/categories', methods=['GET'])
def get_symptom_categories():
    """Retorna todas as categorias de sintomas"""
    try:
        categories = symptom_service.get_all_symptom_categories()
        return jsonify({
            "success": True,
            "categories": categories
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@symptoms_bp.route('/symptoms/search', methods=['GET'])
def search_symptoms():
    """Busca sintomas por termo"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                "success": False,
                "error": "Parâmetro 'q' é obrigatório"
            }), 400
        
        results = symptom_service.search_symptoms(query)
        return jsonify({
            "success": True,
            "query": query,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@symptoms_bp.route('/symptoms/analyze', methods=['POST'])
def analyze_symptoms():
    """Analisa sintomas selecionados e retorna doenças relacionadas"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({
                "success": False,
                "error": "Lista de sintomas é obrigatória"
            }), 400
        
        analysis = symptom_service.get_symptom_analysis(symptoms)
        
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@symptoms_bp.route('/symptoms/related', methods=['POST'])
def get_related_symptoms():
    """Retorna sintomas relacionados aos selecionados"""
    try:
        data = request.get_json()
        selected_symptoms = data.get('symptoms', [])
        
        if not selected_symptoms:
            return jsonify({
                "success": False,
                "error": "Lista de sintomas é obrigatória"
            }), 400
        
        related_symptoms = symptom_service.get_related_symptoms(selected_symptoms)
        
        return jsonify({
            "success": True,
            "related_symptoms": related_symptoms
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@symptoms_bp.route('/symptoms/disease/<cid>', methods=['GET'])
def get_symptoms_by_disease(cid):
    """Retorna sintomas relacionados a uma doença específica"""
    try:
        symptoms = symptom_service.get_symptoms_by_disease(cid)
        
        return jsonify({
            "success": True,
            "disease_cid": cid,
            "symptoms": symptoms
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@symptoms_bp.route('/symptoms/diseases', methods=['POST'])
def get_diseases_by_symptoms():
    """Retorna doenças relacionadas aos sintomas selecionados"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({
                "success": False,
                "error": "Lista de sintomas é obrigatória"
            }), 400
        
        diseases = symptom_service.get_diseases_by_symptoms(symptoms)
        
        return jsonify({
            "success": True,
            "diseases": diseases,
            "total_matches": len(diseases)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500 