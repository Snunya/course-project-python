
    
  
import time

from src.main import (
    add_instruction,
    add_response,
    add_session,
    delete_instruction,
    delete_response,
    delete_session,
    filtered_join,
    get_all_instruction,
    get_all_response,
    get_all_session,
    instruction,
    response,
    session,
    update_instruction,
    update_response,
    update_session,
)


def clear_data():
    session.clear()
    instruction.clear()
    response.clear()


def test_add_session():
    clear_data()
    add_session(1, 100, "error")
    assert session == [[1, 100, "error"]]


def test_get_all_session():
    clear_data()
    add_session(1, 100, "error")
    assert get_all_session() == [[1, 100, "error"]]


def test_update_session():
    clear_data()
    add_session(1, 100, "error")
    update_session(1, 200, "new error")
    assert session == [[1, 200, "new error"]]


def test_delete_session():
    clear_data()
    add_session(1, 100, "error")
    delete_session(1)
    assert session == []


def test_delete_missing_session():
    clear_data()
    add_session(1, 100, "error")
    delete_session(2)
    assert session == [[1, 100, "error"]]


def test_add_instruction():
    clear_data()
    add_instruction(1, 100, "payload", 10, "description", "tag")
    assert instruction == [[1, 100, "payload", 10, "description", "tag"]]


def test_get_all_instruction():
    clear_data()
    add_instruction(1, 100, "payload", 10, "description", "tag")
    assert get_all_instruction() == [[1, 100, "payload", 10, "description", "tag"]]


def test_update_instruction():
    clear_data()
    add_instruction(1, 100, "payload", 10, "description", "tag")
    update_instruction(1, 200, "new payload", 20, "new description", "new tag")
    assert instruction == [[1, 200, "new payload", 20, "new description", "new tag"]]


def test_delete_instruction():
    clear_data()
    add_instruction(1, 100, "payload", 10, "description", "tag")
    delete_instruction(1)
    assert instruction == []


def test_delete_missing_instruction():
    clear_data()
    add_instruction(1, 100, "payload", 10, "description", "tag")
    delete_instruction(2)
    assert instruction == [[1, 100, "payload", 10, "description", "tag"]]


def test_add_response():
    clear_data()

