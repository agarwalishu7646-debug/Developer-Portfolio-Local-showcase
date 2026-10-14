from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "projects.json"

default_projects = [
    {
        "name": "Library Management System",
        "description": "Manage books, issue books and record book returns.",
        "technology": "HTML, CSS, JavaScript"
    },
    {
        "name": "Developer Portfolio",
        "description": "A personal website to showcase projects and skills.",
        "technology": "Python, Flask, HTML, CSS"
    },
    {
        "name": "Attendance and Fee Reminder System",
        "description": "Manage student attendance and fee reminders.",
        "technology": "Python, Flask"
    }
]


def load_projects():
    if not os.path.exists(DATA_FILE):
        return default_projects.copy()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            projects = json.load(file)

        if isinstance(projects, list):
            return projects

        return default_projects.copy()

    except (json.JSONDecodeError, OSError):
        return default_projects.copy()


def save_projects(projects):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(projects, file, indent=4, ensure_ascii=False)


@app.route("/")
def home():
    projects = load_projects()
    return render_template("index.html", projects=projects)


@app.route("/add-project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        technology = request.form.get("technology", "").strip()

        if name and description and technology:
            projects = load_projects()

            projects.append({
                "name": name,
                "description": description,
                "technology": technology
            })

            save_projects(projects)
            return redirect("/")

        return "Please fill in all fields.", 400

    return render_template("add_project.html")


@app.route("/edit-project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    projects = load_projects()

    if project_id < 0 or project_id >= len(projects):
        return "Project not found.", 404

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        technology = request.form.get("technology", "").strip()

        if name and description and technology:
            projects[project_id] = {
                "name": name,
                "description": description,
                "technology": technology
            }

            save_projects(projects)
            return redirect("/")

        return "Please fill in all fields.", 400

    project = projects[project_id]

    return render_template(
        "edit_project.html",
        project=project,
        project_id=project_id
    )


@app.route("/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    projects = load_projects()

    if project_id < 0 or project_id >= len(projects):
        return "Project not found.", 404

    projects.pop(project_id)
    save_projects(projects)

    return redirect("/")


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "Please fill in all fields.", 400

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Submitted</title>
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Thank You!</h1>
        <p>Your message has been submitted successfully.</p>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5001)