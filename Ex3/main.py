#!/usr/bin/env python3

abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# text: Ciphertext in a string
# Returns possible length of the key
def keyLength(text):
    k = 2
    found = False
    while (found == False) and (k < len(text)/2):
        print("Checking keysize = " + str(k))
        col = makeColumns(text, k)
        for i in range(k):
            if abs(IC(col[i]) - 0.067) < 0.001:
                print("Found key size: " + str(k))
                found = True
                break
        k = k + 1

    if (found == False):
        return (0,0)
    else:
        return (k - 1,col)

# text: String to be broken into columns
# num: Number of columns to create
# Return the columns created
def makeColumns(text, num):
    cols = ['' for x in range(num)]
    for i in range(len(text)):
        cols[i%num] = cols[i%num] + text[i]
    return cols

# Computes the index of coincidence
# text: the string to compute IC for
def IC(text):
    total = 0
    k = len(text)
    for l in abc:
        ml = text.count(l)
        total = total + (ml*(ml-1))/(k*(k-1))
    return total

# Tries to find the key of the given text using frequencies
# c: ciphertext encrypted with caesars algorithm
def frequencyAttack(c):
    abc2 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # This is the letter frequency list.
    # The whole list is 'etaoinshrdlcumwfgypbvkjxqz' arranged from most to least common
    abcOnFreq = 'e'.upper() # Here we use only a portion of the list
    freq = []

    # Count the occurencis of each letter in the given string
    for l in abc2:
        freq.append(c.count(l))

    # Sort the list from the most to the least occurencies
    freq, abc2 = zip(*sorted(zip(freq,abc),reverse=True))

    # Find the possible keys that have been used to create that substitution
    for i in range(len(abcOnFreq)):
        num = abs(abc.index(abcOnFreq[i]) - abc.index(abc2[i]))
        print(str(num) + " KEY: " + abc[num])



with open("vigenere.txt") as f:
    cipher = f.read().strip()

# Find the length of the key
(keylength,cols) = keyLength(cipher)
if keylength == 0:
    print("Failed")
    exit()

print("")
print("Trying to find the key")

# Print the key for each column
for i in range(len(cols)):
    print("Column " + str(i))
    frequencyAttack(cols[i])
