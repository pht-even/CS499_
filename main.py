from findKey import *
from jsonSaveLoad import *
from hashPassword import *
from pprint import pprint

# This program was developed for CS-499 at SNHU
# and is based on the ZooAuthenticator from IT-145.
# Users are greeted and asked if they are a new employee.
# New employees register via the input prompts.
# Once employees are registered, their information is stored
# in the dictionary and added to the employees.json file.
# Registered users employees check their login credentials against
# existing values within the JSON file


# Variables to address states within the program
RUNNING = True
SAVED_RESPONSE = ""
SECTION = "RealName"
OPEN_PAGE = ""
ADMIN = False

# User response is used multiple times and always cleared after use
userResponse = ""

# User variables
actualName = ""  # New users only
username = ""
userPass = ""
userJob = ""  # New users only
passOK = False
userOK = False
verify = ""

# Generating the dictionary from the saved JSON file
ZOO_EMPLOYEES = dict(loadEmployees())

print("Welcome to the Megalopolis Zoo Authentication System.\n")

# Keep program running, exit when
while RUNNING:

    userResponse = input("Please select an option:\n1 - New Employee\n2 - Current Employee\n3- Quit\n")

    # Branch depending on yes, no, quit, or invalid answer
    # Creating a new employee
    if userResponse == "1" and SECTION != "Complete":
        userResponse = ""

        # These sections are for obtaining information via user input
        # Responses must be valid and will ask for reentering if not

        # This section takes and stores the users actual name for later use
        while SECTION == "RealName":
            print("Enter the following information:\n")
            userResponse = input("Please enter your name.")
            SAVED_RESPONSE = userResponse

            print("You have entered:", SAVED_RESPONSE, "as your name. Is this correct?")
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
            userResponse = input("Please enter your position. (Admin, Veterinarian, Zookeeper\n")
            SAVED_RESPONSE = userResponse

            print("You have entered:", SAVED_RESPONSE, "as your job. Is this correct?")
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
    elif userResponse == "2":

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
                    print("Accepted\n")
                    # save the response for later use
                    SAVED_RESPONSE = userResponse
                    userResponse = ""
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

                    # Loading the specific job page of the employee from a file
                    try:
                        if ZOO_EMPLOYEES[SAVED_RESPONSE]["Position"].upper() == "ADMIN":
                            ADMIN = True
                            OPEN_PAGE = open("helloAdmin.txt", "r")

                        elif ZOO_EMPLOYEES[SAVED_RESPONSE]["Position"].upper() == "VETERINARIAN":
                            OPEN_PAGE = open("helloVet.txt", "r")

                        elif ZOO_EMPLOYEES[SAVED_RESPONSE]["Position"].upper() == "ZOOKEEPER":
                            OPEN_PAGE = open("helloZookeeper.txt", "r")

                        else:
                            print("Your job page has not been implemented at this time.")

                    except:
                        print("An error occurred when loading the job file.")

                    RUNNING = False
                    break
                else:
                    print("That password is incorrect. Please try again or type \"Q\" to quit.")
            userResponse = ""

    # Exit from the service when "Q" is pressed
    elif userResponse.upper() == "Q":
        print("Thank you fo using the Megalopolis Zoo Authentication System.\nGoodbye.")
        RUNNING = False

    else:
        print(userResponse, "is not a valid response.")

# Show the user their page if it exists
if OPEN_PAGE != "":
    print(OPEN_PAGE.read())

# Initiate the admin program
# Uses a menu to update, remove and find employees
while ADMIN:

    # Start menu
    print("Please select an option from below:\n1- Find an Employee\n"
          "2- Update an Employee's Position\n3- Remove an Employee\n4- Log out")
    userResponse = input()
    SAVED_RESPONSE = userResponse

    # Search the dictionary for employee key and return the entry
    if userResponse == "1":
        print("Please enter the employee's username.")
        userResponse = input()
        try:
            pprint(ZOO_EMPLOYEES[userResponse])
        except:
            print("The username you entered could not be found\n")

    # Update an employee's position
    elif SAVED_RESPONSE == "2":

        print("Please enter the employee's username.")
        userResponse = input()
        if userResponse in ZOO_EMPLOYEES:
            SAVED_RESPONSE = userResponse

            print("Please enter a new position for", SAVED_RESPONSE)
            userResponse = input()

            print("Do you really want to change", SAVED_RESPONSE + "'s job from",
                ZOO_EMPLOYEES[SAVED_RESPONSE]["Position"], "to", userResponse + "?\n")\

            verify = input()

            # Updating both the dictionary and json file to reflect new position
            if verify.upper() == "Y":
                ZOO_EMPLOYEES[SAVED_RESPONSE]["Position"] = userResponse
                saveEmployees(ZOO_EMPLOYEES)
                print("Your changes have been saved.", SAVED_RESPONSE, "is now a", userResponse)
            else:
                verify = userResponse = SAVED_RESPONSE = ""

        else:
            print("The username you entered could not be found.\n")

    # Removing an employee from both dictionary and json file
    elif SAVED_RESPONSE == "3":
        print("Please enter the employee's username.")
        userResponse = input()

        # The changes being made are permanent.
        if userResponse in ZOO_EMPLOYEES:
            print("Do you really want to remove", userResponse, "from the employees list?\nThis cannot be undone.")
            verify = input()

            # Remove the entry from the dictionary, then update the json
            if verify.upper() == "Y":
                try:
                    del ZOO_EMPLOYEES[userResponse]
                    pprint(ZOO_EMPLOYEES)
                    saveEmployees(ZOO_EMPLOYEES)
                    print("The changes have been saved.")
                except:
                    print("An error occurred. Changes were not saved.")
        else:
            print("The username you entered could not be found.\n")

    # Logging out
    elif userResponse == "4":
        ADMIN = False
        print("Logged out")

    else:
        userResponse = SAVED_RESPONSE = ""

