# Générateur de QCM pour le cours Intro au TAL

## Lancer le QCM
```
uv run questionnaire.py
```

Le questionnaire se lance et continue tant que l'on appuye sur `Entrée`.
Au moment de quitter le questionnaire, le script calcule le score et l'affiche.

## Éditer des questions

Lancer le script `editeur.py` :
```
uv run editeur.py
```

L'éditeur se lance et demande un nom pour le fichier dans lequel seront enregistrées les questions;
il est possible de laisser ce champ vide et les questions seront éditées dans `data_perso.json`.

Ensuite, l'éditeur propose de remplir les champs nécessaires pour contruire une question.

L'éditeur continue jusqu'à ce qu'un champ soit vide, alors il enregistre les questions éditées dans le fichier renseigné plus haut.

Les questions éditées sont immédiatement disponibles dans le générateur de QCM.

```
