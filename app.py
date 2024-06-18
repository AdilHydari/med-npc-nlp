import streamlit as st
from openai import OpenAI
import pandas as pd
import json
import time
from transformers import GPT2TokenizerFast
import wandb

# Initialize Weights & Biases for logging
# wandb.init(project="gpt3-fine-tune", entity="your-entity")

# Load the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Fine-tune GPT-3.5 Turbo with MedQuAD", layout="wide")

st.title("Fine-tune GPT-3.5 Turbo with MedQuAD")

# Chatbox setup
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("Chat with Fine-tuned GPT-3.5 Turbo")

# Function to send message
def send_message():
    user_input = st.session_state.user_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.user_input = ""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Chat interface
st.text_input("You: ", key="user_input", on_change=send_message)
for message in st.session_state.messages:
    role = message['role'].capitalize()
    content = message['content']
    if role == 'User':
        st.write(f"**{role}:** {content}")
    else:
        st.write(f"*{role}:* {content}")

# Fine-tuning setup and monitoring
st.header("Fine-tune Model with MedQuAD Dataset")

# Load and prepare the MedQuAD dataset
def prepare_dataset(file):
    df = pd.read_csv(file)
    data = []
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    for index, row in df.iterrows():
        prompt = row['AnswerID']
        completion = row['Answer']
        # Tokenize the text
        tokenized_prompt = tokenizer.encode(prompt, truncation=True, max_length=512)
        tokenized_completion = tokenizer.encode(completion, truncation=True, max_length=512)
        data.append({"prompt": tokenized_prompt, "completion": " " + tokenized_completion})
    with open('medquad.jsonl', 'w') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')
    return 'medquad.jsonl'

# Fine-tuning process
def fine_tune_model(file):
    file_path = prepare_dataset(file)
    with open(file_path, "rb") as f:
        response = client.files.create(file=f, purpose='fine-tune')
    training_file_id = response['id']
    fine_tune_response = client.fine_tunes.create(
        model="gpt-3.5-turbo",
        training_file=training_file_id,
        learning_rate_multiplier=0.2,
        n_epochs=4,
        batch_size=2
    )
    fine_tune_id = fine_tune_response['id']
    st.session_state.fine_tune_id = fine_tune_id

    # Log the fine-tuning process to Weights & Biases
    # wandb.log({"fine_tune_id": fine_tune_id})

# Monitor fine-tuning job
def monitor_fine_tune(fine_tune_id):
    status_response = client.fine_tunes.retrieve(id=fine_tune_id)
    return status_response['status']

# Upload dataset and start fine-tuning
uploaded_file = st.file_uploader("Choose a CSV file with the MedQuAD dataset", type=['csv'])
if uploaded_file is not None:
    if st.button("Start Fine-tuning"):
        try:
            fine_tune_model(uploaded_file)
            st.write("Fine-tuning started. Please wait...")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Check the status of fine-tuning
if "fine_tune_id" in st.session_state:
    status = monitor_fine_tune(st.session_state.fine_tune_id)
    st.write(f"Fine-tuning status: {status}")
    if status in ['succeeded', 'failed']:
        st.session_state.pop('fine_tune_id', None)
    else:
        st.write("Fine-tuning is still in progress. Please refresh the page after some time.")

# Progress bar for fine-tuning
if "fine_tune_id" in st.session_state:
    with st.spinner('Fine-tuning in progress...'):
        status = monitor_fine_tune(st.session_state.fine_tune_id)
        while status not in ['succeeded', 'failed']:
            status = monitor_fine_tune(st.session_state.fine_tune_id)
            st.write(f"Fine-tuning status: {status}")
            time.sleep(10)  # Polling interval
        st.success(f"Fine-tuning {status}!")
        st.session_state.pop('fine_tune_id', None)

# Save chat history for evaluation
def save_chat_history():
    chat_history = pd.DataFrame(st.session_state.messages)
    chat_history.to_csv('chat_history.csv', index=False)
    st.success("Chat history saved successfully.")

st.button("Save Chat History", on_click=save_chat_history)
