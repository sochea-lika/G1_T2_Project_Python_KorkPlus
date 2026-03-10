# Check password
def password_strength_validation(password):
    if len(password) < 8:
        print("Password too short. Must be at least 8 characters.")
        return False
    
    special_character = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in special_character for c in password)

    if not has_lower:
        print("Password must contain at least one lowercase letter.")
    elif not has_upper:
        print("Password must contain at least one uppercase letter.")
    elif not has_digit:
        print("Password must contain at least one digit.")
    elif not has_special:
        print("Password must contain at least one special character.")
    else:
        return True
    
    return False 
