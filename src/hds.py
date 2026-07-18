from math import inf


def borne_demi_somme(D, chemin, cout):
    """
    Heuristique de la demi-somme (version pédagogique améliorée).
    Calcule une borne inférieure pour un chemin partiel.
    """
    n = len(D)
    non_visites = [i for i in range(n) if i not in chemin]

    borne = cout

    # Contribution des sommets non visités
    for v in non_visites:
        distances = []
        for u in range(n):
            if u != v:
                distances.append(D[v][u])
        distances.sort()
        borne += distances[0] + distances[1]

    return borne / 2


def hds(D, start=0, n_max=10):
    """
    Algorithme exact du PVC par Branch & Bound (HDS).
    Utilise l'heuristique de la demi-somme et une exploration best-first.

    ATTENTION :
    - Algorithme exponentiel
    - Limité à n <= n_max
    - Utilisé comme solution exacte de référence
    """
    n = len(D)

    if n > n_max:
        raise ValueError(f"HDS limité à n <= {n_max}")

    meilleur_cout = inf
    meilleur_cycle = None

    def explorer(chemin, cout):
        nonlocal meilleur_cout, meilleur_cycle

        # Calcul de la borne
        borne = borne_demi_somme(D, chemin, cout)
        if borne >= meilleur_cout:
            return

        # Solution complète
        if len(chemin) == n:
            cout_total = cout + D[chemin[-1]][start]
            if cout_total < meilleur_cout:
                meilleur_cout = cout_total
                meilleur_cycle = chemin[:]
            return

        dernier = chemin[-1]

        # Sélection intelligente des successeurs (best-first)
        candidats = []
        for v in range(n):
            if v not in chemin:
                cout_v = cout + D[dernier][v]
                borne_v = borne_demi_somme(D, chemin + [v], cout_v)
                candidats.append((borne_v, v, cout_v))

        # Exploration dans l'ordre croissant de la borne
        for _, v, cout_v in sorted(candidats):
            explorer(chemin + [v], cout_v)

    explorer([start], 0)
    return meilleur_cycle, meilleur_cout
