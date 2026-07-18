import os
import numpy as np
import matplotlib.pyplot as plt

from utils import generer_points, matrice_distances, afficher_cycle, lire_points
from ppp import ppp
from opt_ppp import opt_ppp
from prim import opt_prim
from hds import hds


# ==================================================
# CHEMINS DES FICHIERS
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

FICHIER_POINTS = os.path.join(DATA_DIR, "points.txt")
FICHIER_POINTS_HDS = os.path.join(DATA_DIR, "points_hds.txt")


# ==================================================
# PARAMÈTRES GÉNÉRAUX
# ==================================================
N = 20              # nombre de points (mode aléatoire)
NB_ESSAIS = 100     # nombre d'expériences statistiques
SEED = None         # reproductibilité


# ==================================================
# MODES
# ==================================================
MODE_EXECUTION = "hds"   # "approx" ou "hds"
MODE_ENTREE = "fichier"     # "aleatoire" ou "fichier"


# ==================================================
# MODE APPROXIMATION (PPP / OptPPP / OptPrim)
# ==================================================
if MODE_EXECUTION == "approx":

    if MODE_ENTREE == "fichier":
        NB_ESSAIS = 1

    lp = []    # longueurs PPP
    lop = []   # longueurs OptPPP
    lpr = []   # longueurs OptPrim

    for k in range(NB_ESSAIS):

        # Génération / lecture des points
        if MODE_ENTREE == "aleatoire":
            points = generer_points(N, seed=SEED)
        else:
            points = lire_points(FICHIER_POINTS)

        D = matrice_distances(points)

        # ----------------------------
        # PPP
        # ----------------------------
        cycle_ppp, l_ppp = ppp(points, D)
        lp.append(l_ppp)

        # ----------------------------
        # OptPPP
        # ----------------------------
        cycle_opt, l_opt = opt_ppp(cycle_ppp[:], D)
        lop.append(l_opt)

        # ----------------------------
        # OptPrim
        # ----------------------------
        cycle_prim, l_prim = opt_prim(D)
        lpr.append(l_prim)

        print(f"Essai {k + 1}/{NB_ESSAIS} terminé")

    # ----------------------------
    # MOYENNES
    # ----------------------------
    m_ppp = np.mean(lp)
    m_opt = np.mean(lop)
    m_prim = np.mean(lpr)

    print("\n===== RÉSULTATS MOYENS =====")
    print(f"PPP     : {m_ppp:.4f}")
    print(f"OptPPP  : {m_opt:.4f}")
    print(f"OptPrim : {m_prim:.4f}")

    # ----------------------------
    # GAINS
    # ----------------------------
    gain_opt_ppp = 100 * (m_ppp - m_opt) / m_ppp
    gain_prim_opt = 100 * (m_opt - m_prim) / m_opt

    print("\n===== GAINS (%) =====")
    print(f"Gain OptPPP / PPP     : {gain_opt_ppp:.2f} %")
    print(f"Gain OptPrim / OptPPP : {gain_prim_opt:.2f} %")

    # ----------------------------
    # GRAPHIQUE
    # ----------------------------
    labels = ["PPP", "OptPPP", "OptPrim"]
    moyennes = [m_ppp, m_opt, m_prim]

    plt.figure()
    plt.bar(labels, moyennes)
    plt.ylabel("Longueur moyenne")
    plt.title("Comparaison des algorithmes d’approximation")
    plt.show()

    # ----------------------------
    # VISUALISATION D’UN CAS
    # ----------------------------
    if MODE_ENTREE == "aleatoire":
        points = generer_points(N, seed=42)
    else:
        points = lire_points(FICHIER_POINTS)

    D = matrice_distances(points)

    cycle_ppp, _ = ppp(points, D)
    cycle_opt, _ = opt_ppp(cycle_ppp[:], D)
    cycle_prim, _ = opt_prim(D)

    afficher_cycle(points, cycle_ppp, "PPP")
    afficher_cycle(points, cycle_opt, "OptPPP")
    afficher_cycle(points, cycle_prim, "OptPrim")


# ==================================================
# MODE HDS (SOLUTION EXACTE)
# ==================================================
elif MODE_EXECUTION == "hds":

    points = lire_points(FICHIER_POINTS_HDS)
    D = matrice_distances(points)

    cycle_hds, l_hds = hds(D)

    print("\n===== SOLUTION EXACTE HDS =====")
    print(f"Longueur optimale : {l_hds:.4f}")

    afficher_cycle(points, cycle_hds, "HDS – Solution optimale")


else:
    raise ValueError("MODE_EXECUTION doit être 'approx' ou 'hds'")
