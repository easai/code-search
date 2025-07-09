# Natural Language Code Retriever

This system accepts natural language queries and intelligently retrieves relevant code snippets from GitHub. It leverages AI-powered keyword extraction (using `yake`) to distill the intent behind each query and match it with high-quality code examples.

---

## Features

- Accepts natural language queries
- Uses YAKE for keyword extraction
- Searches GitHub for matching code snippets
- Outputs snippet previews or repository links
- Fully managed with Poetry for dependency handling

---

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/) installed

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/code-retriever.git
cd code-retriever
poetry install
```

---

## Usage

Launch the application with:

```bash
    poetry run python app.py
```

Example input:
```text
    > How do I handle JSON responses in JavaScript?
```

The app will:

1. Extract meaningful keywords using YAKE (e.g. "JSON responses", "JavaScript")
2. Search GitHub repositories for relevant snippets
3. Return curated results in your terminal or app interface


## Architecture Overview

```text
[ Natural Language Input ]
           ↓
[ YAKE Keyword Extraction ]
           ↓
[ GitHub API Search ]
           ↓
[ Code Snippet Retrieval ]
           ↓
[ Display Output to User ]
```