import hashlib

# Functions for hashing passwords


def makeHash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def checkPass(password, hash):
    if makeHash(password) == hash:
        return True

    return False

