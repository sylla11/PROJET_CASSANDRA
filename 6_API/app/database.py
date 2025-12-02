from cassandra.cluster import Cluster

def get_session():
    cluster = Cluster(["127.0.0.1"], port=9042)  # DEV CLUSTER
    session = cluster.connect("paysim_ks")
    return session
