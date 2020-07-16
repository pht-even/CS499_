# This function finds a value in a dictionary, taking two arguments
# Returns a true or false, used in employee username lookup


def findKey(dictionary, key):
    if key in dictionary.keys():
        return True
    else:
        return False
