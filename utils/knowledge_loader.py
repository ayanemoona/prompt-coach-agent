from __future__ import annotations

import json
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
KNOWLEDGE_INDEX = KNOWLEDGE_DIR / "index.json"


def load_knowledge(element_name: str) -> str:
    file_name = find_knowledge_file(element_name)
    if file_name is None:
        return ""

    knowledge_path = KNOWLEDGE_DIR / file_name
    return knowledge_path.read_text(encoding="utf-8")


def find_knowledge_file(element_name: str) -> str | None:
    index = load_knowledge_index()

    for principle in index.get("principles", []):
        if principle.get("key") == element_name:
            return principle.get("file")

    return None


def load_knowledge_index() -> dict:
    index_text = KNOWLEDGE_INDEX.read_text(encoding="utf-8")
    return json.loads(index_text)
