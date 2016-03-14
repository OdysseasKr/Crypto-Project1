#!/usr/bin/env python2.7
import zipfile
# Open zip
zFile=zipfile.ZipFile("test_zip.zip")
# Read dictionary
with open("english.txt") as f:
    content = f.readlines()
# Try every word in the dictionary
for password in content:
    password = password.strip()
    try:
        zFile.extractall(pwd=password)
        print password
        exit()
    except Exception: # If the password was incorrect, move on
        pass
