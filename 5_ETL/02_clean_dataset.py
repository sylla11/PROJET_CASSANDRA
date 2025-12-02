import pandas as pd
import os
from tqdm import tqdm

RAW_PATH = os.path.join('..','2_DATASET','raw','PS_20174392719_1491204439457_log.csv')
CLEAN_DIR = os.path.join('..','2_DATASET','clean')
os.makedirs(CLEAN_DIR, exist_ok=True)
OUT_CLEAN = os.path.join(CLEAN_DIR, 'paysim_clean.csv')

# Colonnes du dataset original
cols = [
    'step','type','amount','nameOrig','oldbalanceOrg','newbalanceOrig',
    'nameDest','oldbalanceDest','newbalanceDest','isFraud','isFlaggedFraud'
]

chunksize = 200000

first = True
for chunk in tqdm(pd.read_csv(RAW_PATH, usecols=cols, chunksize=chunksize)):
    
    # Renommage
    chunk = chunk.rename(columns={
        'nameOrig': 'customer_id',
        'nameDest': 'dest_id'
    })
    
    # Nettoyage des types
    chunk['step'] = chunk['step'].astype(int)
    chunk['amount'] = pd.to_numeric(chunk['amount'], errors='coerce').fillna(0.0)

    for c in ['oldbalanceOrg','newbalanceOrig','oldbalanceDest','newbalanceDest']:
        chunk[c] = pd.to_numeric(chunk[c], errors='coerce').fillna(0.0)

    chunk['isFraud'] = chunk['isFraud'].astype(int)
    chunk['isFlaggedFraud'] = chunk['isFlaggedFraud'].astype(int)

    chunk = chunk.dropna(subset=['customer_id','dest_id'])

    if first:
        chunk.to_csv(OUT_CLEAN, index=False, mode='w')
        first = False
    else:
        chunk.to_csv(OUT_CLEAN, index=False, mode='a', header=False)

print("Nettoyage terminé. Fichier propre :", OUT_CLEAN)