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

                // ========== NUEVA FUNCIONALIDAD PARA ÉPICA 2: GESTIÓN DE GRUPOS ==========
                if (data.rol === 'COORDINADOR' || data.rol === 'ADMIN') {  // Simple rol check (HU3-HU4 acceso)
                    const groupsSectionHTML = `
                        <h3>Gestión de Grupos (Épica 2)</h3>
                        <form id="createGroupForm">
                            <label for="groupNombre">Nombre:</label>
                            <input type="text" id="groupNombre" required>
                            <label for="groupNivel">Nivel:</label>
                            <select id="groupNivel" required>
                                <option value="">Selecciona nivel</option>
                                <option value="Primaria">Primaria</option>
                                <option value="Secundaria">Secundaria</option>
                                <option value="Bachillerato">Bachillerato</option>
                            </select>
                            <label for="groupNum">Num. Estudiantes:</label>
                            <input type="number" id="groupNum" min="1" required>
                            <label for="groupCaracteristicas">Características:</label>
                            <textarea id="groupCaracteristicas"></textarea>
                            <button type="submit">Crear Grupo</button>
                        </form>
                        <div id="groupMessage"></div>
                        <h3>Lista de Grupos</h3>
                        <ul id="groupList"></ul>
                    `;
                    dashboard.innerHTML += groupsSectionHTML;
                    loadGroups();  // Carga inicial lista

                    // Event listener para create form
                    const createGroupForm = document.getElementById('createGroupForm');
                    createGroupForm.addEventListener('submit', (e) => {
                        e.preventDefault();
                        createGroup();
                    });
                } else {
                    dashboard.innerHTML += '<p>Acceso restringido: Solo COORDINADOR/ADMIN para grupos.</p>';
                }

                // ========== NUEVA FUNCIONALIDAD PARA ÉPICA 3: GESTIÓN DE SALONES ==========
                if (data.rol === 'coord_INFRA' || data.rol === 'ADMIN') {  // Simple rol check (HU5-HU6 acceso)
                    const salonesSectionHTML = `
                        <h3>Gestión de Salones (Épica 3)</h3>
                        <form id="createSalonForm">
                            <label for="salonCodigo">Código:</label>
                            <input type="text" id="salonCodigo" required>
                            <label for="salonCapacidad">Capacidad:</label>
                            <input type="number" id="salonCapacidad" min="1" required>
                            <label for="salonUbicacion">Ubicación:</label>
                            <textarea id="salonUbicacion"></textarea>
                            <button type="submit">Crear Salón</button>
                        </form>
                        <div id="salonMessage"></div>
                        <h3>Lista de Salones</h3>
                        <ul id="salonList"></ul>
                    `;
                    dashboard.innerHTML += salonesSectionHTML;
                    loadSalones();  // Carga inicial lista

                    // Event listener para create form
                    const createSalonForm = document.getElementById('createSalonForm');
                    createSalonForm.addEventListener('submit', (e) => {
                        e.preventDefault();
                        createSalon();
                    });
                } else {
                    dashboard.innerHTML += '<p>Acceso restringido: Solo coord_INFRA/ADMIN para salones.</p>';
                }

                // ========== Nueva funcionalidad para Épica 4: Gestión de Profesores ==========
                if (data.rol === 'COORDINADOR' || data.rol === 'ADMIN') {  // Simple rol check (HU7-HU8 acceso)
                    const profesoresSectionHTML = `
                        <h3>Gestión de Profesores (Épica 4)</h3>
                        <form id="createProfesorForm">
                            <label for="profesorUsuarioId">Usuario ID:</label>
                            <input type="text" id="profesorUsuarioId" required>
                            <label for="profesorEspecialidades">Especialidades:</label>
                            <textarea id="profesorEspecialidades"></textarea>
                            <label for="profesorHojaVida">Hoja de Vida URL:</label>
                            <input type="url" id="profesorHojaVida">
                            <button type="submit">Crear Profesor</button>
                        </form>
                        <div id="profesorMessage"></div>
                        <h3>Lista de Profesores</h3>
                        <ul id="profesorList"></ul>
                    `;
                    dashboard.innerHTML += profesoresSectionHTML;
                    loadProfesores();  // Carga inicial lista

                    // Event listener para create form
                    const createProfesorForm = document.getElementById('createProfesorForm');
                    createProfesorForm.addEventListener('submit', (e) => {
                        e.preventDefault();
                        createProfesor();
                    });
                } else {
                    dashboard.innerHTML += '<p>Acceso restringido: Solo COORDINADOR/ADMIN para profesores.</p>';
                }

                // ========== Nueva funcionalidad para Épica 10: Configuración del Sistema ==========
                if (data.rol === 'ADMIN') {  // Simple rol check (HU19 acceso)
                    const paramsSectionHTML = `
                        <h3>Configuración del Sistema (Épica 10)</h3>
                        <form id="createParamForm">
                            <label for="paramClave">Clave:</label>
                            <input type="text" id="paramClave" required>
                            <label for="paramValor">Valor JSON:</label>
                            <textarea id="paramValor" placeholder='{"periodo":"2025"}'></textarea>
                            <label for="paramScope">Scope:</label>
                            <input type="text" id="paramScope">
                            <button type="submit">Crear Parámetro</button>
                        </form>
                        <div id="paramMessage"></div>
                        <h3>Lista de Parámetros</h3>
                        <ul id="paramList"></ul>
                    `;
                    dashboard.innerHTML += paramsSectionHTML;
                    loadParams();  // Carga inicial lista

                    // Event listener para create form
                    const createParamForm = document.getElementById('createParamForm');
                    createParamForm.addEventListener('submit', (e) => {
                        e.preventDefault();
                        createParam();
                    });
                } else {
                    dashboard.innerHTML += '<p>Acceso restringido: Solo ADMIN para configuración.</p>';
                }

                // ========== FIN NUEVA FUNCIONALIDAD ==========

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

// ========== FUNCIONES PARA GRUPOS (NUEVAS) ==========
// Funciones para grupos
async function createGroup() {
    const nombre = document.getElementById('groupNombre').value;
    const nivel = document.getElementById('groupNivel').value;
    const num = parseInt(document.getElementById('groupNum').value);
    const caracteristicas = document.getElementById('groupCaracteristicas').value;
    const message = document.getElementById('groupMessage');

    if (num <= 0) {
        message.textContent = 'Num. estudiantes debe ser >0';
        message.className = 'error';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/grupos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, nivel, num_estudiantes: num, caracteristicas })
        });
        const data = await response.json();

        if (response.ok) {
            message.textContent = data.message || 'Grupo creado!';
            message.className = 'success';
            document.getElementById('createGroupForm').reset();
            loadGroups();  // Refresca lista
        } else {
            message.textContent = data.error || 'Error al crear';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error de conexión: ' + error.message;
        message.className = 'error';
    }
}

async function loadGroups() {
    try {
        const response = await fetch('http://localhost:8000/grupos');
        const groups = await response.json();
        const list = document.getElementById('groupList');
        list.innerHTML = groups.map(group => `
            <li>
                ${group.nombre} (${group.nivel}) - ${group.num_estudiantes} est. ${group.caracteristicas ? `- ${group.caracteristicas}` : ''} 
                ${group.activo ? '(Activo)' : '(Inactivo)'} 
                <button onclick="updateGroup('${group.id}')">Editar</button>
                <button onclick="deleteGroup('${group.id}')">Desactivar</button>
            </li>
        `).join('');
    } catch (error) {
        console.error('Error loading groups:', error);
    }
}

async function updateGroup(groupId) {
    const num = prompt('Nuevo num. estudiantes (actual: ?)', '');  // Simple prompt para update (HU4)
    if (num && parseInt(num) > 0) {
        try {
            const response = await fetch(`http://localhost:8000/grupos/${groupId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_estudiantes: parseInt(num) })
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('groupMessage').textContent = data.message;
                document.getElementById('groupMessage').className = 'success';
                loadGroups();  // Refresca
            } else {
                document.getElementById('groupMessage').textContent = data.error;
                document.getElementById('groupMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error updating group:', error);
        }
    }
}

async function deleteGroup(groupId) {
    if (confirm('Desactivar grupo?')) {
        try {
            const response = await fetch(`http://localhost:8000/grupos/${groupId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('groupMessage').textContent = data.message;
                document.getElementById('groupMessage').className = 'success';
                loadGroups();  // Refresca
            } else {
                document.getElementById('groupMessage').textContent = data.error;
                document.getElementById('groupMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error deleting group:', error);
        }
    }
}

// ========== FUNCIONES PARA SALONES (NUEVAS) ==========
// Funciones para salones
async function createSalon() {
    const codigo = document.getElementById('salonCodigo').value;
    const capacidad = parseInt(document.getElementById('salonCapacidad').value);
    const ubicacion = document.getElementById('salonUbicacion').value;
    const message = document.getElementById('salonMessage');

    if (capacidad <= 0) {
        message.textContent = 'Capacidad debe ser >0';
        message.className = 'error';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/salones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo, capacidad, ubicacion })
        });
        const data = await response.json();

        if (response.ok) {
            message.textContent = data.message || 'Salón creado!';
            message.className = 'success';
            document.getElementById('createSalonForm').reset();
            loadSalones();  // Refresca lista
        } else {
            message.textContent = data.error || 'Error al crear';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error de conexión: ' + error.message;
        message.className = 'error';
    }
}

async function loadSalones() {
    try {
        const response = await fetch('http://localhost:8000/salones');
        const salones = await response.json();
        const list = document.getElementById('salonList');
        list.innerHTML = salones.map(salon => `
            <li>
                ${salon.codigo} (Cap: ${salon.capacidad}) - ${salon.ubicacion} 
                ${salon.activo ? '(Activo)' : '(Inactivo)'} 
                <button onclick="updateSalon('${salon.id}')">Editar</button>
                <button onclick="deleteSalon('${salon.id}')">Desactivar</button>
            </li>
        `).join('');
    } catch (error) {
        console.error('Error loading salones:', error);
    }
}

async function updateSalon(salonId) {
    const cap = prompt('Nueva capacidad (actual: ?)', '');  // Simple prompt para update (HU6)
    if (cap && parseInt(cap) > 0) {
        try {
            const response = await fetch(`http://localhost:8000/salones/${salonId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ capacidad: parseInt(cap) })
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('salonMessage').textContent = data.message;
                document.getElementById('salonMessage').className = 'success';
                loadSalones();  // Refresca
            } else {
                document.getElementById('salonMessage').textContent = data.error;
                document.getElementById('salonMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error updating salon:', error);
        }
    }
}

async function deleteSalon(salonId) {
    if (confirm('Desactivar salón?')) {
        try {
            const response = await fetch(`http://localhost:8000/salones/${salonId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('salonMessage').textContent = data.message;
                document.getElementById('salonMessage').className = 'success';
                loadSalones();  // Refresca
            } else {
                document.getElementById('salonMessage').textContent = data.error;
                document.getElementById('salonMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error deleting salon:', error);
        }
    }
}
// ========== FIN FUNCIONES SALONES ==========

// ========== FUNCIONES PARA PROFESORES (NUEVAS) ==========
// Funciones para profesores 
async function createProfesor() {
    const usuario_id = document.getElementById('profesorUsuarioId').value;
    const especialidades = document.getElementById('profesorEspecialidades').value;
    const hoja_vida_url = document.getElementById('profesorHojaVida').value;
    const message = document.getElementById('profesorMessage');

    if (!usuario_id) {
        message.textContent = 'Usuario ID requerido';
        message.className = 'error';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/profesores', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario_id, especialidades, hoja_vida_url })
        });
        const data = await response.json();

        if (response.ok) {
            message.textContent = data.message || 'Profesor creado!';
            message.className = 'success';
            document.getElementById('createProfesorForm').reset();
            loadProfesores();  // Refresca lista
        } else {
            message.textContent = data.error || 'Error al crear';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error de conexión: ' + error.message;
        message.className = 'error';
    }
}

async function loadProfesores() {
    try {
        const response = await fetch('http://localhost:8000/profesores');
        const profesores = await response.json();
        const list = document.getElementById('profesorList');
        list.innerHTML = profesores.map(profesor => `
            <li>
                Usuario ID: ${profesor.usuario_id} - Especialidades: ${profesor.especialidades} 
                ${profesor.hoja_vida_url ? `- Hoja: ${profesor.hoja_vida_url}` : ''} 
                ${profesor.activo ? '(Activo)' : '(Inactivo)'} 
                <button onclick="updateProfesor('${profesor.id}')">Editar</button>
                <button onclick="deleteProfesor('${profesor.id}')">Desactivar</button>
            </li>
        `).join('');
    } catch (error) {
        console.error('Error loading profesores:', error);
    }
}

async function updateProfesor(profesorId) {
    const espec = prompt('Nuevas especialidades (actual: ?)', '');  // Simple prompt para update (HU8)
    if (espec) {
        try {
            const response = await fetch(`http://localhost:8000/profesores/${profesorId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ especialidades: espec })
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('profesorMessage').textContent = data.message;
                document.getElementById('profesorMessage').className = 'success';
                loadProfesores();  // Refresca
            } else {
                document.getElementById('profesorMessage').textContent = data.error;
                document.getElementById('profesorMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error updating profesor:', error);
        }
    }
}

async function deleteProfesor(profesorId) {
    if (confirm('Desactivar profesor?')) {
        try {
            const response = await fetch(`http://localhost:8000/profesores/${profesorId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('profesorMessage').textContent = data.message;
                document.getElementById('profesorMessage').className = 'success';
                loadProfesores();  // Refresca
            } else {
                document.getElementById('profesorMessage').textContent = data.error;
                document.getElementById('profesorMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error deleting profesor:', error);
        }
    }
} 
// ========== FIN FUNCIONES PROFESORES ==========

// ========== FUNCIONES PARA PARAMETROS (NUEVAS) ==========
// Funciones para parámetros
async function createParam() {
    const clave = document.getElementById('paramClave').value;
    let valor;
    try {
        valor = JSON.parse(document.getElementById('paramValor').value || '{}');  // Parse JSON o empty
    } catch (e) {
        document.getElementById('paramMessage').textContent = 'Valor debe ser JSON válido';
        document.getElementById('paramMessage').className = 'error';
        return;
    }
    const scope = document.getElementById('paramScope').value;
    const message = document.getElementById('paramMessage');

    if (!clave) {
        message.textContent = 'Clave requerida';
        message.className = 'error';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/parametros', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ clave, valor, scope })
        });
        const data = await response.json();

        if (response.ok) {
            message.textContent = data.message || 'Parámetro creado!';
            message.className = 'success';
            document.getElementById('createParamForm').reset();
            loadParams();  // Refresca lista
        } else {
            message.textContent = data.error || 'Error al crear';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error de conexión: ' + error.message;
        message.className = 'error';
    }
}

async function loadParams() {
    try {
        const response = await fetch('http://localhost:8000/parametros');
        const params = await response.json();
        const list = document.getElementById('paramList');
        list.innerHTML = params.map(param => `
            <li>
                Clave: ${param.clave} - Scope: ${param.scope} - Valor: ${JSON.stringify(param.valor)} 
                ${param.activo ? '(Activo)' : '(Inactivo)'} 
                <button onclick="updateParam('${param.id}')">Editar</button>
                <button onclick="deleteParam('${param.id}')">Desactivar</button>
            </li>
        `).join('');
    } catch (error) {
        console.error('Error loading params:', error);
    }
}

async function updateParam(paramId) {
    const valorStr = prompt('Nuevo valor JSON (actual: ?)', '');  // Simple prompt para update (HU19)
    let valor;
    try {
        valor = JSON.parse(valorStr || '{}');
    } catch (e) {
        document.getElementById('paramMessage').textContent = 'Valor debe ser JSON válido';
        document.getElementById('paramMessage').className = 'error';
        return;
    }
    try {
        const response = await fetch(`http://localhost:8000/parametros/${paramId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ valor })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('paramMessage').textContent = data.message;
            document.getElementById('paramMessage').className = 'success';
            loadParams();  // Refresca
        } else {
            document.getElementById('paramMessage').textContent = data.error;
            document.getElementById('paramMessage').className = 'error';
        }
    } catch (error) {
        console.error('Error updating param:', error);
    }
}

async function deleteParam(paramId) {
    if (confirm('Desactivar parámetro?')) {
        try {
            const response = await fetch(`http://localhost:8000/parametros/${paramId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('paramMessage').textContent = data.message;
                document.getElementById('paramMessage').className = 'success';
                loadParams();  // Refresca
            } else {
                document.getElementById('paramMessage').textContent = data.error;
                document.getElementById('paramMessage').className = 'error';
            }
        } catch (error) {
            console.error('Error deleting param:', error);
        }
    }
}
// ========== FIN FUNCIONES PARAMETROS ==========
