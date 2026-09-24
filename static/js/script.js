let saveTimer;

const filePathInput = document.getElementById("filePath");
const editor = document.getElementById("editor");
const status = document.getElementById("status");
const openFileButton = document.getElementById("openFile");
const saveFileButton = document.getElementById("saveFile");
const deleteFileButton = document.getElementById("deleteFile");

async function loadFile() {
    const path = filePathInput.value;

    if (!path) {
        alert("Enter a file path");
        return;
    }

    const response = await fetch(`/files?path=${encodeURIComponent(path)}`);
    const data = await response.json();

    if (!response.ok) {
        status.textContent = data.error;
        return;
    }

    editor.value = data.content;
    status.textContent = "File loaded";
}

async function saveFile() {
    const path = filePathInput.value;

    if (!path) {
        alert("Enter a file path");
        return;
    }

    const response = await fetch("/files", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            path: path,
            content: editor.value
        })
    });

    const data = await response.json();
    status.textContent = data.message || data.error;
}

async function deleteFile() {
    const path = filePathInput.value;

    if (!path) {
        alert("Enter a file path");
        return;
    }

    if (!confirm("Delete this file?")) {
        return;
    }

    const response = await fetch("/files", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({path: path})
    });

    const data = await response.json();
    status.textContent = data.message || data.error;

    if (response.ok) {
        editor.value = "";
    }
}

openFileButton.addEventListener("click", loadFile);
saveFileButton.addEventListener("click", saveFile);
deleteFileButton.addEventListener("click", deleteFile);

function startNewFile() {
    clearTimeout(saveTimer);
    editor.value = "";
    status.textContent = "New file";
}

filePathInput.addEventListener("focus", startNewFile);
filePathInput.addEventListener("input", startNewFile);

editor.addEventListener("input", () => {
    clearTimeout(saveTimer);
    status.textContent = "Unsaved changes";
    saveTimer = setTimeout(saveFile, 1000);
});