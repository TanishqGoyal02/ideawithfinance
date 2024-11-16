import openai
import streamlit as st


# Set your OpenAI API key securely (be careful not to expose your key publicly)


# Initialize session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from OpenAI
    with st.chat_message("assistant"):
        # Collect the response text
        response_text = ""
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream and build the response text
        for chunk in response:
            delta_content = chunk.choices[0].delta.get("content", "")
            response_text += delta_content

        # Display the entire response text at once
        st.markdown(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})