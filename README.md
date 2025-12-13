# Générateur de QCM pour le cours Intro au TAL

## Lancer le QCM

Le script `questionnaire.py` permet de lancer le QCM :
```
uv run questionnaire.py
```
Le questionnaire continue jusqu’à ce que l’utilisateur appuie simplement sur Entrée sans réponse supplémentaire.
À la fin, le score obtenu est affiché automatiquement.

## Éditer des questions

On peut utiliser `editeur.py` pour créer ou modifier des questions.
```
uv run editeur.py
```

L’éditeur interactif demandera :
 * Le nom du fichier de sortie pour enregistrer les questions.
 * Les champs nécessaires pour chaque nouvelle question.
Lorsque l’un des champs est laissé vide, l’édition se termine et les questions sont sauvegardées.

## Format des données 

Les questions sont enregistrées au format JSON dans le dossier `data/`.

Chaque entrée doit contenir :
 * Le texte de la question
 * Les choix proposés
 * La réponse correcte

Voici une entrée type :
```
  {
    "question": "Contenu de la question",
    "theme": "Thème correspondant à la question",
    "answers": [
      {
        "answer_id": "1",
        "answer_text": "réponse a",
        "answer_is_correct": "False"
      },
      {
        "answer_id": "2",
        "answer_text": "réponse b",
        "answer_is_correct": "True"
      },
      {
        "answer_id": "3",
        "answer_text": "réponse c",
        "answer_is_correct": "True"
      }
    ]
  }
```
