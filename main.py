import streamlit as st
from unique_emails import check_uniqueness
from message_design import message_box
import hashlib
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute ("CREATE TABLE IF NOT EXISTS users_table(firstname TEXT, lastname TEXT, emailaddress TEXT,password TEXT)")

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def add_userdata(firstname, lastname, emailaddress, password):
	c.execute("INSERT INTO users_table(firstname,lastname,emailaddress,password) VALUES (?,?,?,?)",(firstname, lastname, emailaddress, password))
	conn.commit()

def login_user(emailaddress,password):
	c.execute('SELECT * FROM users_table WHERE emailaddress =? AND password = ?',(emailaddress,password))
	data = c.fetchall()
	return data

def create_msg_box(value):
    c.execute('CREATE TABLE IF NOT EXISTS {}(message text, category text, Sender text)'.format(value))

def add_msg(message,category,Sender,Receiver):
    c.execute('''INSERT INTO {} VALUES (?, ?, ?)'''.format(Receiver),(message, category, Sender))
    conn.commit()

def call_all_emails():
    c.execute('SELECT emailaddress FROM users_table')
    all_emails=list()
    data=c.fetchall()
    for x in data:
        all_emails.append(x[0])
    return all_emails

def main():
    st.title('Email App')

    menu = ['Home', 'Login', 'Signup']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader("Email Web App")
    elif choice == 'Login':
        st.subheader('Login Section')

        placeholder_1=st.sidebar.empty()
        placeholder_2=st.sidebar.empty()
        emailaddress = placeholder_1.text_input('Email Address',key=1)
        password = placeholder_2.text_input('Password', type='password',key=2)

        def reset_button():
            st.session_state["p"] = False

        if st.sidebar.checkbox('Login',key='p'):

            create_usertable()
            hashed_pswd=make_hashes(password)
            result=login_user(emailaddress, check_hashes(password,hashed_pswd))

            if result:
                placeholder_1.empty()
                placeholder_2.empty()
                st.success('Logged In as {}'.format(emailaddress))

                address=st.text_input('Email_Address',value='')
                message=st.text_input('Type your message')
                submit_button=st.button(label='Send Mail')

                category='primary'
                if submit_button:
                    all_emails=call_all_emails()
                    if len(address)>0 and address in all_emails:
                        local_name, _ = address.split('@')
                        #st.info(local_name)
                        add_msg(message,category,emailaddress,local_name)
                        st.write('Send Your Message to {}'.format(address))
                    else:
                        st.error('Invalid email address')
                st.header('Your Messages')
                message_box(emailaddress)
                reset = st.button('Logout', on_click=reset_button)

            else:
                st.warning('Incorrect Username/Password')
    
    elif choice == 'Signup':
        create_usertable()
        st.subheader('Create New Account')
        first_name = st.text_input('FirstName')
        last_name = st.text_input('LastName')
        email_address = st.text_input('EmailAddress(use domain name @gmail.com)')
        new_password = st.text_input('Password', type='password',value='')

        all_emails= call_all_emails()

        #st.info(all_emails)

        if st.button('Signup'):
            unique_check=check_uniqueness(all_emails, email_address)
            if len(first_name) >= 0 and len(last_name) >= 0 and len(email_address) >= 0 and len(new_password) >= 0 and unique_check:

                add_userdata(first_name, last_name, email_address, make_hashes(new_password))
                st.success('You have successfully created on valid Account')
                st.info('Go to Login Menu to login')
                local_name, _ = email_address.split('@')
                create_msg_box(local_name)
            else:
                st.error('Please use a unique email address')
        


if __name__ == '__main__':
    main()