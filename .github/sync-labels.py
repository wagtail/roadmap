#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# ///

import json
import subprocess
from pathlib import Path

labels_path = Path(__file__).parent / "labels.json"
data = json.loads(labels_path.read_text())

existing_labels = {
    l["name"]
    for l in json.loads(
        subprocess.run(
            ["gh", "label", "list", "--json", "name", "--limit", "999"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
}

for label in data["labels"]:
    action = "create" if label["name"] not in existing_labels else "edit"
    subprocess.run(
        [
            "gh",
            "label",
            action,
            label["name"],
            "--color",
            label["color"],
            "--description",
            label["description"],
        ],
        check=True,
    )
