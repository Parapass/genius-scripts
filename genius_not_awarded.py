import csv
import sys
import os

def find_not_awarded(csv_path):
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row.get("Lyrics Status", "").strip().lower()
            if status != "not awarded":
                continue
            tags = row.get("Tags", "")
            if "non-music" in tags.lower():
                continue
            rows.append({
                "artist": row["Primary Artist"],
                "title":  row["Song Title"],
                "url":    row["URL"],
            })

    if not rows:
        print("no not awarded transcriptions found")
        return

    rows.sort(key=lambda r: r["artist"])

    lines = [f'{r["artist"]} - ["{r["title"]}"]({r["url"]})' for r in rows]
    output = "\n".join(lines)

    print(f"{len(rows)} not awarded transcriptions:\n")
    print(output)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(csv_path))[0] + "_not_awarded.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\nsaved to: {out_path}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python genius_not_awarded.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"error: file not found: {csv_path}")
        sys.exit(1)

    find_not_awarded(csv_path)
