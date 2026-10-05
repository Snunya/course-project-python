import time

from src.rpc_client import RPCClient


def test_all_rpc_operations():
    client = RPCClient()
    now = int(time.time())

    client.add_session(1, now, "нет ошибки")

    sessions = client.get_all_session()
    assert sessions[0]["uid"] == "1"

    client.update_session(
        1,
        now,
        "обновлено",
    )

    sessions = client.get_all_session()
    assert sessions[0]["error"] == "обновлено"

    client.add_instruction(
        10,
        now,
        "payload",
        1,
        "Тестовая инструкция",
        "test",
    )

    instructions = client.get_all_instruction()
    assert instructions[0]["uid"] == "10"

    client.update_instruction(
        10,
        now,
        "updated payload",
        1,
        "Обновленная инструкция",
        "updated",
    )

    instructions = client.get_all_instruction()
    assert instructions[0]["description"] == (
        "Обновленная инструкция"
    )

    client.add_response(
        20,
        now,
        "output",
        "completed",
        "нет ошибки",
        10,
        True,
    )

    responses = client.get_all_response()
    assert responses[0]["uid"] == "20"

    join_result = client.filtered_join()

    assert join_result[0]["description"] == (
        "Обновленная инструкция"
    )

    client.update_response(
        20,
        now,
        "updated output",
        "processing",
        "ошибка",
        10,
        False,
    )

    responses = client.get_all_response()
    assert responses[0]["cache_hit"] == "False"

    client.delete_response(20)
    assert client.get_all_response() == []

    client.delete_instruction(10)
    assert client.get_all_instruction() == []

    client.delete_session(1)
    assert client.get_all_session() == []
    