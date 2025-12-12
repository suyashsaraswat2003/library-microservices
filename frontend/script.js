const BOOK_SERVICE = "http://localhost:8000";
const USER_SERVICE = "http://localhost:8001";
const BORROW_SERVICE = "http://localhost:8002";

// Users
function addUser() {
    const user = {
        id: parseInt(document.getElementById("user-id").value),
        name: document.getElementById("user-name").value
    };
    fetch(`${USER_SERVICE}/users`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(user)
    }).then(res => res.json())
    .then(data => {
        alert("User added!");
        listUsers();
    });
}

function listUsers() {
    fetch(`${USER_SERVICE}/users`)
    .then(res => res.json())
    .then(users => {
        const list = document.getElementById("user-list");
        list.innerHTML = "";
        users.forEach(user => {
            list.innerHTML += `<li>${user.name} (ID: ${user.id})</li>`;
        });
    });
}

// Books
function addBook() {
    const book = {
        id: parseInt(document.getElementById("book-id").value),
        title: document.getElementById("book-title").value,
        author: document.getElementById("book-author").value,
        genre: document.getElementById("book-genre").value
    };

    fetch(`${BOOK_SERVICE}/books`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(book)
    }).then(res => res.json()).then(data => {
        alert("Book added!");
        listBooks();
    });
}

function listBooks() {
    fetch(`${BOOK_SERVICE}/books`)
    .then(res => res.json())
    .then(books => {
        const list = document.getElementById("book-list");
        list.innerHTML = "";
        books.forEach(book => {
            list.innerHTML += `<li>${book.title} by ${book.author} - Available: ${book.available} ${book.borrowed_by ? " | Borrowed by: " + book.borrowed_by : ""}</li>`;
        });
    });
}

// Borrow / Return
function borrowBook() {
    const data = {
        user_id: parseInt(document.getElementById("borrow-user-id").value),
        book_id: parseInt(document.getElementById("borrow-book-id").value)
    };
    fetch(`${BORROW_SERVICE}/borrow`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(res => res.json())
    .then(data => alert(data.message || data.error))
    .finally(listBooks);
}

function returnBook() {
    const data = {
        user_id: parseInt(document.getElementById("borrow-user-id").value),
        book_id: parseInt(document.getElementById("borrow-book-id").value)
    };
    fetch(`${BORROW_SERVICE}/return`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(res => res.json())
    .then(data => alert(data.message || data.error))
    .finally(listBooks);
}

// Delete User
function deleteUser() {
    const userId = parseInt(document.getElementById("delete-user-id").value);
    fetch(`${USER_SERVICE}/users/${userId}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        listUsers();
    });
}

// Delete Book
function deleteBook() {
    const bookId = parseInt(document.getElementById("delete-book-id").value);
    fetch(`${BOOK_SERVICE}/books/${bookId}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        listBooks();
    });
}

// Initial load
listBooks();
listUsers();
