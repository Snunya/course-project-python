from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule

from src.rpc_client import RPCClient

XML_TEXT = st.text(
    alphabet=st.sampled_from(
        list(
            "abcdefghijklmnopqrstuvwxyz"
            "абвгдежзийклмнопрстуфхцчшщ"
        )
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

    # -------------------- SESSION --------------------

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        error=st.text(
            alphabet=st.sampled_from(
                list(
                    "abcdefghijklmnopqrstuvwxyz"
                    "абвгдежзийклмнопрстуфхцчшщ"
                )
            ),
            max_size=20,
        ),
    )
    def add_session(self, uid, created, error):
        self.client.add_session(uid, created, error)

        self.sessions[uid] = {
            "uid": str(uid),
            "created": str(created),
            "error": error,
        }

        sessions = self.client.get_all_session()

        actual = [
            session
            for session in sessions
            if session["uid"] == str(uid)
        ]

        assert actual
        assert actual[-1]["created"] == str(created)
        assert actual[-1]["error"] == error

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
    )
    def delete_session(self, uid):
        self.client.delete_session(uid)
        self.sessions.pop(uid, None)

    @rule()
    def get_all_session(self):
        sessions = self.client.get_all_session()
        assert isinstance(sessions, list)

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        error=XML_TEXT,
    )
    def update_session(self, uid, created, error):
        self.client.update_session(uid, created, error)

    # -------------------- INSTRUCTION --------------------

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        payload=XML_TEXT,
        session_id=st.integers(min_value=1, max_value=100000),
        description=XML_TEXT,
        tags=XML_TEXT,
    )
    def add_instruction(
        self,
        uid,
        created,
        payload,
        session_id,
        description,
        tags,
    ):
        self.client.add_instruction(
            uid,
            created,
            payload,
            session_id,
            description,
            tags,
        )

        self.instructions[uid] = {
            "uid": str(uid),
            "created": str(created),
            "payload": payload,
            "session_id": str(session_id),
            "description": description,
            "tags": tags,
        }

        instructions = self.client.get_all_instruction()

        actual = [
            instruction
            for instruction in instructions
            if instruction["uid"] == str(uid)
        ]

        assert actual
        assert actual[-1]["created"] == str(created)
        assert actual[-1]["payload"] == payload
        assert actual[-1]["description"] == description
        assert actual[-1]["tags"] == tags

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
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        payload=XML_TEXT,
        session_id=st.integers(min_value=1, max_value=100000),
        description=XML_TEXT,
        tags=XML_TEXT,
    )
    def update_instruction(
        self,
        uid,
        created,
        payload,
        session_id,
        description,
        tags,
    ):
        self.client.update_instruction(
            uid,
            created,
            payload,
            session_id,
            description,
            tags,
        )

    # -------------------- RESPONSE --------------------

    @rule(
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        output=XML_TEXT,
        stage=XML_TEXT,
        error=XML_TEXT,
        instruction_id=st.integers(
            min_value=1,
            max_value=100000,
        ),
        cache_hit=st.booleans(),
    )
    def add_response(
        self,
        uid,
        created,
        output,
        stage,
        error,
        instruction_id,
        cache_hit,
    ):
        self.client.add_response(
            uid,
            created,
            output,
            stage,
            error,
            instruction_id,
            cache_hit,
        )

        self.responses[uid] = {
            "uid": str(uid),
            "created": str(created),
            "output": output,
            "stage": stage,
            "error": error,
            "instruction_id": str(instruction_id),
            "cache_hit": str(cache_hit),
        }

        responses = self.client.get_all_response()

        actual = [
            response
            for response in responses
            if response["uid"] == str(uid)
        ]

        assert actual
        assert actual[-1]["created"] == str(created)
        assert actual[-1]["output"] == output
        assert actual[-1]["stage"] == stage
        assert actual[-1]["error"] == error
        assert actual[-1]["cache_hit"] == str(cache_hit)

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
        uid=st.integers(min_value=1, max_value=100000),
        created=st.integers(min_value=1, max_value=2000000000),
        output=XML_TEXT,
        stage=XML_TEXT,
        error=XML_TEXT,
        instruction_id=st.integers(
            min_value=1,
            max_value=100000,
        ),
        cache_hit=st.booleans(),
    )
    def update_response(
        self,
        uid,
        created,
        output,
        stage,
        error,
        instruction_id,
        cache_hit,
    ):
        self.client.update_response(
            uid,
            created,
            output,
            stage,
            error,
            instruction_id,
            cache_hit,
        )

    # -------------------- JOIN --------------------

    @rule()
    def filtered_join(self):
        result = self.client.filtered_join()
        assert isinstance(result, list)


TestRPC = RPCStateMachine.TestCase