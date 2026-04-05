import json
import os
import random
import re

class QuestionRepository:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def load_questions(self) -> list:
        if not os.path.isdir(self.data_dir):
            raise Exception(
                "Le repertoire `data` n'a pas été trouvé.\nAssurez vous d'executer ce script dans le dossier où il se trouve."
            )

        questions_list = []
        for file_name in sorted(os.listdir(self.data_dir)):
            if not file_name.endswith(".json"):
                continue
            path = os.path.join(self.data_dir, file_name)
            with open(path, "r") as f:
                questions_list += json.load(f)
        return questions_list


class QuizGame:
    def __init__(self, questions_list: list):
        self.questions_list = questions_list
        self.score = [0, 0]
        self.selected_theme = None

    @staticmethod
    def convert_str_to_bool(bool_str: str) -> bool:
        match bool_str:
            case "True":
                return True
            case "False":
                return False
            case _:
                raise ValueError("The input value is not a boolean string")

    @staticmethod
    def pick_random_question(questions: list) -> dict[str, str | list]:
        return random.choice(questions)

    def get_available_themes(self) -> list[str]:
        themes = {question["theme"] for question in self.questions_list}
        return sorted(themes)

    def select_theme(self) -> str | None:
        themes = self.get_available_themes()
        if not themes:
            return None

        while True:
            print("\n" + "=" * 76)
            print("Selection du theme")
            print("-" * 76)
            print("  [0] Tous les themes")
            for index, theme in enumerate(themes, start=1):
                print(f"  [{index}] {theme}")

            choice = input("Choisissez un theme (numero) : ").strip()
            if not re.fullmatch(r"\d+", choice):
                print("Choix invalide. Entrez uniquement un numero.")
                continue

            selected_index = int(choice)
            if selected_index == 0:
                return None
            if 1 <= selected_index <= len(themes):
                return themes[selected_index - 1]

            print("Choix invalide. Le numero ne correspond a aucun theme.")

    def filter_questions_by_theme(self, theme: str | None) -> list:
        if theme is None:
            return self.questions_list
        return [question for question in self.questions_list if question["theme"] == theme]

    def generate_question_to_print(
        self,
        question_dict: dict[str, str | list[dict[str, str]]],
    ) -> str:
        to_print = "\n" + "=" * 76 + "\n"
        to_print += "QUESTION\n"
        to_print += "-" * 76 + "\n"
        to_print += f"Theme    : {question_dict['theme']}\n"
        to_print += f"Enonce   : {question_dict['question']}\n"
        to_print += "\nChoix disponibles :\n"
        for answer in question_dict["answers"]:
            to_print += f"  [{answer['answer_id']}] {answer['answer_text']}\n"
        to_print += "=" * 76
        return to_print

    def print_question(self, question_dict: dict):
        question_to_print = self.generate_question_to_print(question_dict)
        print(question_to_print)

    def get_correct_answer_ids_set(
        self,
        question_dict: dict[str, str | list[dict[str, str]]],
    ) -> set:
        correct_answer_ids_set = set()
        for answer in question_dict["answers"]:
            answer_is_correct = self.convert_str_to_bool(answer["answer_is_correct"])
            if answer_is_correct:
                correct_answer_ids_set.add(answer["answer_id"])
        return correct_answer_ids_set

    def get_user_answer_ids_set(self) -> set:
        while True:
            print("\nVotre reponse :")
            user_answer_ids = input(
                "Entrez les numeros des bonnes reponses (ex: 2 ou 1 4) : "
            ).strip()
            if re.fullmatch(r"\d(\s\d)*", user_answer_ids):
                return set(user_answer_ids.split())
            print("Format invalide. Entrez par exemple `3` ou `1 4`.")

    def compare_user_correct_answers(self, user_set: set, correct_set: set) -> bool:
        return user_set == correct_set

    def calculate_score(self, is_correct: bool):
        if is_correct:
            self.score[0] += 1
        self.score[1] += 1

    def generate_correction_to_print(
        self, user_answer_ids_set: set, correct_answer_ids_set: set
    ) -> str:
        to_print = "\n" + "-" * 76 + "\n"
        to_print += "RESULTAT\n"
        to_print += "-" * 76
        is_user_correct = self.compare_user_correct_answers(
            user_answer_ids_set, correct_answer_ids_set
        )
        if is_user_correct:
            to_print += "\nBonne reponse."
        else:
            sorted_correct_ids = sorted(correct_answer_ids_set, key=int)
            correct_ids_str = " ".join(sorted_correct_ids)
            to_print += "\nReponse incorrecte."
            to_print += f"\nBonnes reponses : {correct_ids_str}"
        to_print += "\n" + "-" * 76
        return to_print

    def print_correction(self, user_answer_ids_set: set, correct_answer_ids_set: set):
        correction = self.generate_correction_to_print(
            user_answer_ids_set, correct_answer_ids_set
        )
        print(correction)

    def ask_to_continue(self) -> bool:
        print("\n" + "=" * 76)
        choice = input(
            "Appuyez sur Entree pour une autre question, ou tapez q pour quitter : "
        ).strip()
        return choice == ""

    def print_score(self):
        print("\n" + "=" * 76)
        print("SESSION TERMINEE")
        print("-" * 76)
        print(f"Score final : {self.score[0]}/{self.score[1]}")
        print("=" * 76)

    def run(self):
        print("=" * 76)
        print("Quiz Intro TAL")
        print("Repondez avec un ou plusieurs numeros separes par des espaces.")
        print("=" * 76)
        self.selected_theme = self.select_theme()
        filtered_questions = self.filter_questions_by_theme(self.selected_theme)

        if self.selected_theme is None:
            print(f"\nMode : tous les themes ({len(filtered_questions)} questions disponibles)")
        else:
            print(
                f"\nMode : {self.selected_theme} ({len(filtered_questions)} questions disponibles)"
            )

        if not filtered_questions:
            print("Aucune question disponible pour ce theme.")
            return

        while True:
            want_to_continue = self.ask_to_continue()
            if not want_to_continue:
                self.print_score()
                break
            question_dict = self.pick_random_question(filtered_questions)
            self.print_question(question_dict)
            user_answer_ids_set = self.get_user_answer_ids_set()
            correct_answer_ids_set = self.get_correct_answer_ids_set(question_dict)
            is_correct = self.compare_user_correct_answers(
                user_answer_ids_set, correct_answer_ids_set
            )
            self.print_correction(user_answer_ids_set, correct_answer_ids_set)
            self.calculate_score(is_correct)

if __name__ == "__main__":
    questions_list = QuestionRepository().load_questions()
    game = QuizGame(questions_list)
    game.run()
