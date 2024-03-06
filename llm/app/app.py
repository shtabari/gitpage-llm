import streamlit as st
from llm_engine import llm_response

st.title("LLM ChatBot enhanced by RAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Welcome. How may I assist you ?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(llm_response(prompt,st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



# docker tag gitpage-llm-rag-st us-central1-docker.pkg.dev/github-page-413420/gitpage/gitpage-llm-rag-st:latest
# docker push us-central1-docker.pkg.dev/github-page-413420/gitpage/gitpage-llm-rag-st