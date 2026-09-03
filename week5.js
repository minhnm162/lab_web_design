const fetchUsersButton = document.querySelector('#fetch-users');
const userTableBody = document.querySelector('#user-table-body');

// async function fetchUsers() {
//     fetchUsersButton.disabled = true;
//     fetchUsersButton.textContent = 'Loading...';
//     userTableBody.innerHTML = '';

//     try {
//         const response = await fetch('https://jsonplaceholder.typicode.com/users');

//         if (!response.ok) {
//             throw new Error('Unable to fetch users.');
//         }

//         const users = await response.json();
//         users.forEach((user) => {
//             const row = document.createElement('tr');

//             row.innerHTML = `
//                 <td>${user.id}</td>
//                 <td>${user.name}</td>
//                 <td>${user.phone}</td>
//                 <td>${user.email}</td>
//                 <td>${user.website}</td>
//                 <td>${user.address.city}, ${user.address.street}</td>
//             `;

//             userTableBody.appendChild(row);
//         });
//     } catch (error) {
//         userTableBody.innerHTML = `
//             <tr>
//                 <td colspan="6">${error.message}</td>
//             </tr>
//         `;
//     } finally {
//         fetchUsersButton.disabled = false;
//         fetchUsersButton.textContent = 'Fetch Users';
//     }
// }

// fetchUsersButton.addEventListener('click', fetchUsers);

function renderUsers(users) {
    userTableBody.innerHTML = users.map((user) => `
        <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.phone}</td>
            <td>${user.email}</td>
            <td>${user.website}</td>
            <td>${user.address.city}, ${user.address.street}</td>
        </tr>
    `).join('');
}

async function fetchUsers() {
    fetchUsersButton.disabled = true;
    fetchUsersButton.textContent = 'Loading...';

    try {
        const res = await fetch('https://jsonplaceholder.typicode.com/users');

        if (!res.ok) {
            throw new Error('Unable to fetch users.');
        }

        const users = await res.json();
        renderUsers(users);
    } catch (error) {
        console.error(error);
        userTableBody.innerHTML = `
            <tr>
                <td colspan="6">${error.message}</td>
            </tr>
        `;
    } finally {
        fetchUsersButton.disabled = false;
        fetchUsersButton.textContent = 'Fetch Users';
    }
}

fetchUsersButton.addEventListener('click', fetchUsers);
