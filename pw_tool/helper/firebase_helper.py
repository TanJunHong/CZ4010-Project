import pyrebase

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
