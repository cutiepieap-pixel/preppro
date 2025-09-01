# PowerShell script to launch EC2 instance for Simple HTTP Server Test

# Variables (modify these as needed)
$InstanceType = "t2.micro"
$AmiId = "ami-0c02fb55956c7d316"  # Amazon Linux 2023 (us-east-1)
$KeyName = "your-key-pair-name"   # Replace with your key pair name
$SecurityGroupName = "simple-http-test-sg"

Write-Host "Creating security group..."
try {
    aws ec2 create-security-group --group-name $SecurityGroupName --description "Security group for simple HTTP server test"
} catch {
    Write-Host "Security group might already exist, continuing..."
}

# Get the security group ID
$SgId = aws ec2 describe-security-groups --group-names $SecurityGroupName --query 'SecurityGroups[0].GroupId' --output text

Write-Host "Security Group ID: $SgId"

Write-Host "Adding security group rules..."
# SSH access
aws ec2 authorize-security-group-ingress --group-id $SgId --protocol tcp --port 22 --cidr 0.0.0.0/0

# HTTP port 80
aws ec2 authorize-security-group-ingress --group-id $SgId --protocol tcp --port 80 --cidr 0.0.0.0/0

# Custom port 8080
aws ec2 authorize-security-group-ingress --group-id $SgId --protocol tcp --port 8080 --cidr 0.0.0.0/0

Write-Host "Launching EC2 instance..."
$InstanceId = aws ec2 run-instances --image-id $AmiId --count 1 --instance-type $InstanceType --key-name $KeyName --security-group-ids $SgId --query 'Instances[0].InstanceId' --output text

Write-Host "Instance ID: $InstanceId"
Write-Host "Waiting for instance to be running..."

aws ec2 wait instance-running --instance-ids $InstanceId

# Get public IP
$PublicIp = aws ec2 describe-instances --instance-ids $InstanceId --query 'Reservations[0].Instances[0].PublicIpAddress' --output text

Write-Host "Instance launched successfully!"
Write-Host "Instance ID: $InstanceId"
Write-Host "Public IP: $PublicIp"
Write-Host ""
Write-Host "Connect with: ssh -i $KeyName.pem ec2-user@$PublicIp"
Write-Host "Test URL: http://$PublicIp:8080"