import time

from src.rpc_client import RPCClient


def find_record(records, uid):
    return next(record for record in records if record["uid"] == str(uid))


def test_session_operations():
    client = RPCClient()
    uid = 900001
    now = int(time.time())

    client.add_session(uid, now, "нет ошибки")
    session = find_record(client.get_all_session(), uid)
    assert session["uid"] == str(uid)

    client.update_session(uid, now, "обновлено")
    session = find_record(client.get_all_session(), uid)
    assert session["error"] == "обновлено"

    client.delete_session(uid)
    sessions = client.get_all_session()
    assert not any(item["uid"] == str(uid) for item in sessions)


def test_instruction_operations():
    client = RPCClient()
    uid = 900002
    now = int(time.time())

    client.add_instruction(
        uid, now, "payload", 900001, "Тестовая инструкция", "test"
    )
    instruction = find_record(client.get_all_instruction(), uid)
    assert instruction["uid"] == str(uid)

    client.update_instruction(
        uid,
        now,
        "updated payload",
        900001,
        "Обновленная инструкция",
        "updated",
    )
    instruction = find_record(client.get_all_instruction(), uid)
    assert instruction["description"] == "Обновленная инструкция"

    client.delete_instruction(uid)
    instructions = client.get_all_instruction()
    assert not any(item["uid"] == str(uid) for item in instructions)


def test_response_operations():
    client = RPCClient()
    uid = 900003
    now = int(time.time())

    client.add_response(
        uid, now, "output", "completed", "нет ошибки", 900002, True
    )
    response = find_record(client.get_all_response(), uid)
    assert response["uid"] == str(uid)

    client.update_response(
        uid, now, "updated output", "processing", "ошибка", 900002, False
    )
    response = find_record(client.get_all_response(), uid)
    assert response["cache_hit"] == "False"

    client.delete_response(uid)
    responses = client.get_all_response()
    assert not any(item["uid"] == str(uid) for item in responses)


def test_filtered_join():
    client = RPCClient()
    instruction_uid = 900004
    response_uid = 900005
    now = int(time.time())

    client.add_instruction(
        instruction_uid,
        now,
        "payload",
        900001,
        "Обновленная инструкция",
        "test",
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

    result = client.filtered_join()
    assert any(
        item["description"] == "Обновленная инструкция" for item in result
    )

    client.delete_response(response_uid)
    client.delete_instruction(instruction_uid)
