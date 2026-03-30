import re


def parse_rym_text(raw_text: str) -> list[dict]:
    albums = []
    lines = raw_text.strip().splitlines()

    for line in lines:
        if not line.strip():
            continue
        # Skip headers
        if line.strip().lower().startswith("artist"):
            continue
        if "'s music" in line.lower():
            continue

        # Split by tab
        parts = line.split("\t")

        if len(parts) < 3:
            parts = re.split(r'\s{2,}', line.strip())

        if len(parts) < 3:
            continue

        artist = parts[0].strip()
        title = parts[1].strip()
        rating_str = parts[2].strip()

        try:
            rating = float(rating_str)
        except ValueError:
            continue

        if artist and title:
            albums.append({
                "artist": artist,
                "title": title,
                "rating": rating,
            })

    return albums