# Static Site Generator

This project is a Python-based static site generator that converts markdown files into HTML pages. It processes markdown content from a specified directory, applies a template, and outputs the generated HTML files into a public directory, while also copying static files.

## Project Structure

```graphql
STATIC-SITE-GENERATOR/
│
├── content/              # Markdown content files
├── public/               # Generated site (output)
├── src/                  # Source code
│   ├── copystatic.py     # Copies static files to public directory
│   ├── gencontent.py     # Generates HTML files from markdown
│   ├── htmlnode.py       # HTML node processing (utilities)
│   ├── inline_markdown.py# Inline markdown processing
│   ├── main.py           # Main script to run the site generator
│   ├── markdown_blocks.py# Markdown blocks processing
│   ├── textnode.py       # Text node processing
│   ├── test_*.py         # Test files
├── static/               # Static files (CSS, JS, images, etc.)
├── .gitignore            # Git ignore file
├── main.sh               # Shell script to run the generator
├── README.md             # Project documentation
├── template.html         # HTML template for generating pages
└── test.sh               # Shell script for testing
```

## Setup and Usage:

1. Clone the repository:
2. Add your content:
- Place your markdown (.md) files in the content directory. The generator will process these files and create corresponding HTML files in the public directory.
3. Add your static files:
- Place any static files (CSS, JS, images, etc.) in the static directory. These will be copied to the public directory as-is.
4. Set execute permission on your script using chmod command:
```
chmod +x main.sh
```
5. Run the generator:
```sh
./main.sh
```
6. View the generated site:
- Open your browser and navigate to `http://localhost:8888`.

## How it works:

The main.sh script performs the following steps:

1. Run the Python script to generate the site:
```sh
python3 src/main.py
```
2. Serve the generated site using Python's built-in HTTP server:
```sh
cd public && python3 -m http.server 8888
```
