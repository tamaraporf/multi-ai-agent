pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'multi-ai-agent'
        DOCKER_TAG = "${BUILD_NUMBER}"
        // AWS variables - commented for local testing
        // ECR_REPO = 'multi-ai-agent'
        // AWS_REGION = 'us-east-1'
        // ECS_CLUSTER = 'multi-ai-agent-cluster'
        // ECS_SERVICE = 'multi-ai-agent-service'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo '🔍 Running SonarQube analysis...'
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=multi-ai-agent \
                                -Dsonar.projectName=multi-ai-agent \
                                -Dsonar.sources=app \
                                -Dsonar.python.version=3.11 \
                                -Dsonar.exclusions=**/__pycache__/**,**/venv/**,**/logs/**
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo '🚦 Waiting for SonarQube Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                echo '🧪 Testing Docker image...'
                script {
                    sh """
                        echo "Docker image built successfully:"
                        docker images | grep ${DOCKER_IMAGE}
                    """
                }
            }
        }
        
        /* 
        ============================================================
        AWS DEPLOYMENT STAGES - COMMENTED FOR LOCAL TESTING
        ============================================================
        Uncomment these stages when AWS credentials are configured
        
        stage('Push to ECR') {
            steps {
                echo '📤 Pushing image to AWS ECR...'
                script {
                    withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                        sh '''
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${ECR_REPO}:${DOCKER_TAG}
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${ECR_REPO}:latest
                            docker push ${ECR_REPO}:${DOCKER_TAG}
                            docker push ${ECR_REPO}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to ECS') {
            steps {
                echo '🚀 Deploying to AWS ECS Fargate...'
                script {
                    withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                        sh '''
                            aws ecs update-service \
                                --cluster ${ECS_CLUSTER} \
                                --service ${ECS_SERVICE} \
                                --force-new-deployment
                        '''
                    }
                }
            }
        }
        */
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo '🧹 Cleaning up...'
            sh 'docker system prune -f'
        }
    }
}