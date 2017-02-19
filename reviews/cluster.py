from sklearn.cluster import DBSCAN

def cluster_phrases(phrases, eps=0.5, min_samples=5):
    dbscanner = DBSCAN(metric='cosine', algorithm='brute', eps=eps, min_samples=min_samples)
    labels = dbscanner.fit_predict([phrase.vector for phrase in phrases])
    clusters = {}
    for i in range(len(phrases)):
        label = labels[i] or -1
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(phrases[i])
    return clusters
