import os
import random
import json
from flask import Flask, render_template, request, redirect, flash, session

from rym_parser import parse_rym_text

app = Flask(__name__)
app.secret_key = "rym-shuffler-secret"

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def cache_path(username):
    return os.path.join(CACHE_DIR, f"{username}.json")


def save_collection(username, albums):
    with open(cache_path(username), "w") as f:
        json.dump(albums, f)


def load_collection(username):
    path = cache_path(username)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


@app.route("/")
def index():
    # This ONLY renders the input form — no album variable needed
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse():
    username = request.form.get("username", "").strip() or "anonymous"
    raw_text = request.form.get("collection_text", "").strip()

    if not raw_text:
        flash("Please paste your collection text")
        return redirect("/")

    albums = parse_rym_text(raw_text)

    if not albums:
        flash("Could not parse any albums. Make sure you copied the full page.")
        return redirect("/")

    save_collection(username, albums)
    session["username"] = username

    pick = random.choice(albums)
    return render_template("result.html", album=pick, total=len(albums), username=username)


@app.route("/shuffle", methods=["POST"])
def shuffle():
    username = session.get("username", "")
    albums = load_collection(username)

    if not albums:
        flash("No collection found. Please paste again.")
        return redirect("/")

    min_rating = request.form.get("min_rating")
    filtered = albums
    if min_rating:
        try:
            filtered = [a for a in albums if a["rating"] >= float(min_rating)]
        except ValueError:
            pass

    if not filtered:
        flash("No albums match that filter, showing from all.")
        filtered = albums

    pick = random.choice(filtered)
    return render_template("result.html", album=pick, total=len(filtered), username=username)


if __name__ == "__main__":
    app.run(debug=True, port=5000)