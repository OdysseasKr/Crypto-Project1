#! /usr/bin/env python

"""Cracking LFSR."""

import numpy as np
import lfsr_project as s


def lfsr1(F, Pb, Cb, Ciphertext):
    """Crack the first LFSR."""
    K = s.text_enc(Pb, Cb)
    # Solve the matrix equation, K is part of the Keystream 10-19 bits

    # BERLEKAMP MASSEY ATTACK on the n bits of K and the F so we get the seed!
    S = [0, 1]

    K = s.lfsr(S, F, pow(2, len(F)) - 1, 1)  # Whole Keystream in bits
    # The third argument is the length of the output keystream which can be
    # either the maximum length (2^n - 1 bits) or the length of plaintext
    # with which it will be xored

    C = s.text_enc(Ciphertext)  # Cipher in bits

    # K must be at least the same size as C

    # Xor the keystream and the cipher and we get the plaintext
    P = s.string_xor(K[:len(C)], C)
    P = s.text_dec(P)
    print P
    return P


def lfsr2(F1, S1, K1, F2, Pb2, Cb2, Ciphertext2):
    """Crack the two LFSRs."""
    K3b = s.text_enc(Pb2, Cb2)
    # Solve the matrix, get part of the Keystream 3 10-29 bits

    K2b = s.string_xor(K1[10:29], K3b)  # get 10-29 bits of K2
    print K2b
    # BERLEKAMP ATTACK ON K2b and F2 so we get S2
    S2 = [0, 1]

    K2 = s.lfsr(S2, F2, pow(2, len(F2)) - 1, 1)

    K3 = s.string_xor(K1, K2)  # get the full K3

    C = s.text_enc(Ciphertext2)

    P = s.string_xor(K3, C)

    P = s.text_dec(P)

    print P
    return P

F = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1]  # Feedback Function
Pb = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])  # Part of plaintext in bits
Cb = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0, 0])  # Part of ciphertext in bits
Ciphertext = "i!))aiszwykqnfcyc!?secnncvch"  # Cipher text

F2 = [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
# Second Feedback Function
Pb2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
Cb2 = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
Ciphertext2 = "(fndappt)iy.a)jyyyzp..(cuw?dsu.bake()wuka-)bnndk"

lfsr1(F, Pb, Cb, Ciphertext)
lfsr2(F, F2, Pb2, Cb2, Ciphertext2)
