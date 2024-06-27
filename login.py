import streamlit as st
from auth import register_user, login_user
from app import main
import time

st.title('AI Powered Research Assistant')

# Sidebar options
option = st.sidebar.selectbox('Choose Option', ('Login', 'Signup'))

if option == 'Signup':
    st.subheader('Create New Account')
    new_username = st.text_input('Username')
    new_password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if new_password == confirm_password and st.button('Signup'):
        register_user(new_username, new_password, 'credentials.json')
        st.success('Signup successful! Logging you in...')

elif option == 'Login':
    placeholder = st.empty()
    with st.empty():
        with st.container():    
            st.subheader('Login to Your Account')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')

            if st.button('Login'):
                if login_user(username, password, 'credentials.json'):
                    st.success(f'Please wait, Logging in as {username}...')
                    # Add your main application logic here after successful login
                    time.sleep(5)
                    placeholder.empty()
                    main()
                else:
                    st.error('Invalid username or password')
