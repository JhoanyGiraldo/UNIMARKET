document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const messageBox = document.getElementById("login-message");
  const otpForm = document.getElementById("otp-form"); // formulario OTP oculto
  const otpInput = document.getElementById("otp-input");

  // Obtener CSRF token desde cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  // Paso 1: Enviar email + password
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
      const response = await fetch("/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok && data.ok) {
        if (data.step === "otp") {
          // Mostrar formulario OTP
          messageBox.style.color = "blue";
          messageBox.textContent = "Se envió un código a tu correo. Ingresa el OTP:";
          otpForm.style.display = "block";
        } else if (data.redirect) {
          // Login directo sin OTP
          window.location.href = data.redirect;
        }
      } else {
        messageBox.style.color = "red";
        messageBox.textContent = data.message || "Credenciales inválidas";
      }
    } catch (error) {
      messageBox.style.color = "red";
      messageBox.textContent = "Error de conexión con el servidor";
    }
  });

  // Paso 2: Verificar OTP
  otpForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const otp = otpInput.value;

    try {
      const response = await fetch("/verify-otp/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({ otp })
      });

      const data = await response.json();

      if (response.ok && data.ok) {
        window.location.href = data.redirect;
      } else {
        messageBox.style.color = "red";
        messageBox.textContent = data.message || "Código OTP inválido";
      }
    } catch (error) {
      messageBox.style.color = "red";
      messageBox.textContent = "Error de conexión con el servidor";
    }
  });
});
