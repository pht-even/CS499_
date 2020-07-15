import json


def saveEmployees(dictionary):
    with open('employees.json', 'w') as fp:
        json.dump(dictionary, fp, indent=4)