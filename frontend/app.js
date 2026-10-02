async function fetchData() {
  const response = await fetch("/items");
  const data = await response.json();
  const items = data.items;

  const tableBody = document.querySelector("tbody");
  tableBody.innerHTML = "";

  items.forEach(function (item) {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${item.id}</td>
      <td>${item.name}</td>
      <td>${item.price}</td>
      <td>
        <button onclick="deleteItem(${item.id})">
          Delete
        </button>
      </td>
    `;

    tableBody.appendChild(row);
  });
}


async function deleteItem(itemId) {
  const response = await fetch(`/items/${itemId}`, {
    method: "DELETE"
  });

  if (response.ok) {
    fetchData();
  } else {
    const error = await response.json();
    alert(error.detail);
  }
}
