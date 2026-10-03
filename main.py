import sqlite3
from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "saba_dev_super_secret_key"


# --- DATABASE SETUP ---
def init_db():
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            category_name TEXT NOT NULL,
            title TEXT NOT NULL,
            code TEXT NOT NULL,
            desc TEXT NOT NULL
        )
    """)
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
            header { text-align: center; margin-bottom: 25px; position: relative; }
            .admin-link {
                position: absolute; top: 0; right: 0;
                background: #21262d; color: var(--accent-blue);
                border: 1px solid var(--border-color); padding: 6px 12px;
                border-radius: 6px; text-decoration: none; font-size: 0.85em;
            }
            .admin-link:hover { background: #30363d; }
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
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <a href="/admin" class="admin-link">⚙️ Admin Panel</a>
                <h1>🐍 Saba Dev's Python Hub</h1>
                <p class="tagline">Your ultimate lifetime destination for Python Cheat Sheets, Code Snippets, and Developer Resources.</p>
            </header>

            <div class="controls-container">
                <input type="text" id="searchInput" placeholder="Search Python topics or code snippets..." onkeyup="filterSnippets()">
                <div class="filter-buttons">
                    <button class="filter-btn active" onclick="filterCategory('all', this)">All Topics</button>
                    {% for cat in categories %}
                    <button class="filter-btn" onclick="filterCategory('{{ cat.category }}', this)">{{ cat.category_name }}</button>
                    {% endfor %}
                </div>
            </div>

            <div id="snippetList">
                {% for item in sheets %}
                <div class="card snippet-card" data-category="{{ item.category }}" data-search="{{ item.title | lower }} {{ item.desc | lower }} {{ item.category_name | lower }}">
                    <span class="category-badge">{{ item.category_name }}</span>
                    <h2>{{ item.title }}</h2>
                    <p>{{ item.desc }}</p>
                    <div class="code-header">
                        <span>Python</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copy Code</button>
                    </div>
                    <pre><code>{{ item.code }}</code></pre>
                </div>
                {% endfor %}
            </div>

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

        <script>
            let currentCategory = 'all';
            function filterCategory(category, btn) {
                currentCategory = category;
                let buttons = document.getElementsByClassName('filter-btn');
                for (let b of buttons) { b.classList.remove('active'); }
                btn.classList.add('active');
                applyFilters();
            }
            function applyFilters() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let cards = document.getElementsByClassName('snippet-card');
                for (let i = 0; i < cards.length; i++) {
                    let cardCategory = cards[i].getAttribute('data-category');
                    let searchText = cards[i].getAttribute('data-search');
                    let matchesCategory = (currentCategory === 'all' || cardCategory === currentCategory);
                    let matchesSearch = searchText.includes(input);
                    if (matchesCategory && matchesSearch) {
                        cards[i].style.display = "";
                    } else {
                        cards[i].style.display = "none";
                    }
                }
            }
            function filterSnippets() { applyFilters(); }
            function copyCode(btn) {
                let preTag = btn.parentElement.nextElementSibling;
                navigator.clipboard.writeText(preTag.innerText).then(() => {
                    btn.innerText = "Copied! ✅";
                    setTimeout(() => { btn.innerText = "Copy Code"; }, 2000);
                });
            }
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


# --- LOGIN ROUTE ---
@app.route("/login", methods=["GET", "POST"])
def login():
  error = ""
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    # Default Admin Credentials
    if username == "saba" and password == "saba123":
      session["logged_in"] = True
      return redirect(url_for("admin"))
    else:
      error = "Invalid Username or Password!"

  login_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Saba Dev - Admin Login</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-card { background: #161b22; padding: 30px; border: 1px solid #30363d; border-radius: 10px; width: 350px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
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
                    <input type="text" name="username" required placeholder="saba">
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required placeholder="saba123">
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <a href="/" class="back-link">← Back to Website</a>
        </div>
    </body>
    </html>
    """
  return render_template_string(login_template, error=error)


# --- LOGOUT ROUTE ---
@app.route("/logout")
def logout():
  session.pop("logged_in", None)
  return redirect(url_for("login"))


# --- ADMIN DASHBOARD ROUTE ---
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
        <title>Saba Dev - Admin Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 40px; }
            .container { max-width: 850px; margin: 0 auto; background: #161b22; padding: 30px; border: 1px solid #30363d; border-radius: 10px; }
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
            th, td { border: 1px solid #30363d; padding: 10px; text-align: left; font-size: 0.9em; }
            th { background: #21262d; color: #f0f6fc; }
            hr { border: 0; border-top: 1px solid #30363d; margin: 25px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <a href="/" class="back-link">← Back to Website</a>
                <a href="/logout" class="logout-btn">Logout 🚪</a>
            </div>
            <h2>⚙️ Admin Dashboard</h2>
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


# --- EDIT SNIPPET ROUTE ---
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
        <title>Saba Dev - Edit Snippet</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 40px; }
            .container { max-width: 600px; margin: 0 auto; background: #161b22; padding: 30px; border: 1px solid #30363d; border-radius: 10px; }
            h2 { color: #58a6ff; margin-top: 0; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 6px; font-weight: bold; color: #f0f6fc; }
            input, textarea { width: 100%; padding: 10px; background: #010409; border: 1px solid #30363d; border-radius: 6px; color: white; font-size: 1em; box-sizing: border-box; }
            textarea { height: 120px; font-family: monospace; }
            .btn { background: #1f6feb; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            .btn:hover { background: #388bfd; }
            .back-link { display: inline-block; margin-bottom: 20px; color: #58a6ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/admin" class="back-link">← Back to Dashboard</a>
            <h2>✏️ Edit Snippet</h2>
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


import os

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)