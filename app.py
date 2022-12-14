import streamlit as st
from unique_emails import check_uniqueness
from message_design import message_box
import hashlib
import sqlite3
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import model_from_json
import numpy as np
import pickle
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

def get_value(val,my_dict):
    for a,b in my_dict.items():
      if b==val:
        value=a
    return value

def predictions(model, texts,vec,class_names):
    data = vec.texts_to_sequences([texts])
    pad = pad_sequences(data, maxlen=240)
    pred = model.predict(pad)
    pred = np.argmax(pred, axis=1)
    y_pred = get_value(pred, class_names)
    return y_pred

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

                # def clear_form():
                #     st.session_state["foo"] = ""
                #     st.session_state["bar"] = ""
                # placeholder_3=st.empty()
                # placeholder_4=st.empty()
                # address=placeholder_3.text_input('Email_Address',value='')
                # message=placeholder_4.text_input('Type your message',value='')
                # submit_button=st.button(label='Send Mail',key=3)
                with st.form(key='my_form', clear_on_submit=True):
                    address=st.text_input('Email_Address', value="")
                    message=st.text_input('Type your messages',value='')
                    submit = st.form_submit_button(label='Send')

                all_emails = call_all_emails()
                Emails_Send=False
                if submit and len(address)>0 and address in all_emails:
                    local_name, _ = address.split('@')
                    class_names = {'primary': 1, 'promotion': 2, 'forum': 3, 'social': 4}
                    json_file = open('model.json', 'r')
                    loaded_model_json = json_file.read()
                    json_file.close()
                    loaded_model = model_from_json(loaded_model_json)
                    loaded_model.load_weights("model.h5")
                    with open('tokenizer.pickle', 'rb') as handle:
                        vec = pickle.load(handle)
                    category = predictions(loaded_model, message, vec, class_names)
                    add_msg(message,category,emailaddress,local_name)
                    st.write('Send Your Message to {}'.format(address))
                    Emails_Send=True
                        # placeholder_3.empty()
                        # placeholder_4.empty()
                        # address=placeholder_3.text_input('Email_Address',value='')
                        # message=placeholder_4.text_input('Type your message',value='')
                        # st.session_state['bar'] = ''
                if submit and Emails_Send==False:
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