pipeline{
    agent { label:'agent1' }
    
    environment {
        SONAR_IP=
        ECR_REGISTRY=
        AWS_REGION=
    }    
    
    stages{
        stage('Trivy filesystem scan'){
            steps{
               sh '''docker run --rm \
               -v "$(pwd):/root/src" \
               aquasec/trivy fs --exit-code 1 --severity HIGH,CRITICAL /root/src
               '''
            }
        }

        stage('Testing Backend And Worker'){
            steps{
               sh '''docker run --rm \
               -v "$(pwd):/app" \
               -w "/app" \
               python:3.9-slim sh -c "pip install pytest -r backend/requirements.txt worker/requirements.txt && \
               PYTHONPATH=. pytest tests/backend_test.py tests/worker_test.py --junitxml=pythonresults.xml"
               '''  

            }
        }

        stage('Testing Frontend'){
            steps{
                sh '''docker run --rm \
                -v "$(pwd):/app" \
                -w "/app/frontend" \
                node:22-alpine sh -c "npm ci && \
                npm test ../tests/App.test.js --reporters=default --reporters=jest-junit --watchAll=false"
                '''
            }
        }

        stage('Sonar Scan') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token-new', variable: 'SONAR_TOKEN')]) {
                sh '''docker run --rm \
                    -v "$(pwd):/usr/src" \
                    sonarsource/sonar-scanner-cli \
                    -Dsonar.projectKey=three-tier-app \
                    -Dsonar.projectName="Three Tier DevSecOps App" \
                    -Dsonar.sources="." \
                    -Dsonar.exclusions="**/node_modules/**" \
                    -Dsonar.host.url="http://${SONAR_IP}:9000" \
                    -Dsonar.token="${SONAR_TOKEN}" \
                    -Dsonar.qualitygate.wait=true
                    '''
                }
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker compose build --no-cache'
                }
        }
        
        stage('Trivy Image Scan') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL nginx-custom'
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL frontend'
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL backend'
                }
            }
            
        stage('ECR login and push image to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin $ECR_REGISTRY
                
                docker tag nginx-custom:latest ${ECR_REGISTRY}/frontend:${BUILD_NUMBER}
                docker tag nginx-custom:latest ${ECR_REGISTRY}/frontend:latest

                docker tag backend:latest ${ECR_REGISTRY}/backend:${BUILD_NUMBER}
                docker tag backend:latest ${ECR_REGISTRY}/backend:latest

                docker tag worker:latest ${ECR_REGISTRY}/worker:${BUILD_NUMBER}
                docker tag worker:latest ${ECR_REGISTRY}/worker:latest

                docker push ${ECR_REGISTRY}/frontend:${BUILD_NUMBER}
                docker push ${ECR_REGISTRY}/frontend:latest

                docker push ${ECR_REGISTRY}/backend:${BUILD_NUMBER}
                docker push ${ECR_REGISTRY}/backend:latest

                docker push ${ECR_REGISTRY}/worker:${BUILD_NUMBER}
                docker push ${ECR_REGISTRY}/worker:latest

                '''

                }
            }

        }
    }
