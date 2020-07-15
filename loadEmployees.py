import json


def loadEmployees():
    with open('employees.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
        return data
