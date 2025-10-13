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

                // Adición dinámica para HU1: Form crear usuario y lista (solo post-login)
                const createFormHTML = `
                    <h3>Crear Nuevo Usuario (HU1)</h3>
                    <form id="createUserForm">
                        <label for="nombre">Nombre:</label>
                        <input type="text" id="nombre" required>
                        <label for="newEmail">Email:</label>
                        <input type="email" id="newEmail" required>
                        <label for="newPassword">Contraseña:</label>
                        <input type="password" id="newPassword" required>
                        <label for="newRol">Rol:</label>
                        <select id="newRol" required>
                            <option value="">Selecciona rol</option>
                            <option value="ADMIN">ADMIN</option>
                            <option value="COORDINADOR">COORDINADOR</option>
                            <option value="PROFESOR">PROFESOR</option>
                            <option value="coord_INFRA">Coordinador Infra</option>
                        </select>
                        <button type="submit">Crear Usuario</button>
                    </form>
                    <div id="createMessage"></div>
                    <h3>Lista de Usuarios</h3>
                    <ul id="userList"></ul>
                `;
                dashboard.innerHTML += createFormHTML;
                loadUsers();  // Carga inicial lista post-login

                // Event listener para form crear (agregado dinámicamente)
                const createForm = document.getElementById('createUserForm');
                createForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    createUser();
                });
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

async function createUser() {
    const nombre = document.getElementById('nombre').value;
    const newEmail = document.getElementById('newEmail').value;
    const newPassword = document.getElementById('newPassword').value;
    const newRol = document.getElementById('newRol').value;
    const message = document.getElementById('createMessage');

    try {
        const response = await fetch('http://localhost:8000/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, email: newEmail, password: newPassword, rol: newRol })
        });
        const data = await response.json();

        if (response.ok) {
            message.textContent = data.message || 'Usuario creado!';
            message.className = 'success';
            document.getElementById('createUserForm').reset();
            loadUsers();  // Refresca lista
        } else {
            message.textContent = data.error || 'Error al crear';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error de conexión: ' + error.message;
        message.className = 'error';
    }
}

// Carga y muestra lista usuarios (GET /users)
async function loadUsers() {
    try {
        const response = await fetch('http://localhost:8000/users');
        const users = await response.json();
        const list = document.getElementById('userList');
        list.innerHTML = users.map(user => `<li>${user.nombre} (${user.email}) - ${user.rol} ${user.activo ? '(Activo)' : '(Inactivo)'}</li>`).join('');
    } catch (error) {
        console.error('Error loading users:', error);
    }
}
