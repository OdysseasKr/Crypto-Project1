#! /usr/bin/env python

"""This is an RC4 Implementation with 5-bit encoding."""

import lfsr_project as s


def encrypt(key, text):
    """Encrypt the given text with the key with RC4."""
    keyBits = s.text_enc(key)  # The key in bits with 5bit encoding
    textInBits = s.text_enc(text)  # The text in bits with 5bit encoding
    plen = len(text)  # 31 characters

    S = createS(keyBits)
    # S is now filled with random values of 5bit encoding
    K = outputK(S, plen)
    # K is now filled with random values of 5bit encoding
    Kbits = convertValuesToBits(K)

    # encrypt the bits of the text with the bits of the cipher
    cBits = s.string_xor(textInBits, Kbits[:155])

    # this is what is looks like in a string format
    cText = s.text_dec(cBits)

    return cText


def decrypt(key, cipher):
    """Decrypt the cipher with the key with RC4."""
    keyBits = s.text_enc(key)  # The key in bits with 5bit encoding
    cipherInBits = s.text_enc(cipher)  # The text in bits with 5bit encoding
    plen = len(cipher)  # 31 characters

    S = createS(keyBits)
    # S is now filled with random values of 5bit encoding
    K = outputK(S, plen)
    # K is now filled with random values of 5bit encoding
    Kbits = convertValuesToBits(K)

    originalBits = s.string_xor(cipherInBits, Kbits[:155])

    # this should be the original text
    originalText = s.text_dec(originalBits)

    return originalText


def createS(keyBits):
    """Create the S array."""
    S = []
    j = 0

    # Initialize the Array with values from 0 to 256)
    for i in range(0, 256):
        S.append(i % 256)

    # Create the Array
    # add the index j with the value of S[i] and a bit of a letter
    # in the position i % keylen of the key in bits (155)
    # and mod it with 256
    for i in range(0, 256):
        j = (j + S[i] + int(keyBits[i % len(keyBits)], 2)) % 256
        S[i], S[j] = S[j], S[i]  # now swap the values of S[i] and S[j]

    return S


def outputK(S, plen):
    """Output the encrypted bits."""
    i = 0
    j = 0
    K = []
    while (plen > 0):
        i = (i + 1) % 256  # calculate the value of the index i
        j = (j + S[j]) % 256  # calculate the value of the index j
        S[i], S[j] = S[j], S[i]  # swap the values of S[i] and S[j]
        K.append(S[(S[i] + S[j]) % 256])
        # add the values of S[i], S[j] mod 256 and output the value of S[that]
        plen = plen - 1

    return K


def convertValuesToBits(v):
    """Convert the values of the 5bit encoding to a series of bits."""
    b = []
    for i in v:
        b.append('{0:05b}'.format(i))

    bits = ''.join(b)
    return bits  # return the bits in a string format


key = "MATRIX"  # The key with which the encryption is made

text = "Neversendahumantodoamachinesjob"  # The text to encrypt

cText = encrypt(key, text)
print "Encrypted message: ", cText
# decrypt the encrypted bits with the cipher in order to get the real text bits
originalText = decrypt(key, cText)
print "Decrypted message: ", originalText
