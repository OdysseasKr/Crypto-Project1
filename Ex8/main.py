#!/usr/bin/env python3

#Its 676767
import crypt
with open("password.txt") as f:
    cipher = f.read().strip()[5:-19]

print(cipher)

for i in range(0,1000000):
	password = "%06d" % (i)
	if i % 1000 == 0:
		print(i)
	txt = crypt.crypt(password,"$6$kHnyu3Ni$")
	if txt == cipher:
		print("Found!" + password)
		break
