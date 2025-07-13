# 🚀 Guia de Deploy - Med-IA no Render

## 📋 Pré-requisitos

1. **Conta no Render** (gratuita)
2. **Repositório GitHub** com o código
3. **Arquivos configurados** (já estão prontos!)

## 🎯 Passos para Deploy

### 1. Preparar Repositório GitHub

```bash
# Se ainda não tem um repositório
git init
git add .
git commit -m "Med-IA App v2.0 - Sistema médico inteligente"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/med-ia-app.git
git push -u origin main
```

### 2. Conectar ao Render

1. Acesse [render.com](https://render.com)
2. Faça login/cadastro
3. Clique em **"New +"** → **"Web Service"**
4. Conecte seu repositório GitHub
5. Selecione o repositório `med-ia-app`

### 3. Configuração Automática

O arquivo `render.yaml` já está configurado! O Render vai:

- ✅ Detectar automaticamente que é Python
- ✅ Instalar dependências do `requirements.txt`
- ✅ Usar o `Procfile` para iniciar
- ✅ Configurar variáveis de ambiente

### 4. Configurações Manuais (se necessário)

**Nome do Serviço**: `med-ia-app`
**Plano**: Free
**Branch**: main
**Build Command**: `pip install -r requirements.txt`
**Start Command**: `gunicorn main:app`

### 5. Variáveis de Ambiente

O Render vai configurar automaticamente:
- `PYTHON_VERSION`: 3.12.0
- `FLASK_ENV`: production

### 6. Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build (2-3 minutos)
3. ✅ **Pronto!** Seu app estará online

## 🔗 URLs

- **Produção**: `https://med-ia-app.onrender.com`
- **Health Check**: `https://med-ia-app.onrender.com/health`

## 📊 Monitoramento

### Logs
- Acesse o dashboard do Render
- Vá em **"Logs"** para ver logs em tempo real

### Métricas
- **Uptime**: 99.9% (plano free)
- **Performance**: Monitorada automaticamente

## 🔧 Troubleshooting

### Erro: "Module not found"
```bash
# Verificar se todas as dependências estão no requirements.txt
pip freeze > requirements.txt
```

### Erro: "Port already in use"
```bash
# O Render usa a variável PORT automaticamente
# Verificar se main.py está usando:
port = int(os.environ.get('PORT', 5000))
```

### Erro: "Static files not found"
```bash
# Verificar se a pasta static/ existe
# Verificar se main.py está configurado corretamente
```

## 🚀 Pós-Deploy

### 1. Testar APIs
```bash
# Health check
curl https://med-ia-app.onrender.com/health

# Testar busca de doenças
curl https://med-ia-app.onrender.com/api/diseases/search?q=diabetes
```

### 2. Configurar Domínio Personalizado (Opcional)
- Vá em **"Settings"** → **"Custom Domains"**
- Adicione seu domínio
- Configure DNS conforme instruções

### 3. Configurar CI/CD (Opcional)
- O Render faz deploy automático a cada push
- Configure branch protection no GitHub

## 📈 Escalabilidade

### Plano Free
- ✅ 750 horas/mês
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ✅ Domínio gratuito

### Upgrade (quando necessário)
- **Starter**: $7/mês
- **Standard**: $25/mês
- **Pro**: $50/mês

## 🎉 Sucesso!

Seu Med-IA estará online em:
**https://med-ia-app.onrender.com**

### Funcionalidades Disponíveis:
- ✅ Busca de doenças
- ✅ Análise de sintomas
- ✅ Diagnóstico inteligente
- ✅ Interações medicamentosas
- ✅ Interface responsiva

---

**Med-IA** - Transformando dados médicos em insights inteligentes! 🏥✨ 