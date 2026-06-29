# scripts/generate_table.py
#
# ── Rôle ─────────────────────────────────────────────────────────────
# Interroge l'API GitLab pour récupérer les branches de chaque projet
# déclaré dans PROJETS, puis met à jour le bloc "data" dans le fichier
# docs/pipeline-status.mdx.
#
# Ce script est exécuté par le runner GitLab CI (étape "generate")
# avant le build Docusaurus. Il ne doit jamais être lancé manuellement
# en production — les variables CI ne seraient pas disponibles.
#
# ── Variables injectées automatiquement par GitLab CI ────────────────
# CI_API_V4_URL : URL complète de l'API GitLab interne
#                 ex: https://ton-gitlab-interne.fr/api/v4
# CI_JOB_TOKEN  : token temporaire valide uniquement le temps du job
#                 pas besoin de stocker de secret manuellement
#
# ── Fonctionnement ───────────────────────────────────────────────────
# 1. Lit PROJETS (déclaré ci-dessous)
# 2. Pour chaque projet, appelle l'API GitLab pour lister ses branches
# 3. Construit la structure data [ Domaine > Projet > Composants ]
# 4. Remplace le bloc "export const data" dans le .mdx
#    en utilisant les marqueurs // end-data comme repères
#
# ── Dépendances ──────────────────────────────────────────────────────
# pip install requests
# (installé automatiquement par le job CI avant l'exécution)

import os
import json
import requests


# ── Variables GitLab CI ───────────────────────────────────────────────
# Injectées automatiquement dans l'environnement du job CI
# Le script échoue explicitement si elles sont absentes (normal hors CI)
API_BASE  = os.environ["CI_API_V4_URL"]   # ex: https://gitlab.fr/api/v4
JOB_TOKEN = os.environ["CI_JOB_TOKEN"]    # token temporaire du job

# Header d'authentification à passer dans chaque requête API GitLab
HEADERS = {"JOB-TOKEN": JOB_TOKEN}

# URL de base GitLab sans /api/v4 — utilisée pour construire les URLs
# des badges SVG dans le fichier MDX
# ex: https://gitlab.fr/api/v4 → https://gitlab.fr
GITLAB_BASE = API_BASE.replace("/api/v4", "")


# ── Configuration des projets à surveiller ────────────────────────────
# ⚠️ C'EST ICI QUE TU DÉCLARES TES PROJETS — un dict par projet
#
# Clés :
#   domaine   : regroupement métier affiché en niveau 1 du tableau
#   projet    : nom affiché en niveau 2 (nom lisible, pas technique)
#   namespace : chemin GitLab du repo, visible dans l'URL du projet
#               ex: pour https://gitlab.fr/mon-groupe/mon-repo
#               →   namespace = "mon-groupe/mon-repo"
#
# Les branches de chaque repo deviendront automatiquement les
# "composants" (niveau 3) et colonnes de versions du tableau.
PROJETS = [
    {
        "domaine":   "DevOps",
        "projet":    "GitLab Core",
        "namespace": "groupe/gitlab-runner",   # ← à remplacer
    },
    {
        "domaine":   "DevOps",
        "projet":    "Infrastructure",
        "namespace": "groupe/gitaly",          # ← à remplacer
    },
    {
        "domaine":   "Auth",
        "projet":    "IAM",
        "namespace": "groupe/auth-service",    # ← à remplacer
    },
]

# Chemin du fichier MDX à mettre à jour (relatif à la racine du repo)
CHEMIN_MDX = "docs/pipeline-status.mdx"


def get_branches(namespace: str) -> list[str]:
    """
    Récupère la liste des branches d'un projet GitLab via l'API.

    Le namespace (ex: "groupe/repo") est encodé en URL car il est
    intégré dans le chemin de la requête API :
      /projects/groupe%2Frepo/repository/branches

    Retourne une liste vide en cas d'erreur pour ne pas bloquer
    le build si un seul projet est inaccessible.

    Args:
        namespace: chemin GitLab du projet (ex: "mon-groupe/mon-repo")

    Returns:
        Liste des noms de branches (ex: ["v1", "v2", "main"])
    """
    # Encodage du "/" en "%2F" pour l'URL de l'API
    namespace_encode = namespace.replace("/", "%2F")
    url = f"{API_BASE}/projects/{namespace_encode}/repository/branches"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # Lève une exception si le code HTTP est 4xx ou 5xx
        response.raise_for_status()
        branches = response.json()
        # Extrait uniquement le nom de chaque branche
        return [b["name"] for b in branches]

    except requests.exceptions.HTTPError as e:
        # Erreur HTTP (404 projet introuvable, 403 accès refusé, etc.)
        print(f"⚠️  Erreur HTTP pour '{namespace}' : {e}")
        return []

    except requests.exceptions.RequestException as e:
        # Erreur réseau (timeout, DNS, connexion refusée, etc.)
        print(f"⚠️  Erreur réseau pour '{namespace}' : {e}")
        return []


def build_data() -> list[dict]:
    """
    Construit la structure complète Domaine > Projet > Composants
    en interrogeant l'API GitLab pour chaque projet dans PROJETS.

    Les projets du même domaine sont automatiquement regroupés.
    L'ordre des domaines suit l'ordre de déclaration dans PROJETS.

    Returns:
        Liste de domaines, chacun contenant ses projets et composants
        ex: [
          {
            "domaine": "DevOps",
            "projets": [
              {
                "nom": "GitLab Core",
                "namespace": "groupe/gitlab-runner",
                "composants": ["v1", "v2", "main"]
              }
            ]
          }
        ]
    """
    # Dictionnaire intermédiaire pour regrouper les projets par domaine
    # Utilise un dict pour préserver l'ordre d'insertion (Python 3.7+)
    domaines: dict[str, dict] = {}

    for p in PROJETS:
        domaine   = p["domaine"]
        projet    = p["projet"]
        namespace = p["namespace"]

        # Initialise l'entrée du domaine si c'est la première fois qu'on le voit
        if domaine not in domaines:
            domaines[domaine] = {
                "domaine": domaine,
                "projets": []
            }

        # Récupère les branches du projet via l'API
        print(f"  → {namespace}")
        branches = get_branches(namespace)

        if branches:
            print(f"    branches trouvées : {branches}")
        else:
            print(f"    ⚠️  aucune branche récupérée — vérifier le namespace")

        # Ajoute le projet avec ses composants (branches) au domaine
        domaines[domaine]["projets"].append({
            "nom":        projet,
            "namespace":  namespace,
            "composants": branches,
        })

    return list(domaines.values())


def update_mdx(data: list[dict], chemin: str) -> None:
    """
    Remplace le bloc "export const data" dans le fichier MDX.

    Utilise deux marqueurs textuels pour localiser le bloc à remplacer :
      - Début : "export const data = ["
      - Fin   : "] // end-data"

    ⚠️ Ces marqueurs doivent être présents dans le fichier MDX.
    Ne pas les supprimer manuellement.

    Args:
        data   : structure de données à sérialiser en JSON
        chemin : chemin relatif du fichier MDX à mettre à jour
    """
    MARQUEUR_DEBUT = "export const data = ["
    MARQUEUR_FIN   = "] // end-data"

    # Lecture du contenu actuel du fichier
    with open(chemin, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Vérifie que les marqueurs sont bien présents
    if MARQUEUR_DEBUT not in contenu or MARQUEUR_FIN not in contenu:
        raise ValueError(
            f"Marqueurs introuvables dans {chemin}.\n"
            f"Vérifier que '{MARQUEUR_DEBUT}' et '{MARQUEUR_FIN}' sont présents."
        )

    # Localise les positions des marqueurs dans le fichier
    pos_debut = contenu.index(MARQUEUR_DEBUT)
    pos_fin   = contenu.index(MARQUEUR_FIN) + len(MARQUEUR_FIN)

    # Sérialise la structure data en JSON lisible (indenté)
    data_json = json.dumps(data, indent=2, ensure_ascii=False)

    # Reconstruit le bloc complet avec les nouvelles données
    nouveau_bloc = f"export const data = {data_json}\n{MARQUEUR_FIN}"

    # Remplace l'ancien bloc par le nouveau dans le contenu
    contenu = contenu[:pos_debut] + nouveau_bloc + contenu[pos_fin:]

    # Écrit le fichier mis à jour
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)


# ── Point d'entrée ────────────────────────────────────────────────────
if __name__ == "__main__":

    print("── Récupération des branches GitLab ─────────────────────────")
    data = build_data()

    print(f"\n── Mise à jour de {CHEMIN_MDX} ──────────────────────────────")
    update_mdx(data, CHEMIN_MDX)

    print(f"\n✅ {CHEMIN_MDX} mis à jour avec succès")
