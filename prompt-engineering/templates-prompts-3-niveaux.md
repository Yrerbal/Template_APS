# Templates — Ingénierie de prompt (3 niveaux)

Les trois niveaux ne sont pas une hiérarchie de qualité — ce sont des outils
différents pour des besoins différents. Un prompt léger mal placé donne un
résultat médiocre. Un prompt expert sur une question simple est du gaspillage.

---

## Règle de choix du niveau

```
Prompt léger   → question simple, résultat attendu clair, tolérance aux variations
Prompt médium  → tâche structurée, résultat reproductible attendu, contexte important
Prompt expert  → pipeline ou agent, résultat critique, format strict, réutilisation
```

---
---

# NIVEAU 1 — Prompt léger

**Quand l'utiliser :**
- Question ponctuelle, exploration rapide
- Résultat utilisé une seule fois, pas intégré dans un système
- L'humain relit et ajuste lui-même la réponse

**Ce qu'il contient :**
rôle bref + tâche + une contrainte si nécessaire

---

## Template léger — Structure

```
[Rôle optionnel, une phrase.]
[Tâche claire et directe.]
[Contrainte unique si besoin.]

[Contenu ou question.]
```

---

## Template léger — Usage général

```
Tu es [rôle]. [Tâche en une phrase]. [Contrainte si besoin].

[Contenu à traiter / question posée]
```

**Exemple rempli — résumé :**
```
Tu es un développeur Java senior. Résume ce que fait ce bout de code en 3 phrases
maximum, sans jargon inutile.

[code à analyser]
```

**Exemple rempli — question directe :**
```
Explique la différence entre rebase et merge en Git, en 5 lignes pour quelqu'un
qui connaît déjà les commits mais pas les stratégies de branche.
```

**Exemple rempli — génération rapide :**
```
Rédige un message de commit Git pour ce changement : correction d'un bug de
double débit dans le module paiement lors d'un retry réseau. Respecte le format
"fix(scope): description courte".
```

---
---

# NIVEAU 2 — Prompt médium

**Quand l'utiliser :**
- Tâche répétée plusieurs fois, résultat attendu stable
- Contexte important pour la qualité du résultat
- Résultat réutilisé tel quel ou légèrement retouché
- Usage personnel ou partagé en équipe (pas encore dans un pipeline)

**Ce qu'il contient :**
rôle détaillé + contexte + tâche décomposée + format de sortie + exemples

---

## Template médium — Structure

```
## Rôle
[Qui est l'assistant pour cette tâche — expertise, posture, ton attendu.]

## Contexte
[Informations nécessaires pour que la tâche soit bien comprise :
environnement, contraintes connues, historique si pertinent.]

## Tâche
[Ce qui est demandé, décomposé en étapes si la tâche est complexe.]

## Format de sortie attendu
[Structure, longueur, ton, format (texte, liste, tableau, code...).]

## Contraintes
[Ce qu'il ne faut pas faire, les limites à respecter.]

## Entrée
[Le contenu sur lequel travailler, ou la question posée.]
```

---

## Template médium — Usage général

```markdown
## Rôle
Tu es [expertise précise]. Tu t'adresses à [audience] et adoptes un ton [ton].

## Contexte
[2 à 5 phrases décrivant la situation, l'environnement ou ce qu'il faut savoir
avant de traiter la tâche.]

## Tâche
1. [Première action à effectuer]
2. [Deuxième action]
3. [Troisième action si besoin]

## Format de sortie
- Structure : [liste / tableau / texte structuré / code / JSON]
- Longueur : [contrainte de longueur]
- Langue : [langue attendue]

## Contraintes
- Ne pas [action interdite]
- Ne pas inventer [type d'information] si absent de l'entrée
- [Autre contrainte]

## Entrée
[Contenu à traiter]
```

---

## Template médium — Analyse de code (contexte CI/Java)

```markdown
## Rôle
Tu es un développeur Java senior spécialisé en architecture de systèmes legacy.
Tu t'adresses à un développeur en prise de poste sur un monolithe Java non
mavenisé. Ton ton est pédagogique et direct.

## Contexte
Le projet est un monolithe Java organisé en domaines métier, composants et
unités de build. Les dépendances sont déclarées dans des fichiers XML lus par
un script d'orchestration custom (UBP). Une migration Maven est en cours et
rencontre des problèmes de dépendances croisées.

## Tâche
1. Analyser le fichier XML fourni en entrée
2. Identifier les dépendances déclarées et leur version
3. Repérer les risques de conflit (même artefact, versions différentes)
4. Proposer la déclaration Maven équivalente (dependencyManagement)

## Format de sortie
- D'abord un tableau récapitulatif : artefact | version | risque détecté
- Ensuite le bloc XML Maven correspondant (POM)
- Enfin 2 à 3 observations courtes sur les points d'attention

## Contraintes
- Ne pas modifier la logique de dépendance, seulement la transposer
- Signaler explicitement si une information est manquante plutôt que supposer
- Ne pas proposer de refactoring de l'architecture, seulement la migration

## Entrée
[Coller ici le fichier XML de l'unité de build à analyser]
```

---

## Template médium — Rédaction de documentation technique

```markdown
## Rôle
Tu es un tech writer expérimenté. Tu rédiges de la documentation destinée à
des développeurs qui rejoignent une équipe. Ton ton est concis, direct, sans
jargon inutile ni formalisme excessif.

## Contexte
[Décrire le système ou le processus à documenter.]

## Tâche
Rédige une page de documentation couvrant :
1. Le rôle et le périmètre de [élément à documenter]
2. Les prérequis pour l'utiliser
3. Le fonctionnement pas à pas
4. Les erreurs fréquentes et leur résolution

## Format de sortie
- Markdown, headings H2 et H3 uniquement
- Pas de bullet points pour des phrases complètes (prose préférée)
- Chaque section : 5 à 10 lignes maximum
- Un exemple concret obligatoire dans la section "fonctionnement"

## Contraintes
- Ne pas écrire "ce document a pour but de..." ni de méta-commentaires
- Pas de ton corporate, pas de formules de politesse
- Signaler avec [À COMPLÉTER] les informations que je n'ai pas fournies

## Entrée
[Décrire ici l'élément à documenter, les informations disponibles]
```

---
---

# NIVEAU 3 — Prompt expert

**Quand l'utiliser :**
- Intégration dans un pipeline ou appel API
- Résultat critique, format strict, réutilisé automatiquement
- Comportement doit être identique à chaque exécution
- Plusieurs utilisateurs ou systèmes différents invoquent le même prompt

**Ce qu'il contient :**
system prompt séparé + instructions structurées + schéma de sortie + exemples
positifs ET négatifs + gestion des cas limites

---

## Template expert — Structure générale

```
[SYSTEM PROMPT]
[INSTRUCTIONS STRUCTURÉES EN BLOCS XML OU DÉLIMITEURS]
[SCHÉMA DE SORTIE STRICT]
[EXEMPLE POSITIF]
[EXEMPLE NÉGATIF]
[GESTION DES CAS LIMITES]
[MARQUEUR D'ENTRÉE UTILISATEUR]
```

---

## Template expert — Usage général (avec balises XML)

```xml
<system>
Tu es [rôle précis]. Tu opères dans [contexte du système].
Ta seule fonction est [périmètre strict]. Tu ne sors jamais de ce périmètre.
En cas de demande hors périmètre, tu réponds uniquement : "Hors périmètre."
</system>

<instructions>
  <etape id="1">[Première étape de traitement]</etape>
  <etape id="2">[Deuxième étape]</etape>
  <etape id="3">[Troisième étape]</etape>
  <regles>
    <regle>Ne jamais [action interdite]</regle>
    <regle>Toujours [action obligatoire]</regle>
    <regle>Si [condition] alors [comportement]</regle>
  </regles>
</instructions>

<format_sortie>
Répondre UNIQUEMENT en JSON valide, sans texte avant ni après.
Schema :
{
  "champ_1": "string",
  "champ_2": ["array", "de", "strings"],
  "champ_3": {
    "sous_champ": "valeur"
  },
  "confiance": "haute | moyenne | basse",
  "hors_perimetre": false
}
</format_sortie>

<exemple_positif>
Entrée : [exemple d'entrée valide]
Sortie : [JSON exact attendu]
</exemple_positif>

<exemple_negatif>
Entrée : [exemple d'entrée invalide ou hors périmètre]
Sortie incorrecte à NE PAS produire : [ce qu'il ne faut pas faire]
Sortie correcte : {"hors_perimetre": true}
</exemple_negatif>

<cas_limites>
- Si [situation ambiguë 1] : [comportement attendu]
- Si [situation ambiguë 2] : [comportement attendu]
- Si l'entrée est vide ou malformée : [comportement]
</cas_limites>

<entree>
{{INPUT}}
</entree>
```

---

## Template expert — Analyse XML de dépendances (contexte CI/UBP → Maven)

Exemple concret et réutilisable directement dans un pipeline d'analyse.

```xml
<system>
Tu es un expert en migration Java vers Maven. Tu analyses des fichiers XML issus
d'un système de build custom (UBP) et produis des déclarations Maven
correspondantes. Tu opères dans un pipeline automatisé : ta sortie est lue
par un script, pas par un humain. Le format de sortie doit être respecté
strictement et sans aucune déviation.
</system>

<instructions>
  <etape id="1">
    Lire le XML d'entrée et extraire toutes les dépendances déclarées :
    nom, version, scope si présent.
  </etape>
  <etape id="2">
    Identifier les conflits potentiels : même artefact déclaré en plusieurs
    versions, dépendances transitives implicites détectées.
  </etape>
  <etape id="3">
    Produire le bloc dependencyManagement Maven correspondant.
  </etape>
  <etape id="4">
    Évaluer le niveau de risque de la migration pour ce fichier.
  </etape>
  <regles>
    <regle>Ne jamais supposer une version absente — signaler avec "VERSION_MANQUANTE"</regle>
    <regle>Ne jamais modifier la logique de dépendance, seulement la transposer</regle>
    <regle>Si un artefact n'a pas de groupId Maven connu, utiliser "com.legacy"</regle>
    <regle>Le champ "risque" ne peut valoir que : faible | moyen | élevé | bloquant</regle>
  </regles>
</instructions>

<format_sortie>
JSON strict, sans texte avant ni après :
{
  "module": "string — nom du module analysé",
  "dependances": [
    {
      "artifactId": "string",
      "groupId": "string",
      "version": "string ou VERSION_MANQUANTE",
      "scope": "compile | test | provided | runtime",
      "conflit_detecte": true | false,
      "detail_conflit": "string ou null"
    }
  ],
  "bloc_pom": "string — XML du bloc dependencyManagement complet",
  "risque": "faible | moyen | élevé | bloquant",
  "observations": ["string", "string"]
}
</format_sortie>

<exemple_positif>
Entrée :
  <build-unit name="titi">
    <dependency name="toto" version="1.3"/>
    <dependency name="tata" version="2.0"/>
  </build-unit>

Sortie :
{
  "module": "titi",
  "dependances": [
    {
      "artifactId": "toto",
      "groupId": "com.legacy",
      "version": "1.3",
      "scope": "compile",
      "conflit_detecte": false,
      "detail_conflit": null
    },
    {
      "artifactId": "tata",
      "groupId": "com.legacy",
      "version": "2.0",
      "scope": "compile",
      "conflit_detecte": false,
      "detail_conflit": null
    }
  ],
  "bloc_pom": "<dependencyManagement>\n  <dependencies>\n    <dependency>\n      <groupId>com.legacy</groupId>\n      <artifactId>toto</artifactId>\n      <version>1.3</version>\n    </dependency>\n    <dependency>\n      <groupId>com.legacy</groupId>\n      <artifactId>tata</artifactId>\n      <version>2.0</version>\n    </dependency>\n  </dependencies>\n</dependencyManagement>",
  "risque": "faible",
  "observations": ["Aucun conflit détecté. GroupId supposé com.legacy faute d'information."]
}
</exemple_positif>

<exemple_negatif>
Entrée hors périmètre : "Explique-moi Maven en détail."
Sortie incorrecte à NE PAS produire : une explication textuelle de Maven.
Sortie correcte : {"erreur": "Entrée non valide — XML de build-unit attendu."}
</exemple_negatif>

<cas_limites>
- Version absente dans le XML → VERSION_MANQUANTE dans le champ version, risque = bloquant
- Même artefact déclaré deux fois avec versions différentes → conflit_detecte = true, détailler
- XML malformé ou vide → {"erreur": "XML invalide ou vide"}
- Dépendance circulaire suspectée → observation explicite + risque = bloquant
</cas_limites>

<entree>
{{XML_UNITE_DE_BUILD}}
</entree>
```

---

## Tableau comparatif des trois niveaux

| Critère | Léger | Médium | Expert |
|---|---|---|---|
| Longueur du prompt | 1 à 5 lignes | 15 à 40 lignes | 50 à 150+ lignes |
| Rôle défini | Optionnel | Oui | Oui, précis |
| Contexte | Implicite | Explicite | Exhaustif |
| Format de sortie | Libre | Guidé | Strict / schéma |
| Exemples | Non | 1 positif | Positif + négatif |
| Cas limites | Non | Partiellement | Tous couverts |
| Reproductibilité | Faible | Moyenne | Haute |
| Usage type | Exploration | Travail régulier | Pipeline / API |
| Coût de rédaction | 2 min | 15 min | 1 à 2 h |
| Maintenance | Nulle | Légère | Versionnée |

---

## Principes transversaux (tous niveaux)

**Toujours**
- Rôle avant tâche — le modèle adopte une posture avant d'agir
- Tâche à l'impératif présent — "Analyse", "Produis", "Identifie"
- Une contrainte "ne pas faire" pour chaque risque de dérive identifié

**Sur les exemples**
- Un exemple positif ancre le comportement attendu
- Un exemple négatif est plus puissant qu'une règle écrite — il montre ce
  qu'il ne faut pas faire plutôt que de l'interdire en texte

**Sur le format de sortie**
- Plus le résultat est consommé par une machine, plus le format doit être strict
- JSON sans texte autour pour les pipelines — les modèles ont tendance à ajouter
  du texte avant/après si on ne l'interdit pas explicitement

**Sur la dérive**
- Tout ce qui n'est pas interdit explicitement peut être tenté
- "Ne sors jamais du périmètre" ne suffit pas — définir ce périmètre positivement
  (ce que le modèle fait) ET négativement (ce qu'il ne fait pas)
