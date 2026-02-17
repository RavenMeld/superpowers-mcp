# aws-solution-architect

Design AWS architectures for startups using serverless patterns and IaC templates. Use when asked to design serverless architecture, create CloudFormation templates, optimize AWS costs, set up CI/CD pipelines, or migrate to AWS. Covers Lambda, API Gateway, DynamoDB, ECS, Aurora, and cost optimization.

## Quick Facts
- id: `aws-solution-architect--e1c3559c82`
- worth_using_score: `88/100`
- tags: `github, python, typescript, docker, aws, security, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/aws-solution-architect/SKILL.md`

## Use When
- --

## Workflow / Steps
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
- **Serverless Web**: S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **Event-Driven Microservices**: EventBridge + Lambda + SQS + Step Functions
- **Three-Tier**: ALB + ECS Fargate + Aurora + ElastiCache
- **GraphQL Backend**: AppSync + Lambda + DynamoDB + Cognito

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `14`
- has_scripts: `True`
- has_references: `True`
- has_assets: `True`
