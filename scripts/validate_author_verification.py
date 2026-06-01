from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_IDS = {"AV1", "AV2", "AV3", "AV4", "AV5", "AV6", "AV7"}
REQUIRED_FIELDS = {
    "topic",
    "manuscript_location",
    "required_input",
    "author_confirmed_value",
    "source_record_checked",
}
TODO_VALUES = {"", "TODO", "TBD", "NA", "N/A"}


def is_todo(value: object) -> bool:
    return str(value).strip().upper() in TODO_VALUES


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate author-confirmed manuscript finalization values."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("data/author_verification_template.json"),
        help="Path to author verification JSON.",
    )
    parser.add_argument(
        "--allow-todo",
        action="store_true",
        help="Allow TODO values when validating the public template.",
    )
    args = parser.parse_args()

    data = json.loads(args.path.read_text(encoding="utf-8"))
    items = data.get("items", {})
    ids = set(items)
    if ids != REQUIRED_IDS:
        missing = sorted(REQUIRED_IDS - ids)
        extra = sorted(ids - REQUIRED_IDS)
        raise SystemExit(f"Author verification IDs mismatch. missing={missing}, extra={extra}")

    todo_items: list[str] = []
    for item_id, item in items.items():
        missing_fields = REQUIRED_FIELDS - set(item)
        if missing_fields:
            raise SystemExit(f"{item_id} missing fields: {sorted(missing_fields)}")
        if is_todo(item["author_confirmed_value"]) or is_todo(item["source_record_checked"]):
            todo_items.append(item_id)

    if todo_items and not args.allow_todo:
        raise SystemExit(
            "Author verification incomplete for: "
            + ", ".join(todo_items)
            + ". Fill author_confirmed_value and source_record_checked, or rerun with --allow-todo for template checks."
        )

    if todo_items:
        print(f"Author verification template OK; TODO remains for {', '.join(todo_items)}")
    else:
        print("Author verification complete")


if __name__ == "__main__":
    main()
