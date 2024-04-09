import streamlit as st
import requests

# Assuming your FastAPI server is running locally on port 8006
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
    # Constructing the JSON body according to the Pydantic model
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


st.title("Medical Q&A Bot")

# Generate User ID Section
if st.button("Generate New User ID"):
    user_id = generate_user_id()
    if user_id:
        st.success(f"Generated User ID: {user_id}")

# Conversation Section
user_id = st.text_input("Enter User ID")
question_id = st.selectbox("Select Physician ID", [0, 1], format_func=lambda x: "Dr. William" if x == 0 else "Dr. Elizabeth")
user_query = st.text_area("Your Query")

if st.button("Submit Query"):
    if user_id and user_query:
        response = qna_conversation(user_id, question_id, user_query)
        st.text_area("Response", value=response, height=300)
    else:
        st.error("Please provide both User ID and a query.")
