import csv
import sys
import os

# --- config ---
MIN_VIEWS = 5000
ALLOWED_STATUSES = {"transcribed", "completed"}

TIERS = [
    (1_000_000, "1M+"),
    (500_000,   "500K+"),
    (250_000,   "250K+"),
    (100_000,   "100K+"),
    (50_000,    "50K+"),
    (25_000,    "25K+"),
    (10_000,    "10K+"),
    (5_000,     "5K+"),
    (1_000,     "1K+"),
    (0,         "< 1K"),
]

def format_views(v):
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M+"
    elif v >= 1_000:
        return f"{v // 1000}K+"
    return str(v)

def get_tier(views):
    for threshold, label in TIERS:
        if views >= threshold:
            return label
    return "< 1K"

def generate_list(csv_path, min_views=MIN_VIEWS):
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row.get("Lyrics Status", "").strip().lower()
            if status not in ALLOWED_STATUSES:
                continue
            try:
                pv = int(row["Pageviews"])
            except (ValueError, KeyError):
                continue
            if pv < min_views:
                continue
            rows.append({
                "artist": row["Primary Artist"],
                "title":  row["Song Title"],
                "url":    row["URL"],
                "views":  pv,
            })

    if not rows:
        print(f"no songs found with {min_views}+ pageviews and an allowed lyrics status")
        return

    rows.sort(key=lambda r: r["views"], reverse=True)

    lines = []
    current_tier = None

    for row in rows:
        tier = get_tier(row["views"])
        if tier != current_tier:
            lines.append(f"\n<h3>{tier}</h3>")
            current_tier = tier
        lines.append(f'{row["artist"]} - ["{row["title"]}"]({row["url"]}) - {format_views(row["views"])}')

    output = "\n".join(lines).strip()
    print(output)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.splitext(os.path.basename(csv_path))[0] + "_pageview_list.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\nsaved to: {out_path}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python genius_pageview_list.py <path_to_csv> [min_views]")
        print("example: python genius_pageview_list.py songs.csv 5000")
        sys.exit(1)

    csv_path = sys.argv[1]
    min_views = int(sys.argv[2]) if len(sys.argv) > 2 else MIN_VIEWS

    if not os.path.exists(csv_path):
        print(f"error: file not found: {csv_path}")
        sys.exit(1)

    generate_list(csv_path, min_views)
