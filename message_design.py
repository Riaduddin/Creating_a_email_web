import streamlit as st

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def all_messages(tablename,category):
    c.execute('SELECT message,Sender FROM {} WHERE category=? '.format(tablename), (category,))
    data = c.fetchall()
    mails = list()
    senders = list()
    for x in data:
        mails.append(x[0])
        senders.append(x[1])
    return mails,senders

def message_box(address):
    local_name, _ = address.split('@')
    option = st.selectbox(
        'Your All Messages',
        ('Primary', 'Social', 'Promotion', 'Forum'))
    if option == 'Primary':  # on_click=callback) or st.session_state.button_clicked):
        messages, senders = all_messages(local_name, 'primary')
        col1, col2 = st.columns(2)
        for x, y in zip(messages, senders):
            with col1:
                st.subheader('Messages')
                st.write(x)
            with col2:
                st.subheader('Senders')
                st.write(y)
    elif option == 'Social':
        # st.stop() # on_click=callback) or st.session_state.button_clicked):
        messages, senders = all_messages(local_name, 'social')
        col1, col2 = st.columns(2)
        for x, y in zip(messages, senders):
            # print(x[0])
            # print(y[0])
            with col1:
                st.subheader('Messages')
                st.write(x)
            with col2:
                st.subheader('Senders')
                st.write(y)
    elif option=='Promotion':
        messages, senders = all_messages(local_name, 'promotion')
        col1, col2 = st.columns(2)
        for x, y in zip(messages, senders):
            with col1:
                st.subheader('Messages')
                st.write(x)
            with col2:
                st.subheader('Senders')
                st.write(y)
    elif option== 'Forum':
        messages, senders = all_messages(local_name, 'forum')
        col1, col2 = st.columns(2)
        for x, y in zip(messages, senders):
            with col1:
                st.subheader('Messages')
                st.write(x)
            with col2:
                st.subheader('Senders')
                st.write(y)