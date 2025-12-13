import json
import os


def determine_path() -> str:
    data_dir = "data"
    if not os.path.isdir(data_dir):
        raise Exception(
            "Le repertoire `data` n'a pas été trouvé.\nAssurez vous d'executer ce script dans le dossier où il se trouve."
        )
    file_name = input("Entrez le nom du fichier dans lequel vous voulez écrire : ")
    if file_name == "data.json":
        print(
            "Veuillez trouver un autre nom, celui-ci est réservé au fichier principal."
        )
    path = os.path.join(data_dir, file_name)
    return path


def get_theme() -> str:
    theme = input("Entrez le thème (parmi Histoire, Traitement_linguistique, ...)")
    match theme:
        case "Histoire" | "1":
            theme = "Histoire"
        case "Traitement_linguistique":
            theme = "Traitement Linguistique"
        case _:
            print("Veuillez choisir un thème parmi la liste proposée")
            theme = get_theme()
    return theme


def get_question() -> str:
    question = input("Entrez la question ou laissez vide pour terminer : ")
    return question


def get_answer_id(id: str) -> str:
    id = int(id)
    id += 1
    id = str(id)
    return id


def get_answer_text() -> str:
    answer_text = input("Entrez une réponse, laissez vide pour terminer : ")
    return answer_text


def get_answer_is_correct() -> str:
    answer_is_correct = input("Est-ce une réponse correcte ? [y/n] : ")
    match answer_is_correct:
        case "y":
            answer_is_correct = "True"
        case "n":
            answer_is_correct = "False"
        case _:
            print("Veuillez entrer 'y' ou 'n'.")
            answer_is_correct = get_answer_is_correct()
    return answer_is_correct


def get_answer(previous_answer_id: str) -> dict | None:
    answer_id = get_answer_id(previous_answer_id)
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
    answer_id = "1"
    while True:
        answer = get_answer(answer_id)
        if not answer:
            break
        answer_list.append(answer)
    return answer_list


def get_question_dict() -> dict | None:
    question = get_question()
    if question == "":
        return None
    theme = get_theme()
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


path = determine_path()
data = get_questions_list()
print(data)


json_str = json.dumps(data, indent=2, ensure_ascii=False)

with open(path, "w") as f:
    f.write(json_str)
