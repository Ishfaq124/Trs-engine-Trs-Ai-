from aurelith.engine import Aurelith


def test_trs_lineage(tmp_path):
    agent = Aurelith(str(tmp_path / "test.db"))
    agent.reasoner.api_key = ""

    agent.chat("first observation")
    first = agent.state()

    agent.chat("second observation")
    second = agent.state()

    assert second["parent_state_id"] == first["id"]
    assert second["cycle"] == first["cycle"] + 1
