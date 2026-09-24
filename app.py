from flask import Flask, jsonify, request
from pathlib import Path

app = Flask(__name__)
FILES_DIR=Path("files")


@app.route("/")
def home():
    return "Notepad Tracker is running."

#Create or Update
@app.route("/files",methods=["POST"])
def create_file():
    data=request.get_json()
    file_path =data.get("path")
    content = data.get("content", "")

    if not file_path:
        return jsonify({"error":"File path is required"}), 400
    
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return jsonify({"message": "File saved successfully","path": str(path)}), 201

#Read
@app.route("/files",methods=["GET"])
def get_file():
    data=request.get_json()

    if not data or not data.get("path"):
        return jsonify({"error": "File path is required"}), 400

    path = Path(data["path"])

    if not path.exists():
        return jsonify({"error": "File not found"}), 404
    
    if not path.is_file():
        return jsonify({"error": "Path is not a file"}), 400
    
    content=path.read_text(encoding="utf-8")
    return jsonify({"path": str(path),"content": content})

#Delete
@app.route("/files", methods=["DELETE"])
def delete_file():
    data = request.get_json()

    if not data or not data.get("path"):
        return jsonify({"error": "File path is required"}), 400

    path = Path(data["path"])

    if not path.exists():
        return jsonify({"error": "File not found"}), 404

    if not path.is_file():
        return jsonify({"error": "Path is not a file"}), 400

    path.unlink()
    return jsonify({"message": "File deleted successfully","path": str(path)})

@app.route("/files/list", methods=["GET"])
def list_files():
    data = request.get_json()

    if not data or not data.get("directory"):
        return jsonify({"error": "Directory path is required"}), 400

    directory = Path(data["directory"])

    if not directory.exists():
        return jsonify({"error": "Directory not found"}), 404

    if not directory.is_dir():
        return jsonify({"error": "Path is not a directory"}), 400

    files = [str(path) for path in directory.iterdir() if path.is_file()]

    return jsonify({"directory": str(directory),"files": files})

if __name__ == "__main__":
    app.run(debug=True)