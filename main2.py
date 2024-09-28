import streamlit as st
from model2 import ChatBot

if 'output' not in st.session_state:
    st.session_state.output = ''
if 'cot_flag' not in st.session_state:
    st.session_state.cot_flag = False

@st.cache_resource
def chatBot(dont_reload = True):
    return ChatBot(model='gemini-1.5-flash-latest', enable_cot= st.session_state.cot_flag)

def generate_response():
    if st.session_state.prompt != '':

        if st.session_state.cot_flag:
            with st.spinner("Implimenting Chain-of-thoughts..."):
                st.session_state.output = f'''{str(st.session_state.output)}   
:orange[**{st.session_state.prompt}:**]  
{chatBot().chat_cot(prompt = st.session_state.prompt)}
'''
                st.session_state.prompt = ''
                return

        with st.spinner("Generating..."):

                st.session_state.output = f'''{str(st.session_state.output)}   
:orange[**{st.session_state.prompt}:**]  
{chatBot().chat(prompt = st.session_state.prompt)}
'''
                st.session_state.prompt = ''
                return

def handel_cot():
    st.session_state.output = ''
    chatBot.clear()
    return

st.header("Let's chat")
st.write(st.session_state.output, unsafe_allow_html=True)

st.button("Ask", on_click=generate_response)


st.text_input(label='Chat...', key='prompt', value = '', on_change=generate_response)

if st.button("Restart Session"):
    st.session_state.output = ''
    chatBot().restart_chat()
    st.rerun()

st.toggle('Chain-of-thoughts', key= 'cot_flag', on_change= handel_cot)
