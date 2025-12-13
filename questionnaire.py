import json
import random
import re

# TODO
# Charger tous les json du répertoire data et les concaténer
# Ajouter les bonnes réponses à côté des ids en cas de réponses incorrectes


def convert_str_to_bool(bool_str: str) -> bool:
    match bool_str:
        case "True":
            return True
        case "False":
            return False
        case _:
            raise ValueError("The input value is not a boolean string")


def generate_question_dict(data: list) -> dict[str, str | list]:
    question_dict = random.choice(data)
    return question_dict


def generate_question_to_print(question_dict: dict[str, str | list[dict]]) -> str:
    to_print = "####################################################################################################\n"
    to_print += f"Thème : {question_dict['theme']}\n"
    to_print += "####################################################################################################\n"
    to_print += f"Qestion : {question_dict['question']}\n"
    for answer in question_dict["answers"]:
        to_print += f"\t{answer['answer_id']}\t{answer['answer_text']}\n"
    return to_print


def get_correct_answer_ids_set(question_dict: dict[str, str | list[dict]]) -> set:
    correct_answer_ids_set = set()
    for answer in question_dict["answers"]:
        answer_is_correct = convert_str_to_bool(answer["answer_is_correct"])
        if answer_is_correct:
            correct_answer_ids_set.add(answer["answer_id"])
    return correct_answer_ids_set


def get_user_answer_ids_set() -> set:
    user_answer_ids = input(
        "Entrez les réponses que vous estimez correctes (numéros séparés par des espaces) : "
    )
    if not re.match(r"\d(\s\d)*$", user_answer_ids):
        print(
            "L'entrée attendue doit avoir la forme `3` ou `1 4`, veuillez recommencer."
        )
        user_answer_ids = input(
            "Entrez les réponses que vous estimez correctes (numéros séparés par des espaces) : "
        )
    if not re.match(r"(\d\s?)+$", user_answer_ids):
        raise ValueError("Incorrect user input")
    user_answer_ids_list = user_answer_ids.split()
    user_answer_ids_set = set(user_answer_ids_list)
    return user_answer_ids_set


def compare_user_correct_answers(user_set: set, correct_set: set) -> bool:
    return (
        user_set == correct_set
    )  # Vaut True seulement si toutes les réponses données par l'utilisateur sont correctes


def calculate_score(is_correct: bool, score: list) -> list:
    """score[number_of_correct_answers, total_asked_questions]"""
    if is_correct:
        score[0] += 1
    score[1] += 1
    return score


with open("./data/data_perso.json", "r") as f:
    data = json.load(f)

score = [0, 0]
while True:
    print(
        "####################################################################################################"
    )
    choice = input("Laissez vide pour continuer, entrez q pour sortir.")
    if choice != "":
        print(
            "####################################################################################################"
        )
        print(
            "####################################################################################################"
        )
        print(f"\tVotre score sur cette session est de : {score[0]}/{score[1]}")
        break
    print(
        "####################################################################################################"
    )
    question_dict = random.choice(data)
    to_print = generate_question_to_print(question_dict)
    print(to_print)
    correct_answer_ids_set = get_correct_answer_ids_set(question_dict)
    user_answer_ids_set = get_user_answer_ids_set()
    is_user_correct = compare_user_correct_answers(
        user_answer_ids_set, correct_answer_ids_set
    )
    if is_user_correct:
        print("Correct")
    else:
        print("Non correct\nLes réponses correctes sont :")
        for correct_id in correct_answer_ids_set:
            print(f"\t{correct_id}")

    score = calculate_score(is_user_correct, score)
