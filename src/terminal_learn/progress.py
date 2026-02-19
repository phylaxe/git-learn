"""Progress tracking — stores lesson completion and stars."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROGRESS_DIR = Path.home() / ".terminal-learn"


class Progress:
    """Manages lesson progress stored in a JSON file, keyed by module."""

    def __init__(self, path: Path | None = None, module: str = "git") -> None:
        self.path = path or PROGRESS_DIR / "progress.json"
        self._module = module
        self._data: dict = {}
        if self.path.exists():
            self._data = json.loads(self.path.read_text())
        # Ensure module section exists
        if self._module not in self._data:
            self._data[self._module] = {"lessons": {}}
        # Backward compat: if top-level has "lessons" key, migrate to "git" module
        if "lessons" in self._data and self._module == "git":
            if not self._data["git"]["lessons"]:
                self._data["git"]["lessons"] = self._data.pop("lessons")
            else:
                self._data.pop("lessons", None)

    @property
    def _lessons(self) -> dict:
        return self._data[self._module]["lessons"]

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))

    def get_lesson(self, slug: str) -> dict | None:
        return self._lessons.get(slug)

    def complete_lesson(self, slug: str, stars: int, hints_used: int) -> None:
        existing = self._lessons.get(slug)
        if existing and existing["stars"] >= stars:
            existing["attempts"] = existing.get("attempts", 1) + 1
            self._save()
            return
        self._lessons[slug] = {
            "completed": True,
            "stars": stars,
            "hints_used": hints_used,
            "attempts": (existing["attempts"] + 1) if existing else 1,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()

    @property
    def total_stars(self) -> int:
        return sum(l["stars"] for l in self._lessons.values())

    @property
    def lessons_completed(self) -> int:
        return len(self._lessons)

    def reset(self) -> None:
        self._data[self._module] = {"lessons": {}}
        self._save()
