def username_func(username):
    name_error = ''

    if len(username) < 3 or len(username) > 20 :
        name_error = "You did not enter a valid username (must be 3-20 characters)"
        
    for let in username:
        if let == ' ':
            name_error = "You did not enter a valid username (may not contain spaces)"

    return name_error

def password_func(password):
    pass_error = ''

    if len(password) < 3 or len(password) > 20 :
            pass_error = "You did not enter a valid password (must be 3-20 characters)"
        
    for char in password:
        if char == ' ':
            pass_error = "You did not enter a valid password (may not contain spaces)"

    return pass_error