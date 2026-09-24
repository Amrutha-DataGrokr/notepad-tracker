from flask import Flask, jsonify, render_template, request
from pathlib import Path
import subprocess

app = Flask(__name__)


def git(path, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=path, capture_output=True, text=True
    )


def commit_file(path):
    repository = git(path.parent, "rev-parse", "--show-toplevel")
    if repository.returncode != 0:
        git(path.parent, "init")
        repository = git(path.parent, "rev-parse", "--show-toplevel")

    root = Path(repository.stdout.strip()).resolve()
    relative_path = path.resolve().relative_to(root)
    git(root, "add", "-f", str(relative_path))

    if git(root, "diff", "--cached", "--quiet").returncode == 0:
        return "unchanged"

    result = git(
        root,
        "-c", "user.name=Notepad Tracker",
        "-c", "user.email=notepad-tracker@localhost",
        "commit", "-m", f"Update {path.name}",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "Could not commit file")

    return git(root, "rev-parse", "--short", "HEAD").stdout.strip()


@app.route("/")
def home():
    return render_template("editor.html")


@app.route("/files", methods=["POST"])
def save_file():
    data = request.get_json()
    path = Path(data["path"]).expanduser()

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data.get("content", ""), encoding="utf-8")
        revision = commit_file(path)
    except (OSError, RuntimeError) as error:
        return jsonify({"error": str(error)}), 500

    return jsonify({
        "message": "File saved and committed",
        "path": str(path),
        "revision": revision,
    })


@app.route("/files", methods=["GET"])
def get_file():
    data = request.get_json() 
    path = Path(data["path"]).expanduser()

    if not path.is_file():
        return jsonify({"error": "File not found"}), 404

    return jsonify({
        "path": str(path),
        "content": path.read_text(encoding="utf-8"),
    })


@app.route("/files", methods=["DELETE"])
def delete_file():
    data = request.get_json()
    path = Path(data["path"]).expanduser()

    if not path.is_file():
        return jsonify({"error": "File not found"}), 404

    path.unlink()
    return jsonify({"message": "File deleted", "path": str(path)})


@app.route("/files/list", methods=["GET"])
def list_files():
    directory = Path(request.args["directory"]).expanduser()

    return jsonify({
        "directory": str(directory),
        "files": [str(path) for path in directory.iterdir() if path.is_file()],
    })


if __name__ == "__main__":
    app.run(debug=True)