cd /Users/tamaraporfiroteixeira/Projects/LLMOps-Udemy/multi-ai-agent/custom_jenkins

# 1. Build da imagem Jenkins
docker build -t jenkins-dind .

# 2. Rodar Jenkins container (macOS version)
docker run -d --name jenkins-dind \
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind

# 3. Verificar se está rodando
docker ps

# 4. Pegar a senha inicial do Jenkins
docker logs jenkins-dind | grep -A 5 "Administrator password"

# 5. Instalar Python no container
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3 python3-pip
ln -s /usr/bin/python3 /usr/bin/python
python --version
exit

# 6. Reiniciar Jenkins
docker restart jenkins-dindpipeline{
    agent any

    environment {
        SONAR_PROJECT_KEY = 'multi-ai-agent'
        SONAR_SCANNER_HOME = tool 'Sonarqube'
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'multi-ai-agent'
        IMAGE_TAG = 'latest'
        ECS_CLUSTER = 'multi-ai-agent-cluster'
        ECS_SERVICE = 'multi-ai-agent-service'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/tamaraporf/multi-ai-agent.git']])
                }
            }
        }

        stage('SonarQube Analysis'){
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('Sonarqube') {
                        sh """
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube-dind:9000 \
                        -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                        docker push ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy to ECS Fargate') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        sh """
                        aws ecs update-service \
                          --cluster ${ECS_CLUSTER} \
                          --service ${ECS_SERVICE} \
                          --force-new-deployment \
                          --region ${AWS_REGION}
                        """
                    }
                }
            }
        }
    }
}
