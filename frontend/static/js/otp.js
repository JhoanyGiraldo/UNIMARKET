document.getElementById('otp-form').addEventListener('submit', async function(e){
  e.preventDefault();

  const otp = document.getElementById('otp-input').value.trim();
  const userId = sessionStorage.getItem('user_id_temp');
  const userEmail = sessionStorage.getItem('user_email_temp');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const errorDiv = document.getElementById('otp-error');

  if(!userId || !userEmail){
    errorDiv.textContent = 'No se encontró información de usuario. Por favor inicia sesión de nuevo.';
    return;
  }

  errorDiv.textContent = '';

  try {
    const res = await fetch("/otp_verify/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ user_id: userId, correo: userEmail, otp })
    });

    const data = await res.json();

    if(!data.success){
      errorDiv.textContent = data.message || 'Código OTP incorrecto';
      return;
    }

    // OTP correcto: limpiar sessionStorage y redirigir
    sessionStorage.removeItem('user_id_temp');
    sessionStorage.removeItem('user_email_temp');
    localStorage.setItem('user_name', data.user.nombre);
    localStorage.setItem('user_email', data.user.correo);
    window.location.href = '/';

  } catch(err){
    console.error(err);
    errorDiv.textContent = 'Error al conectar con el servidor';
  }
});
