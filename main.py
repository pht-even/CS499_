import hashlib
import binascii
import json
import os
from saveEmployees import *
from loadEmployees import *

RETRIES = 3
userName = ""
userPass = ""
VALID = False
passOK = False
userOK = False
userResponse = ""
SAVED_RESPONSE = ""

# Generating the dictionary from the saved JSON file
ZOO_EMPLOYEES = dict(loadEmployees())

print(ZOO_EMPLOYEES)
print(ZOO_EMPLOYEES['Employee1234'])

print("Welcome to the Megalopolis Zoo Authentication System.\nType \"Q\' to quit.")

# Keep program running, exit when
while RETRIES > 0:

    userResponse = input("New Employee? (Y/N)\n")

    # Branch depending on yes, no, quit, or invalid answer
    # Creating a new employee
    if userResponse.upper() == "Y":
        print("New User\n")

    # Login as current employee
    elif userResponse.upper() == "N":
        print("Active User")

        while not userOK:

            userResponse = input("Please enter your username.\n")
            SAVED_RESPONSE = userResponse
            if userResponse.upper() == "Q":
                print("Goodbye.")
                RETRIES = 0
                break

            else:
                if userResponse in ZOO_EMPLOYEES:
                    print("Welcome")
                    userOK = True
                else:
                    print("Employee not found")

        while not passOK:

            userResponse = input("Please enter your password")
            if userResponse.upper() == "Q":
                print("Goodbye.")
                break

            else:
                if userResponse in ZOO_EMPLOYEES[SAVED_RESPONSE]["PassHash"]:
                    passOK = True
                    print("Welcome,", SAVED_RESPONSE)
                    break
                else:
                    print("That password is incorrect, please try again or type \"q\"")

    # Exit from the service when "Q" is pressed
    elif userResponse.upper() == "Q":
        print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
        break

    # Invalid responses have three chances to enter a valid response
    else:
        if RETRIES > 1:
            print("Please enter a valid response or type \"Q\" to exit.")
            RETRIES -= 1

        else:
            RETRIES -= 1
            print("goodbye")
            break

        print("Retries left: ", RETRIES)
