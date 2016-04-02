#! /usr/bin/env python

"""Check avalanche effect / impact on small bit modification in AES."""

from Crypto.Cipher import AES
from Crypto import Random
import random


def checkAES_ECB(key, message, dec):
    """Check the avalanche effect on AES with ECB mode."""
    cText = AES_ECB_Encryption(key, message)

    bits2 = asciiToBin(message)  # convert message to bits
    bits2m = modifyBit(bits2)  # modify one bit
    message2 = binToAscii(bits2m)  # convert the bits back to a message

    cText2 = AES_ECB_Encryption(key, message2)

    cBits = asciiToBin(cText)
    cBits2 = asciiToBin(cText2)

    # count the number of different bits in the 2 encrypted messages
    counter = countDiffBits(cBits, cBits2)

    percent = (((1. * counter) / len(cBits)) * 100)

    # decrypt the bits
    if (dec):
        originalMessage = AES_ECB_Decryption(key, cText)
        originalMessage2 = AES_ECB_Decryption(key, cText2)
        print "Decrypted messages from ECB:"
        print originalMessage
        print originalMessage2

    return percent


def checkAES_CBC(key, message, dec):
    """Check the avalanche effect on AES with CBC mode."""
    IV = Random.new().read(16)  # length must be 16 bytes
    cText = AES_CBC_Encryption(key, message, IV)

    bits2 = asciiToBin(message)  # convert message to bits
    bits2m = modifyBit(bits2)  # modify one bit
    message2 = binToAscii(bits2m)  # convert the bits back to a message

    cText2 = AES_CBC_Encryption(key, message2, IV)

    cBits = asciiToBin(cText)
    cBits2 = asciiToBin(cText2)

    # count the number of different bits in the 2 encrypted messages
    counter = countDiffBits(cBits, cBits2)

    percent = (((1. * counter) / len(cBits)) * 100)

    # decrypt the bits
    if (dec):
        originalMessage = AES_CBC_Decryption(key, cText, IV)
        originalMessage2 = AES_CBC_Decryption(key, cText2, IV)
        print "Decrypted messages from CBC:"
        print originalMessage
        print originalMessage2

    return percent


def AES_ECB_Encryption(key, message):
    """Encrypt with AES in ECB mode."""
    obj = AES.new(key, AES.MODE_ECB, "ignore")  # IV is ignored in ECB mode
    return obj.encrypt(message)


def AES_CBC_Encryption(key, message, IV):
    """Encrypt with AES in CBC mode."""
    obj = AES.new(key, AES.MODE_CBC, IV)
    return obj.encrypt(message)


def AES_ECB_Decryption(key, cipher):
    """Decrypt with AES in ECB mode, IV is ignored in ECB mode."""
    obj = AES.new(key, AES.MODE_ECB, "ignore")
    return obj.decrypt(cipher)


def AES_CBC_Decryption(key, cipher, IV):
    """Decrypt with AES in CBC mode."""
    obj = AES.new(key, AES.MODE_CBC, IV)
    return obj.decrypt(cipher)


def asciiToBin(text):
    """Convert ascii text to bits."""
    textHex = text.encode('hex')  # Convert Ascii to hex
    textBin = bin(int(textHex, 16))[2:]  # Convert hex to binary, ignore "0b"
    return textBin


def binToAscii(bits):
    """Convert a series of bits to ascii text."""
    textHex = hex(int(bits, 2))[2:-1]  # Convert bits to hex
    text = textHex.decode("hex")  # Convert hex to ascii
    return text


def modifyBit(bits):
    """Change the value of a random bit in a series of bits."""
    i = random.randrange(1, len(bits) - 1)  # select a random bit
    bitsList = list(bits)
    bitsList[i] = '1' if bitsList[i] == '0' else '0'  # change its value
    bitsString = ''.join(bitsList)
    return bitsString


def countDiffBits(bits1, bits2):
    """Count the number of different bits between two binary strings."""
    counter = 0
    bLen1 = len(bits1)
    bLen2 = len(bits2)

    if (bLen1 > bLen2):  # If for some reason the length of bits is different
        counter = bLen1 - bLen2
    else:
        counter = bLen2 - bLen1

    for i in range(0, min(bLen1, bLen2)):
        if (bits1[i] != bits2[i]):
            counter += 1
    return counter


def printDiffs(text1, text2):
    """Print original and modified text."""
    print "Original: ", text1
    print "Modified: ", text2


msgs = []
num = 0
perCBC = 0
perECB = 0
key = "theimitationgame"  # length must be 16 bytes

f = open("messages.txt", "r")

for line in f:
    msgs.append(line[:16])
    num += 1

for i in msgs:
    perCBC += checkAES_CBC(key, i, False)
    perECB += checkAES_ECB(key, i, False)

print "CBC"
print "Messages: ", num, "Percentage: ", format((perCBC / num), '.2f'), "%"
print "ECB"
print "Messages: ", num, "Percentage: ", format((perECB / num), '.2f'), "%"
