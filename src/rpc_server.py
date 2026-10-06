import socket
from xml.etree import ElementTree

from main import (
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
    update_instruction,
    update_response,
    update_session,
)

HOST = "127.0.0.1"
PORT = 5000
VERSION = 1
REQUEST_HEADER_SIZE = 6

OPERATIONS = {
    1: add_session,
    2: delete_session,
    3: get_all_session,
    4: update_session,
    5: add_instruction,
    6: delete_instruction,
    7: get_all_instruction,
    8: update_instruction,
    9: add_response,
    10: delete_response,
    11: get_all_response,
    12: update_response,
    13: filtered_join,
}

LIST_OPERATIONS = {
    3,
    7,
    11,
}

JOIN_OPERATION = 13

SESSION_FIELDS = [
    "uid",
    "created",
    "error",
]

INSTRUCTION_FIELDS = [
    "uid",
    "created",
    "payload",
    "session_id",
    "description",
    "tags",
]

RESPONSE_FIELDS = [
    "uid",
    "created",
    "output",
    "stage",
    "error",
    "instruction_id",
    "cache_hit",
]

JOIN_FIELDS = [
    "description",
    "cache_hit",
    "stage",
]

RECORD_FIELDS = {
    3: SESSION_FIELDS,
    7: INSTRUCTION_FIELDS,
    11: RESPONSE_FIELDS,
    JOIN_OPERATION: JOIN_FIELDS,
}


def receive_all(connection, size: int) -> bytes:
    data = bytearray()

    while len(data) < size:
        chunk = connection.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Соединение закрыто")

        data.extend(chunk)

    return bytes(data)


def parse_request(data: bytes) -> tuple:
    version = data[0]
    operation = int.from_bytes(data[1:3], "little")
    body_size = int.from_bytes(data[3:6], "little")
    body = data[REQUEST_HEADER_SIZE : REQUEST_HEADER_SIZE + body_size]

    return version, operation, body


def make_response(operation: int, body: bytes) -> bytes:
    body_size = len(body)

    return body_size.to_bytes(3, "little") + operation.to_bytes(1, "little") + body


def add_record(root, fields, record) -> None:
    item = ElementTree.SubElement(root, "record")

    for name, value in zip(fields, record):
        element = ElementTree.SubElement(item, name)
        element.text = str(value)


def make_xml(data, operation: int) -> bytes:
    root = ElementTree.Element("response")

    if data is None:
        return ElementTree.tostring(
            root,
            encoding="utf-8",
        )

    if operation in RECORD_FIELDS:
        fields = RECORD_FIELDS[operation]

        for record in data:
            add_record(root, fields, record)

        return ElementTree.tostring(
            root,
            encoding="utf-8",
        )

    result = ElementTree.SubElement(root, "result")
    result.text = str(data)

    return ElementTree.tostring(
        root,
        encoding="utf-8",
    )


def parse_bool(value: str) -> bool:
    return value.lower() == "true"


ARGUMENT_CONVERTERS = {
    1: (int, int, str),
    2: (int,),
    3: (),
    4: (int, int, str),
    5: (int, int, str, int, str, str),
    6: (int,),
    7: (),
    8: (int, int, str, int, str, str),
    9: (
        int,
        int,
        str,
        str,
        str,
        int,
        parse_bool,
    ),
    10: (int,),
    11: (),
    12: (
        int,
        int,
        str,
        str,
        str,
        int,
        parse_bool,
    ),
    13: (),
}


def get_values(body: bytes) -> list:
    arguments = ElementTree.fromstring(body)

    return [element.text if element.text is not None else "" for element in arguments]


def call_operation(operation: int, values: list):
    function = OPERATIONS[operation]
    converters = ARGUMENT_CONVERTERS[operation]

    if len(values) != len(converters):
        raise ValueError("Неверное количество аргументов")

    arguments = [converter(value) for converter, value in zip(converters, values)]

    return function(*arguments)


def handle_request(data: bytes) -> bytes:
    version, operation, body = parse_request(data)

    if version != VERSION:
        raise ValueError("Неподдерживаемая версия протокола")

    print(
        "RPC request:",
        version,
        operation,
        body.decode("utf-8"),
    )

    values = get_values(body)
    result = call_operation(operation, values)
    response_body = make_xml(result, operation)
    response = make_response(operation, response_body)

    print(
        "RPC response:",
        operation,
        response_body.decode("utf-8"),
    )

    return response


def start_server() -> None:
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    ) as server:
        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        server.bind((HOST, PORT))
        server.listen()

        print(f"RPC server started on {HOST}: {PORT}")

        while True:
            connection, _ = server.accept()

            with connection:
                header = receive_all(
                    connection,
                    REQUEST_HEADER_SIZE,
                )
                body_size = int.from_bytes(
                    header[3:REQUEST_HEADER_SIZE],
                    "little",
                )
                body = receive_all(
                    connection,
                    body_size,
                )
                response = handle_request(header + body)

                connection.sendall(response)


if __name__ == "__main__":
    start_server()
