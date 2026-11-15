import requests
import pandas as pd
import logging
from datetime import datetime, timezone
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"Base directory: {BASE_DIR}")

Path(f"{BASE_DIR}/data/raw").mkdir(parents=True, exist_ok=True)
Path(f"{BASE_DIR}/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=f"{BASE_DIR}/logs/collect.logs",
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

models = ["rtx3060", "rtx3070", "rtx3080", "rtx3090", "rx6700"]
records = []

for model in models:
    try:
        response = requests.get(f"http://0.0.0.0:5000/{model}")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        logging.info(f"Data collected for {model}: {data}")

        records.append({
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "model": model,
            "sales": data
        })

    except Exception as e:
        logging.error(f"Error occurred while collecting data for {model}: {e}")

if records:
    df = pd.DataFrame(records)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv_filename = f"{BASE_DIR}/data/raw/sales_{timestamp}.csv"
    print("Current working directory:", os.getcwd())
    print("CSV path:", csv_filename)
    print("Records count:", len(records))
    print("DataFrame shape:", df.shape)
    df.to_csv(csv_filename, index=False)
    logging.info(f"Data saved to {csv_filename}")
