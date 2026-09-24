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
    filename=data.get("filename")
    content = data.get("content", "")
    if not filename:
        return jsonify({"error":"Filename is required"}), 400
    file_path=FILES_DIR / filename
    file_path.write_text(content,encoding="utf-8")
    return jsonify({"message":"File created successfully","filename":filename}),201

#Read
@app.route("/files/<filename>",methods=["GET"])
def get_file(filename):
    file_path=FILES_DIR/filename
    if not file_path.exists():
        return jsonify({"error":"File not Found"}), 404
    content=file_path.read_text(encoding="utf-8")
    return jsonify({"filename":filename,"content":content})

#Delete
@app.route("/files/<filename>",methods=["DELETE"])
def delete_file(filename):
    file_path=FILES_DIR/filename
    if not file_path.exists():
        return jsonify({"error":"File not Found"}), 404
    file_path.unlink()
    return jsonify({"message":"File deleted successfully","filename":filename})


if __name__ == "__main__":
    app.run(debug=True)