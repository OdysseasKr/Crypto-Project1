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
    # The number of bits is: (period of lfsr) - (starting position of K) +
    # (no of bits of the ciphertext)
    S = s.lfsr(K[::-1], F, 1023 - 10 + len(Ciphertext) * 5, 1)
    print(K)
    print(S[1013:])

    C = s.text_enc(Ciphertext)  # Cipher in bits

    # K must be at least the same size as C

    # Xor the keystream and the cipher and we get the plaintext
    # Use the part of the stream that starts on
    # (period of lfsr) - (starting position of K)
    P = s.string_xor(S[1013:], C)
    P = s.text_dec(P)
    print(P)
    return P


def lfsr2(F1, F2, Pb2, Cb2, Ciphertext2):
    """Crack the two LFSRs."""
    K3b = s.string_xor(Pb2, Cb2)

    C = s.text_enc(Ciphertext2)

    f = open("lfsr.txt", "w")
    f2 = open("K1.txt", "w")

    for i in range(1024):
        # Convert i to binary seed
        b = bin(i)
        S1 = [int(d) for d in b[2:]]
        while (len(S1)<10):
            S1 = [0] + S1

        # Calculate stream from lfsr-10 using S1
        F1copy = F1[:]
        K1 = s.lfsr(S1, F1copy, len(C), 1)
        f2.write(str(K1))
        f2.write("\n")

        K2b = s.string_xor(K1[10:30], K3b)  # get 10-29 bits of K2
        K2b = [int(d) for d in K2b[:16]]

        S2 = reverseLfsr(K2b[::-1], 9, 0)

        F2copy = F2[:]
        K2 = s.lfsr(S2, F2copy, len(C), 1)


        K3 = s.string_xor(K1, K2)
        P = s.string_xor(K3, C)
        P = s.text_dec(P)

        f.write(P)
        f.write("\n")

    return P

def reverseLfsr(state, n, print):
    for i in range(n):
        tmp = state[0] ^ state[8]
        tmp = tmp ^ state[7]
        tmp = tmp ^ state[3]
        tmp = tmp ^ state[2]
        state = state[1:]
        state.append(tmp)

        if print == 1:
            print("state: " + str(i))
            print(state)

    return state


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
Fcopy = F[:]
lfsr1(Fcopy, Pb, Cb, Ciphertext)
print("LFSR 2:")
Fcopy = F[:]
lfsr2(Fcopy, F2, Pb2, Cb2, Ciphertext2)
