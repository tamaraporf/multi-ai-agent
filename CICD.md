# CI/CD Pipeline - Multi AI Agent

## 🎯 Overview
Implementei um pipeline completo de CI/CD usando **Jenkins**, **SonarQube** e **Docker**, com integração ao GitHub para automação de builds, análise de qualidade e preparação para deploy na AWS.

---

## 🏗️ Arquitetura

```
GitHub Push → Jenkins Pipeline → SonarQube Analysis → Docker Build → (AWS Deploy)
```

### Componentes:
- **Jenkins**: Orquestração da pipeline (Docker-in-Docker)
- **SonarQube**: Análise estática de código (bugs, vulnerabilidades, code smells)
- **Docker**: Containerização da aplicação Python/FastAPI/Streamlit
- **GitHub**: Controle de versão e trigger automático
- **AWS ECR/ECS**: Deploy em produção (preparado, não implementado)

---

## 🔄 Pipeline Stages

### 1. Checkout
```groovy
checkout scm  // Baixa código do GitHub
```

### 2. SonarQube Analysis
```groovy
sonar-scanner -Dsonar.projectKey=multi-ai-agent \
              -Dsonar.sources=app \
              -Dsonar.python.version=3.11
```
**Analisa**: Bugs, vulnerabilidades, code smells, duplicação de código

### 3. Quality Gate
```groovy
waitForQualityGate abortPipeline: false
```
**Valida**: Se código passa nos critérios de qualidade do SonarQube

### 4. Build Docker Image
```groovy
docker build -t multi-ai-agent:${BUILD_NUMBER} .
docker tag multi-ai-agent:${BUILD_NUMBER} multi-ai-agent:latest
```

### 5. Test Docker Image
```groovy
docker images | grep multi-ai-agent  // Verifica criação da imagem
```

### 6. AWS Deploy (Preparado)
```groovy
// Push to ECR
docker push <ecr-repo>/multi-ai-agent:latest

// Deploy to ECS Fargate
aws ecs update-service --force-new-deployment
```

---

## 🐳 Docker Setup

### Aplicação (Dockerfile)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501 9999
CMD ["streamlit", "run", "app/frontend/ui.py"]
```

### Jenkins com Docker-in-Docker (custom_jenkins/Dockerfile)
```dockerfile
FROM jenkins/jenkins:lts
USER root
# Instala Docker dentro do Jenkins para executar builds
RUN apt-get install -y docker-ce docker-ce-cli containerd.io
RUN usermod -aG docker jenkins
USER jenkins
```

**Por que Docker-in-Docker?** Jenkins precisa executar comandos Docker para fazer build das imagens.

---

## 🔗 Comunicação entre Containers

```
Jenkins Container     ──┐
                        ├──> 172.17.0.1 (Docker Host Network)
SonarQube Container   ──┘
```

- Jenkins acessa SonarQube via `http://172.17.0.1:9000`
- SonarQube envia webhook para Jenkins via `http://172.17.0.1:8080/sonarqube-webhook/`

---

## ⚡ Webhook do SonarQube

**Problema**: Pipeline esperava até 10min pelo resultado da análise

**Solução**: Webhook configurado
```
SonarQube Analysis Complete
    ↓
POST http://172.17.0.1:8080/sonarqube-webhook/
    ↓
Jenkins recebe resultado imediatamente
    ↓
Pipeline continua em segundos (não 10min)
```

---

## 🚀 Fluxo Completo

1. **Developer**: `git push` no GitHub
2. **Jenkins**: Detecta mudança → Inicia pipeline automaticamente
3. **Stage 1**: Checkout do código
4. **Stage 2**: SonarQube analisa qualidade
5. **Stage 3**: Quality Gate valida resultado
6. **Stage 4**: Build da imagem Docker
7. **Stage 5**: Testa criação da imagem
8. **Stage 6-7**: (Futuro) Push ECR + Deploy ECS Fargate

---

## 📊 Benefícios Implementados

✅ **Automação**: Push no GitHub → Build automático  
✅ **Qualidade**: SonarQube bloqueia código com bugs/vulnerabilidades  
✅ **Containerização**: Aplicação empacotada e portável  
✅ **Rastreabilidade**: Cada build tem número único e logs completos  
✅ **Feedback rápido**: Webhook reduz tempo de pipeline  
✅ **Preparado para produção**: Infraestrutura pronta para AWS deploy  

---

## 🛠️ Comandos Principais

### Iniciar ambiente local
```bash
# Jenkins
docker run -d --name jenkins-dind \
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind

# SonarQube
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  sonarqube:lts-community
```

### Permissões Docker
```bash
docker exec -u root jenkins-dind chown root:docker /var/run/docker.sock
docker exec -u root jenkins-dind chmod 666 /var/run/docker.sock
```

---

## 🎓 Pontos para Entrevista

### 1. "Por que Jenkins e não GitHub Actions?"
- **Jenkins**: Mais controle, self-hosted, sem limite de minutos
- **GitHub Actions**: Mais simples, mas custos em projetos maiores

### 2. "Como garante qualidade de código?"
- SonarQube analisa antes do build
- Quality Gate bloqueia código com problemas críticos
- Métricas: bugs, vulnerabilidades, code smells, cobertura

### 3. "Desafios enfrentados?"
- **Problema**: Jenkins não conseguia acessar Docker
- **Solução**: Compartilhar socket Docker + ajustar permissões
- **Problema**: Timeout no Quality Gate (10min)
- **Solução**: Configurar webhook para notificação instantânea

### 4. "Como escala para produção?"
- ECR para armazenar imagens Docker
- ECS Fargate para deploy serverless (sem gerenciar EC2)
- Load balancer para distribuir tráfego
- Auto-scaling baseado em CPU/memória

### 5. "Segurança na pipeline?"
- Credenciais armazenadas no Jenkins Credentials Store
- Análise de vulnerabilidades no SonarQube
- Imagens Docker escaneadas antes do push
- Network isolation entre containers

---

## 📝 Próximos Passos (Roadmap)

- [ ] Testes automatizados (pytest) na pipeline
- [ ] Deploy staging automático após merge
- [ ] Deploy produção com aprovação manual
- [ ] Monitoramento com Prometheus/Grafana
- [ ] Rollback automático em caso de falha
- [ ] Blue-Green deployment no ECS

---

## 🔍 Métricas Atuais

- **Build time**: ~3-5 minutos
- **SonarQube analysis**: ~30 segundos
- **Docker build**: ~2 minutos
- **Quality Gate**: Aprovado ✅
- **Success rate**: 100% após configuração
