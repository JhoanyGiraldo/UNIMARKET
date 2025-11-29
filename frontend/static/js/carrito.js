// CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Toast
function toast(msg, ms = 1500){
  const t=document.createElement("div");
  t.textContent=msg;
  Object.assign(t.style,{
    position:"fixed", right:"20px", bottom:"20px",
    background:"#0b4b83", color:"#fff",
    padding:"10px 14px", borderRadius:"8px",
    zIndex:9999, opacity:0, transition:"300ms"
  });
  document.body.appendChild(t);
  requestAnimationFrame(()=>t.style.opacity=1);
  setTimeout(()=>{t.style.opacity=0; setTimeout(()=>t.remove(),300)},ms);
}

// Actualizar contador
function actualizarContador(carrito){
  let totalItems = 0;
  for (const key in carrito) {
    totalItems += carrito[key].cantidad;
  }
  document.getElementById("cart-count").textContent = totalItems;
}

// Render resumen
function renderResumen(carrito){
  const resumen = document.getElementById("resumen");
  resumen.innerHTML = "";

  const productos = Object.keys(carrito);
  if (productos.length === 0){
    resumen.innerHTML = `
      <p>Tu carrito está vacío</p>
      <a href="/catalogo" class="btn btn-success">Ir al catálogo</a>
    `;
    return;
  }

  let total = 0;
  let html = `<h3>Resumen</h3><p>Productos: ${productos.length}</p>`;

  productos.forEach(id => {
    const item = carrito[id];
    const subtotal = item.cantidad * item.precio;
    total += subtotal;
    html += `
      <div class="resumen-item cart-item-card" data-id="${id}">
        <strong>${item.nombre}</strong><br>
        <small style="color:#555;">${item.descripcion || ""}</small><br>
        <span class="resumen-cantidad">Cantidad: ${item.cantidad}</span><br>
        <span class="resumen-subtotal">Subtotal: $${subtotal}</span>
      </div>`;
  });

  html += `
    <h2 id="total">Total: $${total}</h2>
    <button class="btn btn-danger" onclick="vaciarCarrito()">Vaciar carrito</button>
    <a href="/crear_checkout" class="btn btn-primary">Proceder al pago</a>
  `;

  resumen.innerHTML = html;

  // Activar botones dinámicos
  bindListeners();
}


// Actualizar item
function actualizarItem(productoId, carrito){
  const card = document.querySelector(`.cart-item-card[data-id="${productoId}"]`);
  if (!card) return;
  const cantidadSpan = card.querySelector(".cantidad-control span");
  const subtotalP = card.querySelector("p strong");
  const item = carrito[productoId];
  if (item) {
    cantidadSpan.textContent = item.cantidad;
    subtotalP.textContent = "Subtotal: $" + (item.cantidad * item.precio);
  } else {
    card.remove();
  }
}

// Agregar cantidad
function updateCarrito(productoId, cantidad){
  fetch("/agregar_carrito/", {
    method: "POST",
    headers:{ "Content-Type":"application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify({ producto_id: productoId, cantidad })
  }).then(r=>r.json()).then(data=>{
    if(data.ok){
      toast("Producto actualizado ✔");
      actualizarContador(data.carrito);
      actualizarItem(productoId, data.carrito);
      renderResumen(data.carrito);
    } else {
      toast(data.error || "No se pudo agregar");
    }
  });
}

// Quitar cantidad
function quitarCarrito(productoId){
  fetch("/eliminar_carrito/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ producto_id: productoId, cantidad: 1 })
  }).then(r => r.json()).then(data => {
    if (data.ok){
      toast("Cantidad reducida");
      actualizarContador(data.carrito);
      actualizarItem(productoId, data.carrito);
      renderResumen(data.carrito);
      verificarCarritoVacio(data.carrito);
    }
  });
}

function eliminarProducto(productoId){
  fetch("/eliminar_carrito/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ producto_id: productoId, cantidad: 9999 })
  }).then(r => r.json()).then(data => {
    if (data.ok){
      toast("Producto eliminado");
      actualizarContador(data.carrito);
      renderResumen(data.carrito);
      verificarCarritoVacio(data.carrito);
    }
  });
}


function vaciarCarrito(){
  fetch("/eliminar_carrito/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ producto_id: "all" })
  }).then(r => r.json()).then(data => {
    if (data.ok){
      toast("Carrito vacío");
      actualizarContador(data.carrito);
      renderResumen(data.carrito);
      verificarCarritoVacio(data.carrito);
    }
  });
}

function verificarCarritoVacio(carrito){
  if (Object.keys(carrito).length === 0) {
    const contenedor = document.createElement("div");
    contenedor.className = "center empty-block fade-in";
    contenedor.innerHTML = `
      <p>Tu carrito está vacío</p>
      <a href="/catalogo/" class="btn">Ir al catálogo</a>
    `;
    const layout = document.querySelector(".carrito-layout");
    if (layout) layout.prepend(contenedor);
  }
}

// Listeners iniciales
function bindListeners(){
  document.querySelectorAll(".agregar").forEach(btn => {
    btn.onclick = () => updateCarrito(btn.dataset.id, 1);
  });
  document.querySelectorAll(".quitar").forEach(btn => {
    btn.onclick = () => quitarCarrito(btn.dataset.id);
  });
  document.querySelectorAll(".eliminar").forEach(btn => {
    btn.onclick = () => eliminarProducto(btn.dataset.id);
  });
}

document.addEventListener("DOMContentLoaded", bindListeners);
