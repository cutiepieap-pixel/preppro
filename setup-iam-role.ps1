# PowerShell script to create IAM role for App Runner with Bedrock permissions
# Run this script with AWS CLI configured

$RoleName = "AppRunnerBedrockRole"
$PolicyName = "BedrockKnowledgeBasePolicy"

Write-Host "Creating IAM role for App Runner..." -ForegroundColor Green

# Create trust policy for App Runner
$TrustPolicy = @"
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
"@

$TrustPolicy | Out-File -FilePath "trust-policy.json" -Encoding utf8

try {
    # Create the IAM role
    aws iam create-role `
        --role-name $RoleName `
        --assume-role-policy-document file://trust-policy.json `
        --description "Role for App Runner to access Bedrock Knowledge Base"

    # Create and attach the custom policy
    aws iam put-role-policy `
        --role-name $RoleName `
        --policy-name $PolicyName `
        --policy-document file://iam-policy.json

    Write-Host "IAM role '$RoleName' created successfully!" -ForegroundColor Green
    
    $RoleArn = aws iam get-role --role-name $RoleName --query 'Role.Arn' --output text
    Write-Host "Role ARN: $RoleArn" -ForegroundColor Yellow

    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to AWS App Runner Console"
    Write-Host "2. Create a new service"
    Write-Host "3. Use this role: $RoleName"
    Write-Host "4. Set environment variables:"
    Write-Host "   - AWS_REGION: us-east-1 (or your region)"
    Write-Host "   - KB_ID: YOUR_KNOWLEDGE_BASE_ID"
}
catch {
    Write-Host "Error creating IAM role: $_" -ForegroundColor Red
}
finally {
    # Clean up temporary file
    Remove-Item "trust-policy.json" -ErrorAction SilentlyContinue
}