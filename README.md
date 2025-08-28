# PrepPro Chat - AWS App Runner Deployment Guide

This is a Streamlit chat application that uses AWS Bedrock Knowledge Base for question answering.

## Prerequisites

1. AWS Account with access to:
   - AWS App Runner
   - AWS Bedrock
   - AWS IAM
2. A configured Knowledge Base in AWS Bedrock
3. GitHub repository with this code

## Deployment Steps

### 1. Create IAM Role for App Runner

1. Go to AWS IAM Console
2. Create a new role with the following settings:
   - **Trusted entity**: AWS service
   - **Use case**: App Runner
3. Attach a custom policy using the content from `iam-policy.json`
4. Name the role: `AppRunnerBedrockRole`

### 2. Deploy to App Runner

1. Go to AWS App Runner Console
2. Click "Create service"
3. Choose "Source code repository"
4. Connect your GitHub account and select this repository
5. Configure the following:

#### Source and deployment settings:
- **Repository**: Your GitHub repo
- **Branch**: main (or your default branch)
- **Deployment trigger**: Automatic
- **Configuration file**: Use configuration file (apprunner.yaml)

#### Service settings:
- **Service name**: `preppro-chat`
- **Virtual CPU**: 0.25 vCPU
- **Memory**: 0.5 GB
- **Port**: 8080

#### Security settings:
- **Instance role**: Select `AppRunnerBedrockRole` (created in step 1)

#### Environment variables:
Add these environment variables:
- `AWS_REGION`: `us-east-1` (or your preferred region)
- `KB_ID`: `YOUR_KNOWLEDGE_BASE_ID` (replace with actual KB ID)
- `MODEL_ID`: `anthropic.claude-3-sonnet-20240229-v1:0` (optional)

### 3. Get Your Knowledge Base ID

1. Go to AWS Bedrock Console
2. Navigate to "Knowledge bases"
3. Find your knowledge base and copy its ID
4. Update the `KB_ID` environment variable in App Runner

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `AWS_REGION` | Yes | AWS region where your KB is located | `us-east-1` |
| `KB_ID` | Yes | Your Bedrock Knowledge Base ID | `ABCD1234` |
| `MODEL_ID` | No | Bedrock model to use | `anthropic.claude-3-sonnet-20240229-v1:0` |

## Troubleshooting

### App shows only skeletons
- Check if `bedrock.py` imports successfully
- Verify environment variables are set correctly
- Check App Runner logs for import errors

### Permission errors
- Ensure IAM role has correct permissions from `iam-policy.json`
- Verify the role is attached to App Runner service
- Check that Knowledge Base is in the same region as specified in `AWS_REGION`

### Knowledge Base not found
- Verify `KB_ID` environment variable matches your actual Knowledge Base ID
- Ensure Knowledge Base is in the correct AWS region

## Files Overview

- `app.py`: Main Streamlit application
- `bedrock.py`: AWS Bedrock integration functions
- `requirements.txt`: Python dependencies
- `apprunner.yaml`: App Runner configuration
- `Dockerfile`: Container configuration (alternative to apprunner.yaml)
- `iam-policy.json`: Required IAM permissions