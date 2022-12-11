
def check_uniqueness(emails,email):
    local_name, domain_name = email.split('@')
    if domain_name != 'gmail.com':
        return False
    if email in emails:
        return False
    else:
        return True


