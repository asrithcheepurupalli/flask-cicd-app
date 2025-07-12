import os
import json
from datetime import datetime
import frontmatter
from slugify import slugify

MD_DIR = "posts"
OUT_DIR = "posts"

def convert_all_md_to_json():
    for filename in os.listdir(MD_DIR):
        if filename.endswith(".md"):
            path = os.path.join(MD_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)

            title = post.get("title", "Untitled")
            date_str = post.get("date", datetime.today().strftime("%Y-%m-%d"))

            # Normalize date format if needed
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except:
                date = datetime.today().strftime("%Y-%m-%d")

            content = post.content
            slug = slugify(title)

            post_data = {
                "title": title,
                "slug": slug,
                "date": date,
                "content": content
            }

            json_path = os.path.join(OUT_DIR, f"{slug}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(post_data, f, indent=2)

            print(f"✅ Converted: {filename} → {slug}.json")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    convert_all_md_to_json()
