from sklearn.cluster import DBSCAN

def cluster_phrases(phrases):
    dbscanner = DBSCAN()
    lables = dbscanner.fit_predict([phrase.vector for phrase in phrases])
    clusters = {}
    for i in range(len(phrases)):
        if i not in lables:
            clusters[lables[i]] = []
        clusters[lables[i]].append(phrases[i])
    return clusters
