const API_URL = "http://127.0.0.1:8000";
const API_KEY = "expected-secret";
const authHeaders = { "X-API-Key": API_KEY };
const jsonHeaders = { "Content-Type": "application/json", ...authHeaders };


async function login() {
  await fetch(`${API_URL}/login`, {
    method: "POST",
    credentials: "include"
  });
}


document.getElementById("item-form").addEventListener("submit", async function (event) {
  event.preventDefault();

  await fetch(`${API_URL}/admin/items`, {
    method: "POST",
    headers: jsonHeaders,
    credentials: "include",
    body: JSON.stringify({
      name: document.getElementById("name").value,
      price: Number(document.getElementById("price").value)
    })
  });

  clearForm();
  fetchData();
});


async function fetchData(skip = 0, limit = 100) {
  const response = await fetch(`${API_URL}/admin/items?skip=${skip}&limit=${limit}`, {
    headers: authHeaders,
    credentials: "include"
  });
  const items = await response.json();

  document.querySelector("tbody").innerHTML = items.map(item => `
    <tr>
      <td>${item.id}</td>
      <td>${item.name}</td>
      <td>${item.price}</td>
      <td><button onclick="handleDelete(${item.id})">Delete</button></td>
    </tr>
  `).join("");
}


async function handleDelete(itemId) {
  await fetch(`${API_URL}/admin/items/${itemId}`, {
    method: "DELETE",
    headers: authHeaders,
    credentials: "include"
  });
  fetchData();
}


async function fetchCustomers(skip = 0, limit = 100) {
  const response = await fetch(`${API_URL}/customers?skip=${skip}&limit=${limit}`, {
    credentials: "include"
  });
  const customers = await response.json();

  document.getElementById("customers-body").innerHTML = customers.map(customer => `
    <tr>
      <td>${customer.id}</td>
      <td>${customer.name}</td>
      <td>${customer.email}</td>
    </tr>
  `).join("");
}


function clearForm() {
  document.getElementById("name").value = "";
  document.getElementById("price").value = "";
}


async function init() {
  await login();
  fetchData();
  fetchCustomers();
}


init();
