# Requirements API (Serverless)

A serverless cloud service that automatically extracts requirements from XML documents using AI. Built on AWS with a fully serverless architecture, scalable, secure, and deployable via CI/CD.

---

## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Getting Started](#getting-started)  
- [Environment Variables](#environment-variables)  
- [Serverless Configuration](#serverless-configuration)  
- [Deployment](#deployment)  
- [API Endpoints](#api-endpoints)  
- [Contributing](#contributing)  

---

## Features

- Upload XML documents for asynchronous requirement extraction  
- Retrieve parsed results via API  
- Synchronous parsing for small XML snippets  
- Scalable and serverless architecture  
- CI/CD deployable  
- Fully integrated with AWS S3, DynamoDB, Lambda, and API Gateway  
- Future plan: semantic search of requirements  

---

## Architecture

- **AWS Lambda** – Handles API requests and parsing jobs  
- **S3 Bucket** – Stores uploaded XML files  
- **DynamoDB Table** – Stores job status and results  
- **API Gateway** – Exposes REST API endpoints  
- **Serverless Framework** – Manages deployment and infrastructure as code  

Optional future integrations:

- Vector search for requirements similarity  
- Secrets Manager for API keys  

---

## Getting Started

### Prerequisites

- Python 3.11  
- Node.js & npm  
- Serverless Framework v4  
- AWS account and CLI configured  

### Setup

```bash
# Clone repo
git clone https://github.com/your-username/requirements-api.git
cd requirements-api

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install Python dependencies
pip install -r requirements.txt
```

## Environment Variables

The following environment variables are required (configured in `serverless.yml`):

```yaml
JOBS_TABLE: requirements-api-${stage}-jobs
UPLOADS_BUCKET: requirements-api-${stage}-${aws:accountId}-uploads
OPENAI_API_KEY: <your-openai-api-key>
```

## Serverless Configuration

The `serverless.yml` file defines the infrastructure and application logic:

### Functions
- **submitJob** – Upload an XML file for asynchronous parsing (stores in S3, creates a job record in DynamoDB).
- **getResults** – Fetch parsing results for a given job.
- **parseSync** – Parse an XML file synchronously and return results immediately.
- **parseJob** – Triggered automatically by an S3 upload event to process the file in the background.

### Resources
- **S3 Bucket** – Stores uploaded XML files.
- **DynamoDB Table** – Persists job metadata and results.
- **IAM Roles/Permissions** – Grants Lambda functions the ability to read/write S3 and DynamoDB.

### Plugins
- **serverless-python-requirements** – Packages Python dependencies with the Lambda functions.
- **serverless-openapi-integration-helper** – Integrates the API Gateway with the OpenAPI schema (`schema.yml`).

## Deployments

This project uses the [Serverless Framework](https://www.serverless.com/) for automated deployments to AWS.

### Prerequisites
- Node.js and npm installed
- AWS CLI configured with appropriate credentials
- Serverless Framework (v4) installed globally:  

```bash
npm install -g serverless
```

### Deploy to AWS

You can deploy to AWS with a single command:

```bash
sls deploy --stage dev --region eu-central-1
```

### Stages

Stages allow you to manage multiple environments:

dev – Development environment

prod – Production environment

Deploy to a specific stage:

```bash
sls deploy --stage prod
```

### CI/CD

The stack can be deployed automatically via a CI/CD pipeline using Github actions.