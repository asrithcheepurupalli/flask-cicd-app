# Flask Blog with CI/CD

A minimal personal blog app built using Flask, Markdown, and GitHub Actions CI/CD pipeline. Designed to be clean, readable, and fully editable.

## Features

- Write, edit, and delete blog posts in Markdown
- Post previews and tag-based filtering
- RSS feed for readers
- SimpleMDE Markdown editor integration
- Dark mode toggle and responsive UI
- GitHub Actions for automatic testing and deployment
- Posts stored as JSON files

## Folder Structure

```
flask-cicd-app/
├── app.py
├── templates/
│   ├── index.html
│   ├── post.html
│   ├── new.html
│   └── edit.html
├── static/
│   ├── style.css
│   └── dark-toggle.js
├── posts/
│   └── example.json
├── .github/workflows/
│   └── deploy.yml
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repo

```bash
git clone https://github.com/asrithcheepurupalli/flask-cicd-app.git
cd flask-cicd-app
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run locally

```bash
python app.py
```

Visit `http://127.0.0.1:5000` to access the blog.

## Deployment

This project includes a `deploy.yml` GitHub Actions workflow. You can configure it to:

- Run tests (if added)
- Deploy to AWS S3 or other services

## Requirements

- Python 3.x
- Flask
- markdown
- feedgen

Install with:

```bash
pip install flask markdown feedgen
```

## Author

Built by Asrith Cheepurupalli — [asrithcheepurupalli.codes](https://asrithcheepurupalli.codes)
"""
