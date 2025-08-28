#!/bin/bash

# Script to create IAM role for App Runner with Bedrock permissions
# Run this script with AWS CLI configured

ROLE_NAME="AppRunnerBedrockRole"
POLICY_NAME="BedrockKnowledgeBasePolicy"

echo "Creating IAM role for App Runner..."

# Create trust policy for App Runner
cat > trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "tasks.apprunner.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Create the IAM role
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document file://trust-policy.json \
    --description "Role for App Runner to access Bedrock Knowledge Base"

# Create and attach the custom policy
aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name $POLICY_NAME \
    --policy-document file://iam-policy.json

echo "IAM role '$ROLE_NAME' created successfully!"
echo "Role ARN: $(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)"

# Clean up temporary file
rm trust-policy.json

echo ""
echo "Next steps:"
echo "1. Go to AWS App Runner Console"
echo "2. Create a new service"
echo "3. Use this role: $ROLE_NAME"
echo "4. Set environment variables:"
echo "   - AWS_REGION: us-east-1 (or your region)"
echo "   - KB_ID: YOUR_KNOWLEDGE_BASE_ID"