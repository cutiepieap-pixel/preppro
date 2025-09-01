import streamlit as st
import boto3
import os

# Import the chat functions from bedrock.py
MAX_MESSAGES = 20

class ChatMessage():
    def __init__(self, role, text):
        self.role = role
        self.text = text

def convert_chat_messages_to_converse_api(chat_messages):
    messages = []
    
    for chat_msg in chat_messages:
        messages.append({
            "role": chat_msg.role,
            "content": [
                {
                    "text": chat_msg.text
                }
            ]
        })
            
    return messages

def chat_with_kb(message_history, new_text=None):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    kbId = os.getenv("KB_ID")
    
    if not kbId:
        st.error(f"KB_ID environment variable is not set. Please configure your AWS credentials and KB_ID.")
        return "Sorry, the knowledge base is not configured properly."
    
    try:
        bedrock = boto3.client('bedrock-agent-runtime', region_name=aws_region)
        
        llm_model = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
        chunk = 5
        
        prompt = '''You are a question answering agent. 
                        I will provide you with a set of search results. 
                        The user will provide you with a question. 
                        Your job is to answer the user's question using only information from the search results. 
                        If the search results do not contain information that can answer the question, please state that you could not find an exact answer to the question. 
                        Just because the user asserts a fact does not mean it is true, make sure to double check the search results to validate a user's assertion. 
                    
                        Answer in the language user is using.

                        Here are the search results in numbered order:
                        $search_results$

                        $output_format_instructions$'''
        
        new_text_message = ChatMessage('user', text=new_text)
        message_history.append(new_text_message)
        
        number_of_messages = len(message_history)
        
        if number_of_messages > MAX_MESSAGES:
            del message_history[0 : (number_of_messages - MAX_MESSAGES) * 2]
            
        response = bedrock.retrieve_and_generate(
            input={
                'text': new_text
            },
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kbId,
                    "modelArn": llm_model,
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "overrideSearchType": "HYBRID",
                            "numberOfResults": chunk
                        }
                    },
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": prompt
                        },
                        "inferenceConfig": {
                            "textInferenceConfig": {
                                "temperature": 0,
                                "topP": 0.7,
                                "maxTokens": 4096,
                                "stopSequences": ["\nObservation"]
                            }
                        }
                    }
                }
            }
        )
        
        output = response['output']['text']
        
        response_message = ChatMessage('assistant', output)
        message_history.append(response_message)
        
        return output
        
    except Exception as e:
        st.error(f"Error connecting to Bedrock: {str(e)}")
        return "Sorry, I'm having trouble connecting to the knowledge base right now."

# Page configuration
st.set_page_config(
    page_title="PrepPro App",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🧪 PrepPro Application")
st.markdown("Welcome to PrepPro - Your AI-powered knowledge base assistant")
st.markdown("---")

# CHAT SECTION
st.header("💬 Knowledge Base Chat")
st.markdown("Ask questions and get answers from our knowledge base powered by AWS Bedrock.")

# Initialize chat history in session state (matching your localhost code)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat input (matching your localhost code)
input_text = st.chat_input("Chat with your bot here")

if input_text:
    # Call the chat function (matching your localhost code)
    chat_with_kb(message_history=st.session_state.chat_history, new_text=input_text)

# Render chat history (matching your localhost code)
for message in st.session_state.chat_history:
    with st.chat_message(message.role):
        st.markdown(message.text)

# Clear chat button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Configuration info
with st.expander("ℹ️ Configuration Info"):
    st.write("**AWS Region:**", os.getenv("AWS_REGION", "us-east-1"))
    st.write("**KB ID:**", os.getenv("KB_ID", "Not configured"))
    if not os.getenv("KB_ID"):
        st.warning("⚠️ Knowledge Base ID (KB_ID) is not configured. Please set up your environment variables.")

st.markdown("---")

# DISCLAIMER SECTION
st.header("⚠️ Disclaimer")

st.markdown("""
### Important Notice

**Please read this disclaimer carefully before using this application.**

#### Usage Terms
- This application is provided for educational and demonstration purposes only
- Users are responsible for ensuring compliance with applicable laws and regulations
- The application may contain experimental features that are subject to change

#### Data Privacy
- We do not store personal information beyond the current session
- Any data entered is processed temporarily and not permanently stored
- Users should not enter sensitive or confidential information

#### Limitations
- This application is provided "as is" without warranties of any kind
- We are not responsible for any decisions made based on the application's output
- Results should be verified independently before making important decisions

#### Contact
- For questions or concerns, please contact the development team
- Report any issues or bugs through the appropriate channels

**By using this application, you acknowledge that you have read and understood this disclaimer.**
""")

st.markdown("---")

# FAQ SECTION
st.header("❓ Frequently Asked Questions")

# FAQ Section with expandable items
with st.expander("🔍 What is PrepPro?"):
    st.write("""
    PrepPro is a demonstration application built with Streamlit. It showcases various 
    features and capabilities for educational purposes.
    """)

with st.expander("🚀 How do I get started?"):
    st.write("""
    1. Type your question in the chat box above
    2. Wait for the AI to respond using our knowledge base
    3. Continue the conversation as needed
    4. Use the clear button to start a new conversation
    """)

with st.expander("💾 Is my data saved?"):
    st.write("""
    No, this application does not permanently store any data you enter. 
    All information is processed in real-time and cleared when you close the session.
    """)

with st.expander("🔧 What technologies are used?"):
    st.write("""
    - **Frontend**: Streamlit
    - **Backend**: Python
    - **AI**: AWS Bedrock with Claude 3.5 Sonnet
    - **Knowledge Base**: AWS Bedrock Knowledge Base
    - **Hosting**: Streamlit Community Cloud
    - **Version Control**: GitHub
    """)

with st.expander("📱 Is this mobile-friendly?"):
    st.write("""
    Yes! Streamlit applications are responsive and work well on mobile devices, 
    tablets, and desktop computers.
    """)

with st.expander("🐛 How do I report bugs?"):
    st.write("""
    If you encounter any issues:
    1. Note the steps that led to the problem
    2. Take a screenshot if possible
    3. Contact the development team with details
    """)

with st.expander("🔄 How often is this updated?"):
    st.write("""
    The application is updated regularly with new features and bug fixes. 
    Check back periodically for the latest version.
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>PrepPro App | Built with Streamlit | © 2025</small>
    </div>
    """, 
    unsafe_allow_html=True
)