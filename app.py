import streamlit as st
from streamlit_chat import message
import requests


def generate_response(prompt, model):
    if model == 'Spotify Email Model':
        query_endpoint = "http://18.130.29.55/api/user/query"
    else:
        query_endpoint = "http://18.130.29.55/api/user/query1"
    data = {"userId":"7wew123",
            "API_Key":"5041ca9f28c84587b503ccbbed9af0e4",
            "Query": prompt}
    # Make POST request
    response = requests.post(query_endpoint, json=data)
    if response.status_code == 200:
        data = response.json()
        message = data["message"].strip("b'")
    else:
        message = "Sorry! I did not quite understand your question."
    return message 

#Creating the chatbot interface
st.title("Email ChatBot")

model = st.radio(
    "Choose your model",
    ('Spotify Email Model', 'Sales Email Model')
)

if model:
    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'something' not in st.session_state:
        st.session_state.something = ''

    def submit():
        st.session_state.something = st.session_state.input
        st.session_state.input = ''

    # We will get the user's input by calling the get_text function
    def get_text():
        st.text_input("You: ", key="input", on_change=submit)
        input_text = st.session_state.something
        return input_text

    user_input = get_text()
    if user_input:
        output = generate_response(user_input, model)
        # store the output
        st.session_state.generated.append(output)
        st.session_state.past.append(user_input)

    if st.session_state['generated']:
        
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
else:
    st.write("You did not choose any model")