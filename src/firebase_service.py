import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://console.firebase.google.com/u/0/project/human-pose-573eb/database/human-pose-573eb-default-rtdb/data/~2F'
})

def save_to_firebase(count, stage):
    ref = db.reference("/workouts")
    data = {
        "timestamp": datetime.now().isoformat(),
        "count": count,
        "stage": stage
    }
    ref.push(data)
    
