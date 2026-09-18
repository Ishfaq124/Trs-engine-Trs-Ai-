from aurelith.models import Evidence
from aurelith.self_model import SelfModel
from aurelith.store import Store


def test_high_stability_claim_moves_slowly(tmp_path):
    model = SelfModel(Store(str(tmp_path / "test.db")))
    before = model.claims["identity"].confidence

    evidence = Evidence(
        id="e1",
        text="single weak contradictory observation",
        weight=0.3,
        source="test",
    )

    after = model.apply_evidence(
        "identity",
        evidence,
        supports=False,
    ).confidence

    assert after < before
    assert before - after < 0.03
