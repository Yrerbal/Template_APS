# pipeline-status — Tableau de statut CI/CD pour Docusaurus

Tableau hiérarchique à 3 niveaux (Domaine → Projet → Composant) affichant
les badges de pipeline GitLab en temps réel, généré automatiquement via CI.

---

## Structure des fichiers

```
.
├── .gitlab-ci.yml                 ← orchestration CI (3 étapes dans l'ordre)
├── scripts/
│   └── generate_table.py          ← interroge l'API GitLab, met à jour le MDX
├── docs/
│   └── pipeline-status.mdx        ← page Docusaurus (mise à jour par le script)
└── src/
    └── css/
        └── pipeline.module.css    ← styles externalisés du tableau (livrable 2)
```

---

## Livrables progressifs

### Livrable 1 — Semi-statique (disponible immédiatement)

Le fichier `docs/pipeline-status.mdx` est utilisable tel quel.  
Les badges SVG se chargent dynamiquement depuis GitLab à chaque affichage.  
La structure Domaine/Projet/Composant est déclarée manuellement dans `data`.

**À modifier avant d'utiliser :**
1. `GITLAB` dans `pipeline-status.mdx` → ton URL GitLab interne
2. Le bloc `data` → tes vrais projets et branches

### Livrable 2 — Styles externalisés

Copier `src/css/pipeline.module.css` dans ton projet Docusaurus et
mettre à jour l'import dans `pipeline-status.mdx` :

```js
import styles from '@site/src/css/pipeline.module.css'
```

Remplacer ensuite les styles inline par les classes CSS du module.

### Livrable 3 — Automatisation complète via CI

1. Déclarer tes projets dans `PROJETS` dans `scripts/generate_table.py`
2. Ajouter le `.gitlab-ci.yml` à la racine du repo Docusaurus
3. Pousser sur `main` — le pipeline se charge du reste

---

## Configuration minimale (livrable 3)

Dans `scripts/generate_table.py`, modifier uniquement le bloc `PROJETS` :

```python
PROJETS = [
    {
        "domaine":   "Mon Domaine",
        "projet":    "Mon Projet",
        "namespace": "mon-groupe/mon-repo",  # chemin visible dans l'URL GitLab
    },
]
```

Le namespace est visible dans l'URL du repo :  
`https://ton-gitlab.fr/mon-groupe/mon-repo` → `mon-groupe/mon-repo`

---

## Prérequis

- Docusaurus v2 ou v3 avec support MDX
- Runner GitLab avec accès Docker
- Accès à l'API GitLab interne depuis le runner (réseau)
