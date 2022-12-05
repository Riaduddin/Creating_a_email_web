import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def Unique_emails_checking(emails,email):
    unique_email = set()
    for x in emails:
        # spliting the local & domain name
        local_name, domain_name = x.split('@')






    return True
