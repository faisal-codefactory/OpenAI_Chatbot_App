import openai
import streamlit as st
from streamlit_chat import message
# from pathlib import Path
# from configparser import ConfigParser

openai.api_key = st.secrets['OPENAI_API_KEY']
# cfg_reader = ConfigParser()
# fpath = Path.cwd() / Path('config.ini')
# cfg_reader.read(str(fpath))
# openai.api_key = cfg_reader.get('API_KEYS','OPENAI_API_KEY')

system_role_dict = {"role": "system",
                    "content": "You are a helpful Assistant. Create concise answer with engaging tone."}

if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [system_role_dict]
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=st.session_state['prompts']
    )
    # print(st.session_state['prompts'])
    # print("*"*50)
    message = completion.choices[0].message.content
    return message


def end_click():
    # st.session_state['prompts'] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]
    st.session_state['prompts'] = [system_role_dict]
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['user'] = ""


def chat_click():
    if st.session_state['user'] != '':
        chat_input = st.session_state['user']
        with st.spinner('Generating response...'):
            output = generate_response(chat_input)
            # store the output
            st.session_state['past'].append(chat_input)
            st.session_state['generated'].append(output)
            st.session_state['prompts'].append(
                {"role": "assistant", "content": output})
        st.session_state['user'] = ""


# st.image("{Your logo}", width=80)
st.title("OpenAI Chatbot with Conversation Memory")

user_input = st.text_input("You:", key="user")

chat_button = st.button("Send", on_click=chat_click)
end_button = st.button("New Chat", on_click=end_click)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
