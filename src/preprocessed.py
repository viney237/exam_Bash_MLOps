"""
-------------------------------------------------------------------------------
Ce script preprocessed.py récupère les données du dernier fichier CSV créé 
dans le dossier 'data/raw/'.

1. Il applique un prétraitement aux données
   
2. Les résultats du prétraitement sont enregistrés dans un nouveau fichier CSV 
   dans le dossier 'data/processed/', avec un nom au format 
   'sales_processed_YYYYMMDD_HHMM.csv'.
   
3. Toutes les étapes du prétraitement sont enregistrées dans le fichier 
   'logs/preprocessed.logs' afin de garantir un suivi détaillé du processus.

Les erreurs ou anomalies éventuelles sont également loguées pour assurer la traçabilité.
-------------------------------------------------------------------------------
"""

import os
import sys
import glob
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"Base directory: {BASE_DIR}")

Path(f"{BASE_DIR}/data/preprocessed").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=f"{BASE_DIR}/logs/preprocessed.logs",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

raw_files=glob.glob("data/raw/*")

if not raw_files:
   logging.error("Aucun fichier CSV trouvé dans le dossier 'data/raw/'.")
   sys.exit(1)

last_raw_file = max(raw_files, key=os.path.getmtime)

try:
    sales = pd.read_csv(last_raw_file)
    logging.info(f"Fichier chargé : {last_raw_file}")
except FileNotFoundError:
    logging.error(f"Fichier introuvable : {last_raw_file}")
    sys.exit(1)

logging.info("Prétraitement des données en cours...")

sales["timestamp"] = pd.to_datetime(sales["timestamp"])

sales["year"] = sales["timestamp"].dt.year
sales["month"] = sales["timestamp"].dt.month
sales["day_of_month"] = sales["timestamp"].dt.day
sales["day_of_week"] = sales["timestamp"].dt.day_of_week
sales["hour"] = sales["timestamp"].dt.hour
sales["minute"] = sales["timestamp"].dt.minute

logging.info("Encodage des modèles")

le = LabelEncoder()
sales["model"] = le.fit_transform(sales["model"])

sales = sales.drop(columns=["timestamp"])

missing = sales.isnull().sum().sum()
if missing > 0:
    logging.warning(f"{missing} valeurs manquantes détectées dans le dataset. Elles seront supprimées.")
    sales = sales.dropna()

parts = last_raw_file.split(".")[0].split("_")
date_str = parts[-2] + "_" + parts[-1]
sales.to_csv(f"data/preprocessed/sales_processed_{date_str}.csv", index=False)
logging.info("Prétraitement terminé et fichier enregistré dans data/preprocessed/")
