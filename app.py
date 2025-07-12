import os
import json
from flask import Flask, render_template, request, redirect, url_for, abort, Response
from datetime import datetime
from slugify import slugify
import markdown

app = Flask(__name__)
POSTS_DIR = "posts"

# ---------- Utilities ----------
def get_post_path(slug):
    return os.path.join(POSTS_DIR, f"{slug}.json")

def load_post(slug):
    path = get_post_path(slug)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        post = json.load(f)
    # Parse date from string to datetime
    if isinstance(post.get("date"), str):
        try:
            post["date"] = datetime.strptime(post["date"], "%Y-%m-%d")
        except ValueError:
            post["date"] = datetime.min
    return post

def list_posts():
    posts = []
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".json"):
            with open(os.path.join(POSTS_DIR, file), "r") as f:
                post = json.load(f)
                if isinstance(post.get("date"), str):
                    try:
                        post["date"] = datetime.strptime(post["date"], "%Y-%m-%d")
                    except ValueError:
                        post["date"] = datetime.min
                    post["preview"] = " ".join(post["content"].split()[:40])
                    posts.append(post)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

def save_post(post):
    slug = post["slug"]
    with open(get_post_path(slug), "w") as f:
        json.dump(post, f, indent=2, default=str)

def delete_post(slug):
    path = get_post_path(slug)
    if os.path.exists(path):
        os.remove(path)

# ---------- Routes ----------
@app.route("/")
def index():
    posts = list_posts()
    return render_template("index.html", posts=posts)

@app.route("/post/<slug>")
def post(slug):
    post = load_post(slug)
    if not post:
        abort(404)
    post["content"] = markdown.markdown(post["content"])
    return render_template("post.html", post=post)

@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date_str = request.form.get("date", datetime.today().strftime("%Y-%m-%d"))
        slug = slugify(title)
        post = {
            "title": title,
            "content": content,
            "date": date_str,
            "slug": slug
        }
        save_post(post)
        return redirect(url_for("post", slug=slug))
    return render_template("new.html")

@app.route("/edit/<slug>", methods=["GET", "POST"])
def edit_post(slug):
    post = load_post(slug)
    if not post:
        abort(404)

    if request.method == "POST":
        post["title"] = request.form["title"]
        post["content"] = request.form["content"]
        post["date"] = request.form.get("date", datetime.today().strftime("%Y-%m-%d"))
        save_post(post)
        return redirect(url_for("post", slug=slug))

    return render_template("edit.html", post=post)


@app.route("/delete/<slug>")
def delete(slug):
    post_path = os.path.join(POSTS_DIR, f"{slug}.json")
    if os.path.exists(post_path):
        os.remove(post_path)
    return redirect(url_for("index"))


@app.route("/rss.xml")
def rss():
    posts = list_posts()
    rss_items = ""
    for post in posts:
        date_str = post["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")
        rss_items += f"""
        <item>
            <title>{post['title']}</title>
            <link>{request.url_root}post/{post['slug']}</link>
            <description>{post['content'][:100]}</description>
            <pubDate>{date_str}</pubDate>
        </item>
        """
    rss_feed = f"""<?xml version="1.0"?>
    <rss version="2.0">
        <channel>
            <title>Asrith's Blog</title>
            <link>{request.url_root}</link>
            <description>Personal blog posts by Asrith Cheepurupalli</description>
            {rss_items}
        </channel>
    </rss>"""
    return Response(rss_feed, mimetype="application/rss+xml")

# ---------- Main ----------
if __name__ == "__main__":
    os.makedirs(POSTS_DIR, exist_ok=True)
    app.run(debug=True)
