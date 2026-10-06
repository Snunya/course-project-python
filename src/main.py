import time


response = []
instruction = []
session = []

SIX_MINUTES = 6 * 60


def add_session(uid: int, created: int, error: str) -> None:
    """Создаёт новую сессию."""
    session.append([uid, created, error])
    print("Сессия создана")


def delete_session(uid: int) -> None:
    """Удаляет сессию по идентификатору."""
    for i in range(len(session)):
        if session[i][0] == uid:
            session.pop(i)
            print("Сессия удалена")
            return

    print("Сессия не найдена")


def get_all_session() -> list:
    """Возвращает все сессии."""
    return session


def update_session(uid: int, new_created: int, new_error: str) -> None:
    """Изменяет данные сессии по идентификатору."""
    for i in range(len(session)):
        if session[i][0] == uid:
            session[i][1] = new_created
            session[i][2] = new_error
            print("Сессия успешно обновлена")
            return

    print("Сессия не найдена")


def add_instruction(
    uid: int,
    created: int,
    payload: str,
    session_id: int,
    description: str,
    tags: str,
) -> None:
    """Создаёт новую инструкцию."""
    instruction.append(
        [uid, created, payload, session_id, description, tags]
    )
    print("Инструкция создана")


def delete_instruction(uid: int) -> None:
    """Удаляет инструкцию по идентификатору."""
    for i in range(len(instruction)):
        if instruction[i][0] == uid:
            instruction.pop(i)
            print("Инструкция удалена")
            return

    print("Инструкция не найдена")


def get_all_instruction() -> list:
    """Возвращает все инструкции."""
    return instruction


def update_instruction(
    uid: int,
    new_created: int,
    new_payload: str,
    new_session: int,
    new_description: str,
    new_tags: str,
) -> None:
    """Изменяет данные инструкции по идентификатору."""
    for i in range(len(instruction)):
        if instruction[i][0] == uid:
            instruction[i][1] = new_created
            instruction[i][2] = new_payload
            instruction[i][3] = new_session
            instruction[i][4] = new_description
            instruction[i][5] = new_tags
            print("Инструкция успешно обновлена")
            return

    print("Инструкция не найдена")


def add_response(
    uid: int,
    created: int,
    output: str,
    stage: str,
    error: str,
    instruction_id: int,
    cache_hit: bool,
) -> None:
    """Создаёт новый ответ."""
    response.append(
        [uid, created, output, stage, error, instruction_id, cache_hit]
    )
    print("Ответ создан")


def delete_response(uid: int) -> None:
    """Удаляет ответ по идентификатору."""
    for i in range(len(response)):
        if response[i][0] == uid:
            response.pop(i)
            print("Ответ удален")
            return

    print("Ответ не найден")


def get_all_response() -> list:
    """Возвращает все ответы."""
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
    """Изменяет данные ответа по идентификатору."""
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

    print("Ответ не найден")


def filtered_join() -> list:
    """Возвращает выборку Instruction и Response за последние 6 минут."""
    current_time = int(time.time())
    result = []

    for current_response in response:
        (
            response_uid,
            response_created,
            response_output,
            response_stage,
            response_error,
            response_instruction,
            response_cache,
        ) = current_response

        if response_created >= current_time - SIX_MINUTES:
            for current_instruction in instruction:
                (
                    instruction_uid,
                    instruction_created,
                    instruction_payload,
                    instruction_session,
                    instruction_description,
                    instruction_tags,
                ) = current_instruction

                if instruction_uid == response_instruction:
                    result.append(
                        [
                            instruction_description,
                            response_cache,
                            response_stage,
                        ]
                    )

    return result


def parse_bool(value: str) -> bool:
    """Преобразует строковое значение в логическое."""
    value = value.lower()

    if value == "true":
        return True
    if value == "false":
        return False

    raise ValueError


def process_session_command(cmd: list[str]) -> None:
    """Обрабатывает команды для работы с сессиями."""
    action = cmd[0]

    if action == "add_session":
        add_session(int(cmd[1]), int(cmd[2]), cmd[3])
    elif action == "show_sessions":
        print(get_all_session())
    elif action == "update_session":
        update_session(int(cmd[1]), int(cmd[2]), cmd[3])
    elif action == "delete_session":
        delete_session(int(cmd[1]))


def process_instruction_command(cmd: list[str]) -> None:
    """Обрабатывает команды для работы с инструкциями."""
    action = cmd[0]

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


def process_response_command(cmd: list[str]) -> None:
    """Обрабатывает команды для работы с ответами."""
    action = cmd[0]

    if action == "add_response":
        add_response(
            int(cmd[1]),
            int(cmd[2]),
            cmd[3],
            cmd[4],
            cmd[5],
            int(cmd[6]),
            parse_bool(cmd[7]),
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
            parse_bool(cmd[7]),
        )
    elif action == "delete_response":
        delete_response(int(cmd[1]))


def process_command(cmd: list[str]) -> None:
    """Обрабатывает одну команду REPL."""
    action = cmd[0]

    if action == "exit":
        raise SystemExit

    if action in {
        "add_session",
        "show_sessions",
        "update_session",
        "delete_session",
    }:
        process_session_command(cmd)
    elif action in {
        "add_instruction",
        "show_instructions",
        "update_instruction",
        "delete_instruction",
    }:
        process_instruction_command(cmd)
    elif action in {
        "add_response",
        "show_responses",
        "update_response",
        "delete_response",
    }:
        process_response_command(cmd)
    elif action == "join":
        print("Результат выборки:", filtered_join())
    else:
        print("Неизвестная команда.")


def main() -> None:
    """Запускает интерактивный режим работы с моделью."""
    print("Практическая работа №1. Вариант 2")
    print("Введите команду (например: show_sessions, join, exit)")

    while True:
        try:
            cmd = input(">> ").split()

            if not cmd:
                continue

            process_command(cmd)
        except (ValueError, IndexError):
            print("Ошибка: неверный формат команды.")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break


if __name__ == "__main__":
    main()

def clear_data() -> None:
    session.clear()
    instruction.clear()
    response.clear()
    