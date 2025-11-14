/* main.js (API-enabled)
   This file mirrors the original UI logic but fetches products from api/products.php when available.
*/

let PRODUCTS = [];
// API base for Django backend. During development Django typically runs at http://localhost:8000
const API_BASE = (window.API_BASE || 'http://localhost:8000') + '/api';

function escapeHtml(s){ return (s||'').toString().replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function formatPrice(n){ return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."); }

async function loadProducts(){
  try{
    const res = await fetch(API_BASE + '/products/');
    const data = await res.json();
    if(data && data.success){ PRODUCTS = data.products.map(p=>({ id: parseInt(p.id_producto || p.id), name: p.nombre, description: p.descripcion, price: parseFloat(p.precio || p.price), image: p.imagen || p.image })); }
  }catch(e){ console.warn('No se pudo cargar productos desde API Django, se usará listado local si existe.'); }
}

/* original placeholder products fallback (kept small) */
const FALLBACK = [
  { id:1, name:'Camiseta USC Azul', price:45000, image: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="100%" height="100%" fill="%23cfe7ff"/><text x="50%" y="50%" font-size="40" dominant-baseline="middle" text-anchor="middle">Camiseta</text></svg>' },
  { id:4, name:'Bolígrafo USC', price:15000, image: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="100%" height="100%" fill="%23e6fff0"/><text x="50%" y="50%" font-size="40" dominant-baseline="middle" text-anchor="middle">Bolígrafo</text></svg>' }
];

function getCart(){ return JSON.parse(localStorage.getItem('cart_usc') || '[]'); }
function saveCart(c){ localStorage.setItem('cart_usc', JSON.stringify(c)); updateCartCount(); }
function getAuthToken(){ return localStorage.getItem('auth_token'); }

async function addToCart(id, qty=1){
  const prod = PRODUCTS.find(p=>p.id===id) || FALLBACK.find(p=>p.id===id);
  if(!prod) return;
  const token = getAuthToken();
  if(token){
    // call backend cart add
    try{
      const res = await fetch(API_BASE + '/cart/add/', { method:'POST', headers: { 'Content-Type':'application/json', 'Authorization':'Token ' + token }, body: JSON.stringify({ product_id: id, quantity: qty }) });
      const data = await res.json();
      if(data && data.success){ toast('Producto agregado al carrito',1200); return; }
    }catch(e){ console.warn('Error añadiendo al carrito en backend, guardando local'); }
  }
  const cart=getCart(); const e=cart.find(i=>i.id===id); if(e){ e.qty+=qty; } else { cart.push({ id:prod.id, name:prod.name, price:prod.price, image:prod.image, qty:qty }); } saveCart(cart); toast('Producto agregado',1200);
}
function removeFromCart(id){ let c=getCart(); c=c.filter(i=>i.id!==id); saveCart(c); }
function updateQty(id, qty){ const c=getCart(); const it=c.find(i=>i.id===id); if(it){ it.qty = Math.max(1, parseInt(qty)||1); saveCart(c); } }
function cartTotal(){ return getCart().reduce((s,i)=> s + (i.price*i.qty), 0); }
function updateCartCount(){ const count = getCart().reduce((s,i)=> s + i.qty, 0); const span = document.getElementById('cart-count'); if(span) span.textContent = count; }

function toast(msg, ms=1500){ const t=document.createElement('div'); t.textContent=msg; Object.assign(t.style,{position:'fixed',right:'20px',bottom:'20px',background:'#111',color:'#fff',padding:'10px 14px',borderRadius:'8px',zIndex:9999,opacity:0,transition:'300ms'}); document.body.appendChild(t); requestAnimationFrame(()=>t.style.opacity=1); setTimeout(()=>{ t.style.opacity=0; setTimeout(()=>t.remove(),300); }, ms); }

function renderProducts(containerId){ const cont=document.getElementById(containerId); if(!cont) return; cont.innerHTML=''; const list = (PRODUCTS.length?PRODUCTS:FALLBACK); for(const p of list){ const card=document.createElement('div'); card.className='card'; card.innerHTML = `<img src="${p.image}" alt="${escapeHtml(p.name)}"><div class="title">${escapeHtml(p.name)}</div><div class="kicker">${escapeHtml(p.description||'')}</div><div class="price">$${formatPrice(p.price)}</div><div class="actions"><button class="btn" data-add="${p.id}">Agregar</button><a class="btn secondary" href="producto.html?id=${p.id}">Ver</a></div>`; cont.appendChild(card); }
  cont.querySelectorAll('[data-add]').forEach(btn=> btn.addEventListener('click', ()=> addToCart(parseInt(btn.dataset.add))));
}

function renderCartPage(){
  const wrap=document.getElementById('cart-wrap'); if(!wrap) return;
  const cart=getCart(); wrap.innerHTML='';
  if(cart.length===0){ wrap.innerHTML='<div class="center"><h3>Tu carrito está vacío</h3><p class="kicker">Agrega productos desde el catálogo.</p></div>'; document.getElementById('cart-summary').innerHTML=''; updateCartCount(); return; }

  const token = getAuthToken();
  if(token){
    fetch(API_BASE + '/cart/', { headers: { 'Authorization':'Token ' + token } }).then(r=>r.json()).then(data=>{
      if(data && data.success){
        const cartServer = data.cart;
        wrap.innerHTML = '';
        (cartServer.items || []).forEach(item=>{
          const row = document.createElement('div'); row.className='cart-row';
          row.innerHTML = `<img src="" alt=""><div style="flex:1;"><div style="font-weight:700">Producto ${item.id_producto}</div><div class="kicker">Cantidad: ${item.cantidad}</div></div><div style="width:120px;text-align:right;">$${formatPrice(item.subtotal)}</div><div><button class="btn secondary" data-remove="${item.id_detalle}">Eliminar</button></div>`;
          wrap.appendChild(row);
        });
        document.getElementById('cart-summary').innerHTML = `<div class="total-box"><div style="display:flex;justify-content:space-between"><div>Subtotal</div><div>$${formatPrice((cartServer.items||[]).reduce((s,i)=> s + (i.subtotal||0), 0))}</div></div><div style="margin-top:8px;display:flex;gap:8px;"><button class="btn" id="checkout-btn">Finalizar compra</button><button class="btn secondary" id="clear-cart">Vaciar</button></div></div>`;
        wrap.querySelectorAll('[data-remove]').forEach(b=> b.addEventListener('click', e=> { const id = parseInt(e.target.dataset.remove); fetch(API_BASE + '/cart/item/' + id + '/', { method:'DELETE', headers:{ 'Authorization':'Token ' + token } }).then(()=> renderCartPage()); }));
        document.getElementById('checkout-btn').addEventListener('click', ()=> { fetch(API_BASE + '/cart/checkout/', { method:'POST', headers: { 'Content-Type':'application/json', 'Authorization':'Token ' + token }, body: JSON.stringify({}) }).then(r=>r.json()).then(d=> { if(d.success){ alert('Pedido creado: ' + (d.order.id_pedido || d.order.id)); window.location.href='index.html'; } else alert('Error al crear pedido'); }); });
        document.getElementById('clear-cart').addEventListener('click', ()=> { alert('Vaciar en servidor no implementado.'); });
        updateCartCount();
        return;
      }
    }).catch(()=>{});
  }

  for(const item of cart){ const row=document.createElement('div'); row.className='cart-row'; row.innerHTML = `<img src="${item.image}" alt="${escapeHtml(item.name)}"><div style="flex:1;"><div style="font-weight:700">${escapeHtml(item.name)}</div><div class="kicker">$${formatPrice(item.price)} x ${item.qty}</div></div><div class="qty"><button class="btn round" data-dec="${item.id}">-</button><input type="number" min="1" value="${item.qty}" style="width:60px;padding:6px;border-radius:6px;border:1px solid #eee" data-q="${item.id}"><button class="btn round" data-inc="${item.id}">+</button></div><div style="width:120px;text-align:right;">$${formatPrice(item.price * item.qty)}</div><div><button class="btn secondary" data-remove="${item.id}">Eliminar</button></div>`; wrap.appendChild(row); }
  document.getElementById('cart-summary').innerHTML = `<div class="total-box"><div style="display:flex;justify-content:space-between"><div>Subtotal</div><div>$${formatPrice(cartTotal())}</div></div><div style="margin-top:8px;display:flex;gap:8px;"><button class="btn" id="checkout-btn">Finalizar compra</button><button class="btn secondary" id="clear-cart">Vaciar</button></div></div>`;
  wrap.querySelectorAll('[data-remove]').forEach(b=> b.addEventListener('click', e=> { removeFromCart(parseInt(e.target.dataset.remove)); renderCartPage(); }));
  wrap.querySelectorAll('[data-inc]').forEach(b=> b.addEventListener('click', e=> { const id=parseInt(e.target.dataset.inc); const cart=getCart(); const it=cart.find(i=>i.id===id); if(it){ it.qty++; saveCart(cart); renderCartPage(); } }));
  wrap.querySelectorAll('[data-dec]').forEach(b=> b.addEventListener('click', e=> { const id=parseInt(e.target.dataset.dec); const cart=getCart(); const it=cart.find(i=>i.id===id); if(it){ it.qty=Math.max(1, it.qty-1); saveCart(cart); renderCartPage(); } }));
  wrap.querySelectorAll('input[type="number"][data-q]').forEach(inp=> inp.addEventListener('change', e=> { updateQty(parseInt(e.target.dataset.q), parseInt(e.target.value)); renderCartPage(); }));
  document.getElementById('clear-cart').addEventListener('click', ()=> { localStorage.removeItem('cart_usc'); renderCartPage(); updateCartCount(); });
  document.getElementById('checkout-btn').addEventListener('click', ()=> { alert('Este flujo de pago es demo. Aquí deberías llamar al backend para crear el pedido y la sesión de pago (Stripe).'); });
  updateCartCount();
}

document.addEventListener('DOMContentLoaded', async ()=>{ updateCartCount(); await loadProducts(); if(document.getElementById('products-grid')) renderProducts('products-grid'); if(document.getElementById('products-home')) renderProducts('products-home'); if(document.getElementById('cart-wrap')) renderCartPage(); });
