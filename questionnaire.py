import json
import random
import re
import os

# TODO
# Ajouter les bonnes réponses à côté des ids en cas de réponses incorrectes
# Créer un filtre par thème


def load_questions_list_from_json_files(data_dir: str = "data") -> list:
    if not os.path.isdir(data_dir):
        raise Exception(
            "Le repertoire `data` n'a pas été trouvé.\nAssurez vous d'executer ce script dans le dossier où il se trouve."
        )
    questions_list = []
    all_json_questions_lists = os.listdir(data_dir)
    for json_questions_list in all_json_questions_lists:
        path = os.path.join(data_dir, json_questions_list)
        with open(path, "r") as f:
            questions_list += json.load(f)
    return questions_list


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


def generate_question_to_print(
    question_dict: dict[str, str | list[dict[str, str]]],
) -> str:
    to_print = f"    ###### Question ############################################################\n"
    to_print += f"    Thème : {question_dict['theme']}\n"
    to_print += f" => Question : {question_dict['question']}\n"
    for answer in question_dict["answers"]:
        to_print += f"    {answer['answer_id']}\t{answer['answer_text']}\n"
    return to_print


def print_question(question_dict: dict):
    question_to_print = generate_question_to_print(question_dict)
    print(question_to_print)


def get_correct_answer_ids_set(
    question_dict: dict[str, str | list[dict[str, str]]],
) -> set:
    correct_answer_ids_set = set()
    for answer in question_dict["answers"]:
        answer_is_correct = convert_str_to_bool(answer["answer_is_correct"])
        if answer_is_correct:
            correct_answer_ids_set.add(answer["answer_id"])
    return correct_answer_ids_set


def get_user_answer_ids_set() -> set:
    print("    Votre réponse :")
    user_answer_ids = input(
        "    Entrez les réponses que vous estimez correctes\n    (numéros séparés par des espaces) : "
    )
    if not re.match(r"\d(\s\d)*$", user_answer_ids):
        print(
            "    L'entrée attendue doit avoir la forme `3` ou `1 4`, veuillez recommencer."
        )
        user_answer_ids_set = get_user_answer_ids_set()
    else:
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


def generate_correction_to_print(
    user_answer_ids_list: set, correct_answer_ids_set: set
) -> str:
    to_print = "    ###### Réponse #############################################################"
    is_user_correct = compare_user_correct_answers(
        user_answer_ids_set, correct_answer_ids_set
    )
    if is_user_correct:
        to_print += "\tCorrect"
    else:
        to_print += "\n\tNon correct\n\tLes réponses correctes sont :\n\t"
        for correct_id in correct_answer_ids_set:
            to_print += f"{correct_id} "
    return to_print


def print_correction(user_answer_ids_list: set, correct_answer_ids_set: set):
    correction = generate_correction_to_print(
        user_answer_ids_list, correct_answer_ids_set
    )
    print(correction)


def ask_to_continue() -> bool:
    print(
        "########## Une autre question ? ################################################"
    )
    choice = input("Laissez vide pour continuer, entrez q pour sortir. ")
    match choice:
        case "":
            return True
        case _:
            return False


def print_score(score: list):
    print(
        "########## C'est fini ##########################################################"
    )
    print(f"Votre score pour cette session est de {score[0]}/{score[1]}.")


if __name__ == "__main__":
    questions_list = load_questions_list_from_json_files()
    score = [0, 0]
    while True:
        want_to_continue = ask_to_continue()
        if not want_to_continue:
            print_score(score)
            break
        question_dict = generate_question_dict(questions_list)
        print_question(question_dict)
        user_answer_ids_set = get_user_answer_ids_set()
        correct_answer_ids_set = get_correct_answer_ids_set(question_dict)
        print_correction(user_answer_ids_set, correct_answer_ids_set)
