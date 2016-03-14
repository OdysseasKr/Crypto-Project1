#!/usr/bin/env python3
with open("thema4.txt") as f:
    cipher = f.read().strip()

abc = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'

# Attempt to decrypt with every possible key
for k in range(1, len(abc)):
    m = ''
    for c in cipher:
        i = abc.index(c)
        m = m + abc[(i-k)%len(abc)]

    print("Key: " + str(k))
    print(m)
