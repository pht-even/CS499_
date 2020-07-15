from saveEmployees import *
from loadEmployees import *
from hashPassword import *

RUNNING = True
SAVED_RESPONSE = ""
VALID = False

userName = ""
userPass = ""
userResponse = ""
passOK = False
userOK = False

# Generating the dictionary from the saved JSON file
ZOO_EMPLOYEES = dict(loadEmployees())

print(ZOO_EMPLOYEES)
print(ZOO_EMPLOYEES['Employee1234'])

print("Welcome to the Megalopolis Zoo Authentication System.\nType \"Q\' to quit.")

# Keep program running, exit when
while RUNNING:

    userResponse = input("New Employee? (Y/N)\n")

    # Branch depending on yes, no, quit, or invalid answer
    # Creating a new employee
    if userResponse.upper() == "Y":
        print("New User\n")

    # Login as current employee
    elif userResponse.upper() == "N":
        print("Active User")

        # get the username
        while RUNNING and not userOK:
            userResponse = input("Please enter your username.\n")
            # Quitting
            if userResponse.upper() == "Q":
                print("Goodbye.")
                RUNNING = False
                break
            # Look for the entered username
            else:
                if userResponse in ZOO_EMPLOYEES:
                    print("Accepted")
                    # save the response for later use
                    SAVED_RESPONSE = userResponse
                    userOK = True
                else:
                    print("Employee not found")

        # Check the password for a match under the user's information
        while RUNNING and not passOK:
            userResponse = input("Please enter your password\n")
            # Quitting
            if userResponse.upper() == "Q":
                print("Goodbye.")
                RUNNING = False
                break
            else:
                if checkPass(userResponse, ZOO_EMPLOYEES[SAVED_RESPONSE]["PassHash"]):
                    passOK = True
                    print("Password accepted.\nWelcome,", SAVED_RESPONSE)
                    RUNNING = False
                    break
                else:
                    print("That password is incorrect, please try again or type \"q\"")

    # Exit from the service when "Q" is pressed
    elif userResponse.upper() == "Q":
        print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
        RUNNING = False

    else:
        print(userResponse, "is not a valid response.")