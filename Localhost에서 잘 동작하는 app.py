import streamlit as st #모든 streamlit 명령은 "st" 별칭을 통해 사용할 수 있습니다
import bedrock as glib #로컬 라이브러리 스크립트에 대한 참조

st.set_page_config(page_title="Chatbot") #HTML 제목
st.title("Chatbot") #페이지 제목

if 'chat_history' not in st.session_state: #채팅 내역이 아직 생성되지 않았는지 확인합니다.
    st.session_state.chat_history = [] #채팅 내역 초기화
    
chat_container = st.container()

input_text = st.chat_input("Chat with your bot here") #채팅 입력창 표시

if input_text:
    glib.chat_with_kb(message_history=st.session_state.chat_history, new_text=input_text)

#채팅 기록 다시 렌더링하기 (Streamlit이 이 스크립트를 다시 실행하므로 이전 채팅 메시지를 보존할 필요가 있습니다.
for message in st.session_state.chat_history: #채팅 기록 루프
    with st.chat_message(message.role): #지정된 역할에 대한 챗 라인을 렌더링하며, with 블록의 모든 내용을 포함합니다.
        st.markdown(message.text) #챗 컨텐츠 출력
