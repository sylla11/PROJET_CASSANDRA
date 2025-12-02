from cassandra.cluster import Cluster

# -------------------------------------------------------------------
#   CONNEXION CASSANDRA SIMPLE
# -------------------------------------------------------------------
def get_session():
    """
    Renvoie une session Cassandra connectée à KEYSPACE paysim_ks.
    Connexion au cluster 'transaction' sur port 9042.
    """
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect("paysim_ks")
    return session
