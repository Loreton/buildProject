#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import codecs
import zlib
import binascii
fDEBUG = False

def encodePassword(password):

    # Base64,  ascii
    output = codecs.encode(password, 'base64')
    output = codecs.encode(output, 'ascii')

    # Compress with zlib
    output = zlib.compress(output)

    # Base64, ascii, rot13
    output = codecs.encode(output, 'base64')
    output = codecs.encode(output, 'ascii')
    output = codecs.encode(output, 'rot13')
    if output and fDEBUG:
        print
        print "Unencoded...: " + password
        print "Encoded.....: " + output

    return output


def decodePassword(hashedPassword):
    try:
        # Decode rot13, ascii, base64
        output = codecs.decode(hashedPassword, 'rot13')
        output = codecs.decode(output, 'ascii')
        output = codecs.decode(output, 'base64')

        # Decompress zlib
        output = zlib.decompress(output)

        # Decode ascii, base64
        output = codecs.decode(output, 'ascii')
        output = codecs.decode(output, 'base64')

    except (binascii.Error), why:
        print "LN: no correct base64", why
        output = None

    except (zlib.error), why:
        print "LN: no correct zlib:", why
        output = None

    except (StandardError), why:
        print why
        output = None

    if output and fDEBUG:
        print
        print "Unencoded...: " + hashedPassword
        print "Encoded.....: " + output

    return output



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    new_pass = raw_input('Please enter a password: ')
    hashed_password = encodePassword(new_pass)
    print('The string to store in the db is: ' + hashed_password)

    hashed_password = raw_input('Now please enter the hashed password: ')
    if decodePassword(hashed_password):
        print('You entered the right password')
    else:
        print('I am sorry but the password does not match')
