document.addEventListener("DOMContentLoaded", function () {

    const searchBtn = document.getElementById("searchBtn");

    searchBtn.addEventListener("click", function () {

        const title = document.getElementById("title").value;
        const author = document.getElementById("author").value;
        const category = document.getElementById("category").value;

        fetch(`/books/search/?title=${encodeURIComponent(title)}&author=${encodeURIComponent(author)}&category=${encodeURIComponent(category)}`)
            .then(response => response.json())
            .then(data => {

                const tbody = document.getElementById("bookTableBody");
                tbody.innerHTML = "";

                if (data.length === 0) {

                    tbody.innerHTML = `
                        <tr>
                            <td colspan="4" class="no-data">
                                No books found.
                            </td>
                        </tr>
                    `;

                    return;
                }

                data.forEach(book => {

                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>
                            /books/${book.id}/checkout/
                                ${book.title}
                            </a>
                        </td>
                        <td>${book.author}</td>
                        <td>${book.category}</td>
                        <td>${book.available_copies}</td>
                    `;

                    tbody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error:", error);
            });

    });

    function logout() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login/';
        }
    })
    .catch(error => {
        console.error('Logout failed:', error);
    });
}

});