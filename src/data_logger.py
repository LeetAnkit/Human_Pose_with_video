import csv
import os
from datetime import datetime

def log_to_csv(count, stage, file_path="workout_data.csv"):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Reps", "Stage"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count, stage])
