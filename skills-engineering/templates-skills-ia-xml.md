# Templates — Rédaction de skills IA

Un "skill" au sens IA désigne une capacité définie et encadrée qu'on confie à
un agent ou un assistant : périmètre clair, entrées attendues, sorties produites,
contraintes respectées. Un skill mal défini donne un agent imprévisible. Un skill
bien défini est réutilisable, testable et transmissible à quelqu'un d'autre.

---

## Structure canonique d'un skill

```
NOM DU SKILL
Rôle          : ce que le skill fait (une phrase, verbe d'action)
Déclencheur   : quand l'invoquer (condition, mot-clé, contexte)
Entrées       : ce que le skill reçoit (type, format, optionnel/obligatoire)
Sorties       : ce que le skill produit (type, format, niveau de détail)
Contraintes   : ce qu'il ne fait PAS, les limites explicites
Exemple       : cas concret d'entrée → sortie attendue
```

---

## Template 1 — Skill simple (capacité unique)

À utiliser pour une tâche atomique, bien délimitée, sans branchement.

```markdown
## Skill : [NOM EN MAJUSCULES]

**Rôle**
[Verbe à l'infinitif] + [objet] + [dans quel but].
Ex : "Résumer un texte technique en langage accessible pour un public non-expert."

**Déclencheur**
Ce skill s'active quand :
- [condition 1]
- [condition 2]
Ne pas activer si : [contre-indication explicite]

**Entrées**
<entrees>
  <param nom="[param_1]" type="texte" obligatoire="oui">[description courte]</param>
  <param nom="[param_2]" type="liste" obligatoire="non" defaut="[valeur]">[description courte]</param>
</entrees>

**Sorties**
Format : [texte libre / JSON / liste / tableau / code]
Longueur : [indicative — ex : 3 à 5 phrases, moins de 200 mots]
Ton : [neutre / technique / pédagogique / formel]

**Contraintes**
- Ne pas [action interdite]
- Ne pas supposer [information manquante] — demander si nécessaire
- Rester dans le périmètre de [domaine] — ne pas dériver vers [hors-scope]

**Exemple**
Entrée :
  [exemple d'entrée concret]

Sortie attendue :
  [exemple de sortie concret — pas un placeholder, un vrai exemple]
```

---

## Template 2 — Skill composite (plusieurs étapes internes)

À utiliser quand le skill enchaîne des opérations distinctes avant de produire
le résultat final. L'utilisateur ne voit que l'entrée et la sortie — les étapes
sont internes.

```markdown
## Skill : [NOM EN MAJUSCULES]

**Rôle**
[Description en une phrase.]

**Déclencheur**
Ce skill s'active quand : [condition]
Priorité par rapport aux autres skills : [plus haute / standard / fallback]

**Entrées**
<entrees>
  <param nom="[param]" type="[type]" obligatoire="oui|non">[desc]</param>
</entrees>

**Étapes internes** *(non visibles de l'utilisateur)*
1. [Étape 1 — ex : extraire les entités clés de l'entrée]
2. [Étape 2 — ex : valider que les contraintes sont respectées]
3. [Étape 3 — ex : structurer la réponse selon le format de sortie]
4. [Étape 4 — ex : vérifier la cohérence avant d'envoyer]

**Sorties**
Format : [format exact]
Structure :
  - [champ 1] : [description]
  - [champ 2] : [description]

**Contraintes**
- [contrainte 1]
- [contrainte 2]
- En cas d'ambiguïté sur [situation précise] : [comportement attendu]

**Comportement en cas d'erreur**
Si [condition d'échec] → [comportement : demander, ignorer, signaler, fallback]

**Exemple**
Entrée : [exemple]
Sortie : [exemple]
```

---

## Template 3 — Skill avec mémoire / contexte persistant

À utiliser quand le skill doit tenir compte d'informations accumulées au fil
d'une session ou de plusieurs interactions.

```markdown
## Skill : [NOM EN MAJUSCULES]

**Rôle**
[Description en une phrase.]

**Contexte persistant attendu**
Ce skill utilise les informations suivantes accumulées en session :
- [info_1] : [comment elle est utilisée]
- [info_2] : [comment elle est utilisée]

Si le contexte est absent ou incomplet : [comportement — demander / supposer / signaler]

**Entrées**
<entrees>
  <param nom="[param]" type="[type]" obligatoire="oui|non">[desc]</param>
</entrees>

**Logique de mise à jour du contexte**
Après chaque exécution, mettre à jour :
- [élément de contexte 1] si [condition]
- [élément de contexte 2] si [condition]

**Sorties**
[Format et structure]

**Contraintes**
- Ne pas réinitialiser le contexte sans confirmation explicite
- [autres contraintes]

**Exemple de session**
Tour 1 — Entrée : [exemple]  →  Sortie : [exemple]  →  Contexte mémorisé : [x]
Tour 2 — Entrée : [exemple]  →  Sortie utilisant [x] : [exemple]
```

---

## Template 4 — Skill d'orchestration (fait appel à d'autres skills)

À utiliser pour un skill "chef d'orchestre" qui délègue à des skills spécialisés.

```markdown
## Skill : [NOM EN MAJUSCULES — ORCHESTRATEUR]

**Rôle**
Analyser la demande entrante et déléguer au skill approprié parmi :
- [Skill A] — pour les cas de type [description]
- [Skill B] — pour les cas de type [description]
- [Skill C] — pour les cas de type [description]

**Déclencheur**
Point d'entrée par défaut de [agent / assistant / pipeline].

**Logique de routage**
```
SI [condition 1] → invoquer Skill A avec [paramètres]
SI [condition 2] → invoquer Skill B avec [paramètres]
SI [condition 3] ET [condition 4] → invoquer Skill A puis Skill C
SINON → [comportement par défaut : demander / répondre directement / signaler]
```

**Gestion des cas ambigus**
Si la demande correspond à plusieurs skills → [priorité ou question de clarification]
Si aucun skill ne correspond → [comportement]

**Contraintes**
- Ne pas traiter directement ce que les skills spécialisés peuvent traiter
- [autres contraintes]
```

---

## Anti-patterns à éviter

<anti-patterns>
  <cas probleme="skill trop large" impact="imprévisible, non testable" correction="découper en skills atomiques"/>
  <cas probleme="contraintes absentes" impact="agent déborde du périmètre" correction="définir explicitement ce qu'il ne fait PAS"/>
  <cas probleme="exemple absent" impact="comportement ambigu" correction="inclure au moins un exemple complet"/>
  <cas probleme="déclencheur vague" impact="activation incohérente" correction="condition précise et exclusive"/>
  <cas probleme="sortie non spécifiée" impact="format variable" correction="format, longueur, ton explicites"/>
</anti-patterns>

---

## Checklist avant de déclarer un skill prêt

- [ ] Le rôle tient en une phrase avec un verbe d'action
- [ ] Le déclencheur est précis et non ambigu
- [ ] Toutes les entrées sont typées et leur caractère obligatoire est précisé
- [ ] La sortie est spécifiée en format, longueur et ton
- [ ] Au moins une contrainte "ne pas faire" est explicite
- [ ] Au moins un exemple complet (entrée → sortie) est fourni
- [ ] Le comportement en cas d'erreur ou d'ambiguïté est défini
