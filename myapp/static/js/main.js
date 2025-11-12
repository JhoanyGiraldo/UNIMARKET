/* main.js
 - Frontend-only shopping cart using localStorage.
 - Use images from products[].image (can be dataURI placeholders or relative paths to /images/)
*/

const PRODUCTS = [
  { id:1, name:'Camiseta USC Azul', price:45000, image: placeholderSVG('Camiseta','#cfe7ff') },
  { id:2, name:'Sudadera USC Negra', price:95000, image: placeholderSVG('Sudadera','#e9e6ff') },
  { id:3, name:'Gorra USC Blanca', price:30000, image: placeholderSVG('Gorra','#fff0e0') },
  { id:4, name:'Bolígrafo USC', price:15000, image: placeholderSVG('Bolígrafo','#e6fff0') },
  { id:5, name:'Uniforme Odontología', price:120000, image: placeholderSVG('Uniforme','#ffe6f2') }
];

// UTIL: crea un SVG data URI con texto (temporal)
function placeholderSVG(label, bg='#ddd'){
  const w=800, h=600;
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}'>
    <rect width='100%' height='100%' fill='${bg}'/>
    <text x='50%' y='50%' font-size='40' dominant-baseline='middle' text-anchor='middle' fill='#222' font-family='Arial'>
      ${escapeHtml(label)}
    </text>
  </svg>`;
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
}
function escapeHtml(s){ return s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

/* CART functions */
function getCart(){
  return JSON.parse(localStorage.getItem('cart_usc') || '[]');
}
function saveCart(c){ localStorage.setItem('cart_usc', JSON.stringify(c)); updateCartCount(); }
function addToCart(id, qty=1){
  const prod = PRODUCTS.find(p=>p.id===id);
  if(!prod) return;
  const cart = getCart();
  const exists = cart.find(it=>it.id===id);
  if(exists){ exists.qty += qty; }
  else{ cart.push({ id:prod.id, name:prod.name, price:prod.price, image:prod.image, qty: qty }); }
  saveCart(cart);
  toast('Producto agregado', 1200);
}
function removeFromCart(id){
  let cart = getCart();
  cart = cart.filter(it=>it.id!==id);
  saveCart(cart);
}
function updateQty(id, qty){
  const cart = getCart();
  const it = cart.find(i=>i.id===id);
  if(it){ it.qty = Math.max(1, parseInt(qty)||1); saveCart(cart); }
}
function cartTotal(){
  const cart = getCart();
  return cart.reduce((s,i)=> s + (i.price * i.qty), 0);
}
function updateCartCount(){
  const cart = getCart();
  const count = cart.reduce((s,i)=> s + i.qty, 0);
  const span = document.getElementById('cart-count');
  if(span) span.textContent = count;
}

/* UI utilities */
function toast(msg, ms=1500){
  const t = document.createElement('div');
  t.textContent = msg;
  Object.assign(t.style,{position:'fixed',right:'20px',bottom:'20px',background:'#111',color:'#fff',padding:'10px 14px',borderRadius:'8px',zIndex:9999,opacity:0,transition:'300ms'});
  document.body.appendChild(t);
  requestAnimationFrame(()=> t.style.opacity=1);
  setTimeout(()=> { t.style.opacity=0; setTimeout(()=> t.remove(),300); }, ms);
}

/* Render products into a container with id */
function renderProducts(containerId){
  const cont = document.getElementById(containerId);
  if(!cont) return;
  cont.innerHTML = '';
  for(const p of PRODUCTS){
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${p.image}" alt="${p.name}">
      <div class="title">${p.name}</div>
      <div class="kicker">${p.description || ''}</div>
      <div class="price">$${formatPrice(p.price)}</div>
      <div class="actions">
        <button class="btn" data-add="${p.id}">Agregar</button>
        <a class="btn secondary" href="producto.html?id=${p.id}">Ver</a>
      </div>`;
    cont.appendChild(card);
  }
  // add event listeners
  cont.querySelectorAll('[data-add]').forEach(btn=>{
    btn.addEventListener('click', ()=> addToCart(parseInt(btn.dataset.add)));
  });
}

function formatPrice(n){ return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."); }

/* Render cart page */
function renderCartPage(){
  const wrap = document.getElementById('cart-wrap');
  if(!wrap) return;
  const cart = getCart();
  wrap.innerHTML = '';
  if(cart.length===0){
    wrap.innerHTML = `<div class="center"><h3>Tu carrito está vacío</h3><p class="kicker">Agrega productos desde el catálogo.</p></div>`;
    document.getElementById('cart-summary').innerHTML = '';
    updateCartCount();
    return;
  }
  for(const item of cart){
    const row = document.createElement('div'); row.className='cart-row';
    row.innerHTML = `
      <img src="${item.image}" alt="${item.name}">
      <div style="flex:1;">
        <div style="font-weight:700">${item.name}</div>
        <div class="kicker">$${formatPrice(item.price)} x ${item.qty}</div>
      </div>
      <div class="qty">
        <button class="btn round" data-dec="${item.id}">-</button>
        <input type="number" min="1" value="${item.qty}" style="width:60px;padding:6px;border-radius:6px;border:1px solid #eee" data-q="${item.id}">
        <button class="btn round" data-inc="${item.id}">+</button>
      </div>
      <div style="width:120px;text-align:right;">$${formatPrice(item.price * item.qty)}</div>
      <div><button class="btn secondary" data-remove="${item.id}">Eliminar</button></div>
    `;
    wrap.appendChild(row);
  }
  // summary
  document.getElementById('cart-summary').innerHTML = `
    <div class="total-box">
      <div style="display:flex;justify-content:space-between"><div>Subtotal</div><div>$${formatPrice(cartTotal())}</div></div>
      <div style="margin-top:8px;display:flex;gap:8px;">
        <button class="btn" id="checkout-btn">Finalizar compra</button>
        <button class="btn secondary" id="clear-cart">Vaciar</button>
      </div>
    </div>
  `;
  // listeners
  wrap.querySelectorAll('[data-remove]').forEach(b=> b.addEventListener('click', e=> {
    removeFromCart(parseInt(e.target.dataset.remove)); renderCartPage();
  }));
  wrap.querySelectorAll('[data-inc]').forEach(b=> b.addEventListener('click', e=> {
    const id=parseInt(e.target.dataset.inc);
    const cart=getCart(); const it=cart.find(i=>i.id===id); if(it){ it.qty++; saveCart(cart); renderCartPage(); }
  }));
  wrap.querySelectorAll('[data-dec]').forEach(b=> b.addEventListener('click', e=> {
    const id=parseInt(e.target.dataset.dec);
    const cart=getCart(); const it=cart.find(i=>i.id===id); if(it){ it.qty = Math.max(1, it.qty-1); saveCart(cart); renderCartPage(); }
  }));
  wrap.querySelectorAll('input[type="number"][data-q]').forEach(inp=>{
    inp.addEventListener('change', e=> { updateQty(parseInt(e.target.dataset.q), parseInt(e.target.value)); renderCartPage(); });
  });
  document.getElementById('clear-cart').addEventListener('click', ()=> { localStorage.removeItem('cart_usc'); renderCartPage(); updateCartCount(); });
  document.getElementById('checkout-btn').addEventListener('click', ()=> { alert('Este flujo de pago es demo. Aquí deberías llamar al backend para crear el pedido y la sesión de pago (Stripe).'); });
  updateCartCount();
}

/* Init: wire up basic pages */
document.addEventListener('DOMContentLoaded', ()=>{
  updateCartCount();
  // if container for products exists, render
  if(document.getElementById('products-grid')) renderProducts('products-grid');
  if(document.getElementById('products-home')) renderProducts('products-home');
  if(document.getElementById('cart-wrap')) renderCartPage();
});