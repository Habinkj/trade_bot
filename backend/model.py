# NOTE:
# Model is trained OFFLINE using historical data.
# For MVP, prediction is rule-based using SMA crossover.

def predict(latest_row):
    if latest_row["SMA_5"] > latest_row["SMA_20"]:
        return "UP", 0.62
    else:
        return "DOWN", 0.38
