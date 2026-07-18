from utils import longueur_cycle


def opt_ppp(cycle, D):
    """
    Procédure OptPPP : amélioration d’un cycle par décroisement des arêtes.
    Version strictement conforme à l’énoncé du cours.
    """
    n = len(cycle)
    amelioration = True

    while amelioration:
        amelioration = False

        for i in range(n - 2):
            for j in range(i + 2, n):

                # cas interdit : arêtes adjacentes du cycle
                if i == 0 and j == n - 1:
                    continue

                a = cycle[i]
                b = cycle[i + 1]
                c = cycle[j]
                d = cycle[(j + 1) % n]

                # coût avant décroisement
                cout_avant = D[a][b] + D[c][d]

                # coût après décroisement
                cout_apres = D[a][c] + D[b][d]

                if cout_apres < cout_avant:
                    # décroisement : inversion du sous-cycle
                    cycle[i + 1:j + 1] = reversed(cycle[i + 1:j + 1])
                    amelioration = True

    return cycle, longueur_cycle(cycle, D)
