"""Progress tracking — stores lesson completion and stars."""

import json
from datetime import datetime, timezone
from pathlib import Path


class Progress:
    """Manages lesson progress stored in a JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".git-learn" / "progress.json"
        self._data: dict = {"lessons": {}}
        if self.path.exists():
            self._data = json.loads(self.path.read_text())

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))

    def get_lesson(self, slug: str) -> dict | None:
        return self._data["lessons"].get(slug)

    def complete_lesson(self, slug: str, stars: int, hints_used: int) -> None:
        existing = self._data["lessons"].get(slug)
        if existing and existing["stars"] >= stars:
            existing["attempts"] = existing.get("attempts", 1) + 1
            self._save()
            return
        self._data["lessons"][slug] = {
            "completed": True,
            "stars": stars,
            "hints_used": hints_used,
            "attempts": (existing["attempts"] + 1) if existing else 1,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()

    @property
    def total_stars(self) -> int:
        return sum(l["stars"] for l in self._data["lessons"].values())

    @property
    def lessons_completed(self) -> int:
        return len(self._data["lessons"])

    def reset(self) -> None:
        self._data = {"lessons": {}}
        self._save()
