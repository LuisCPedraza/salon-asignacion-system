document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const message = document.getElementById('message');
    const dashboard = document.getElementById('dashboard');
    const userRol = document.getElementById('userRol');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();

            if (data.success) {
                message.textContent = 'Login exitoso!';
                message.className = 'success';
                userRol.textContent = data.rol;
                form.style.display = 'none';
                dashboard.style.display = 'block';
            } else {
                message.textContent = data.error || 'Error en login';
                message.className = 'error';
            }
        } catch (error) {
            message.textContent = 'Error de conexión: ' + error.message;
            message.className = 'error';
        }
    });
});

function logout() {
    location.reload();  // Simple reset (sin session real aún)
}
