document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const messageBox = document.getElementById("login-message");

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
        messageBox.style.color = "green";
        messageBox.textContent = "Login exitoso ✔";
        window.location.href = data.redirect;
      } else {
        messageBox.style.color = "red";
        messageBox.textContent = data.message || "Credenciales inválidas";
      }
    } catch (error) {
      messageBox.style.color = "red";
      messageBox.textContent = "Error de conexión con el servidor";
    }
  });
});
