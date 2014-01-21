#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import uuid
import hashlib

def hashPassword(password):
        # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def checkPassword(hashedPassword, clearPassword):
    password, salt = hashedPassword.split(':')
    return password == hashlib.sha256(salt.encode() + clearPassword.encode()).hexdigest()



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    new_pass = raw_input('Please enter a password: ')
    hashed_password = hashPassword(new_pass)
    print('The string to store in the db is: ' + hashed_password)
    old_pass = raw_input('Now please enter the password again to check: ')
    if checkPassword(hashed_password, old_pass):
        print('You entered the right password')
    else:
        print('I am sorry but the password does not match')
