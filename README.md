# Notepad Tracker

A simple Flask web application for creating, editing, saving, and deleting text files. Every saved change is tracked with Git.

## Features

- Write notes in a basic text editor
- Create or update files in any directory
- Automatically save changes after you stop typing
- Commit saved changes to Git
- Open and delete files
- List files in a directory through the API

## Requirements

- Python 3
- Flask
- Git

## Setup

Create and activate the virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install Flask:

```powershell
pip install flask
```

## Run

Start the application:

```powershell
python app.py
```

Open the editor at:

```text
http://127.0.0.1:5000
```

Enter a file path, write content, and click **Save File**. The file is created or updated, then committed to Git.

## API

### Save a file

`POST /files`

```json
{
  "path": "C:\\Assignments\\Python\\notepad-tracker\\files\\notes.txt",
  "content": "My note"
}
```

### Read a file

`GET /files`

```json
{
  "path": "C:\\Assignments\\Python\\notepad-tracker\\files\\notes.txt"
}
```

### Delete a file

`DELETE /files`

```json
{
  "path": "C:\\Assignments\\Python\\notepad-tracker\\files\\notes.txt"
}
```

### List files

`GET /files/list?directory=files`

## Project Structure

```text
notepad-tracker/
├── app.py
├── files/
├── static/
│   ├── css/styles.css
│   └── js/script.js
└── templates/
    └── editor.html
```

## Git Tracking

When a file is saved, the application initializes a Git repository in its directory if necessary, stages the file, and creates a commit using a message such as:

```text
Update notes.txt
```