CREATE KEYSPACE IF NOT EXISTS paysim_ks
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE paysim_ks;

CREATE TABLE IF NOT EXISTS transactions_by_customer (
    customer_id text,
    step int,
    transaction_id uuid,
    type text,
    amount double,
    dest_id text,
    oldbalanceOrg double,
    newbalanceOrg double,
    isFraud int,
    isFlaggedFraud int,
    PRIMARY KEY ((customer_id), step, transaction_id)
) WITH CLUSTERING ORDER BY (step ASC, transaction_id ASC);

CREATE TABLE IF NOT EXISTS transactions_by_dest (
    dest_id text,
    step int,
    transaction_id uuid,
    type text,
    amount double,
    customer_id text,
    oldbalanceDest double,
    newbalanceDest double,
    isFraud int,
    PRIMARY KEY ((dest_id), step, transaction_id)
) WITH CLUSTERING ORDER BY (step ASC, transaction_id ASC);

CREATE TABLE IF NOT EXISTS transactions_by_datebucket (
    date_bucket text,
    step int,
    transaction_id uuid,
    customer_id text,
    dest_id text,
    type text,
    amount double,
    isFraud int,
    PRIMARY KEY ((date_bucket), step, transaction_id)
) WITH CLUSTERING ORDER BY (step ASC, transaction_id ASC);
