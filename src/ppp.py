from utils import longueur_cycle


def ppp(points, D, start=0):
    """
    Algorithme du Point le Plus Proche (PPP)
    Version strictement conforme à l’énoncé du cours.
    """
    n = len(points)

    cycle = [start]
    non_visites = set(range(n))
    non_visites.remove(start)

    while non_visites:
        meilleur_point = None
        meilleur_sommet = None
        meilleure_distance = float("inf")

        # Chercher le point Qi le plus proche du cycle
        for p in non_visites:
            for v in cycle:
                if D[p][v] < meilleure_distance:
                    meilleure_distance = D[p][v]
                    meilleur_point = p
                    meilleur_sommet = v

        # Insertion entre Qj et son successeur dans le cycle
        idx = cycle.index(meilleur_sommet)
        cycle.insert(idx + 1, meilleur_point)

        non_visites.remove(meilleur_point)

    longueur = longueur_cycle(cycle, D)
    return cycle, longueur
