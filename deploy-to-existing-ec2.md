# Deploy to Your Existing EC2 Instance

## Your Instance Details
- **Public IP:** 107.23.146.216
- **Instance ID:** i-0ba008d2c9bc6aded
- **Key Pair:** preppro

## Step 1: Connect to Your Instance
```bash
ssh -i preppro.pem ec2-user@107.23.146.216
```

## Step 2: Create the App Directory
```bash
mkdir ~/simple-http-test
cd ~/simple-http-test
```

## Step 3: Create the Python Server File
```bash
nano simple_http_server.py
```

Copy and paste your simple_http_server.py content, then save (Ctrl+X, Y, Enter).

## Step 4: Make it Executable and Run
```bash
chmod +x simple_http_server.py
python3 simple_http_server.py
```

## Step 5: Test the App
Open in browser: **http://107.23.146.216:8080**

## Important: Security Group Check
Your instance needs to allow inbound traffic on port 8080. If it doesn't work, you may need to:

1. Go to EC2 Console → Security Groups
2. Find the security group for your instance
3. Add inbound rule: TCP port 8080 from 0.0.0.0/0

## Quick Test Commands
```bash
# Test locally on the instance
curl http://localhost:8080

# Test health endpoint
curl http://localhost:8080/health
```