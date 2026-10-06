from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule

from src.rpc_client import RPCClient

XML_TEXT = st.text(
    alphabet=st.sampled_from(
        list("abcdefghijklmnopqrstuvwxyz" "абвгдежзийклмнопрстуфхцчшщ")
    ),
    max_size=20,
)


@settings(
    max_examples=10,
    stateful_step_count=20,
    deadline=None,
)
class RPCStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.client = RPCClient()
        self.sessions = {}
        self.instructions = {}
        self.responses = {}

    @rule(
        data=st.fixed_dictionaries(
            {
                "uid": st.integers(min_value=1, max_value=100000),
                "created": st.integers(min_value=1, max_value=2000000000),
                "payload": XML_TEXT,
                "session_id": st.integers(min_value=1, max_value=100000),
                "description": XML_TEXT,
                "tags": XML_TEXT,
            }
        )
    )
    def add_instruction(self, data):
        self.client.add_instruction(
            data["uid"],
            data["created"],
            data["payload"],
            data["session_id"],
            data["description"],
            data["tags"],
        )

        self.instructions[data["uid"]] = {
            "uid": str(data["uid"]),
            "created": str(data["created"]),
            "payload": data["payload"],
            "session_id": str(data["session_id"]),
            "description": data["description"],
            "tags": data["tags"],
        }

        instructions = self.client.get_all_instruction()
        actual = [
            item for item in instructions if item["uid"] == str(data["uid"])
        ]

        assert actual
        assert actual[-1]["created"] == str(data["created"])
        assert actual[-1]["payload"] == data["payload"]
        assert actual[-1]["description"] == data["description"]
        assert actual[-1]["tags"] == data["tags"]

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
    )
    def delete_instruction(self, uid):
        self.client.delete_instruction(uid)
        self.instructions.pop(uid, None)

    @rule()
    def get_all_instruction(self):
        instructions = self.client.get_all_instruction()
        assert isinstance(instructions, list)

    @rule(
        data=st.fixed_dictionaries(
            {
                "uid": st.integers(min_value=1, max_value=100000),
                "created": st.integers(min_value=1, max_value=2000000000),
                "payload": XML_TEXT,
                "session_id": st.integers(min_value=1, max_value=100000),
                "description": XML_TEXT,
                "tags": XML_TEXT,
            }
        )
    )
    def update_instruction(self, data):
        self.client.update_instruction(
            data["uid"],
            data["created"],
            data["payload"],
            data["session_id"],
            data["description"],
            data["tags"],
        )

    @rule(
        data=st.fixed_dictionaries(
            {
                "uid": st.integers(min_value=1, max_value=100000),
                "created": st.integers(min_value=1, max_value=2000000000),
                "output": XML_TEXT,
                "stage": XML_TEXT,
                "error": XML_TEXT,
                "instruction_id": st.integers(min_value=1, max_value=100000),
                "cache_hit": st.booleans(),
            }
        )
    )
    def add_response(self, data):
        self.client.add_response(
            data["uid"],
            data["created"],
            data["output"],
            data["stage"],
            data["error"],
            data["instruction_id"],
            data["cache_hit"],
        )

        self.responses[data["uid"]] = {
            "uid": str(data["uid"]),
            "created": str(data["created"]),
            "output": data["output"],
            "stage": data["stage"],
            "error": data["error"],
            "instruction_id": str(data["instruction_id"]),
            "cache_hit": str(data["cache_hit"]),
        }

        responses = self.client.get_all_response()
        actual = [
            item for item in responses if item["uid"] == str(data["uid"])
        ]

        assert actual
        assert actual[-1]["created"] == str(data["created"])
        assert actual[-1]["output"] == data["output"]
        assert actual[-1]["stage"] == data["stage"]
        assert actual[-1]["error"] == data["error"]
        assert actual[-1]["cache_hit"] == str(data["cache_hit"])

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
    )
    def delete_response(self, uid):
        self.client.delete_response(uid)
        self.responses.pop(uid, None)

    @rule()
    def get_all_response(self):
        responses = self.client.get_all_response()
        assert isinstance(responses, list)

    @rule(
        data=st.fixed_dictionaries(
            {
                "uid": st.integers(min_value=1, max_value=100000),
                "created": st.integers(min_value=1, max_value=2000000000),
                "output": XML_TEXT,
                "stage": XML_TEXT,
                "error": XML_TEXT,
                "instruction_id": st.integers(min_value=1, max_value=100000),
                "cache_hit": st.booleans(),
            }
        )
    )
    def update_response(self, data):
        self.client.update_response(
            data["uid"],
            data["created"],
            data["output"],
            data["stage"],
            data["error"],
            data["instruction_id"],
            data["cache_hit"],
        )

    @rule()
    def filtered_join(self):
        result = self.client.filtered_join()
        assert isinstance(result, list)


TestRPC = RPCStateMachine.TestCase
