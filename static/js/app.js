// =========================
// HELPERS
// =========================
function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
}

// =========================
// SIDEBAR
// =========================
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.toggle('show');
}

function setActiveSidebarLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.toggle(
            'active',
            link.getAttribute('href') === currentPath
        );
    });
}

// =========================
// NOTEPAD (EDITOR)
// =========================
const noteArea = document.getElementById('note');

// Load draft note
if (noteArea) {
    noteArea.value = localStorage.getItem('myNote') || '';
    autoResize(noteArea);

    noteArea.addEventListener('input', () => {
        localStorage.setItem('myNote', noteArea.value);
        autoResize(noteArea);
    });
}

function saveNote() {
    if (!noteArea) return;

    const text = noteArea.value.trim();
    if (!text) {
        showToast("Note is empty", "warning");
        return;
    }

    fetch("/note&do/note/add", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `note=${encodeURIComponent(text)}`
    })
    .then(res => res.json())
    .then(() => {
        localStorage.removeItem('myNote');
        showToast("Note saved successfully", "success");
        setTimeout(() => {
            window.location.href = "/note&do/notes";
        }, 700);
    })
    .catch(() => showToast("Failed to save note", "danger"));
}

function clearNote() {
    if (!noteArea) return;
    if (confirm('Clear the note?')) {
        noteArea.value = '';
        localStorage.removeItem('myNote');
        autoResize(noteArea);
        showToast("Note cleared", "warning");
    }
}


// =========================
// TODO LIST
// =========================
const todoList = document.getElementById("Todo-List");
function loadTodos() {
    if (!todoList) return;

    fetch("/note&do/todo/all")
        .then(res => res.json())
        .then(todos => {
            todoList.innerHTML = "";
            todos.forEach(todo => {
                const li = document.createElement("li");

                const text = document.createElement("span");
                text.textContent = todo[1];
                text.className = "todo-text";

                const del = document.createElement("button");
                del.className = "delete-btn";
                del.textContent = "🗑️";
                del.onclick = () => deleteTodo(todo[0]);

                li.append(text, del);
                todoList.appendChild(li);
            });
        })
        .catch(() => showToast("Failed to load todos", "danger"));
}

function deleteTodo(id) {
    fetch(`/note&do/todo/remove/${id}`, { method: "DELETE" })
        .then(() => {
            showToast("Todo removed", "success");
            loadTodos();
        })
        .catch(() => showToast("Failed to delete todo", "danger"));
}

// =========================
// NOTES GRID
// =========================
const notesGrid = document.getElementById('notes-grid');
function loadNotes() {
    if (!notesGrid) return;

    fetch("/note&do/notes/all")
        .then(res => res.json())
        .then(notes => {
            notesGrid.querySelectorAll('.note-item').forEach(n => n.remove());

            notes.forEach(note => {
                const col = document.createElement('div');
                col.className = 'col-12 col-sm-6 col-md-4 col-lg-3 note-item';

                col.innerHTML = `
                  <div class="card note-card shadow-sm h-100">
                    <div class="card-body d-flex flex-column">
                      <div class="note-preview flex-grow-1">
                        ${note[1].replace(/\n/g, '<br>')}
                      </div>
                      <div class="d-flex justify-content-end gap-2 mt-3">
                        <button class="btn btn-sm btn-outline-danger"
                                onclick="deleteNote(${note[0]})">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                `;
                notesGrid.appendChild(col);
            });
        })
        .catch(() => showToast("Failed to load notes", "danger"));
}

function deleteNote(id) {
    fetch(`/note&do/note/remove/${id}`, { method: "DELETE" })
        .then(() => {
            showToast("Note deleted", "success");
            loadNotes();
        })
        .catch(() => showToast("Failed to delete note", "danger"));
}

function createNewNote(){   
    localStorage.removeItem('myNote');
    window.location.href = "/note&do/notepad";}


// =========================
// INIT
// =========================
document.addEventListener("DOMContentLoaded", () => {
    setActiveSidebarLink();
    loadTodos();
    loadNotes();

    if (window.FLASH_MESSAGES && Array.isArray(window.FLASH_MESSAGES)) {
        window.FLASH_MESSAGES.forEach(([category, message]) => {
            showToast(message, category);
        });
    }
});

const socket = io("", {
    transports: ["websocket"],
    withCredentials: true
});

const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");
console.log("FORM:", form);
console.log("INPUT:", input);
let aiBubble = null;
socket.on("connect", () => {
    console.log("✅ connected to socket", socket.id);
});
form.addEventListener("submit", e => {
    e.preventDefault();

    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    aiBubble = addMessage("", "ai");
    socket.emit("user_message", { message: text });
});

socket.on("ai_token", data => {
    aiBubble.textContent += data.token;
    messages.scrollTop = messages.scrollHeight;
    
    
});

socket.on("ai_done", () => {
   
    aiBubble = null;
   
    
});

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = text;
    messages.appendChild(div);
    return div;
}
function showToast(message, type = "info") {
    const container = document.querySelector(".toast-container");

    const colors = {
        success: "bg-success text-white",
        danger: "bg-danger text-white",
        warning: "bg-warning text-dark",
        info: "bg-primary text-white"
    };

    const toast = document.createElement("div");
    toast.className = `toast align-items-center ${colors[type] || colors.info} border-0`;
    toast.role = "alert";
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto"
                    data-bs-dismiss="toast"></button>
        </div>
    `;

    container.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, { delay: 2500 });
    bsToast.show();

    toast.addEventListener("hidden.bs.toast", () => toast.remove());
}

