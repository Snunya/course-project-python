import time

response = []
instruction = []
session = []

#---

def add_session(uid: int, created: int, error: str) -> None:
    session.append([uid, created, error])
    print("Сессия создана")

def delete_session(uid: int):
    for i in range(len(session)):
        if session[i][0] == uid:
            session.pop(i)
            print("Сессия удалена")
            return
    print("Сессия не найдена")

def get_all_session() -> list:
    return session

def update_session(uid: int, new_created: int, new_error: str) -> None:
    for i in range(len(session)):
        if session[i][0] == uid:
            session[i][1] = new_created
            session[i][2] = new_error
            print("Сессия успешно обновлена")
            return
    print("Ошибка")

#---

def add_instruction(uid: int, created: int, payload: str, session_id: int, description: str, tags: str):
    instruction.append([uid, created, payload, session_id, description, tags])
    print("Инструкция создана")

def delete_instruction(uid: int):
    for i in range(len(instruction)):
        if instruction[i][0] == uid:
            instruction.pop(i)
            print("Инструкция удалена")
            return
    print("Инструкция не найдена")

def get_all_instruction() -> list:
    return instruction

def update_instruction(uid: int, new_created: int, new_payload: str, new_session: int, new_description: str, new_tags: str) -> None:
    for i in range(len(instruction)):
        if instruction[i][0] == uid:
            instruction[i][1] = new_created
            instruction[i][2] = new_payload
            instruction[i][3] = new_session
            instruction[i][4] = new_description
            instruction[i][5] = new_tags
            print("Инструкция успешно обновлена")
            return
    print("Ошибка")

#---

def add_response(uid: int, created: int, output: str, stage: str, error: str, instruction_id: int, cache_hit: bool) -> None:
    response.append([uid, created, output, stage, error, instruction_id, cache_hit])
    print("Ответ создан")

def delete_response(uid: int):
    for i in range(len(response)):
        if response[i][0] == uid:
            response.pop(i)
            print("Ответ удален")
            return
    print("Ответ не найден")

def get_all_response() -> list:
    return response

def update_response(uid: int, new_created: int, new_output: str, new_stage: str, new_error: str, new_instruction: int, new_cache_hit: bool) -> None:
    for i in range(len(response)):
        if response[i][0] == uid:
            response[i][1] = new_created
            response[i][2] = new_output
            response[i][3] = new_stage
            response[i][4] = new_error
            response[i][5] = new_instruction
            response[i][6] = new_cache_hit
            print("Ответ успешно обновлен")
            return
    print("Ошибка")

#---

def filtered_join():
    current_time = int(time.time())
    result = []

    for r in response:
        r_uid, r_creat, r_out, r_stage, r_err, r_inst, r_cache = r

        if r_creat >= (current_time - 360):
            for inst in instruction:
                i_uid, i_creat, i_payload, i_sess, i_desc, i_tags = inst

                if i_uid == r_inst:
                    result.append([i_desc, r_cache, r_stage])
    return result  # Исправлено: теперь возвращаем собранный результат!

#---

def main():
    print("Практическая работа №1. Вариант 2")
    print("Введите команду (например: show_sessions, join, exit)")

    while True:
        cmd = input(">> ").split()
        if not cmd:
            continue

        action = cmd[0]

        if action == "exit":
            break

        # Сессии команды
        elif action == "add_session":
            add_session(int(cmd[1]), int(cmd[2]), cmd[3])
        elif action == "show_sessions":
            print(get_all_session())
        elif action == "update_session":
            update_session(int(cmd[1]), int(cmd[2]), cmd[3])
        elif action == "delete_session":
            delete_session(int(cmd[1]))

        # Инструкции команды
        elif action == "add_instruction":
            add_instruction(int(cmd[1]), int(cmd[2]), cmd[3], int(cmd[4]), cmd[5], cmd[6])
        elif action == "show_instructions":
            print(get_all_instruction())
        elif action == "update_instruction":
            update_instruction(int(cmd[1]), int(cmd[2]), cmd[3], int(cmd[4]), cmd[5], cmd[6])
        elif action == "delete_instruction":
            delete_instruction(int(cmd[1]))

        # Ответы команды
        elif action == "add_response":
            cache = True if cmd[7].lower() == 'true' else False
            add_response(int(cmd[1]), int(cmd[2]), cmd[3], cmd[4], cmd[5], int(cmd[6]), cache)
        elif action == "show_responses":
            print(get_all_response())
        elif action == "update_response":
            cache = True if cmd[7].lower() == 'true' else False
            update_response(int(cmd[1]), int(cmd[2]), cmd[3], cmd[4], cmd[5], int(cmd[6]), cache)
        elif action == "delete_response":
            delete_response(int(cmd[1]))

        # Спец-выборка по варианту
        elif action == "join":
            print("Результат выборки:", filtered_join())

        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()