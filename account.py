import streamlit as st
import firebase_admin

from firebase_admin import credentials, auth, firestore
import os

cred = credentials.Certificate('.env.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def app(): 
    st.title("Haiiiii")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.email = ''
    if 'stock_preferences' not in st.session_state:
        st.session_state.stock_preferences = []


    def login(email):
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email

            user_ref = db.collection('users').document(user.uid)
            user_data = user_ref.get()

            if user_data.exists:
                st.session_state.user_full_name = user_data.to_dict().get('full_name', 'No name provided')
                st.session_state.stock_preferences = user_data.to_dict().get('stock_preferences', [])
            else:
                st.session_state.user_full_name = 'No name found in profile'

            st.session_state.signout = True
            st.session_state.signedout = True
            st.success('Login Successful')

        except Exception as e:
            st.warning(f'Login Failed: {str(e)}')  # Show actual error message
            print(f"Login Error: {e}")  # Print to Streamlit logs for debugging

    def signOutUser():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])

        if choice == 'Login':
            email = st.text_input('Email Account')
            password = st.text_input('Password', type = 'password')

            st.button('Login', on_click=login, args=(email,))

        else:
            email = st.text_input('Email Account')
            username = st.text_input('Unique Username')
            password = st.text_input('Password', type = 'password')

            if st.button('Create my Account'):
                user = auth.create_user(email = email, password = password, uid = username)
                st.success('Account created successfully!')

                user_ref = db.collection('users').document(user.uid)
                user_ref.set({
                    'email': email,
                    'username': username,
                    'stock_preferences': []  # Empty list for stock preferences
                })

                st.markdown('Please log in using your email and password')
            
    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email ' + st.session_state.useremail)
        st.button('Sign out', on_click = signOutUser)

        st.write("Your stock preferences:", st.session_state.stock_preferences)

        # Add stock preferences
        new_stock = st.text_input('Enter a stock ticker to add to your preferences')
        if st.button('Add to preferences'):
            if new_stock and new_stock not in st.session_state.stock_preferences:
                user_ref = db.collection('users').document(st.session_state.username)
                user_data = user_ref.get()

                if not user_data.exists:
                    # Create a new user document if it doesn’t exist
                    user_ref.set({
                        'email': st.session_state.useremail,
                        'username': st.session_state.username,
                        'stock_preferences': [new_stock]  # Add the first stock
                    })
                else:
                    # Update existing stock preferences
                    updated_preferences = st.session_state.stock_preferences + [new_stock]
                    user_ref.update({'stock_preferences': updated_preferences})

                # Update session state
                st.session_state.stock_preferences.append(new_stock)
                st.success(f'{new_stock} added to your preferences!')

        # Display updated preferences
        st.write("Updated stock preferences:", st.session_state.stock_preferences)