import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth
import os

cred = credentials.Certificate('.env.json')
firebase_admin.initialize_app(cred)

def app(): 
    st.title("Haiiiii")

    choice = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])
    def login():
        try:
            user = auth.get_user_by_email(email)
            st.write('Login Successful')

        except:
            st.warning('Login Failed')

    if choice == 'Login':
        email = st.text_input('Email Account')
        password = st.text_input('Password', type = 'password')

        st.button('Login', on_click=login)

    else:
        email = st.text_input('Email Account')
        username = st.text_input('Unique Username')
        password = st.text_input('Password', type = 'password')

        if st.button('Create my Account'):
            user = auth.create_user(email = email, password = password, uid = username)
            st.success('Account created successfully!')
            st.markdown('Please log in using your email and password')
        