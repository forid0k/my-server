import csv
from datetime import datetime

def export_to_csv(signals, filename="signals.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Pair", "Direction", "Accuracy", "Price"])
        for sig in signals:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                sig["pair"], sig["direction"], sig["accuracy"], sig["price"]
            ])
    return filename