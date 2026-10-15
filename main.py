import os
import re
import secrets
import sqlite3
from flask import (
    Flask,
    flash,
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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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

    return render_template(
        "index.html",
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
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not all((name, email, subject, message)):
            flash("Please complete every field before submitting.", "error")
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.", "error")
        elif any(len(value) > limit for value, limit in (
            (name, 120),
            (email, 254),
            (subject, 200),
            (message, 5000),
        )):
            flash("One or more fields exceed the allowed length.", "error")
        else:
            conn = sqlite3.connect("database.db")
            try:
                conn.execute(
                    """
                    INSERT INTO contact_messages (name, email, subject, message)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, email, subject, message),
                )
                conn.commit()
            except sqlite3.Error:
                app.logger.exception("Could not save a contact form submission.")
                flash(
                    "We couldn't save your message. Please try again later.",
                    "error",
                )
            else:
                flash("Thank you! Your message has been received.", "success")
                return redirect(url_for("contact"))
            finally:
                conn.close()

        form_data = request.form
    else:
        form_data = {}

    return render_template(
        "contact.html",
        form_data=form_data,
        contact_subject=request.args.get("subject", ""),
    )


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