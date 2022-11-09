import json

def create_auth_file_template():
    auth_file = open("auth.json", encoding="utf-8", mode="w+")
    auth_file.write("{\n\t\"username\": \"<username>\",\n\t\"password\": \"<password>\"\n}")
    auth_file.close()

def get_spot_username() -> str:
    try:
        auth_file = open("auth.json", encoding="utf-8", mode="r")
    except FileNotFoundError as e:
        print("Auth file not found, creating one")
        create_auth_file_template()
        exit()

    try:
        return json.loads(auth_file.read())["username"]
    except KeyError as e:
        print("username field not found")
        exit()


def get_spot_password() -> str:
    try:
        auth_file = open("auth.json", encoding="utf-8", mode="r")
    except FileNotFoundError as e:
        print("Auth file not found, creating one")
        create_auth_file_template()
        exit()

    try:
        return json.loads(auth_file.read())["password"]
    except KeyError as e:
        print("password field not found")
        exit()

        