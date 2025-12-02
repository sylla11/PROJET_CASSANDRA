import os
import glob
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from tqdm import tqdm

PROCESSED_DIR = os.path.join('..','2_DATASET','processed')
KEYSPACE = 'paysim_ks'

def get_session():
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)
    return session

def load_file(session, fp, batch_size=100):

    df = pd.read_csv(fp)

    ps_customer = session.prepare("""
        INSERT INTO transactions_by_customer 
        (customer_id, step, transaction_id, type, amount, dest_id, oldbalanceOrg, newbalanceOrg, isFraud, isFlaggedFraud)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    ps_dest = session.prepare("""
        INSERT INTO transactions_by_dest 
        (dest_id, step, transaction_id, type, amount, customer_id, oldbalanceDest, newbalanceDest, isFraud)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)

    ps_date = session.prepare("""
        INSERT INTO transactions_by_datebucket 
        (date_bucket, step, transaction_id, customer_id, dest_id, type, amount, isFraud)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """)

    batch = BatchStatement()
    count = 0

    for _, r in df.iterrows():
        batch.add(ps_customer, (
            r['customer_id'], int(r['step']), r['transaction_id'], r['type'], float(r['amount']),
            r['dest_id'], float(r['oldbalanceOrg']), float(r['newbalanceOrig']),
            int(r['isFraud']), int(r['isFlaggedFraud'])
        ))

        batch.add(ps_dest, (
            r['dest_id'], int(r['step']), r['transaction_id'], r['type'], float(r['amount']),
            r['customer_id'], float(r['oldbalanceDest']), float(r['newbalanceDest']), int(r['isFraud'])
        ))

        batch.add(ps_date, (
            r['date_bucket'], int(r['step']), r['transaction_id'], r['customer_id'], r['dest_id'],
            r['type'], float(r['amount']), int(r['isFraud'])
        ))

        count += 1
        if count % batch_size == 0:
            session.execute(batch)
            batch = BatchStatement()

    if len(batch) > 0:
        session.execute(batch)

    print("✔ Chargé :", fp)

if __name__ == "__main__":
    session = get_session()

    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, 'processed_*.csv')))
    print("Fichiers détectés :", len(files))

    for f in files:
        print("Chargement :", f)
        load_file(session, f)

    print("🚀 INGESTION FINALE TERMINÉE.")
