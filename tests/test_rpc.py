import time

from src.rpc_client import RPCClient


def find_record(records, uid):
    return next(
        record for record in records
        if record["uid"] == str(uid)
    )


def test_all_rpc_operations():
    client = RPCClient()
    now = int(time.time())

    session_uid = 900001
    instruction_uid = 900002
    response_uid = 900003

    client.add_session(
        session_uid,
        now,
        "нет ошибки",
    )

    sessions = client.get_all_session()
    session = find_record(sessions, session_uid)
    assert session["uid"] == str(session_uid)

    client.update_session(
        session_uid,
        now,
        "обновлено",
    )

    sessions = client.get_all_session()
    session = find_record(sessions, session_uid)
    assert session["error"] == "обновлено"

    client.add_instruction(
        instruction_uid,
        now,
        "payload",
        session_uid,
        "Тестовая инструкция",
        "test",
    )

    instructions = client.get_all_instruction()
    instruction = find_record(instructions, instruction_uid)
    assert instruction["uid"] == str(instruction_uid)

    client.update_instruction(
        instruction_uid,
        now,
        "updated payload",
        session_uid,
        "Обновленная инструкция",
        "updated",
    )

    instructions = client.get_all_instruction()
    instruction = find_record(
        instructions,
        instruction_uid,
    )
    assert instruction["description"] == (
        "Обновленная инструкция"
    )

    client.add_response(
        response_uid,
        now,
        "output",
        "completed",
        "нет ошибки",
        instruction_uid,
        True,
    )

    responses = client.get_all_response()
    response = find_record(responses, response_uid)
    assert response["uid"] == str(response_uid)

    join_result = client.filtered_join()

    assert any(
        item["description"] == "Обновленная инструкция"
        for item in join_result
    )

    client.update_response(
        response_uid,
        now,
        "updated output",
        "processing",
        "ошибка",
        instruction_uid,
        False,
    )

    responses = client.get_all_response()
    response = find_record(responses, response_uid)
    assert response["cache_hit"] == "False"

    client.delete_response(response_uid)

    responses = client.get_all_response()
    assert not any(
        response["uid"] == str(response_uid)
        for response in responses
    )

    client.delete_instruction(instruction_uid)

    instructions = client.get_all_instruction()
    assert not any(
        instruction["uid"] == str(instruction_uid)
        for instruction in instructions
    )

    client.delete_session(session_uid)

    sessions = client.get_all_session()
    assert not any(
        session["uid"] == str(session_uid)
        for session in sessions
    )