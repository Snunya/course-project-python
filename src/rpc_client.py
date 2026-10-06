import socket
from xml.etree import ElementTree


HOST = "127.0.0.1"
PORT = 5000


OPERATIONS = {
    "add_session": 1,
    "delete_session": 2,
    "get_all_session": 3,
    "update_session": 4,
    "add_instruction": 5,
    "delete_instruction": 6,
    "get_all_instruction": 7,
    "update_instruction": 8,
    "add_response": 9,
    "delete_response": 10,
    "get_all_response": 11,
    "update_response": 12,
    "filtered_join": 13,
}


def build_request(operation: int, body: bytes) -> bytes:
    version = 1
    body_size = len(body)

    return (
        version.to_bytes(1, "little")
        + operation.to_bytes(2, "little")
        + body_size.to_bytes(3, "little")
        + body
    )


def make_xml(tag: str, data: dict) -> bytes:
    root = ElementTree.Element(tag)

    for key, value in data.items():
        element = ElementTree.SubElement(root, key)
        element.text = str(value)

    return ElementTree.tostring(
        root,
        encoding="utf-8",
    )


def parse_xml(body: bytes) -> list | dict:
    root = ElementTree.fromstring(body)
    result = []

    for record in root.findall("record"):
        values = {}

        for element in record:
            values[element.tag] = (
                element.text if element.text is not None else ""
            )

        result.append(values)

    if result:
        return result

    result_element = root.find("result")

    if result_element is not None:
        return {"result": result_element.text}

    return []


class RPCClient:
    def __init__(
        self,
        host: str = HOST,
        port: int = PORT,
    ) -> None:
        self.host = host
        self.port = port

    def receive_all(
        self,
        connection,
        size: int,
    ) -> bytes:
        data = bytearray()

        while len(data) < size:
            chunk = connection.recv(size - len(data))

            if not chunk:
                raise ConnectionError("Соединение закрыто")

            data.extend(chunk)

        return bytes(data)

    def call(
        self,
        operation: int,
        data: dict,
    ) -> list | dict:
        body = make_xml("request", data)
        request = build_request(operation, body)

        with socket.create_connection((self.host, self.port)) as connection:
            connection.sendall(request)
            connection.shutdown(socket.SHUT_WR)

            header = self.receive_all(connection, 4)
            body_size = int.from_bytes(
                header[:3],
                "little",
            )
            response_operation = header[3]

            response_body = self.receive_all(
                connection,
                body_size,
            )

        print(
            "RPC response:",
            response_operation,
            response_body.decode("utf-8"),
        )

        return parse_xml(response_body)

    def add_session(
        self,
        uid: int,
        created: int,
        error: str,
    ) -> list | dict:
        return self.call(
            OPERATIONS["add_session"],
            {
                "uid": uid,
                "created": created,
                "error": error,
            },
        )

    def delete_session(self, uid: int) -> list | dict:
        return self.call(
            OPERATIONS["delete_session"],
            {"uid": uid},
        )

    def get_all_session(self) -> list | dict:
        return self.call(
            OPERATIONS["get_all_session"],
            {},
        )

    def update_session(
        self,
        uid: int,
        created: int,
        error: str,
    ) -> list | dict:
        return self.call(
            OPERATIONS["update_session"],
            {
                "uid": uid,
                "created": created,
                "error": error,
            },
        )

    def add_instruction(
        self,
        uid: int,
        created: int,
        payload: str,
        session_id: int,
        description: str,
        tags: str,
    ) -> list | dict:
        return self.call(
            OPERATIONS["add_instruction"],
            {
                "uid": uid,
                "created": created,
                "payload": payload,
                "session_id": session_id,
                "description": description,
                "tags": tags,
            },
        )

    def delete_instruction(self, uid: int) -> list | dict:
        return self.call(
            OPERATIONS["delete_instruction"],
            {"uid": uid},
        )

    def get_all_instruction(self) -> list | dict:
        return self.call(
            OPERATIONS["get_all_instruction"],
            {},
        )

    def update_instruction(
        self,
        uid: int,
        created: int,
        payload: str,
        session_id: int,
        description: str,
        tags: str,
    ) -> list | dict:
        return self.call(
            OPERATIONS["update_instruction"],
            {
                "uid": uid,
                "created": created,
                "payload": payload,
                "session_id": session_id,
                "description": description,
                "tags": tags,
            },
        )

    def add_response(
        self,
        uid: int,
        created: int,
        output: str,
        stage: str,
        error: str,
        instruction_id: int,
        cache_hit: bool,
    ) -> list | dict:
        return self.call(
            OPERATIONS["add_response"],
            {
                "uid": uid,
                "created": created,
                "output": output,
                "stage": stage,
                "error": error,
                "instruction_id": instruction_id,
                "cache_hit": cache_hit,
            },
        )

    def delete_response(self, uid: int) -> list | dict:
        return self.call(
            OPERATIONS["delete_response"],
            {"uid": uid},
        )

    def get_all_response(self) -> list | dict:
        return self.call(
            OPERATIONS["get_all_response"],
            {},
        )

    def update_response(
        self,
        uid: int,
        created: int,
        output: str,
        stage: str,
        error: str,
        instruction_id: int,
        cache_hit: bool,
    ) -> list | dict:
        return self.call(
            OPERATIONS["update_response"],
            {
                "uid": uid,
                "created": created,
                "output": output,
                "stage": stage,
                "error": error,
                "instruction_id": instruction_id,
                "cache_hit": cache_hit,
            },
        )

    def filtered_join(self) -> list | dict:
        return self.call(
            OPERATIONS["filtered_join"],
            {},
        )
