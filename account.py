import firebase_admin.auth
import streamlit as st
import firebase_admin
import yfinance as yf

from firebase_admin import credentials, auth, firestore
import os
from analysisFunctions import create_dashboard


auth = firebase_admin.auth

firebase_creds = st.secrets["FIREBASE"]

if not firebase_admin._apps:
    cred = credentials.Certificate({
    "type": firebase_creds["type"],
    "project_id": firebase_creds["project_id"],
    "private_key_id": firebase_creds["private_key_id"],
    "private_key": firebase_creds["private_key"],
    "client_email": firebase_creds["client_email"],
    "client_id": firebase_creds["client_id"],
    "auth_uri": firebase_creds["auth_uri"],
    "token_uri": firebase_creds["token_uri"],
    "auth_provider_x509_cert_url": firebase_creds["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_creds["client_x509_cert_url"],
    "universe_domain": firebase_creds["universe_domain"]
    })

    firebase_admin.initialize_app(cred)

db = firestore.client()

'''
def app(): 
    st.title("Welcome!")

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
            st.warning(f'Login Failed: {str(e)}')

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
                    'stock_preferences': []
                })

                st.markdown('Please log in using your email and password')
            
    if st.session_state.signout:
        st.button('Sign out', on_click=signOutUser)

        st.subheader('Add another stock!')
        new_stock = st.text_input('Enter a stock ticker to add to your preferences')
        new_stock_shares = st.number_input('Shares:', min_value=0, step=1)

        if st.button('Add to preferences'):
            if new_stock and new_stock_shares:
                user_ref = db.collection('users').document(st.session_state.username)
                user_data = user_ref.get()

                new_stock_entry = {"symbol": new_stock, "shares": new_stock_shares}

                if not user_data.exists:
                    user_ref.set({
                        'email': st.session_state.useremail,
                        'username': st.session_state.username,
                        'stock_preferences': [new_stock_entry] 
                    })
                    st.session_state.stock_preferences = [new_stock_entry]
                else:
                    existing_preferences = user_data.to_dict().get('stock_preferences', [])

                    updated_preferences = existing_preferences.copy()
                    for stock in updated_preferences:
                        if stock["symbol"] == new_stock:
                            stock["shares"] += new_stock_shares
                            break
                    else:
                        updated_preferences.append(new_stock_entry)

                    user_ref.update({'stock_preferences': updated_preferences})
                    st.session_state.stock_preferences = updated_preferences

                st.success(f'{new_stock} ({new_stock_shares} shares) added to your preferences!')
            else:
                st.warning('Make sure ticker is valid and shares is greater than zero')

        st.subheader("Your Stocks")
        for stock in st.session_state.stock_preferences:
            st.write(f"{stock['symbol']}: {stock['shares']} shares")
        
        stockPreferences = st.session_state.stock_preferences

        create_dashboard(stockPreferences)
'''

def app():

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.email = ''
    if 'stock_preferences' not in st.session_state:
        st.session_state.stock_preferences = []
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    if 'showInit' not in st.session_state:
        st.session_state.showInit = True


    if not st.session_state['signedout']:

        if st.session_state.showInit:
            st.title('Stock Dashboard')
            #stuff for logging in
            st.write('Welcome back! Log into see your dashboard:')
            if st.button('Log in!', on_click=logIn, type = 'primary'):
                st.session_state.showInit = False

            st.write('Don`t have an account? Click below to create an account:')
            if st.button('Sign up!', on_click=signUp, type='primary'):
                st.session_state.showInit = False

    if st.session_state.signout:
        st.button('Sign out', on_click = signOut)

        st.subheader('Add another stock!')
        new_stock = st.text_input('Enter a stock ticker to add to your preferences')
        new_stock_shares = st.number_input('Shares:', min_value=0, step=1)

        if st.button('Add to preferences'):
            if new_stock and new_stock_shares:
                user_ref = db.collection('users').document(st.session_state.username)
                user_data = user_ref.get()

                new_stock_entry = {"symbol": new_stock, "shares": new_stock_shares}

                if not user_data.exists:
                    user_ref.set({
                        'email': st.session_state.useremail,
                        'username': st.session_state.username,
                        'stock_preferences': [new_stock_entry] 
                    })
                    st.session_state.stock_preferences = [new_stock_entry]
                else:
                    existing_preferences = user_data.to_dict().get('stock_preferences', [])

                    updated_preferences = existing_preferences.copy()
                    for stock in updated_preferences:
                        if stock["symbol"] == new_stock:
                            stock["shares"] += new_stock_shares
                            break
                    else:
                        updated_preferences.append(new_stock_entry)

                    user_ref.update({'stock_preferences': updated_preferences})
                    st.session_state.stock_preferences = updated_preferences

                st.success(f'{new_stock} ({new_stock_shares} shares) added to your preferences!')
            else:
                st.warning('Make sure ticker is valid and shares is greater than zero')

            st.subheader("Your Stocks")
            for stock in st.session_state.stock_preferences:
                st.write(f"{stock['symbol']}: {stock['shares']} shares")
            
            stockPreferences = st.session_state.stock_preferences
            create_dashboard(stockPreferences)

def logIn():
    st.title('Stock Dashboard')
    email = st.text_input('Email Account')
    st.session_state.showInit = False
    password = st.text_input('Password', type = 'password')

    st.button('Log in', on_click=logInFinal, args=(email,))

def logInFinal(email):
    try:
        user = auth.get_user_by_email(email)
        st.session_state.username = user.uid
        st.session_state.useremail = user.email

        user_ref = db.collection('users').document(user.uid)
        user_data = user_ref.get()

        if user_data.exists:
            st.write(user_data)
            st.session_state.user_full_name = user_data.to_dict().get('full_name', 'No name provided')
            st.session_state.stock_preferences = user_data.to_dict().get('stock_preferences', [])
        else:
            st.session_state.user_full_name = 'No name found in profile'
        
        st.session_state.signout = True
        st.session_state.signedout = True
        st.success('Log in Successful')
        
    except Exception as e:
        st.warning(f'Login Failed: {str(e)}')
    

def signUp():
    st.title('Stock Dashboard')
    st.session_state.showInit = False
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
            'password': password,
            'stock_preferences': []
        })

        st.markdown('Please log in using your email and password')

    st.button('Log in!', on_click=logIn, type = 'primary')

def signOut():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''