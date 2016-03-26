#! /usr/bin/env python3

"""Cracking LFSR."""

import numpy as np
import lfsr_project as s


def lfsr1(F, Pb, Cb, Ciphertext):

    """Crack the first LFSR."""
    K = list(s.string_xor(Pb, Cb))
    K = [int(k) for k in K]

    # This gets the stream that will be used to decrypt the message
    # Using the reverse K, it gets the lfsr keystream.
    # The number of bits is: (period of lfsr) - (starting position of K) + (no of bits of the ciphertext)
    S = s.lfsr(K[::-1], F, 1023 - 10 + len(Ciphertext) * 5, 1)

    C = s.text_enc(Ciphertext)  # Cipher in bits

    # K must be at least the same size as C

    # Xor the keystream and the cipher and we get the plaintext
    # Use the part of the stream that starts on (period of lfsr) - (starting position of K)
    P = s.string_xor(S[1013:], C)
    P = s.text_dec(P)
    print(P)
    return P


def lfsr2(F1, F2, Pb2, Cb2, Ciphertext2):
    """Crack the two LFSRs."""
    K3b = s.text_enc(Pb2, Cb2)
    # Solve the matrix, get part of the Keystream 3 10-29 bits

    K2b = s.string_xor(K1[10:29], K3b)  # get 10-29 bits of K2
    print(K2b)
    # BERLEKAMP ATTACK ON K2b and F2 so we get S2
    S2 = [0, 1]

    K2 = s.lfsr(S2, F2, pow(2, len(F2)) - 1, 1)

    K3 = s.string_xor(K1, K2)  # get the full K3

    C = s.text_enc(Ciphertext2)

    P = s.string_xor(K3, C)

    P = s.text_dec(P)

    print(P)
    return P

F = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1]  # Feedback Function
Pb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  # Part of plaintext in bits
Cb = [1, 0, 0, 1, 0, 1, 0, 0, 0, 0]  # Part of ciphertext in bits
Ciphertext = "i!))aiszwykqnfcyc!?secnncvch"  # Cipher text

F2 = [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# Second Feedback Function
Pb2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
Cb2 = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
Ciphertext2 = "(fndappt)iy.a)jyyyzp..(cuw?dsu.bake()wuka-)bnndk"
print("LFSR 1:")
lfsr1(F, Pb, Cb, Ciphertext)
print("LFSR 2:")
#lfsr2(F, F2, Pb2, Cb2, Ciphertext2)
