import streamlit as st
import requests
from streamlit_chat import message

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []  # This will store tuples of (query, response)

if 'instagram' not in st.session_state:
    st.session_state['instagram'] = []

if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ""  # Holds the current value of the query text area

API_BASE_URL = "https://gppod-devbe.xeventechnologies.com"

def generate_user_id():
    response = requests.get(f"{API_BASE_URL}/generateUserId")
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        st.error("Failed to generate user ID")
        return None

def qna_conversation(user_id, id, user_query):
    json_body = {
        "user_id": user_id,
        "id": id,
        "user_query": user_query
    }
    response = requests.post(f"{API_BASE_URL}/qnaConversation", json=json_body)
    if response.status_code == 200:
        data = response.json()
        data = data['data']
        refined = data.replace("<END_OF_TURN>", " ")
        return refined
    else:
        st.error("Conversation failed")
        return "Error in conversation"

st.title("Medical Assistant")
st.write("Please generate UserId first")

# Generate User ID Section
if st.button("Generate New User ID"):
    user_id = generate_user_id()
    if user_id:
        st.session_state['instagram'] = user_id
        st.success(f"Generated User ID: {user_id}")

if st.session_state['instagram']:
    # Conversation Section
    user_id_input = st.text_input("Enter User ID", value=st.session_state['instagram'])
    question_id = st.selectbox("Select Physician ID", [0, 1], format_func=lambda x: "Dr. William" if x == 0 else "Dr. Elizabeth")
    st.session_state['user_query'] = st.text_area("Your Query", value=st.session_state['user_query'])

    submit_col, clear_col = st.columns([3, 1])  # Adjust the column ratio as needed
    if submit_col.button("Submit Query"):
        if user_id_input and st.session_state['user_query']:
            response = qna_conversation(user_id_input, question_id, st.session_state['user_query'])
            # Append the new query and response pair to the chat history
            st.session_state['chat_history'].append((st.session_state['user_query'], response))
            st.session_state['user_query'] = ""  # Clear the query text area after submitting

    if clear_col.button("Clear Text"):
        # Clear the text area by resetting its state value
        st.session_state['user_query'] = ""

# Display the chat history
for query, response in st.session_state['chat_history']:
    message(query, is_user=True)
    message(response, is_user=False)
