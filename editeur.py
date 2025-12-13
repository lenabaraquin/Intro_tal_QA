import json
import os


def determine_path() -> str:
    data_dir = "data"
    if not os.path.isdir(data_dir):
        raise Exception(
            "Le repertoire `data` n'a pas été trouvé.\nAssurez vous d'executer ce script dans le dossier où il se trouve."
        )
    file_name = (
        input(
            "\nEntrez le nom du fichier dans lequel vous voulez écrire \n(data_perso.json par défaut) : "
        )
        or "data_perso.json"
    )
    if file_name == "data.json":
        print(
            "Veuillez trouver un autre nom, celui-ci est réservé au fichier principal."
        )
    path = os.path.join(data_dir, file_name)
    return path


def save_json(questions_list: list, path: str):
    if os.path.isfile(path):
        with open(path, "r") as f:
            existing_json_questions_list = json.load(f)
    else:
        existing_json_questions_list = []
    data_to_write = existing_json_questions_list + questions_list
    json_str = json.dumps(data_to_write, indent=2, ensure_ascii=False)
    with open(path, "w") as f:
        f.write(json_str)


def get_theme() -> str | None:
    print(
        "\n########## Choix du thème ######################################################"
    )
    print("""Liste des thèmes : 
          1: Histoire
          2: Traitements linguistiques
          3: Pretraitements linguistiques
          4: Pretraitements informatiques
          5: Methodes et approches
          6: Evaluation""")
    theme = input(
        "Entrez un thème parmi la liste (numéro ou nom) ou laissez vide pour terminer : "
    )
    match theme:
        case "Histoire" | "1":
            theme = "Histoire du TAL"
        case "Traitements linguistiques" | "2":
            theme = "Traitements linguistiques"
        case "Pretraitements linguistiques" | "3":
            theme = "Prétraitements linguistiques"
        case "Pretraitements informatiques" | "4":
            theme = "Prétraitements informatiques"
        case "Methodes et approches" | "5":
            theme = "Méthodes et approches"
        case "Evaluation" | "6":
            theme = "Évaluation"
        case "":
            theme = ""
        case _:
            print("Veuillez choisir un thème parmi la liste proposée")
            theme = get_theme()
    return theme


def get_question() -> str:
    print(
        "\n########## Édition d'une question ##############################################"
    )
    question = input("Entrez la question ou laissez vide pour terminer : \n")
    return question


def get_answer_id(id: int) -> str:
    return str(id)


def get_answer_text() -> str:
    answer_text = input(
        "          Entrez une réponse, laissez vide pour terminer : \n          "
    )
    return answer_text


def get_answer_is_correct() -> str:
    answer_is_correct = input("          Est-ce une réponse correcte ? [y/n] : ")
    match answer_is_correct:
        case "y":
            answer_is_correct = "True"
        case "n":
            answer_is_correct = "False"
        case _:
            print("Veuillez entrer 'y' ou 'n'.")
            answer_is_correct = get_answer_is_correct()
    return answer_is_correct


def get_answer(id: int) -> dict | None:
    print(
        "\n          ########## Édition d'une réponse #####################################"
    )
    answer_id = get_answer_id(id)
    answer_text = get_answer_text()
    if answer_text == "":
        return None
    answer_is_correct = get_answer_is_correct()
    answer = {
        "answer_id": answer_id,
        "answer_text": answer_text,
        "answer_is_correct": answer_is_correct,
    }
    return answer


def get_answers() -> list:
    answer_list = []
    id = 1
    while True:
        answer = get_answer(id)
        id += 1
        if not answer:
            break
        answer_list.append(answer)
    return answer_list


def get_question_dict() -> dict | None:
    theme = get_theme()
    if theme == "":
        return None
    question = get_question()
    if question == "":
        return None
    answers = get_answers()
    question_dict = {"question": question, "theme": theme, "answers": answers}
    return question_dict


def get_questions_list() -> list:
    questions_list = []
    while True:
        question_dict = get_question_dict()
        if not question_dict:
            break
        questions_list.append(question_dict)
    return questions_list


if __name__ == "__main__":
    path = determine_path()
    questions_list = get_questions_list()

    save_json(questions_list, path)
