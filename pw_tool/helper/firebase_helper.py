import pyrebase

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


def register(email, password):
    auth.create_user_with_email_and_password(email=email, password=password)


def login(email, password):
    auth.sign_in_with_email_and_password(email=email, password=password)
    pw_tool.helper.vault_helper.generate_vault_key(secret=email + password)
    generate_auth_key(secret=pw_tool.helper.vault_helper.vault_key + password.encode(encoding="utf-8"))


def generate_auth_key(secret):
    global auth_key
    auth_key = pw_tool.helper.vault_helper.context.hash(secret=secret, salt=pw_tool.helper.vault_helper.vault_iv)
