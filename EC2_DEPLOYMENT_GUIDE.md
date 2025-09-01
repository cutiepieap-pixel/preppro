# EC2 Deployment Guide - Simple HTTP Server

## Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose **Amazon Linux 2023** (free tier eligible)
4. Instance type: **t2.micro** (free tier)
5. Create or select a key pair for SSH access
6. Security Group settings:
   - SSH (port 22) - Your IP only
   - HTTP (port 80) - Anywhere (0.0.0.0/0)
   - Custom TCP (port 8080) - Anywhere (0.0.0.0/0)

## Step 2: Connect to EC2

```bash
# Replace with your key file and instance IP
ssh -i your-key.pem ec2-user@your-instance-ip
```

## Step 3: Setup Python Environment

```bash
# Update system
sudo yum update -y

# Python3 should already be installed, verify:
python3 --version

# Create app directory
mkdir ~/test-app
cd ~/test-app
```

## Step 4: Upload Your App

Option A - Copy/paste the code:
```bash
nano simple_http_server.py
# Paste the code from your local file
```

Option B - Use git (if you have a repo):
```bash
git clone your-repo-url .
```

## Step 5: Run the App

```bash
# Make executable
chmod +x simple_http_server.py

# Run on port 8080
python3 simple_http_server.py

# Or run on port 80 (requires sudo)
sudo PORT=80 python3 simple_http_server.py
```

## Step 6: Test the App

Open in browser:
- `http://your-instance-ip:8080` (if running on port 8080)
- `http://your-instance-ip` (if running on port 80)

Health check: `http://your-instance-ip:8080/health`

## Step 7: Run as Background Service (Optional)

```bash
# Install screen to run in background
sudo yum install screen -y

# Start screen session
screen -S webapp

# Run your app
python3 simple_http_server.py

# Detach: Ctrl+A, then D
# Reattach: screen -r webapp
```

## Notes

- This simple HTTP server has **no WebSocket dependencies**
- Uses only Python standard library
- Should work perfectly on EC2 without any connection issues
- Much simpler than Streamlit or Flask for basic testing