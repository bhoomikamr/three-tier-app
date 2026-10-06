pipeline{
    agent { label:'agent1' }
    
    stages{
        stage('Trivy filesystem scan'){
            steps{
               sh '''docker run --rm \
               -v "$(pwd):/root/src" \
               aquasec/trivy fs --exit-code 1 --severity HIGH,CRITICAL /root/src
               '''
            }
        }

        stage('Testing backend and worker'){
            steps{
               sh '''docker run --rm \
               -v "$(pwd):/app" \
               -w "/app" \
               python:3.9-slim sh -c "pip install pytest -r backend/requirements.txt && \
               PYTHONPATH=. pytest tests/backend_test.py tests/worker_test.py --junitxml=pythonresults.xml"
               '''  

            }
        }

        stage('Testing frontend'){
            steps{
                sh '''docker run --rm \
                -v "$(pwd):/app" \
                -w "/app" \
                node:22-alpine sh -c "npm ci && \
                npm test ./tests/App.test.js --reporters=default --reporters=jest-junit --watchAll=false"
                '''
            }
        }
    }
}