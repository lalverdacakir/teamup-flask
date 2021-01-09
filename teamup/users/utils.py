import os
import hashlib

def hash(password):
    key = hashlib.md5(password.encode())
    return key.hexdigest()

def verify(password,password_to_check):
    new_pass = hash(password_to_check)
    
    if new_pass==password:
        return True
    else:
        return False
