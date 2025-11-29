/* main.js – versión Django (carrito 100% backend) */

/* ---------------------------
   Helpers
---------------------------- */
function escapeHtml(s){
  return (s||'').toString().replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}
function formatPrice(n){
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

/* ---------------------------
   Toast
---------------------------- */
function toast(msg, ms = 1500){
  const t=document.createElement("div");
  t.textContent=msg;
  Object.assign(t.style,{
    position:"fixed", right:"20px", bottom:"20px",
    background:"#111", color:"#fff",
    padding:"10px 14px", borderRadius:"8px",
    zIndex:9999, opacity:0, transition:"300ms"
  });
  document.body.appendChild(t);
  requestAnimationFrame(()=>t.style.opacity=1);
  setTimeout(()=>{t.style.opacity=0; setTimeout(()=>t.remove(),300)},ms);
}

/* ---------------------------
   Agregar producto al carrito
---------------------------- */
function addToCart(id){
  fetch("/agregar_carrito/", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      "X-CSRFToken": getCsrfToken()
    },
    body: JSON.stringify({ producto_id: id })
  })
  .then(r => r.json())
  .then(data=>{
    if(data.success){
      toast("Producto agregado al carrito ✔");
      updateCartCount();
    } else {
      toast("Error agregando producto");
    }
  });
}

function getCsrfToken(){
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
}

/* ---------------------------
   Cargar y renderizar productos
---------------------------- */
async function loadProducts(){
  try {
    const res = await fetch("/productos_api/");
    const data = await res.json();
    return data.productos || [];
  } catch(err){
    console.error("Error cargando productos", err);
    return [];
  }
}

async function renderProducts(containerId){
  const cont = document.getElementById(containerId);
  if(!cont) return;

  const products = await loadProducts();
  cont.innerHTML = "";

  products.forEach(p =>{
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${p.imagen}" alt="${escapeHtml(p.nombre)}">
      <div class="title">${escapeHtml(p.nombre)}</div>
      <div class="kicker">${escapeHtml(p.descripcion)}</div>
      <div class="price">$${formatPrice(p.precio)}</div>
      <div class="actions">
        <button class="btn" data-add="${p.id}">Agregar</button>
        <a class="btn secondary" href="/producto/${p.id}/">Ver</a>
      </div>
    `;
    cont.appendChild(card);
  });

  cont.querySelectorAll("[data-add]").forEach(btn=>{
    btn.addEventListener("click", ()=> addToCart(btn.dataset.add));
  });
}

/* ---------------------------
   Contador carrito
---------------------------- */
function updateCartCount(){
  fetch("/carrito_count/")
    .then(r=>r.json())
    .then(data=>{
      const span = document.getElementById("cart-count");
      if(span) span.textContent = data.count || 0;
    });
}

/* ---------------------------
   Carrito en la página
---------------------------- */
function renderCartPage(){
  const wrap = document.getElementById("cart-wrap");
  if(!wrap) return;

  fetch("/carrito/")
    .then(r => r.json())
    .then(data =>{
      wrap.innerHTML = "";

      if(!data.items || data.items.length === 0){
        wrap.innerHTML = `<div class="center"><h3>Tu carrito está vacío</h3></div>`;
        return;
      }

      data.items.forEach(item =>{
        const row = document.createElement("div");
        row.className="cart-row";
        row.innerHTML = `
          <img src="${item.imagen}" alt="">
          <div style="flex:1;">
            <div style="font-weight:700">${escapeHtml(item.nombre)}</div>
            <div class="kicker">$${formatPrice(item.precio)} x ${item.cantidad}</div>
          </div>
          <div style="width:120px;text-align:right;">$${formatPrice(item.subtotal)}</div>
          <div><button class="btn secondary" data-remove="${item.id}">Eliminar</button></div>
        `;
        wrap.appendChild(row);
      });

      wrap.querySelectorAll("[data-remove]").forEach(btn=>{
        btn.addEventListener("click", ()=>{
          fetch("/eliminar_carrito/", {
            method:"POST",
            headers:{ "Content-Type":"application/json", "X-CSRFToken":getCsrfToken() },
            body: JSON.stringify({ item_id: btn.dataset.remove })
          }).then(()=> renderCartPage());
        });
      });
    });
}

/* ---------------------------
   Inicialización
---------------------------- */
document.addEventListener("DOMContentLoaded", ()=>{
  updateCartCount();

  if(document.getElementById("products-grid"))
    renderProducts("products-grid");

  if(document.getElementById("products-home"))
    renderProducts("products-home");

  if(document.getElementById("cart-wrap"))
    renderCartPage();
});
