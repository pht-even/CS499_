from findKey import *
from jsonSaveLoad import *
from hashPassword import *

# This program was developed for CS-499 at SNHU
# and is based on the ZooAuthenticator from IT-145.
# Users are greeted and asked if they are a new employee.
# New employees register via the input prompts.
# Once employees are registered, their information is stored
# to a JSON file. Returning employees check their login
# Credentials against existing values within the JSON file


# Variables to address states within the program
RUNNING = True
SAVED_RESPONSE = ""
SECTION = "RealName"

# User response is used multiple times and always cleared after use
userResponse = ""

# User variables
actualName = ""  # New users only
username = ""
userPass = ""
userJob = ""  # New users only
passOK = False
userOK = False

# Generating the dictionary from the saved JSON file
ZOO_EMPLOYEES = dict(loadEmployees())

print("Welcome to the Megalopolis Zoo Authentication System.\nType \"Q\' to quit.")

# Keep program running, exit when
while RUNNING:

    userResponse = input("New Employee? (Y/N)\n")

    # Branch depending on yes, no, quit, or invalid answer
    # Creating a new employee
    if userResponse.upper() == "Y" and SECTION != "Complete":
        print("New User\n")

        # These sections are for obtaining information via user input
        # Reponses must be valid and will ask for reentering if not

        # This section takes and stores the users actual name for later use
        while SECTION == "RealName":
            print("Enter the following information:\n")
            userResponse = input("Please enter your name.")
            SAVED_RESPONSE = userResponse

            print("You have entered:", SAVED_RESPONSE, "as your name. is this correct?")
            userResponse = input()

            if userResponse.upper() == "Y":
                # Store the User's name into the actualName variable for later use
                actualName = SAVED_RESPONSE
                # Flush the user response
                userResponse = ""
                # Switch to the next session
                SECTION = "Job"

            # If the user is not satisfied with their response, restart the section
            elif userResponse.upper() == "N":
                userResponse = ''

            # Exit out of the system
            elif userResponse.upper() == "Q":
                print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
                RUNNING = False

            else:
                print(userResponse, "is not a valid response.")

        # This section obtains the job assignment
        while SECTION == "Job":
            userResponse = input("Please enter your position.\n")
            SAVED_RESPONSE = userResponse

            print("You have entered:", SAVED_RESPONSE, "as your job. is this correct?")
            userResponse = input()

            if userResponse.upper() == "Y":
                # Store the User's name into the actualName variable for later use
                userJob = SAVED_RESPONSE
                userResponse = ""
                SECTION = "UserName"
            elif userResponse.upper() == "N":
                userResponse = ''
            elif userResponse.upper() == "Q":
                print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
                RUNNING = False
            else:
                print(userResponse, "is not a valid response.")

        # Selecting a username
        while SECTION == "UserName":
            userResponse = input("Please enter a username.\n")

            if findKey(ZOO_EMPLOYEES, userResponse):
                print("Sorry, that name is taken. Please choose another.")

            else:
                SAVED_RESPONSE = userResponse

                print("You have entered:", SAVED_RESPONSE, "as your username. Is this correct?")
                userResponse = input()

                if userResponse.upper() == "Y":
                    # Store the User's name into the actualName variable for later use
                    userName = SAVED_RESPONSE
                    userResponse = ""
                    SECTION = "Password"
                elif userResponse.upper() == "N":
                    userResponse = ''
                elif userResponse.upper() == "Q":
                    print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
                    RUNNING = False
                else:
                    print(userResponse, "is not a valid response.")

        while SECTION == "Password":
            userResponse = input("Please enter a password\n")
            SAVED_RESPONSE = userResponse
            userResponse = input("Please please renter your password\n")

            if userResponse == SAVED_RESPONSE:
                userPass = makeHash(userResponse)
                userResponse = ""
                SECTION = "Update"
            else:
                print("The passwords you entered do not match.\n")

        if SECTION == "Update":
            # Attempt to upload the data to the JSON file, throw error if exception occurs
            try:
                newEmployee = {userName: {"Name": actualName, "Position": userJob, "PassHash": userPass}}
                ZOO_EMPLOYEES.update(newEmployee)
                print(ZOO_EMPLOYEES)
                saveEmployees(ZOO_EMPLOYEES)
            except:
                print("An error occurred when writing to employees.json. Data was not saved.")

            RUNNING = False

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
                # Check the provided password hash against the stored hash
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
