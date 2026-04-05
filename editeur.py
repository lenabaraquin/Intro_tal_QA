import json
import os


class JsonQuestionStore:
    def save(self, questions_list: list, path: str):
        if os.path.isfile(path):
            with open(path, "r") as f:
                existing_json_questions_list = json.load(f)
        else:
            existing_json_questions_list = []
        data_to_write = existing_json_questions_list + questions_list
        json_str = json.dumps(data_to_write, indent=2, ensure_ascii=False)
        with open(path, "w") as f:
            f.write(json_str)


class QuestionnaireEditor:
    THEMES_MAPPING = {
        "Histoire": "Histoire du TAL",
        "1": "Histoire du TAL",
        "Traitements linguistiques": "Traitements linguistiques",
        "2": "Traitements linguistiques",
        "Pretraitements linguistiques": "Prétraitements linguistiques",
        "3": "Prétraitements linguistiques",
        "Pretraitements informatiques": "Prétraitements informatiques",
        "4": "Prétraitements informatiques",
        "Methodes et approches": "Méthodes et approches",
        "5": "Méthodes et approches",
        "Evaluation": "Évaluation",
        "6": "Évaluation",
    }

    def determine_path(self) -> str:
        data_dir = "data"
        if not os.path.isdir(data_dir):
            raise Exception(
                "Le repertoire `data` n'a pas été trouvé.\nAssurez vous d'executer ce script dans le dossier où il se trouve."
            )
        print("\n" + "=" * 76)
        print("Editeur de questions")
        print("=" * 76)
        while True:
            file_name = (
                input("Nom du fichier de sortie (data_perso.json par defaut) : ").strip()
                or "data_perso.json"
            )
            if file_name == "data.json":
                print(
                    "Veuillez trouver un autre nom, celui-ci est reserve au fichier principal."
                )
                continue
            return os.path.join(data_dir, file_name)

    def get_theme(self) -> str | None:
        while True:
            print("\n" + "-" * 76)
            print("Choix du theme")
            print("-" * 76)
            print("""Themes disponibles :
  1: Histoire
  2: Traitements linguistiques
  3: Pretraitements linguistiques
  4: Pretraitements informatiques
  5: Methodes et approches
  6: Evaluation""")
            theme = input(
                "Entrez un theme (numero ou nom), ou vide pour terminer : "
            ).strip()
            if theme == "":
                return ""
            mapped_theme = self.THEMES_MAPPING.get(theme)
            if mapped_theme is not None:
                return mapped_theme
            print("Veuillez choisir un theme parmi la liste proposee.")

    def get_question(self) -> str:
        print("\n" + "-" * 76)
        print("Nouvelle question")
        print("-" * 76)
        question = input("Texte de la question (vide pour terminer) :\n")
        return question

    def get_answer_id(self, answer_id: int) -> str:
        return str(answer_id)

    def get_answer_text(self) -> str:
        answer_text = input(
            "  Reponse (vide pour terminer) :\n  "
        )
        return answer_text

    def get_answer_is_correct(self) -> str:
        while True:
            answer_is_correct = input("  Est-ce une bonne reponse ? [y/n] : ").strip()
            match answer_is_correct:
                case "y":
                    return "True"
                case "n":
                    return "False"
                case _:
                    print("Veuillez entrer 'y' ou 'n'.")

    def get_answer(self, answer_id: int) -> dict | None:
        print(f"\n  Reponse #{answer_id}")
        answer_text = self.get_answer_text()
        if answer_text == "":
            return None
        answer = {
            "answer_id": self.get_answer_id(answer_id),
            "answer_text": answer_text,
            "answer_is_correct": self.get_answer_is_correct(),
        }
        return answer

    def get_answers(self) -> list:
        answer_list = []
        answer_id = 1
        while True:
            answer = self.get_answer(answer_id)
            answer_id += 1
            if not answer:
                break
            answer_list.append(answer)
        return answer_list

    def get_question_dict(self) -> dict | None:
        theme = self.get_theme()
        if theme == "":
            return None
        question = self.get_question()
        if question == "":
            return None
        answers = self.get_answers()
        question_dict = {"question": question, "theme": theme, "answers": answers}
        return question_dict

    def get_questions_list(self) -> list:
        questions_list = []
        while True:
            question_dict = self.get_question_dict()
            if not question_dict:
                break
            questions_list.append(question_dict)
        return questions_list


if __name__ == "__main__":
    editor = QuestionnaireEditor()
    store = JsonQuestionStore()
    path = editor.determine_path()
    questions_list = editor.get_questions_list()
    store.save(questions_list, path)
