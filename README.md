# 🏥 Med-IA - Sistema Médico Inteligente

Sistema médico inteligente com backend em Flask e frontend web, que consome dados de doenças do Datasus (Tabela 2) e oferece funcionalidades avançadas de diagnóstico e análise de sintomas.

## 🚀 Funcionalidades

### ✅ Sistema de Doenças
- **217+ doenças** do CID-10 do Datasus
- Busca por nome e categoria
- Autocomplete inteligente
- Detalhes completos de cada doença
- Categorização por sistemas do corpo

### 🧠 Sistema de Sintomas Aprimorado
- **Mapeamento inteligente** entre sintomas e doenças
- Análise de confiança para diagnósticos
- Sugestões de sintomas relacionados
- Categorização por sistemas do corpo
- Busca contextual

### 💊 Sistema de Interações Medicamentosas
- Verificação de interações entre medicamentos
- Alertas de segurança
- Base de dados atualizada

### 🔍 Motor de Diagnóstico
- Análise baseada em sintomas
- Sugestões de exames
- Probabilidades de diagnóstico
- Recomendações médicas

## 🛠️ Tecnologias

- **Backend**: Flask, Python 3.12
- **Frontend**: HTML5, CSS3, JavaScript
- **Dados**: Datasus (CID-10), OMS
- **Deploy**: Render
- **Cache**: JSON local com atualização automática

## 📊 Dados

O sistema utiliza dados oficiais do:
- **Datasus** (Tabela 2 - CID-10)
- **OMS** (Classificação Internacional de Doenças)
- **217+ doenças** mapeadas com sintomas específicos

## 🚀 Como Usar

### Localmente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python main.py

# Acessar
http://localhost:5000
```

### No Render
1. Conecte seu repositório GitHub ao Render
2. Configure como Web Service
3. Use o arquivo `render.yaml` para configuração automática

## 📁 Estrutura do Projeto

```
MED-IA-APP/
├── main.py                 # Aplicação principal
├── enhanced_symptom_service.py  # Serviço de sintomas
├── doencas_cache.json      # Cache de doenças (217+)
├── src/routes/            # Rotas da API
├── static/               # Frontend
├── requirements.txt       # Dependências
├── Procfile             # Configuração Render
└── render.yaml          # Deploy automático
```

## 🔗 APIs Disponíveis

### Doenças
- `GET /api/diseases` - Lista todas as doenças
- `GET /api/diseases/search?q=termo` - Busca doenças
- `GET /api/diseases/categories` - Categorias
- `GET /api/diseases/<id>` - Detalhes da doença

### Sintomas
- `GET /api/symptoms/categories` - Categorias de sintomas
- `GET /api/symptoms/search?q=termo` - Busca sintomas
- `POST /api/symptoms/analyze` - Análise de sintomas
- `POST /api/symptoms/related` - Sintomas relacionados
- `GET /api/symptoms/disease/<cid>` - Sintomas por doença

### Diagnóstico
- `POST /api/v2/diagnose` - Diagnóstico inteligente
- `POST /api/v2/interactions` - Interações medicamentosas

## 🔄 Atualização de Dados

O sistema possui atualização automática diária do cache de doenças através do script `update_cache.py`.

## 📈 Status do Projeto

- ✅ Backend Flask funcionando
- ✅ Frontend responsivo
- ✅ Sistema de sintomas aprimorado
- ✅ Cache de 217+ doenças
- ✅ APIs documentadas
- ✅ Pronto para deploy no Render

## 🎯 Próximos Passos

1. **Deploy no Render** - Publicar aplicação
2. **Monitoramento** - Logs e métricas
3. **Expansão de dados** - Mais doenças do CID-10
4. **Machine Learning** - Diagnósticos mais precisos

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Med-IA** - Transformando dados médicos em insights inteligentes! 🏥✨ 