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
    import time
    import random
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    kbId = os.getenv("KB_ID", "your-knowledge-base-id-here")  # Replace with your actual KB ID
    
    if not kbId:
        st.error(f"KB_ID environment variable is not set. Please configure your AWS credentials and KB_ID.")
        return "Sorry, the knowledge base is not configured properly."
    
    # Rate limiting check
    if 'last_request_time' not in st.session_state:
        st.session_state.last_request_time = 0
    
    current_time = time.time()
    time_since_last = current_time - st.session_state.last_request_time
    
    # Enforce minimum 2 seconds between requests
    if time_since_last < 2:
        wait_time = 2 - time_since_last
        st.warning(f"⏳ Please wait {wait_time:.1f} seconds before sending another message...")
        time.sleep(wait_time)
    
    st.session_state.last_request_time = time.time()
    
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
        
        # Retry logic for throttling
        max_retries = 3
        for attempt in range(max_retries):
            try:
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
                                        "temperature": 0.7,
                                        "topP": 0.9,
                                        "maxTokens": 4096,
                                        "stopSequences": ["\nObservation"]
                                    }
                                }
                            }
                        }
                    }
                )
                break  # Success, exit retry loop
                
            except Exception as retry_error:
                if "ThrottlingException" in str(retry_error) and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                    st.warning(f"⏳ Rate limited. Retrying in {wait_time:.1f} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise retry_error  # Re-raise if not throttling or max retries reached
        
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

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Create a container for the chat interface
with st.container():
    st.subheader("💭 Ask Your Question")
    st.markdown("Type your question below and click 'Send' or press Ctrl+Enter:")
    
    # Create form for better UX
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            input_text = st.text_area(
                "Your Question:",
                placeholder="💬 Type your question here...",
                height=100,
                label_visibility="collapsed"
            )
        
        with col2:
            st.write("")  # Add some spacing
            submit_button = st.form_submit_button("📤 Send", use_container_width=True)
        
        if submit_button and input_text.strip():
            # Call the chat function
            chat_with_kb(message_history=st.session_state.chat_history, new_text=input_text.strip())

# Chat history section
if st.session_state.chat_history:
    st.subheader("📝 Conversation History")
    
    # Render chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message.role):
            st.markdown(message.text)
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
else:
    st.info("👋 Start a conversation by typing your question in the chat box above!")

st.markdown("---")

# DISCLAIMER SECTION
st.header("⚠️ Disclaimer")

st.markdown("""
### Important Notice

**Please read this disclaimer carefully before using this application.**

#### Usage Terms
- THIS WAS CREATED JUST FOR LEARNING PURPOSES, DO NOT USE FOR ANY SENSITIVE OR CONFIDENTIAL DATA THAT CANNOT BE SHARED WITH THE PUBLIC.

Hello candidates!

My name is PrepPro, your AI assistant designed to help you succeed at Amazon Web Services Loop Interviews.

I understand that the Loop interview process at AWS can be quite challenging, which is why I'm here to provide you with guidance and support. My goal is to ensure you are well-prepared and confident going into your interviews.

I have in-depth knowledge of the core Leadership Principles that AWS looks for. I can help you craft compelling Situation, Task, Action, Result (STAR) examples that demonstrate how you embody these principles through real-life experiences.

Additionally, I'm well-versed in the different question types you may encounter, such as behavioral, situational, and case study questions. I can provide tips on how to structure your responses, what to emphasize, and how to effectively communicate your thought process.

So let's get started! I'm excited to work with you and help you put your best foot forward. Don't hesitate to ask me any questions you may have.

DISCLAIMER: I'm an AI assistant unaffiliated with Amazon Web Services (AWS). My responses are for practice only, not reflecting AWS's actual interviews. AWS isn't responsible for interview outcomes based on my information. Verify through official AWS resources. Use this exercise cautiously and do not solely rely on my responses for AWS or other interviews. Please do not share any personal or confidential data with the chatbot to ensure your data privacy.

**By using this application, you acknowledge that you have read and understood this disclaimer.**
""")

st.markdown("---")

# FAQ SECTION
st.header("❓ Frequently Asked Questions")

# FAQ Section with expandable items

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

with st.expander("📱 Is this mobile-friendly?"):
    st.write("""
    Yes! Streamlit applications are responsive and work well on mobile devices, 
    tablets, and desktop computers.
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