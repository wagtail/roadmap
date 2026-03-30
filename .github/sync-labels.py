#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# ///

import json
import subprocess
from pathlib import Path

labels_path = Path(__file__).parent / "labels.json"
data = json.loads(labels_path.read_text())

for label in data["labels"]:
    subprocess.run(
        [
            "gh",
            "label",
            "edit",
            label["name"],
            "--color",
            label["color"],
            "--description",
            label["description"],
        ],
        check=True,
    )
