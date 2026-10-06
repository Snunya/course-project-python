import time

response = []
instruction = []
session = []

RECENT_INTERVAL = 6 * 60


def add_session(uid: int, created: int, error: str) -> None:
    session.append([uid, created, error])
    print("Сессия создана")


def delete_session(uid: int) -> None:
    for i, item in enumerate(session):
        if item[0] == uid:
            session.pop(i)
            print("Сессия удалена")
            return
    print("Сессия не найдена")


def get_all_session() -> list:
    return session


def update_session(uid: int, new_created: int, new_error: str) -> None:
    for item in session:
        if item[0] == uid:
            item[1] = new_created
            item[2] = new_error
            print("Сессия успешно обновлена")
            return
    print("Ошибка")


def add_instruction(
    uid: int,
    created: int,
    payload: str,
    session_id: int,
    description: str,
    tags: str,
) -> None:
    instruction.append(
        [uid, created, payload, session_id, description, tags]
    )
    print("Инструкция создана")


def delete_instruction(uid: int) -> None:
    for i, item in enumerate(instruction):
        if item[0] == uid:
            instruction.pop(i)
            print("Инструкция удалена")
            return
    print("Инструкция не найдена")


def get_all_instruction() -> list:
    return instruction


def update_instruction(
    uid: int,
    new_created: int,
    new_payload: str,
    new_session: int,
    new_description: str,
    new_tags: str,
) -> None:
    for item in instruction:
        if item[0] == uid:
            item[1] = new_created
            item[2] = new_payload
            item[3] = new_session
            item[4] = new_description
            item[5] = new_tags
            print("Инструкция успешно обновлена")
            return
    print("Ошибка")


def add_response(
    uid: int,
    created: int,
    output: str,
    stage: str,
    error: str,
    instruction_id: int,
    cache_hit: bool,
) -> None:
    response.append(
        [uid, created, output, stage, error, instruction_id, cache_hit]
    )
    print("Ответ создан")


def delete_response(uid: int) -> None:
    for i, item in enumerate(response):
        if item[0] == uid:
            response.pop(i)
            print("Ответ удален")
            return
    print("Ответ не найден")


def get_all_response() -> list:
    return response


def update_response(
    uid: int,
    new_created: int,
    new_output: str,
    new_stage: str,
    new_error: str,
    new_instruction: int,
    new_cache_hit: bool,
) -> None:
    for item in response:
        if item[0] == uid:
            item[1] = new_created
            item[2] = new_output
            item[3] = new_stage
            item[4] = new_error
            item[5] = new_instruction
            item[6] = new_cache_hit
            print("Ответ успешно обновлен")
            return
    print("Ошибка")


def filtered_join() -> list:
    current_time = int(time.time())
    result = []

    for item in response:
        instruction_id = item[5]
        created = item[1]
        cache_hit = item[6]
        stage = item[3]

        if created >= current_time - RECENT_INTERVAL:
            for current_instruction in instruction:
                if current_instruction[0] == instruction_id:
                    description = current_instruction[4]
                    result.append([description, cache_hit, stage])
    return result


def parse_cache(value: str) -> bool:
    return value.lower() == "true"


def handle_session_command(action: str, cmd: list[str]) -> bool:
    if action == "add_session":
        add_session(int(cmd[1]), int(cmd[2]), cmd[3])
    elif action == "show_sessions":
        print(get_all_session())
    elif action == "update_session":
        update_session(int(cmd[1]), int(cmd[2]), cmd[3])
    elif action == "delete_session":
        delete_session(int(cmd[1]))
    else:
        return False
    return True


def handle_instruction_command(action: str, cmd: list[str]) -> bool:
    if action == "add_instruction":
        add_instruction(
            int(cmd[1]),
            int(cmd[2]),
            cmd[3],
            int(cmd[4]),
            cmd[5],
            cmd[6],
        )
    elif action == "show_instructions":
        print(get_all_instruction())
    elif action == "update_instruction":
        update_instruction(
            int(cmd[1]),
            int(cmd[2]),
            cmd[3],
            int(cmd[4]),
            cmd[5],
            cmd[6],
        )
    elif action == "delete_instruction":
        delete_instruction(int(cmd[1]))
    else:
        return False
    return True


def handle_response_command(action: str, cmd: list[str]) -> bool:
    if action == "add_response":
        add_response(
            int(cmd[1]),
            int(cmd[2]),
            cmd[3],
            cmd[4],
            cmd[5],
            int(cmd[6]),
            parse_cache(cmd[7]),
        )
    elif action == "show_responses":
        print(get_all_response())
    elif action == "update_response":
        update_response(
            int(cmd[1]),
            int(cmd[2]),
            cmd[3],
            cmd[4],
            cmd[5],
            int(cmd[6]),
            parse_cache(cmd[7]),
        )
    elif action == "delete_response":
        delete_response(int(cmd[1]))
    else:
        return False
    return True


def process_command(cmd: list[str]) -> bool:
    if not cmd:
        return True

    action = cmd[0]

    if action == "exit":
        return False
    if handle_session_command(action, cmd):
        return True
    if handle_instruction_command(action, cmd):
        return True
    if handle_response_command(action, cmd):
        return True
    if action == "join":
        print("Результат выборки:", filtered_join())
        return True

    print("Неизвестная команда.")
    return True


def main() -> None:
    print("Практическая работа №1. Вариант 2")
    print("Введите команду (например: show_sessions, join, exit)")

    while True:
        cmd = input(">> ").split()
        if not process_command(cmd):
            break


if __name__ == "__main__":
    main()
