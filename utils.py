from pathlib import Path
import json

FILE_PATH = Path("data.json")


def load_data() -> dict:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
