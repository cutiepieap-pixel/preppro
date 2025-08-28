# App Runner Deployment Checklist

## Pre-deployment Setup

- [ ] AWS CLI configured with appropriate permissions
- [ ] Knowledge Base created in AWS Bedrock
- [ ] Knowledge Base ID noted down
- [ ] GitHub repository with code pushed

## Step 1: Create IAM Role

Choose one method:

### Option A: Using AWS Console
- [ ] Go to IAM Console → Roles → Create role
- [ ] Select "AWS service" → "App Runner"
- [ ] Create custom policy using content from `iam-policy.json`
- [ ] Name role: `AppRunnerBedrockRole`

### Option B: Using AWS CLI
- [ ] Run: `bash setup-iam-role.sh` (Linux/Mac)
- [ ] Or run: `.\setup-iam-role.ps1` (Windows PowerShell)

## Step 2: Deploy to App Runner

- [ ] Go to AWS App Runner Console
- [ ] Click "Create service"
- [ ] Select "Source code repository"
- [ ] Connect GitHub account
- [ ] Select your repository
- [ ] Choose branch (usually `main`)
- [ ] Set deployment trigger to "Automatic"
- [ ] Select "Use configuration file" (uses apprunner.yaml)

## Step 3: Configure Service

### Service Settings
- [ ] Service name: `preppro-chat`
- [ ] Virtual CPU: 0.25 vCPU
- [ ] Memory: 0.5 GB
- [ ] Port: 8080

### Security
- [ ] Instance role: `AppRunnerBedrockRole`

### Environment Variables
- [ ] `AWS_REGION`: Your AWS region (e.g., `us-east-1`)
- [ ] `KB_ID`: Your Knowledge Base ID
- [ ] `MODEL_ID`: (Optional) Model identifier

## Step 4: Deploy and Test

- [ ] Click "Create & deploy"
- [ ] Wait for deployment to complete (5-10 minutes)
- [ ] Test the application URL
- [ ] Verify chat functionality works
- [ ] Check that Knowledge Base responses are working

## Troubleshooting

If deployment fails:
- [ ] Check App Runner logs in AWS Console
- [ ] Verify environment variables are set correctly
- [ ] Ensure IAM role has correct permissions
- [ ] Confirm Knowledge Base ID is correct
- [ ] Check that all files are committed to GitHub

## Post-deployment

- [ ] Test the chat functionality
- [ ] Verify Korean responses (if applicable)
- [ ] Monitor App Runner metrics
- [ ] Set up any additional monitoring/alerting

## Environment Variables Reference

| Variable | Value | Notes |
|----------|-------|-------|
| `AWS_REGION` | `us-east-1` | Replace with your region |
| `KB_ID` | `XXXXXXXXXX` | Your actual Knowledge Base ID |
| `MODEL_ID` | `anthropic.claude-3-sonnet-20240229-v1:0` | Optional, has default |

## Account Information
- Target AWS Account: 602682890021
- User: [email]