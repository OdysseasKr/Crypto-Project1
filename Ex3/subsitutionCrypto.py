#!/usr/bin/env python3

# Decrypts text that has been encrypted using the substitution method
# c: cyphertext
# k: key
# Return original message
def decrypt(c,k):
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    m = ''
    for i in range(len(c)):
        kl = k[i%len(k)]
        pos = abc.index(c[i]) - abc.index(kl)%len(abc)
        m = m + abc[pos]

    return m

with open("vigenere.txt") as f:
    cipher = f.read().strip()

print(decrypt(cipher, 'EMPEROR'))
