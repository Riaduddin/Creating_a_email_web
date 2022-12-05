import streamlit as st
from unique_emails import Unique_emails_checking

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute ("CREATE TABLE IF NOT EXISTS users_table(firstname TEXT, lastname TEXT, emailaddress TEXT,password TEXT)")


def add_userdata(firstname, lastname, emailaddress, password):
	c.execute("INSERT INTO users_table(firstname,lastname,emailaddress,password) VALUES (?,?,?,?)",(firstname, lastname, emailaddress, password))
	conn.commit()

def login_user(emailaddress,password):
	c.execute('SELECT * FROM users_table WHERE emailaddress =? AND password = ?',(emailaddress,password))
	data = c.fetchall()
	return data

def call_all_emails():
    c.execute('SELECT emailaddress FROM users_table')
    data=c.fetchall()
    return data

def main():
    st.title('Email App')

    menu = ['Home', 'Login', 'Signup']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader("Email Web App")
    elif choice == 'Login':
        st.subheader('Login Section')

        emailaddress = st.sidebar.text_input('Email Address')
        password = st.sidebar.text_input('Password', type='password')
        if st.sidebar.button('Login'):
            # if password == '12345':
            create_usertable()
            result=login_user(emailaddress, password)
            if result:
                st.success('Logged In as {}'.format(emailaddress))

                msg=st.text_input('Type your message')

            else:
                st.warning('Incorrect Username/Password')
    
    elif choice == 'Signup':
        st.subheader('Create New Account')
        first_name = st.text_input('FirstName')
        last_name = st.text_input('LastName')
        email_address = st.text_input('EmailAddress(use domain name @gmail.com)')
        new_password = st.text_input('Password', type='password')

        all_emails=call_all_emails()

        if st.button('Signup'):
            unique_check=Unique_emails_checking(all_emails, email_address)
            if unique_check:
                create_usertable()
                add_userdata(first_name, last_name, email_address, new_password)
                st.success('You have successfully created on valid Account')
                st.info('Go to Login Menu to login')
            else:
                st.error('Please use a unique email address')
        


if __name__ == '__main__':
    main()