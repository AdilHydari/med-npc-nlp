import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
import sqlite3
from advanced_nlp_utils import extract_symptoms

# Set up OpenAI API key

# Database functions
def create_connection():
    return sqlite3.connect('chat_history.db')

def insert_chat(session_id, user_message, bot_response):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chat_history (session_id, user_message, bot_response) VALUES (?, ?, ?)',
                   (session_id, user_message, bot_response))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_message, bot_response FROM chat_history WHERE session_id = ?', (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Streamlit app
st.title("Medical Recommendation Chatbot")

# Generate a session ID for the user
if 'session_id' not in st.session_state:
    st.session_state.session_id = st.text_input("Enter your session ID or leave it blank to start a new session:")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = get_chat_history(st.session_state.session_id)

def get_response(query):
    symptoms = extract_symptoms(query)
    refined_query = f"Please provide possible conditions or advice, keeping in mind that Write empathetic and supportive messages for patients who have received a {', '.join(symptoms)}. Further, you should provide progressive prompting to further analyze the user's symptoms in order to provide a cursory diagnosis to the healthcare provider. "

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant knowledgeable about common medical conditions."},
        {"role": "user", "content": refined_query}
    ],
    max_tokens=150)

    bot_response = response.choices[0].message.content.strip()

    insert_chat(st.session_state.session_id, query, bot_response)
    st.session_state.chat_history.append((query, bot_response))
    return bot_response

user_input = st.text_input("Enter your symptoms or how you feel:")

if st.button("Submit"):
    if user_input:
        response = get_response(user_input)
        st.write(f"Bot: {response}")

st.write("Chat History:")
for user_message, bot_response in st.session_state.chat_history:
    st.write(f"User: {user_message}")
    st.write(f"Bot: {bot_response}")
