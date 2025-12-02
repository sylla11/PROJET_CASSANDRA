import pandas as pd
import os
import uuid
from tqdm import tqdm

CLEAN_FP = os.path.join('..','2_DATASET','clean','paysim_clean.csv')
PROCESSED_DIR = os.path.join('..','2_DATASET','processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

chunksize = 200000
file_idx = 0
rows_per_file = 100000

buf = []
buf_count = 0

def flush_buffer(buf, idx):
    out_fp = os.path.join(PROCESSED_DIR, f'processed_{idx:04d}.csv')
    pd.DataFrame(buf).to_csv(out_fp, index=False)
    print('[OK] Fichier généré =>', out_fp)

for chunk in tqdm(pd.read_csv(CLEAN_FP, chunksize=chunksize)):
    
    # Ajout d'un UUID par transaction
    chunk['transaction_id'] = [str(uuid.uuid4()) for _ in range(len(chunk))]
    
    # Date bucket simple basé sur le step
    chunk['date_bucket'] = 'step_' + chunk['step'].astype(str)

    chunk = chunk[[
        'transaction_id','customer_id','dest_id','step','date_bucket',
        'type','amount','oldbalanceOrg','newbalanceOrig','oldbalanceDest',
        'newbalanceDest','isFraud','isFlaggedFraud'
    ]]

    for _, row in chunk.iterrows():
        buf.append(row.to_dict())
        buf_count += 1

        if buf_count >= rows_per_file:
            flush_buffer(buf, file_idx)
            file_idx += 1
            buf = []
            buf_count = 0

if buf_count > 0:
    flush_buffer(buf, file_idx)

print("TRANSFORMATION TERMINÉE.")