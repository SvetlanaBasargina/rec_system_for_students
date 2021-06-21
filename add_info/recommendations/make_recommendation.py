from math import log
from operator import itemgetter
from .metrix import distCosine, distManhetten, distPirsonCoef, distCoefTanimoto, distEvclid


def makeRecommendationColl(userID, userRates, nBestUsers, nBestProducts, method, num):
    print(userID)
    if method == 'pir':
        matches = [(u, distPirsonCoef(userRates[userID], userRates[u], num)) for u in userRates if u != userID]
    elif method == 'evc':
        matches = [(u, distEvclid(userRates[userID], userRates[u], num)) for u in userRates if u != userID]
    elif method == 'man':
        matches = [(u, distManhetten(userRates[userID], userRates[u], num)) for u in userRates if u != userID]
    elif method == 'tan':
        matches = [(u, distCoefTanimoto(userRates[userID], userRates[u])) for u in userRates if u != userID]
    else:
        matches = [(u, distCosine(userRates[userID], userRates[u])) for u in userRates if u != userID]
    bestMatches = sorted(matches, reverse=True)[:nBestUsers]
    print("Most correlated with '%s' users:" % userID)
    for line in bestMatches:
        print("UserID: %6s  Coeff: %6.4f" % (line[0], line[1]))
    sim = dict()
    sim_all = sum([x[1] for x in bestMatches])
    bestMatches = dict([x for x in bestMatches if x[1] > 0.0])
    for relatedUser in bestMatches:
        for product in userRates[relatedUser]:
            if not product in userRates[userID]:
                if not product in sim:
                    sim[product] = 0.0
                sim[product] += userRates[relatedUser][product] * bestMatches[relatedUser]
    for product in sim:
        sim[product] /= sim_all
    bestProducts = sorted(sim.items(), key=itemgetter(1), reverse=True)[:nBestProducts * 2]
    print("Most correlated products:")
    for prodInfo in bestProducts:
        print("  ProductID: %6s  CorrelationCoeff: %6.4f" % (prodInfo[0], prodInfo[1]))
    return [(x[0], x[1]) for x in bestProducts]


def bag_of_words(items):
    corpus = []
    for i in items:
        l_A = i[1].lower().split()
        corpus.append(l_A)

    word_set = set()
    for i in corpus:
        word_set = word_set.union(set(i))

    word_dict = []
    for i in items:
        a = dict.fromkeys(word_set, 0)
        for word in i:
            a[word] += 1
        word_dict.append(a)

    return word_dict


def compute_tf(word_dict, l):
    tf = {}
    sum_nk = len(l)
    for word, count in word_dict.items():
        tf[word] = count / sum_nk
    return tf


def compute_idf(strings_list):
    n = len(strings_list)
    idf = dict.fromkeys(strings_list[0].keys(), 0)
    for l in strings_list:
        for word, count in l.items():
            if count > 0:
                idf[word] += 1

    for word, v in idf.items():
        idf[word] = log(n / float(v))
    return idf


def compute_tf_idf(tf, idf):
    tf_idf = dict.fromkeys(tf.keys(), 0)
    for word, v in tf.items():
        tf_idf[word] = v * idf[word]
    return tf_idf


def make_vectors(items):
    word_dict = bag_of_words(items)

    tfs = []
    for i in range(0, len(items), 1):
        tfs.append(compute_tf(word_dict[i], items[i][1]))

    idf = compute_idf(word_dict)

    tf_idf = []
    for i in range(0, len(items), 1):
        tf_idf.append([items[i][0], compute_tf_idf(tfs[i], idf)])

    return tf_idf


def makeRecommendationContent(item, items, nBestItems, method, num):
    matrix = make_vectors(items)
    if method == 'pir':
        sim_scores = [(u, distPirsonCoef(matrix[item], matrix, num)) for u in items if u != item]
    elif method == 'evc':
        sim_scores = [(u, distEvclid(matrix[item], matrix, num)) for u in items if u != item]
    elif method == 'man':
        sim_scores = [(u, distManhetten(matrix[item], matrix, num)) for u in items if u != item]
    elif method == 'tan':
        sim_scores = [(u, distCoefTanimoto(matrix[item], matrix)) for u in items if u != item]
    else:
        sim_scores = [(u, distCosine(matrix[item], matrix)) for u in items if u != item]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:nBestItems]
    indices = [i[0] for i in sim_scores]
    return items['title'].iloc[indices]


