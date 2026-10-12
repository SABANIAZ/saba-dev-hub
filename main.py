import os
import secrets
import sqlite3
from flask import (
    Flask,
    redirect,
    render_template,
    render_template_string,
    request,
    session,
    url_for,
)

app = Flask(__name__)
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if FLASK_SECRET_KEY:
    app.secret_key = FLASK_SECRET_KEY
else:
    app.secret_key = secrets.token_urlsafe(48)
    app.logger.warning("FLASK_SECRET_KEY is not configured; sessions reset on restart.")

REFERENCE_SNIPPETS = [
    (
        "basics",
        "Basics & Variables",
        "Type Checks and Conversion",
        '''value = "42"
number = int(value)

print(number, type(number))
print(isinstance(number, int))''',
        "Convert common values and check types with isinstance().",
    ),
    (
        "operators",
        "Operators",
        "Arithmetic and Comparison Operators",
        '''total = 17 // 5
remainder = 17 % 5
power = 2 ** 3

is_valid = total == 3 and remainder > 0
print(total, remainder, power, is_valid)''',
        "Use arithmetic, comparison, and logical operators together.",
    ),
    (
        "strings",
        "Strings",
        "String Slicing and Methods",
        '''message = "  learn python  "
clean = message.strip()

print(clean.title())
print(clean[0:5])
print("-".join(clean.split()))''',
        "Trim, transform, slice, and join text with built-in string methods.",
    ),
    (
        "collections",
        "Collections",
        "Lists, Dictionaries, and Sets",
        '''tasks = ["read", "practice"]
tasks.append("build")

profile = {"name": "Saba", "tasks": len(tasks)}
labels = {"python", "beginner", "python"}

print(profile.get("name", "Guest"), tasks[-1], sorted(labels))''',
        "Choose lists for ordered items, dictionaries for key-value data, and sets for unique values.",
    ),
    (
        "comprehensions",
        "Comprehensions",
        "List and Dictionary Comprehensions",
        '''numbers = range(1, 8)
squares = [number ** 2 for number in numbers if number % 2 == 0]
lookup = {number: number ** 2 for number in range(4)}

print(squares)
print(lookup)''',
        "Build lists and dictionaries from iterables with optional conditions.",
    ),
    (
        "functions",
        "Functions & Scope",
        "Flexible Function Arguments",
        '''def make_message(name, *topics, excited=False, **details):
    message = f"Hi {name}: {', '.join(topics)}"
    return message.upper() if excited else message

print(make_message("Sam", "lists", "loops", excited=True))''',
        "Use defaults, *args, and keyword options to make functions reusable.",
    ),
    (
        "functions",
        "Functions & Scope",
        "Iterate with enumerate and zip",
        '''names = ["Ada", "Grace", "Linus"]
scores = [98, 94, 91]

for position, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{position}. {name}: {score}")''',
        "Pair related sequences with zip() and include an index with enumerate().",
    ),
    (
        "functions",
        "Functions & Scope",
        "Generator Functions",
        '''def countdown(start):
    while start > 0:
        yield start
        start -= 1

print(list(countdown(3)))''',
        "Yield values one at a time instead of building a complete list up front.",
    ),
    (
        "oop",
        "Object-Oriented Python",
        "Classes and Inheritance",
        '''class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof"

print(Dog("Milo").speak())''',
        "Define instance data in __init__() and specialize behavior in a subclass.",
    ),
    (
        "exceptions",
        "Exceptions",
        "Handle Specific Exceptions",
        '''raw_value = "12"

try:
    quantity = int(raw_value)
    average = 100 / quantity
except ValueError:
    print("Enter a whole number")
except ZeroDivisionError:
    print("Quantity must not be zero")
else:
    print(f"Average: {average}")''',
        "Catch expected exception types; use else for code that runs after success.",
    ),
    (
        "file_handling",
        "File Handling",
        "Work with Paths Safely",
        '''from pathlib import Path

notes_path = Path("notes.txt")
notes_path.write_text("First line\\n", encoding="utf-8")
notes_path.write_text(
    notes_path.read_text(encoding="utf-8") + "Second line\\n",
    encoding="utf-8",
)

print(notes_path.exists(), notes_path.read_text(encoding="utf-8"))''',
        "Use pathlib.Path for readable file paths and specify text encodings.",
    ),
    (
        "builtins",
        "Built-in Functions",
        "Useful Built-in Functions",
        '''temperatures = [18, 22, 20, 25]

print(len(temperatures), min(temperatures), max(temperatures))
print(sum(temperatures) / len(temperatures))
print(all(temp > 0 for temp in temperatures))
print(sorted(temperatures, reverse=True))''',
        "Combine common built-ins to inspect, aggregate, and sort data.",
    ),
    (
        "regex",
        "Regular Expressions",
        "Find Patterns in Text",
        '''import re

text = "Contact team@example.com or help@example.org"
addresses = re.findall(r"[\\w.+-]+@[\\w.-]+\\.[A-Za-z]{2,}", text)

print(addresses)''',
        "Use re.findall() to collect all matches for a regular expression.",
    ),
    (
        "debugging",
        "Debugging & Logging",
        "Log Useful Runtime Information",
        '''import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
item_count = 3
logging.info("Loaded %d items", item_count)
logging.warning("No configuration file was found")''',
        "Use logging levels and parameterized messages instead of scattered print calls.",
    ),
    (
        "testing",
        "Testing",
        "Write a Small Unit Test",
        '''import unittest

def add(left, right):
    return left + right

class AddTests(unittest.TestCase):
    def test_adds_two_numbers(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()''',
        "Use unittest assertions to check behavior and catch regressions.",
    ),
    (
        "modules",
        "Modules & Data Formats",
        "Encode and Decode JSON",
        '''import json

user = {"name": "Ada", "active": True}
payload = json.dumps(user, indent=2)
restored = json.loads(payload)

print(payload)
print(restored["name"])''',
        "Convert between Python values and JSON text with the standard library.",
    ),
    (
        "decorators",
        "Decorators",
        "Measure a Function Call",
        '''from functools import wraps
from time import perf_counter

def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        result = function(*args, **kwargs)
        print(f"Elapsed: {perf_counter() - started:.6f}s")
        return result
    return wrapper

@timed
def total(values):
    return sum(values)

print(total([1, 2, 3]))''',
        "Wrap a function to add behavior while preserving its metadata.",
    ),
    (
        "typing",
        "Type Hints",
        "Annotate Function Inputs and Outputs",
        '''def average(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)

print(average([2.0, 4.0, 6.0]))''',
        "Use annotations to document expected values; Python does not enforce them at runtime.",
    ),
    (
        "python_idioms",
        "Pythonic Patterns",
        "Sort Records with a Key",
        '''students = [
    {"name": "Mina", "score": 84},
    {"name": "Omar", "score": 92},
]

ranked = sorted(students, key=lambda student: student["score"], reverse=True)
print([student["name"] for student in ranked])''',
        "Pass a key function to sorted() when records need a custom sort order.",
    ),
]


# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            category_name TEXT NOT NULL,
            title TEXT NOT NULL,
            code TEXT NOT NULL,
            desc TEXT NOT NULL
        )
    """
    )
    cursor.execute("SELECT COUNT(*) FROM snippets")
    if cursor.fetchone()[0] == 0:
        default_snippets = [
            (
                "file_handling",
                "File Handling",
                "Reading and Writing Files",
                (
                    '# Writing to a file\nwith open("note.txt", "w") as f:\n'
                    '    f.write("Hello Saba Dev!")\n\n# Reading from a file\nwith'
                    ' open("note.txt", "r") as f:\n    print(f.read())'
                ),
                (
                    "Learn how to create, write, and read files securely using"
                    " Python's built-in with open() context manager."
                ),
            ),
            (
                "basics",
                "Basics & Variables",
                "Variables and Data Types",
                (
                    'name = "Saba Dev"\nage = 25\nprice = 19.99\nis_active ='
                    ' True\nprint(f"Name: {name}, Age: {age}")'
                ),
                (
                    "Learn how to declare variables and understand basic data types"
                    " like integers, floats, strings, and booleans in Python."
                ),
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO snippets (category, category_name, title, code, desc)
            VALUES (?, ?, ?, ?, ?)
        """,
            default_snippets,
        )
        conn.commit()
    cursor.executemany(
        """
        INSERT INTO snippets (category, category_name, title, code, desc)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM snippets WHERE category = ? AND title = ?
        )
        """,
        [
            (*snippet, snippet[0], snippet[2])
            for snippet in REFERENCE_SNIPPETS
        ],
    )
    conn.commit()
    conn.close()


init_db()

pro_resources = [
    {
        "title": "Python Master Cheat Sheet (PDF)",
        "desc": (
            "A comprehensive guide covering advanced syntax, data structures,"
            " and interview questions."
        ),
        "badge": "Coming Soon",
    },
    {
        "title": "Flask Full-Stack Starter Kit",
        "desc": (
            "Ready-to-use boilerplate code for building professional web"
            " applications quickly."
        ),
        "badge": "Free Resource",
    },
]


# --- HOME ROUTE ---
@app.route("/home")
@app.route("/home/")
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM snippets ORDER BY id DESC")
    cheatsheets = cursor.fetchall()

    cursor.execute(
        "SELECT DISTINCT category, category_name FROM snippets ORDER BY id"
    )
    categories = cursor.fetchall()
    conn.close()

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saba Dev - Ultimate Python Cheat Sheet & Snippet Hub</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='site.css') }}">
        <style>
            :root {
                --bg-color: #0d1117;
                --card-bg: #161b22;
                --border-color: #30363d;
                --text-main: #c9d1d9;
                --accent-blue: #58a6ff;
                --accent-green: #7ee787;
                --accent-purple: #bc8cff;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-main);
                margin: 0;
                padding: 30px;
            }
            .container { max-width: 900px; margin: 0 auto; }
            header {
                display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
                gap: 12px; margin-bottom: 25px; text-align: left;
            }
            .brand { flex: 1 1 280px; }
            .header-nav {
                display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
                justify-content: flex-end; flex: 1 1 300px;
            }
            .admin-link {
                background: #21262d; color: var(--accent-blue);
                border: 1px solid var(--border-color); padding: 8px 14px;
                border-radius: 6px; text-decoration: none; font-size: 0.85em;
                white-space: nowrap;
            }
            .admin-link:hover { background: #30363d; }
            @media (max-width: 620px) {
                header { justify-content: center; text-align: center; }
                .brand, .header-nav { flex-basis: 100%; }
                .header-nav { justify-content: center; }
            }
            h1 { color: var(--accent-blue); font-size: 2.5em; margin-bottom: 10px; }
            .tagline { color: #8b949e; font-size: 1.1em; }
            .controls-container { display: flex; flex-direction: column; gap: 15px; margin-bottom: 35px; align-items: center; }
            #searchInput {
                width: 100%; max-width: 500px; padding: 12px 20px;
                background: #161b22; border: 1px solid var(--border-color);
                border-radius: 8px; color: white; font-size: 1em; outline: none;
            }
            #searchInput:focus { border-color: var(--accent-blue); }
            .filter-buttons { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
            .filter-btn {
                background: #21262d; color: var(--text-main); border: 1px solid var(--border-color);
                padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.9em; transition: 0.2s;
            }
            .filter-btn:hover, .filter-btn.active { background: var(--accent-blue); color: white; border-color: var(--accent-blue); }
            .card {
                background: var(--card-bg); border: 1px solid var(--border-color);
                border-radius: 10px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            .category-badge {
                background: #1f6feb; color: white; padding: 4px 10px;
                font-size: 0.85em; border-radius: 20px; text-transform: uppercase; font-weight: bold;
            }
            h2 { color: #f0f6fc; margin-top: 15px; }
            .code-header {
                display: flex; justify-content: space-between; align-items: center;
                background: #21262d; padding: 5px 15px; border-top-left-radius: 6px;
                border-top-right-radius: 6px; border: 1px solid #30363d; border-bottom: none;
                font-size: 0.85em; color: #8b949e;
            }
            .copy-btn {
                background: #30363d; color: #c9d1d9; border: none; padding: 4px 10px;
                border-radius: 4px; cursor: pointer; font-size: 0.85em;
            }
            .copy-btn:hover { background: #484f58; color: white; }
            pre {
                background: #010409; margin-top: 0; padding: 15px; border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px; color: var(--accent-green); overflow-x: auto;
                font-family: 'Courier New', Courier, monospace; font-size: 0.95em; border: 1px solid #30363d;
            }
            .pro-section-title { color: var(--accent-purple); margin-top: 40px; margin-bottom: 20px; font-size: 1.8em; text-align: center; }
            .pro-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .pro-card { background: linear-gradient(135deg, #161b22, #1f1a24); border: 1px solid #3b2352; border-radius: 10px; padding: 20px; position: relative; }
            .pro-badge { background: #8957e5; color: white; padding: 3px 10px; font-size: 0.75em; border-radius: 20px; text-transform: uppercase; font-weight: bold; }
            .download-btn {
                display: inline-block; background: #8957e5; color: white; padding: 8px 16px;
                border-radius: 6px; text-decoration: none; font-size: 0.9em; font-weight: bold; margin-top: 15px;
            }
            .download-btn:hover { background: #986ee2; }
            .site-footer {
                border-top: 1px solid var(--border-color); margin-top: 45px;
                padding: 20px 0; display: flex; justify-content: center;
                flex-wrap: wrap; gap: 22px; font-size: 0.9em;
            }
            .site-footer a { color: #8b949e; text-decoration: none; }
            .site-footer a:hover { color: var(--accent-blue); }
            .quick-actions {
                display: flex; flex-wrap: wrap; justify-content: center;
                align-items: center; gap: 10px;
            }
            .tool-btn {
                background: #21262d; color: var(--text-main);
                border: 1px solid var(--border-color); padding: 8px 14px;
                border-radius: 6px; cursor: pointer; font-size: 0.9em;
            }
            .tool-btn:hover, .tool-btn[aria-pressed="true"] {
                background: #30363d; border-color: var(--accent-blue);
            }
            .results-count { color: #8b949e; font-size: 0.9em; margin: 18px 0; }
            .empty-state {
                padding: 24px; border: 1px dashed var(--border-color);
                border-radius: 8px; color: #8b949e; text-align: center;
            }
            .save-btn {
                background: transparent; color: #c9d1d9; border: 1px solid #484f58;
                padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.85em;
            }
            .save-btn[aria-pressed="true"] {
                color: #f2cc60; border-color: #9e6a03;
            }
            .quiz-panel {
                max-width: 700px; margin: 0 auto 30px; padding: 22px;
                background: #161b22; border: 1px solid var(--border-color);
                border-top: 3px solid var(--accent-green); border-radius: 8px;
            }
            .quiz-panel h2 { margin: 0 0 8px; color: #f0f6fc; font-size: 1.25em; }
            .quiz-progress, .quiz-feedback { color: #8b949e; }
            .quiz-question { color: #f0f6fc; font-weight: 600; }
            .quiz-options { display: grid; gap: 8px; margin: 16px 0; }
            .quiz-option {
                display: flex; align-items: flex-start; gap: 10px; padding: 11px 12px;
                background: #0d1117; border: 1px solid var(--border-color); border-radius: 6px;
                cursor: pointer;
            }
            .quiz-option:has(input:checked) { border-color: var(--accent-blue); }
            .quiz-feedback { min-height: 1.5em; }
            .quiz-feedback.correct { color: var(--accent-green); }
            .quiz-feedback.incorrect { color: #ff7b72; }
            .quiz-controls { display: flex; flex-wrap: wrap; gap: 10px; }
            .quiz-controls button { background: #21262d; color: var(--text-main); }
            .quiz-controls .check-answer { background: #238636; color: white; border-color: #2ea043; }
            @media print {
                body { background: white; color: #111; padding: 0; }
                header, .controls-container, #quizPanel, .pro-section-title, .pro-grid,
                .site-footer, .copy-btn, .save-btn { display: none !important; }
                .container { max-width: none; }
                .card { background: white; color: #111; border-color: #bbb; box-shadow: none; break-inside: avoid; }
                h2, .card h2 { color: #111; }
                pre { color: #111; background: #f4f4f4; white-space: pre-wrap; }
                .category-badge { background: #ddd; color: #111; }
            }
            .container { max-width: 1080px; }
            header {
                gap: 24px; margin-bottom: 34px; padding: 24px 28px;
                border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 22px;
                background: linear-gradient(135deg, rgba(18, 31, 49, 0.9), rgba(12, 19, 31, 0.74));
                box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22); backdrop-filter: blur(18px);
            }
            h1 {
                margin-top: 0; color: #eaf6ff; font-size: clamp(2rem, 5vw, 3.1rem);
                letter-spacing: -0.05em; line-height: 1.12;
            }
            .tagline { max-width: 600px; line-height: 1.7; }
            .admin-link {
                padding: 9px 14px; border-color: rgba(148, 163, 184, 0.2);
                border-radius: 12px; background: rgba(15, 27, 43, 0.72);
                color: #c4eaff; font-weight: 600;
            }
            .admin-link:hover { background: rgba(37, 89, 120, 0.36); border-color: rgba(114, 199, 255, 0.55); }
            .home-hero {
                position: relative; overflow: hidden; margin: 0 0 28px; padding: clamp(26px, 5vw, 48px);
                border: 1px solid rgba(114, 199, 255, 0.22); border-radius: 24px;
                background: linear-gradient(120deg, rgba(21, 49, 69, 0.9), rgba(29, 28, 57, 0.78));
                box-shadow: 0 28px 80px rgba(0, 0, 0, 0.24); backdrop-filter: blur(18px);
            }
            .home-hero::after {
                position: absolute; top: -100px; right: -70px; width: 300px; height: 300px;
                border: 1px solid rgba(150, 219, 255, 0.12); border-radius: 50%;
                box-shadow: 0 0 0 35px rgba(150, 219, 255, 0.025), 0 0 0 70px rgba(150, 219, 255, 0.02);
                content: ""; pointer-events: none;
            }
            .hero-eyebrow {
                margin: 0 0 10px; color: #8cebd0; font-size: 0.78rem;
                font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase;
            }
            .hero-snake {
                position: absolute; top: 50%; right: clamp(24px, 7vw, 82px);
                color: #a6f2d7; font-size: clamp(4rem, 9vw, 7rem); line-height: 1;
                filter: drop-shadow(0 14px 28px rgba(120, 230, 192, 0.22));
                opacity: 0.92; transform: translateY(-50%) rotate(-12deg);
                animation: snake-float 5s ease-in-out infinite;
                pointer-events: none;
            }
            @keyframes snake-float {
                0%, 100% { transform: translateY(-50%) rotate(-12deg); }
                50% { transform: translateY(calc(-50% - 10px)) rotate(-5deg); }
            }
            .home-hero h2 {
                max-width: 660px; margin: 0 0 12px; color: #f2f8ff;
                font-size: clamp(1.7rem, 4vw, 2.5rem); letter-spacing: -0.04em; line-height: 1.2;
            }
            .home-hero > p:last-of-type { max-width: 650px; margin: 0; color: #bdcde0; }
            .hero-stats { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
            .hero-stats span {
                padding: 7px 12px; border: 1px solid rgba(180, 219, 244, 0.16);
                border-radius: 999px; background: rgba(8, 17, 29, 0.32); color: #d9efff;
                font-size: 0.83rem;
            }
            .controls-container {
                padding: 20px; border: 1px solid var(--border-color); border-radius: 18px;
                background: rgba(14, 23, 36, 0.8); box-shadow: 0 18px 44px rgba(0, 0, 0, 0.18);
                backdrop-filter: blur(14px);
            }
            #searchInput {
                max-width: 680px; min-height: 50px; border-radius: 13px;
                background: rgba(6, 12, 21, 0.86);
            }
            .filter-btn, .tool-btn, .copy-btn, .save-btn, .download-btn {
                border-radius: 10px; transition: transform 160ms ease, border-color 160ms ease, background-color 160ms ease;
            }
            .filter-btn:hover, .tool-btn:hover, .copy-btn:hover, .download-btn:hover { transform: translateY(-1px); }
            .filter-btn { padding: 8px 14px; }
            .filter-btn.active { box-shadow: 0 6px 22px rgba(88, 166, 255, 0.2); }
            .card, .quiz-panel {
                border-color: rgba(148, 163, 184, 0.18); border-radius: 18px;
                background: rgba(17, 26, 40, 0.86); box-shadow: 0 18px 48px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(14px);
            }
            .card { padding: clamp(18px, 3vw, 28px); }
            .card h2 { margin-bottom: 8px; letter-spacing: -0.025em; }
            .card > p { color: #aab9cb; line-height: 1.65; }
            .category-badge { display: inline-flex; padding: 5px 11px; border-radius: 999px; font-size: 0.75em; letter-spacing: 0.04em; }
            .code-header { min-height: 46px; border-radius: 11px 11px 0 0; }
            .code-header + pre { padding: 18px; border-radius: 0 0 11px 11px; line-height: 1.65; }
            .pro-section-title { color: #d5b8ff; letter-spacing: -0.035em; }
            .pro-card {
                padding: 24px; border-color: rgba(188, 140, 255, 0.24); border-radius: 18px;
                background: linear-gradient(145deg, rgba(30, 28, 49, 0.92), rgba(17, 26, 40, 0.9));
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.2);
            }
            .site-footer { border-color: rgba(148, 163, 184, 0.16); }
            .site-footer a { padding: 6px 10px; border-radius: 8px; }
            .site-footer a:hover { background: rgba(114, 199, 255, 0.08); }
            @media (max-width: 620px) {
                body { padding: 16px; }
                header { padding: 20px 16px; }
                .controls-container { padding: 14px; }
                .hero-snake { top: 22px; right: 20px; font-size: 2.6rem; opacity: 0.58; transform: none; }
            }
            @media (prefers-reduced-motion: reduce) {
                .hero-snake { animation: none; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="brand">
                    <h1><span aria-hidden="true">🐍</span> Saba Dev's Python Hub</h1>
                    <p class="tagline">Your ultimate lifetime destination for Python Cheat Sheets, Code Snippets, and Developer Resources.</p>
                </div>
                <nav class="header-nav" aria-label="Main navigation">
                    <a href="/contact" class="admin-link">Contact Us</a>
                    <a href="/about" class="admin-link">About Us</a>
                    <a href="/privacy" class="admin-link">Privacy Policy</a>
                    <a href="/admin" class="admin-link">⚙️ Admin Panel</a>
                </nav>
            </header>

            <section class="home-hero" aria-labelledby="homeHeroTitle">
                <span class="hero-snake" aria-hidden="true">🐍</span>
                <p class="hero-eyebrow">A practical Python reference</p>
                <h2 id="homeHeroTitle">Less searching. More building.</h2>
                <p>Find clear, copy-ready examples for everyday Python, then save the snippets you want to revisit.</p>
                <div class="hero-stats" aria-label="Hub contents">
                    <span>{{ sheets | length }} practical snippets</span>
                    <span>{{ categories | length }} topics to explore</span>
                    <span>Free learning tools</span>
                </div>
            </section>

            <div class="controls-container">
                <input type="search" id="searchInput" placeholder="Search topics, examples, or code..." aria-label="Search Python topics and code" oninput="filterSnippets()">
                <div class="filter-buttons">
                    <button id="allTopicsBtn" class="filter-btn active" onclick="filterCategory('all', this)">All Topics</button>
                    {% for cat in categories %}
                    <button class="filter-btn" onclick="filterCategory('{{ cat.category }}', this)">{{ cat.category_name }}</button>
                    {% endfor %}
                </div>
                <div class="quick-actions" aria-label="Reference tools">
                    <button id="savedFilterBtn" class="tool-btn" type="button" aria-pressed="false" onclick="filterSaved(this)">Saved (0)</button>
                    <button id="quizToggle" class="tool-btn" type="button" aria-expanded="false" aria-controls="quizPanel" onclick="toggleQuiz()">Practice Quiz</button>
                    <button class="tool-btn" type="button" onclick="window.print()">Print / Save PDF</button>
                </div>
            </div>

            <section id="quizPanel" class="quiz-panel" hidden aria-labelledby="quizTitle">
                <h2 id="quizTitle">Python Quick Check</h2>
                <p id="quizProgress" class="quiz-progress"></p>
                <p id="quizQuestion" class="quiz-question"></p>
                <div id="quizOptions" class="quiz-options" role="radiogroup" aria-labelledby="quizQuestion"></div>
                <p id="quizFeedback" class="quiz-feedback" role="status" aria-live="polite"></p>
                <div class="quiz-controls">
                    <button id="quizCheck" class="tool-btn check-answer" type="button" onclick="checkQuizAnswer()">Check Answer</button>
                    <button id="quizNext" class="tool-btn" type="button" onclick="advanceQuiz()" hidden>Next Question</button>
                </div>
            </section>

            <p id="resultsCount" class="results-count" aria-live="polite"></p>
            <div id="snippetList">
                {% for item in sheets %}
                <div class="card snippet-card" data-id="{{ item.id }}" data-category="{{ item.category }}" data-search="{{ item.title | lower }} {{ item.desc | lower }} {{ item.category_name | lower }} {{ item.code | lower }}">
                    <span class="category-badge">{{ item.category_name }}</span>
                    <h2>{{ item.title }}</h2>
                    <p>{{ item.desc }}</p>
                    <div class="code-header">
                        <span>Python</span>
                        <div class="code-actions">
                            <button class="save-btn" type="button" data-save-id="{{ item.id }}" aria-pressed="false" onclick="toggleSaved(this)">Save</button>
                            <button class="copy-btn" type="button" onclick="copyCode(this)">Copy Code</button>
                        </div>
                    </div>
                    <pre><code>{{ item.code }}</code></pre>
                </div>
                {% endfor %}
            </div>
            <p id="noResults" class="empty-state" hidden>No matching snippets. Try another search or topic.</p>

            <h2 class="pro-section-title">🚀 Saba Dev Pro Resources</h2>
            <div class="pro-grid">
                {% for res in resources %}
                <div class="pro-card">
                    <span class="pro-badge">{{ res.badge }}</span>
                    <h3 style="color: #f0f6fc; margin: 12px 0 8px 0;">{{ res.title }}</h3>
                    <p style="font-size: 0.9em; color: #8b949e;">{{ res.desc }}</p>
                    <a href="#" class="download-btn">Access Resource</a>
                </div>
                {% endfor %}
            </div>
        </div>

        <footer class="site-footer" aria-label="Footer navigation">
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy Policy</a>
        </footer>

        <script>
            let currentCategory = 'all';
            let savedOnly = false;
            const savedStorageKey = 'saba-python-hub-saved-snippets';
            let savedSnippetIds = new Set();
            try {
                savedSnippetIds = new Set(JSON.parse(localStorage.getItem(savedStorageKey) || '[]'));
            } catch (error) {
                savedSnippetIds = new Set();
            }

            const quizQuestions = [
                {
                    question: 'What values does list(range(3)) produce?',
                    options: ['[1, 2, 3]', '[0, 1, 2]', '[0, 1, 2, 3]'],
                    answer: 1,
                    explanation: 'range(3) starts at 0 and stops before 3.'
                },
                {
                    question: 'Which expression safely reads a missing dictionary key with a fallback?',
                    options: ['profile["city"]', 'profile.get("city", "Unknown")', 'profile.city'],
                    answer: 1,
                    explanation: 'dict.get(key, default) returns the fallback when the key is absent.'
                },
                {
                    question: 'Which keyword skips to the next loop iteration?',
                    options: ['break', 'return', 'continue'],
                    answer: 2,
                    explanation: 'continue skips the rest of the current iteration.'
                },
                {
                    question: 'What does a with statement help manage when opening a file?',
                    options: ['Automatic file cleanup', 'The file name extension', 'The file contents format'],
                    answer: 0,
                    explanation: 'A with block closes the file when the block exits.'
                },
                {
                    question: 'Which built-in creates a new sorted list without changing the original?',
                    options: ['list.sort()', 'sorted()', 'order()'],
                    answer: 1,
                    explanation: 'sorted(iterable) returns a new list; list.sort() changes a list in place.'
                }
            ];
            let quizIndex = 0;
            let quizScore = 0;
            let quizComplete = false;

            function setActiveFilter(btn) {
                for (let button of document.getElementsByClassName('filter-btn')) {
                    button.classList.remove('active');
                }
                btn.classList.add('active');
            }

            function filterCategory(category, btn) {
                currentCategory = category;
                savedOnly = false;
                document.getElementById('savedFilterBtn').setAttribute('aria-pressed', 'false');
                setActiveFilter(btn);
                applyFilters();
            }

            function filterSaved(btn) {
                savedOnly = !savedOnly;
                currentCategory = 'all';
                btn.setAttribute('aria-pressed', String(savedOnly));
                setActiveFilter(savedOnly ? btn : document.getElementById('allTopicsBtn'));
                applyFilters();
            }

            function applyFilters() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let cards = document.getElementsByClassName('snippet-card');
                let visibleCount = 0;
                for (let i = 0; i < cards.length; i++) {
                    let cardCategory = cards[i].getAttribute('data-category');
                    let searchText = cards[i].getAttribute('data-search');
                    let snippetId = cards[i].getAttribute('data-id');
                    let matchesCategory = (currentCategory === 'all' || cardCategory === currentCategory);
                    let matchesSearch = searchText.includes(input);
                    let matchesSaved = !savedOnly || savedSnippetIds.has(snippetId);
                    if (matchesCategory && matchesSearch && matchesSaved) {
                        cards[i].style.display = "";
                        visibleCount += 1;
                    } else {
                        cards[i].style.display = "none";
                    }
                }
                document.getElementById('resultsCount').textContent =
                    `${visibleCount} ${visibleCount === 1 ? 'snippet' : 'snippets'}`;
                document.getElementById('noResults').hidden = visibleCount !== 0;
            }

            function filterSnippets() { applyFilters(); }

            function updateSavedControls() {
                document.getElementById('savedFilterBtn').textContent = `Saved (${savedSnippetIds.size})`;
                for (let button of document.querySelectorAll('.save-btn')) {
                    const isSaved = savedSnippetIds.has(button.dataset.saveId);
                    button.textContent = isSaved ? 'Saved' : 'Save';
                    button.setAttribute('aria-pressed', String(isSaved));
                }
            }

            function toggleSaved(btn) {
                const snippetId = btn.dataset.saveId;
                if (savedSnippetIds.has(snippetId)) {
                    savedSnippetIds.delete(snippetId);
                } else {
                    savedSnippetIds.add(snippetId);
                }
                try {
                    localStorage.setItem(savedStorageKey, JSON.stringify([...savedSnippetIds]));
                } catch (error) {
                    // Keep the current page usable if browser storage is unavailable.
                }
                updateSavedControls();
                applyFilters();
            }

            function toggleQuiz() {
                const panel = document.getElementById('quizPanel');
                const toggle = document.getElementById('quizToggle');
                panel.hidden = !panel.hidden;
                toggle.setAttribute('aria-expanded', String(!panel.hidden));
                if (!panel.hidden) {
                    renderQuizQuestion();
                    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            }

            function renderQuizQuestion() {
                const question = quizQuestions[quizIndex];
                const options = document.getElementById('quizOptions');
                document.getElementById('quizProgress').textContent =
                    `Question ${quizIndex + 1} of ${quizQuestions.length} | Score ${quizScore}`;
                document.getElementById('quizQuestion').textContent = question.question;
                document.getElementById('quizFeedback').textContent = '';
                document.getElementById('quizFeedback').className = 'quiz-feedback';
                document.getElementById('quizCheck').hidden = false;
                document.getElementById('quizNext').hidden = true;
                options.replaceChildren();
                question.options.forEach((text, index) => {
                    const label = document.createElement('label');
                    const radio = document.createElement('input');
                    radio.type = 'radio';
                    radio.name = 'quick-quiz-answer';
                    radio.value = String(index);
                    label.className = 'quiz-option';
                    label.append(radio, document.createTextNode(text));
                    options.append(label);
                });
            }

            function checkQuizAnswer() {
                const selected = document.querySelector('input[name="quick-quiz-answer"]:checked');
                const feedback = document.getElementById('quizFeedback');
                if (!selected) {
                    feedback.textContent = 'Choose an answer first.';
                    return;
                }
                const correct = Number(selected.value) === quizQuestions[quizIndex].answer;
                if (correct) quizScore += 1;
                for (let option of document.querySelectorAll('input[name="quick-quiz-answer"]')) {
                    option.disabled = true;
                }
                feedback.textContent = `${correct ? 'Correct.' : 'Not quite.'} ${quizQuestions[quizIndex].explanation}`;
                feedback.classList.add(correct ? 'correct' : 'incorrect');
                document.getElementById('quizCheck').hidden = true;
                const next = document.getElementById('quizNext');
                next.textContent = quizIndex === quizQuestions.length - 1 ? 'Finish Quiz' : 'Next Question';
                next.hidden = false;
            }

            function advanceQuiz() {
                if (quizComplete) {
                    quizComplete = false;
                    quizIndex = 0;
                    quizScore = 0;
                    renderQuizQuestion();
                    return;
                }
                if (quizIndex === quizQuestions.length - 1) {
                    quizComplete = true;
                    document.getElementById('quizProgress').textContent = `Final score: ${quizScore} / ${quizQuestions.length}`;
                    document.getElementById('quizQuestion').textContent = 'Quick check complete';
                    document.getElementById('quizOptions').replaceChildren();
                    document.getElementById('quizFeedback').textContent = 'Review a topic above, or take the quiz again.';
                    document.getElementById('quizNext').textContent = 'Try Again';
                    return;
                }
                quizIndex += 1;
                renderQuizQuestion();
            }

            async function copyCode(btn) {
                let preTag = btn.parentElement.nextElementSibling;
                try {
                    await navigator.clipboard.writeText(preTag.innerText);
                    btn.innerText = "Copied! ✅";
                    setTimeout(() => { btn.innerText = "Copy Code"; }, 2000);
                } catch (error) {
                    btn.innerText = "Select Code";
                    setTimeout(() => { btn.innerText = "Copy Code"; }, 2000);
                }
            }

            updateSavedControls();
            applyFilters();
        </script>
    </body>
    </html>
    """
    return render_template_string(
        html_template,
        sheets=cheatsheets,
        resources=pro_resources,
        categories=categories,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    msg_sent = False
    if request.method == "POST":
        msg_sent = True
    return render_template("contact.html", msg_sent=msg_sent)


# --- LOGIN ROUTE ---
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username") or ""
        password = request.form.get("password") or ""
        if not (FLASK_SECRET_KEY and ADMIN_USERNAME and ADMIN_PASSWORD):
            error = "Admin login is not configured on this server."
        elif (
            secrets.compare_digest(username, ADMIN_USERNAME)
            and secrets.compare_digest(password, ADMIN_PASSWORD)
        ):
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error = "Invalid Username or Password!"

    login_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saba Dev - Admin Login</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='site.css') }}">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
            .login-card { background: rgba(17, 26, 40, 0.88); padding: 32px; border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 20px; width: min(100%, 390px); box-shadow: 0 28px 80px rgba(0,0,0,0.35); backdrop-filter: blur(18px); }
            h2 { color: #58a6ff; margin-top: 0; text-align: center; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input { width: 100%; padding: 10px; background: #010409; border: 1px solid #30363d; border-radius: 6px; color: white; box-sizing: border-box; }
            .btn { width: 100%; background: #238636; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
            .btn:hover { background: #2ea043; }
            .error { color: #f85149; font-size: 0.9em; text-align: center; margin-bottom: 10px; }
            .back-link { display: block; text-align: center; margin-top: 15px; color: #58a6ff; text-decoration: none; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>🔐 Admin Login</h2>
            {% if error %}<p class="error">{{ error }}</p>{% endif %}
            <form method="POST">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required placeholder="Admin username" autocomplete="username">
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required placeholder="Admin password" autocomplete="current-password">
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <a href="/" class="back-link">← Back to Website</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(login_template, error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    message = ""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        if "delete_id" in request.form:
            snippet_id = request.form.get("delete_id")
            cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
            conn.commit()
            message = "Snippet deleted successfully! 🗑️"
        else:
            category = request.form.get("category")
            category_name = request.form.get("category_name")
            title = request.form.get("title")
            code = request.form.get("code")
            desc = request.form.get("desc")

            if category and title and code:
                cursor.execute(
                    """
                    INSERT INTO snippets (category, category_name, title, code, desc)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (category, category_name, title, code, desc),
                )
                conn.commit()
                message = "Snippet successfully added! 🎉"

    cursor.execute("SELECT * FROM snippets ORDER BY id DESC")
    snippets = cursor.fetchall()
    conn.close()

    admin_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saba Dev - Admin Dashboard</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='site.css') }}">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; padding: clamp(16px, 4vw, 40px); }
            .container { width: min(100%, 1000px); margin: 0 auto; background: rgba(17, 26, 40, 0.88); padding: clamp(20px, 4vw, 36px); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 20px; box-shadow: 0 28px 80px rgba(0,0,0,0.3); backdrop-filter: blur(18px); }
            h2, h3 { color: #58a6ff; }
            .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 6px; font-weight: bold; color: #f0f6fc; }
            input, textarea { width: 100%; padding: 10px; background: #010409; border: 1px solid #30363d; border-radius: 6px; color: white; font-size: 1em; box-sizing: border-box; }
            textarea { height: 90px; font-family: monospace; }
            .btn { background: #238636; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            .btn:hover { background: #2ea043; }
            .delete-btn { background: #da3633; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 0.85em; }
            .delete-btn:hover { background: #f85149; }
            .edit-btn { background: #1f6feb; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 0.85em; text-decoration: none; display: inline-block; margin-right: 5px; }
            .edit-btn:hover { background: #388bfd; }
            .logout-btn { background: #21262d; color: #f85149; border: 1px solid #30363d; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 0.9em; }
            .logout-btn:hover { background: #30363d; }
            .back-link { color: #58a6ff; text-decoration: none; }
            .msg { color: #7ee787; margin-bottom: 15px; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th, td { border: 1px solid #30363d; padding: 12px; text-align: left; font-size: 0.9em; }
            th { background: #21262d; color: #f0f6fc; }
            hr { border: 0; border-top: 1px solid #30363d; margin: 25px 0; }
            input, textarea { min-height: 44px; border-radius: 10px; }
            textarea { min-height: 100px; }
            .btn, .delete-btn, .edit-btn, .logout-btn { border-radius: 9px; }
            @media (max-width: 640px) {
                .top-bar { gap: 12px; }
                table { display: block; overflow-x: auto; white-space: nowrap; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <a href="/" class="back-link">Back to Website</a>
                <a href="/logout" class="logout-btn">Logout</a>
            </div>
            <h2>Admin Dashboard</h2>
            {% if message %}<p class="msg">{{ message }}</p>{% endif %}

            <h3>Add New Python Snippet</h3>
            <form method="POST">
                <div class="form-group">
                    <label>Category Key (e.g. basics, file_handling):</label>
                    <input type="text" name="category" required placeholder="basics">
                </div>
                <div class="form-group">
                    <label>Category Display Name (e.g. Basics & Variables):</label>
                    <input type="text" name="category_name" required placeholder="Basics & Variables">
                </div>
                <div class="form-group">
                    <label>Snippet Title:</label>
                    <input type="text" name="title" required placeholder="Variables and Data Types">
                </div>
                <div class="form-group">
                    <label>Short Description:</label>
                    <input type="text" name="desc" placeholder="Brief professional description">
                </div>
                <div class="form-group">
                    <label>Python Code:</label>
                    <textarea name="code" required placeholder="print('Hello')"></textarea>
                </div>
                <button type="submit" class="btn">Save Snippet to Database</button>
            </form>

            <hr>

            <h3>Manage Existing Snippets</h3>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in snippets %}
                    <tr>
                        <td>{{ s.title }}</td>
                        <td>{{ s.category_name }}</td>
                        <td>
                            <a href="/edit/{{ s.id }}" class="edit-btn">Edit</a>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="delete_id" value="{{ s.id }}">
                                <button type="submit" class="delete-btn" onclick="return confirm('Are you sure you want to delete this snippet?');">Delete</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(admin_template, message=message, snippets=snippets)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_snippet(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        category = request.form.get("category")
        category_name = request.form.get("category_name")
        title = request.form.get("title")
        code = request.form.get("code")
        desc = request.form.get("desc")

        cursor.execute(
            """
            UPDATE snippets
            SET category = ?, category_name = ?, title = ?, code = ?, desc = ?
            WHERE id = ?
        """,
            (category, category_name, title, code, desc, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin"))

    cursor.execute("SELECT * FROM snippets WHERE id = ?", (id,))
    snippet = cursor.fetchone()
    conn.close()

    edit_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saba Dev - Edit Snippet</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='site.css') }}">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; padding: clamp(16px, 4vw, 40px); }
            .container { width: min(100%, 640px); margin: 0 auto; background: rgba(17, 26, 40, 0.88); padding: clamp(20px, 4vw, 36px); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 20px; box-shadow: 0 28px 80px rgba(0,0,0,0.3); backdrop-filter: blur(18px); }
            h2 { color: #58a6ff; margin-top: 0; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 6px; font-weight: bold; color: #f0f6fc; }
            input, textarea { width: 100%; padding: 10px; background: #010409; border: 1px solid #30363d; border-radius: 6px; color: white; font-size: 1em; box-sizing: border-box; }
            input { min-height: 44px; }
            textarea { min-height: 150px; font-family: monospace; }
            .btn { background: #1f6feb; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            .btn:hover { background: #388bfd; }
            .back-link { display: inline-block; margin-bottom: 20px; color: #58a6ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/admin" class="back-link">Back to Dashboard</a>
            <h2>Edit Snippet</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Category Key:</label>
                    <input type="text" name="category" value="{{ snippet.category }}" required>
                </div>
                <div class="form-group">
                    <label>Category Display Name:</label>
                    <input type="text" name="category_name" value="{{ snippet.category_name }}" required>
                </div>
                <div class="form-group">
                    <label>Snippet Title:</label>
                    <input type="text" name="title" value="{{ snippet.title }}" required>
                </div>
                <div class="form-group">
                    <label>Short Description:</label>
                    <input type="text" name="desc" value="{{ snippet.desc }}">
                </div>
                <div class="form-group">
                    <label>Python Code:</label>
                    <textarea name="code" required>{{ snippet.code }}</textarea>
                </div>
                <button type="submit" class="btn">Update Snippet</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(edit_template, snippet=snippet)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)