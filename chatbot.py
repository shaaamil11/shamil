import streamlit as st
from google import genai

# -----------------------------------------
# Streamlit page settings
# -----------------------------------------

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Gemini AI Chatbot")

st.write(
    "Ask any question. The chatbot uses Gemini API to generate responses."
)

# -----------------------------------------
# Gemini client
# -----------------------------------------

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------------------
# Initialize chat history
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------
# Display previous chat messages
# -----------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------------------
# User input
# -----------------------------------------

user_prompt = st.chat_input("Type your question here...")

if user_prompt:
    # Store and display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.write(user_prompt)

    # Build conversation context
    conversation = ""

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        conversation += f"{role}: {content}\n"

    prompt = f"""
    You are a helpful AI tutor.
    Answer clearly and simply.

    Conversation so far:
    {conversation}

    Assistant:
    """

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            assistant_reply = response.text
            st.write(assistant_reply)

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# -----------------------------------------
# Clear chat button
# -----------------------------------------

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()