import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("Claude AI Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.completions.create(  
            prompt=f"Human: {prompt}\n\nAssistant:",
            stop_sequences=["\nHuman:"],
            model="claude-v1",
            max_tokens_to_sample=300,
        )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.completion)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.completion})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()