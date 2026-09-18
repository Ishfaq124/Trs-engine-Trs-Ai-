from aurelith.models import WorkspaceItem
from aurelith.workspace import GlobalWorkspace


def test_workspace_is_bounded():
    w = GlobalWorkspace(capacity=2)
    items = [
        WorkspaceItem(id="a", kind="x", content="a", relevance=0.2),
        WorkspaceItem(id="b", kind="x", content="b", relevance=1.0),
        WorkspaceItem(id="c", kind="x", content="c", relevance=0.7),
    ]

    chosen = w.select(items)
    assert len(chosen) == 2
    assert chosen[0].id == "b"
