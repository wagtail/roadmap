#!/usr/bin/env bash
set -euo pipefail

jq -c '.labels[]' "labels.json" | while read -r l; do
  name=$(jq -r .name <<<"$l")
  color=$(jq -r .color <<<"$l")
  desc=$(jq -r .description <<<"$l")
  gh label edit "$name" --color "$color" --description "$desc"
done
