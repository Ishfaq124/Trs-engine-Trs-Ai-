from .models import WorkspaceItem


class GlobalWorkspace:
    def __init__(self, capacity: int = 7):
        if capacity < 1:
            raise ValueError("workspace capacity must be >= 1")
        self.capacity = capacity

    def select(self, candidates: list[WorkspaceItem]):
        return sorted(candidates, key=lambda x: x.priority, reverse=True)[:self.capacity]
