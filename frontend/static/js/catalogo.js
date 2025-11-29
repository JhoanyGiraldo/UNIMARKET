// CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Toast
function toast(msg, ms = 1800){
  const t = document.createElement("div");
  t.textContent = msg;
  Object.assign(t.style, {
    position: "fixed", right: "20px", bottom: "20px",
    background: "#0b4b83", color: "#fff",
    padding: "10px 14px", borderRadius: "8px",
    zIndex: 9999, opacity: 0, transition: "300ms"
  });
  document.body.appendChild(t);
  requestAnimationFrame(() => t.style.opacity = 1);
  setTimeout(() => {
    t.style.opacity = 0;
    setTimeout(() => t.remove(), 300);
  }, ms);
}

// Render productos
function renderProductos(productos){
  const grid = document.getElementById("products-grid");
  grid.innerHTML = "";
  productos.forEach(p => {
    const card = document.createElement("div");
    card.className = "product-card";
    card.innerHTML = `
      <img src="${p.imagen}" alt="${p.nombre}" style="width:100%; height:200px; object-fit:cover;">
      <h3>${p.nombre}</h3>
      <p>$${p.precio}</p>
      <p>Stock disponible: ${p.stock}</p>
      <button class="btn add-to-cart-btn" data-id="${p.id}">Agregar al carrito</button>
    `;
    grid.appendChild(card);
  });
  grid.querySelectorAll(".add-to-cart-btn").forEach(btn => {
    btn.addEventListener("click", () => agregarCarrito(btn.dataset.id));
  });
}

// Agregar al carrito
function agregarCarrito(productoId){
  fetch("/agregar_carrito/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ producto_id: productoId, cantidad: 1 })
  })
  .then(r => r.json())
  .then(data => {
    if (data.ok) {
      toast("Producto agregado ✔");
      let totalItems = 0;
      for (const key in data.carrito) {
        totalItems += data.carrito[key].cantidad;
      }
      document.getElementById("cart-count").textContent = totalItems;
    } else {
      toast(data.error || "No se pudo agregar ❌");
    }
  });
}

// Búsqueda
document.getElementById("global-search").addEventListener("keyup", () => {
  const q = searchInput.value;
  fetch(`/filtrar_productos?q=${encodeURIComponent(q)}`)
    .then(r => r.json())
    .then(data => renderProductos(data.productos));
});

// Categorías
document.querySelectorAll("aside ul li").forEach(li => {
  li.addEventListener("click", () => {
    document.querySelectorAll("aside ul li").forEach(el => el.classList.remove("active"));
    li.classList.add("active");
    const categoria = li.textContent.trim();
    const url = categoria === "Todos"
      ? "/filtrar_productos"
      : `/filtrar_productos?categoria=${encodeURIComponent(categoria)}`;
    fetch(url)
      .then(r => r.json())
      .then(data => renderProductos(data.productos));
  });
});

// Inicializar listeners
document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
  btn.addEventListener("click", () => agregarCarrito(btn.dataset.id));
});
