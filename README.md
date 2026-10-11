# Three-Tier Application – DevSecOps Project

A containerized three-tier application with an automated CI/CD pipeline, security scanning, and AWS infrastructure provisioning. This project is being developed to explore DevSecOps practices, infrastructure as code, GitOps-based deployment, and application monitoring.

**Status:** Work in Progress 🚧

## Architecture

The application consists of a React frontend, Flask backend, PostgreSQL database, Redis message queue, and a background worker. Docker Compose is used for local container orchestration, while AWS infrastructure and deployment automation are being developed.

### Application Components

- **Frontend:** React application for creating and viewing tasks.
- **Backend:** Python Flask REST API for task management.
- **Database:** PostgreSQL for persistent task storage.
- **Message Queue:** Redis for asynchronous task processing.
- **Worker:** Python service that processes queued tasks and updates task status.
- **Containerization:** Docker and Docker Compose.

### Planned DevSecOps Workflow

The intended workflow is:

1. Source code is maintained in GitHub.
2. Jenkins runs automated backend, worker, and frontend tests.
3. Trivy scans the filesystem and container images for vulnerabilities.
4. SonarQube performs static code analysis and quality-gate checks.
5. Docker images are built, tagged, and pushed to Amazon Elastic Container Registry (ECR).
6. AWS infrastructure is provisioned and managed using Terraform.
7. Argo CD is planned for GitOps-based application deployment to Kubernetes.
8. Grafana is planned for application and infrastructure monitoring.

*The workflow is under development; individual stages and integrations will be validated as implementation progresses.*

## Technologies Used

| Category | Technologies |
|---|---|
| Frontend | React, JavaScript, Nginx |
| Backend | Python, Flask, REST API |
| Database | PostgreSQL |
| Messaging | Redis |
| Containers | Docker, Docker Compose |
| CI/CD | Jenkins |
| Security Scanning | Trivy |
| Code Quality | SonarQube |
| Cloud | AWS, Amazon ECR |
| Infrastructure as Code | Terraform |
| GitOps – Planned | Argo CD |
| Monitoring – Planned | Grafana |

## Repository Structure

```text
three-tier-app/
├── Infra/          # AWS infrastructure configuration
├── backend/        # Flask REST API
├── frontend/       # React application and Dockerfile
├── worker/         # Background task processing service
├── tests/          # Application and worker tests
├── Jenkinsfile     # CI/CD pipeline definition
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Git
- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/bhoomikamr/three-tier-app.git
cd three-tier-app
```

### Run the Application

Review the Dockerfiles and Docker Compose configuration, configure the required environment variables, and ensure the application containers can communicate with PostgreSQL and Redis.

Then build and start the services:

```bash
docker compose up --build
```

The current Compose configuration maps the frontend to port `8080` and the backend to port `5000`.

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:5000/api/v1/tasks`

**Note:** Local execution is still being validated. The Dockerfiles, service configuration, and frontend API routing must be corrected and tested before these instructions can be considered verified.

To stop the containers:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/tasks` | Retrieve tasks |
| POST | `/api/v1/tasks` | Create a new task |

Example request to create a task:

```bash
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test DevSecOps Pipeline"}'
```

New tasks are stored in PostgreSQL and submitted to Redis for asynchronous processing by the worker.

## Infrastructure and Deployment Roadmap

The following capabilities are planned or being developed:

- [x] Containerized frontend, backend, and worker components
- [x] Docker Compose service configuration
- [x] Initial Jenkins pipeline stages for testing and security scanning
- [x] Initial Terraform infrastructure configuration
- [ ] Validate local application builds and integration tests
- [ ] Complete AWS infrastructure provisioning using Terraform
- [ ] Validate Jenkins pipeline end to end
- [ ] Complete secure image publishing to Amazon ECR
- [ ] Deploy the application to Kubernetes
- [ ] Integrate Argo CD for GitOps-based deployments
- [ ] Configure Grafana dashboards and monitoring
- [ ] Validate application health, logs, and monitoring alerts

*Checkboxes indicate implementation or configuration present in the shared repository; they do not imply that the corresponding functionality has passed end-to-end testing.*

## Security Considerations

- Avoid committing AWS credentials, access keys, tokens, database passwords, or other secrets.
- Use Jenkins credentials or an appropriate secrets-management solution for sensitive configuration.
- Use least-privilege IAM permissions for AWS operations.
- Review Trivy findings and remediate applicable vulnerabilities.
- Validate application configuration and access controls before deployment to a shared or production environment.

## Learning Objectives

This project is intended to develop practical skills in:

- Containerizing multi-service applications.
- Building and testing CI/CD pipelines.
- Integrating security scanning into delivery workflows.
- Provisioning AWS infrastructure using Terraform.
- Implementing GitOps deployments using Argo CD.
- Monitoring application and infrastructure health using Grafana.

## Author

**Bhoomika M R**

GitHub: https://github.com/bhoomikamr

This is a personal learning project and is not intended to represent a production-ready deployment.
