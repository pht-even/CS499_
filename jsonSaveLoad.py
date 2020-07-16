import json

# Functions to both load a JSON file and write to a JSON file


def loadEmployees():
    with open('employees.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        return data


def saveEmployees(dictionary):
    with open('employees.json', 'w') as fp:
        json.dump(dictionary, fp, indent=4)