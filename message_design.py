import streamlit as st

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
st.set_page_config(layout="centered")
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


        for x, y in zip(messages, senders):
            # with col1(use_column_width=True):
            #     st.subheader('Messages')
            #     st.write(x)
            with st.container():
                col1, col2 = st.columns([2, .5])
                col1.subheader('Messages')
                col1.write(x)
                col2.subheader('Senders')
                col2.write(y)
            # with col2(use_column_width=True):
            #     st.subheader('Senders')
            #     st.write(y)
    elif option == 'Social':
        # st.stop() # on_click=callback) or st.session_state.button_clicked):
        messages, senders = all_messages(local_name, 'social')
        for x, y in zip(messages, senders):
            # print(x[0])
            # print(y[0])
            with st.container():
                col1, col2 = st.columns([2, .5])
                col1.subheader('Messages')
                col1.write(x)
                col2.subheader('Senders')
                col2.write(y)
    elif option=='Promotion':
        messages, senders = all_messages(local_name, 'promotion')
        for x, y in zip(messages, senders):
            with st.container():
                col1, col2 = st.columns([2, .5])
                col1.subheader('Messages')
                col1.write(x)
                col2.subheader('Senders')
                col2.write(y)
    elif option== 'Forum':
        messages, senders = all_messages(local_name, 'forum')
        for x, y in zip(messages, senders):
            with st.container():
                col1, col2 = st.columns([2, .5])
                col1.subheader('Messages')
                col1.write(x)
                col2.subheader('Senders')
                col2.write(y)