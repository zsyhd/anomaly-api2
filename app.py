from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
from collections import Counter

app = FastAPI(title="Anomaly Pie Chart API")

CLASS_MAP = {
    0: ("normal", "#4caf50"),
    1: ("flow instability", "#2196f3"),
    2: ("pressure anomaly", "#f44336"),
    3: ("temperature anomaly", "#ff9800"),
    4: ("fluid level anomaly", "#9c27b0"),
    5: ("viscosity anomaly", "#3f51b5"),
    6: ("gas anomaly", "#00bcd4"),
    7: ("chemical composition", "#009688"),
    8: ("flow rate", "#795548"),
}

JSON_PATH = "MData.json"

@app.get("/")
def root():
    return {"message": "API is running. Visit /anomaly-stats"}

@app.get("/anomaly-stats")
def get_anomaly_stats():
    if not os.path.exists(JSON_PATH):
        return JSONResponse(status_code=500, content={"error": "MData.json not found."})

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    class_counts = Counter(item["class"] for item in data)

    items = []
    for cls, count in class_counts.items():
        name, color = CLASS_MAP.get(cls, ("unknown", "#000000"))
        items.append({
            "name": name,
            "value": count,
            "color": color
        })

    return {"items": items}
