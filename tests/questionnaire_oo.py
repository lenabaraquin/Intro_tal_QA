from __future__ import annotations
from typing import List, Set
from pathlib import Path

from dataclasses import dataclass
import json
import random


@dataclass
class Answer:
    id: int
    text: str
    is_correct: bool

    @staticmethod
    def _convert_str_to_bool(bool_str: str) -> bool:
        match bool_str:
            case "True":
                return True
            case "False":
                return False
            case _:
                raise ValueError("The input value is not a boolean string")

    @staticmethod
    def from_dict(answer_dict: dict) -> "Answer":
        id = answer_dict.get("answer_id", "-1")
        id = int(id)
        text = answer_dict.get("answer_text", "")
        text = str(text).strip()
        is_correct = answer_dict.get("answer_is_correct", "")
        is_correct = Answer._convert_str_to_bool(is_correct)
        return Answer(
            id=id,
            text=text,
            is_correct=is_correct,
        )


@dataclass
class Question:
    text: str
    theme: str
    answers: List[Answer]

    @staticmethod
    def from_dict(question_dict: dict) -> "Question":
        answers = [Answer.from_dict(a) for a in question_dict.get("answers", [])]
        return Question(
            text=str(question_dict.get("question", "")).strip(),
            theme=str(question_dict.get("theme", "")).strip(),
            answers=answers,
        )

    def correct_answer_ids(self) -> Set[int]:
        return {answer.id for answer in self.answers if answer.is_correct}

    def display(self) -> None:
        print("\n" + "#" * 80)
        if self.theme:
            print(f"Thème : {self.theme}")
        print(f"Question : {self.text}\n")
        for answer in self.answers:
            print(f"  [{answer.id}] {answer.text}")
        print()

    def parse_user_input_to_set(self, user_input: str) -> Set[str]:
        """
        Autorise :
          - '2'
          - '2 3'
          - '2,3'
          - '2, 3'
        """
        user_input = user_input.strip()
        if not user_input:
            return set()
        parts = user_input.replace(",", " ").split()
        return {p.strip() for p in parts if p.strip()}

    def is_user_correct(self, user_ids: Set[str]) -> bool:
        # Politique stricte : il faut donner exactement l'ensemble des bonnes réponses
        return user_ids == self.correct_answer_ids()

    def feedback(self, user_ids: Set[str]) -> str:
        correct = self.correct_answer_ids()
        if user_ids == correct:
            return "Correct."
        # Afficher la/les bonne(s) réponse(s)
        correct_texts = [answer.text for answer in self.answers if answer.id in correct]
        return f"Incorrect. Bonne(s) réponse(s) : {', '.join(correct_texts)}"


class JsonQuestionRepository:
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path

    def load(self) -> List[Question]:
        if not self.json_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {self.json_path}")

        with self.json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Le JSON doit contenir une liste de questions.")

        questions = [Question.from_dict(item) for item in data]
        # garde-fou minimal
        questions = [q for q in questions if q.text and q.answers]
        return questions


class Quiz:
    def __init__(self, questions: List[Question]) -> None:
        self.questions = questions
        self.correct_count = 0
        self.asked_count = 0

    def run(self) -> None:
        print("QCM — appuie sur Entrée (vide) pour arrêter.\n")

        for question in self.questions:
            question.display()
            user_input = input("Ta réponse (ex: 2 ou 2 3) : ").strip()
            if user_input == "":
                break

            user_ids = question.parse_user_input_to_set(user_input)
            self.asked_count += 1

            if question.is_user_correct(user_ids):
                self.correct_count += 1

            print(question.feedback(user_ids))

        self.print_summary()

    def print_summary(self) -> None:
        print("\n" + "#" * 80)
        print(f"Questions répondues : {self.asked_count}")
        print(f"Bonnes réponses     : {self.correct_count}")
        if self.asked_count > 0:
            pct = (self.correct_count / self.asked_count) * 100
            print(f"Score              : {pct:.1f}%")
        print("-" * 80)


def main() -> None:
    # Ajuste le chemin si besoin : data/questions.json, data/qcm.json, etc.
    # Ici, on prend un fichier par défaut si tu en as un (à adapter).
    json_path = Path("data") / "data.json"

    repo = JsonQuestionRepository(json_path)
    questions = repo.load()

    quiz = Quiz(questions)
    quiz.run()


if __name__ == "__main__":
    main()
