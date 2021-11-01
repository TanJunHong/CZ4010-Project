import json

import pyrebase
import requests.exceptions

import pw_tool.helper.vault_helper

firebaseConfig = {
    "apiKey":            "AIzaSyBq943MX4OSMQoEG9WOEdATSlvxU5daxwQ",
    "authDomain":        "cz4010-project.firebaseapp.com",
    "databaseURL":       "https://cz4010-project-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId":         "cz4010-project",
    "storageBucket":     "cz4010-project.appspot.com",
    "messagingSenderId": "619927596323",
    "appId":             "1:619927596323:web:8058b593610fe37624b096",
    "measurementId":     "G-JSG28W1D2G"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()
auth_key = None
user = {}


def register(email, password):
    """Registers account on firebase with email and password
    It will also delete email and password variables after registering.
    """
    auth.create_user_with_email_and_password(email=email, password=password)
    del email
    del password


def login(email, password):
    """Login with email and password
    It will also delete email and password variables after login.
    """
    global user
    global auth_key
    user = auth.sign_in_with_email_and_password(email=email, password=password)
    pw_tool.helper.vault_helper.generate_vault_key(secret=email + password)
    auth_key = generate_auth_key(secret=pw_tool.helper.vault_helper.vault_key + password.encode(encoding="utf-8"))
    del email
    del password


def generate_auth_key(secret):
    """Generates authentication key with secret
    It will also save the authentication key.
    """
    return pw_tool.helper.vault_helper.context.hash(secret=secret, salt=pw_tool.helper.vault_helper.auth_iv)


def validate_old_password(old_password):
    """Validate old password
    It will generate authentication key and compare to see if the old password is correct.
    """
    return generate_auth_key(
        secret=pw_tool.helper.vault_helper.vault_key + old_password.encode(encoding="utf-8")) == auth_key


def change_password(password):
    global auth_key
    global user

    request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:update?key={0}".format(firebaseConfig["apiKey"])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": user["idToken"], "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(e, request_object.text)

    result = request_object.json()
    for key in auth.current_user.keys() & result.keys():
        # if key in result:
        auth.current_user[key] = result[key]
    user = auth.current_user

    pw_tool.helper.vault_helper.generate_vault_key(secret=user["email"] + password)
    pw_tool.helper.vault_helper.delete_vault(auth_key=auth_key)
    auth_key = generate_auth_key(secret=pw_tool.helper.vault_helper.vault_key + password.encode(encoding="utf-8"))
    pw_tool.helper.vault_helper.upload_vault()
    return request_object.json()
