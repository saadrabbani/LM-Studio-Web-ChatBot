# Imports
import streamlit as st
from streamlit_chat import message
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

st.title("Chatbot")

if 'history' not in st.session_state:
    st.session_state['history'] = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    ]

def get_text():
    input_text = st.text_input("You:", "", key="input")
    return input_text

user_input = get_text()
send_button = st.button("Send")

if send_button:
    if not user_input:
        st.warning("Please enter a message before sending.")
    else:
        st.session_state.history.append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            messages=st.session_state.history,
            model='',
            temperature=0.7,
        )

        output = completion.choices[0].message.content

        st.session_state.history.append({"role": "assistant", "content": output})

if st.session_state['history']:
    for i in range(len(st.session_state['history']) - 1, -1, -1):
        if st.session_state['history'][i]['role'] == 'assistant':
            message(st.session_state["history"][i]['content'], key=str(i))
        else:
            message(st.session_state['history'][i]['content'], is_user=True, key=str(i) + '_user')
