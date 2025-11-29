document.getElementById('register-form').addEventListener('submit', async function(e){
  e.preventDefault();

  const nombre = document.getElementById('reg-nombre').value;
  const apellido = document.getElementById('reg-apellido').value;
  const correo = document.getElementById('reg-correo').value;
  const password = document.getElementById('reg-password').value;

  const BASE = (window.API_BASE || 'http://localhost:8000/api');

  try {
    const res = await fetch(BASE + '/users/register/', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ nombre, apellido, correo, password })
    });

    if(!res.ok){
      const txt = await res.text().catch(()=>null);
      console.error('Register failed', res.status, txt);
      alert('Error del servidor: ' + res.status);
      return;
    }

    const data = await res.json();

    if(data && data.success){
      alert('Registro exitoso. Inicia sesión.');
      window.location.href = "/login/";
      return;
    }

    alert('Error en registro');
  } catch(err){
    console.error(err);
    alert('Error al conectar con el servidor. Asegúrate de que Django esté corriendo.');
  }
});
