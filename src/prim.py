import heapq
from utils import longueur_cycle


def prim_mst(D, start=0):
    """
    Algorithme de Prim (version efficace).
    Construit une arborescence couvrante de poids minimum.
    Retourne le tableau des prédécesseurs parent.
    """
    n = len(D)
    cle = [float("inf")] * n
    parent = [-1] * n
    dans_arbre = [False] * n

    cle[start] = 0
    heap = [(0, start)]

    while heap:
        _, u = heapq.heappop(heap)
        if dans_arbre[u]:
            continue

        dans_arbre[u] = True

        for v in range(n):
            if not dans_arbre[v] and D[u][v] < cle[v]:
                cle[v] = D[u][v]
                parent[v] = u
                heapq.heappush(heap, (cle[v], v))

    return parent


def parcours_prefixe(parent, racine=0):
    """
    Parcours préfixe d'une arborescence définie par le tableau parent.
    """
    n = len(parent)
    enfants = [[] for _ in range(n)]

    for v in range(n):
        if parent[v] != -1:
            enfants[parent[v]].append(v)

    ordre = []

    def dfs(u):
        ordre.append(u)
        for v in enfants[u]:
            dfs(v)

    dfs(racine)
    return ordre


def opt_prim(D, start=0):
    """
    Approximation du PVC par arbre couvrant minimum (Prim)
    et parcours préfixe de l'arborescence.
    """
    parent = prim_mst(D, start)
    cycle = parcours_prefixe(parent, start)
    longueur = longueur_cycle(cycle, D)
    return cycle, longueur
