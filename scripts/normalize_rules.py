from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE_DIR = ROOT / "rule" / "list"

def normalize_line(line):
    line = line.strip().replace("\ufeff", "")
    if not line:
        return None

    # 去掉逗号后空格
    while ", " in line:
        line = line.replace(", ", ",")

    return line

def process_file(path):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    seen = set()
    result = []

    for line in lines:
        line = normalize_line(line)
        if not line:
            continue

        key = line.lower()
        if key in seen:
            continue

        seen.add(key)
        result.append(line)

    new_content = "\n".join(result) + "\n"
    path.write_text(new_content, encoding="utf-8")

def main():
    for file in RULE_DIR.rglob("*.list"):
        process_file(file)

if __name__ == "__main__":
    main()
