import numpy as np
import math
import matplotlib.pyplot as plt


def generer_points(n, seed=None):
    if seed is not None:
        np.random.seed(seed)
    return [(np.random.rand(), np.random.rand()) for _ in range(n)]


def lire_points(fichier):
    """
    Lecture robuste de points depuis un fichier texte.
    Format attendu : (x, y) par ligne.
    """
    points = []
    with open(fichier, "r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            ligne = ligne.strip("()")
            x_str, y_str = ligne.split(",")
            x = float(x_str.strip())
            y = float(y_str.strip())
            points.append((x, y))
    return points


def matrice_distances(points):
    n = len(points)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(n):
            xj, yj = points[j]
            D[i][j] = math.hypot(xi - xj, yi - yj)
    return D


def longueur_cycle(cycle, D):
    total = 0.0
    n = len(cycle)
    for i in range(n):
        total += D[cycle[i]][cycle[(i + 1) % n]]
    return total


def afficher_cycle(points, cycle, titre=""):
    x = [points[i][0] for i in cycle] + [points[cycle[0]][0]]
    y = [points[i][1] for i in cycle] + [points[cycle[0]][1]]

    plt.figure()
    plt.plot(x, y, marker="o")
    plt.title(titre)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
