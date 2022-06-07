"""
The commit SHA before I first ran this tool: dc560a63feb8f656f7fc9c78d46a49ad98681211
If you need to get the original fixtures back. You can check out that commit and grab them.
-Todd
"""

import json

LINEBREAK = "\r\n"
NOTE_FILE_TO_PK = {
    "./default_narrative_note.txt": 1,
    "./default_stability_plan.txt": 2,
    "./allina_narrative_note.txt": 3,
    "./providence_narrative_note.txt": 4,
    "./st_patricks_narrative_note.txt": 5,
    "./allina_stability_plan.txt": 6,
    "./swedish_edmonds_narrative_note.txt": 7,
}
FIXTURE_FILES = [
    "../jaspr_media.json",
    "../jaspr_content.json"
]


def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        content = LINEBREAK.join(content.splitlines())
        return content


def read_json(fp):
    with open(fp, "r") as f:
        items = json.load(f)
        return items


def write_json(fp, content):
    with open(fp, "w", newline="\n") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def update_fixtures(pk, content):
    for fp in FIXTURE_FILES:
        items = read_json(fp)
        for item in items:
            if item["model"] == "kiosk.notetemplate" and item["pk"] == pk:
                item["fields"]["template"] = content
                break
        write_json(fp, items)


def main():
    for fp, pk in NOTE_FILE_TO_PK.items():
        result = process_file(fp)
        update_fixtures(pk, result)


if __name__ == "__main__":
    main()
