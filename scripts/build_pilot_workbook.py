from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / "pilot_data" / "first_pilot_run"
OUTPUT_FILE = SOURCE_DIR / "final_pilot_workbook.xlsx"

SHEETS = [
    ("supervisors", SOURCE_DIR / "final_supervisors_list.csv"),
    ("residents", SOURCE_DIR / "final_residents_list.csv"),
    ("supervision_links", SOURCE_DIR / "final_supervision_links.csv"),
    ("training_programs", SOURCE_DIR / "final_training_programs.csv"),
    ("resident_training_records", SOURCE_DIR / "final_resident_training_records.csv"),
]


def read_csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [row for row in csv.reader(handle)]


def main() -> None:
    workbook = Workbook()
    first_sheet = True

    for title, csv_path in SHEETS:
        rows = read_csv_rows(csv_path)
        if first_sheet:
            sheet = workbook.active
            sheet.title = title
            first_sheet = False
        else:
            sheet = workbook.create_sheet(title=title)

        for row in rows:
            sheet.append(row)

    workbook.save(OUTPUT_FILE)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
