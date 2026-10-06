import pytest

from src.rpc_client import RPCClient, parse_xml


def test_receive_all_connection_closed():
    client = RPCClient()

    class ClosedConnection:
        def recv(self, size):
            return b""

    with pytest.raises(ConnectionError):
        client.receive_all(ClosedConnection(), 10)


def test_parse_xml_result():
    body = b"<response><result>test</result></response>"

    result = parse_xml(body)

    assert result == {"result": "test"}
