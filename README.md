# AWS Bedrock Chatbot

A Streamlit chatbot application that uses AWS Bedrock and Knowledge Base for intelligent conversations.

## Features
- Chat interface powered by Claude 3.5 Sonnet
- Knowledge Base integration for contextual responses
- Clean and intuitive Streamlit UI

## Setup
1. Set up AWS credentials with Bedrock access
2. Configure Knowledge Base ID
3. Install dependencies: `pip install -r requirements.txt`
4. Run locally: `streamlit run streamlit_app.py`

## Environment Variables
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key  
- `AWS_REGION`: AWS region (default: us-east-1)
- `KB_ID`: Your Knowledge Base ID