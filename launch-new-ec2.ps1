# Launch new EC2 instance with EC2 Instance Connect support

$SecurityGroupId = "sg-0e0bb4833faa7692f"  # Your existing security group
$AmiId = "ami-0c02fb55956c7d316"           # Amazon Linux 2023 with EC2 Instance Connect
$InstanceType = "t2.micro"
$KeyName = "preppro"

Write-Host "Launching new EC2 instance with EC2 Instance Connect support..."

$InstanceId = aws ec2 run-instances `
    --image-id $AmiId `
    --count 1 `
    --instance-type $InstanceType `
    --key-name $KeyName `
    --security-group-ids $SecurityGroupId `
    --query 'Instances[0].InstanceId' `
    --output text

Write-Host "Instance ID: $InstanceId"
Write-Host "Waiting for instance to be running..."

aws ec2 wait instance-running --instance-ids $InstanceId

$PublicIp = aws ec2 describe-instances `
    --instance-ids $InstanceId `
    --query 'Reservations[0].Instances[0].PublicIpAddress' `
    --output text

Write-Host "New instance launched successfully!"
Write-Host "Instance ID: $InstanceId"
Write-Host "Public IP: $PublicIp"
Write-Host ""
Write-Host "Try EC2 Instance Connect with this new instance."