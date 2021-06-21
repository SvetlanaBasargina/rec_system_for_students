import math
from scipy.spatial import distance


def get_vect(x, y, num):
    x_new, y_new = [], []
    for i in range(num):
        if str(i + 1) in list(x):
            x_new.append(x[str(i + 1)])
        else:
            x_new.append(0)
    for i in range(num):
        if str(i + 1) in list(y):
            y_new.append(y[str(i + 1)])
        else:
            y_new.append(0)
    return x_new, y_new


def distPirsonCoef(x, y, num):
    x, y = get_vect(x, y, num)
    n = len(x)
    miu_x = sum(x) / n
    miu_y = sum(y) / n
    stdev_x = (sum([(i - miu_x) ** 2 for i in x]) / n) ** 0.5
    stdev_y = (sum([(i - miu_y) ** 2 for i in y]) / n) ** 0.5
    covariance = sum([(x[i] - miu_x) * (y[i] - miu_y) for i in range(n)])
    pearson_coefficient = covariance / (n * stdev_x * stdev_y)
    return round(pearson_coefficient, 3)


def distEvclid(x, y, num):
    x, y = get_vect(x, y, num)
    dist = math.sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(x, y)]))
    return dist


def distCosine(vecA, vecB):
    def dotProduct(vecA, vecB):
        d = 0.0
        for dim in vecA:
            if dim in vecB:
                d += vecA[dim] * vecB[dim]
        return d

    return dotProduct(vecA, vecB) / math.sqrt(dotProduct(vecA, vecA)) / math.sqrt(dotProduct(vecB, vecB))


def distCoefTanimoto(x, y):
    n_x = len(list(x))
    n_y = len(list(y))
    n = 0
    for i in range(36):
        if (str(i + 1) in list(x)) and (str(i + 1) in list(y)):
            n += 1

    return n / (n_x + n_y - n)


def distManhetten(x, y, num):
    x, y = get_vect(x, y, num)
    dst = distance.cityblock(x, y)
    return dst
