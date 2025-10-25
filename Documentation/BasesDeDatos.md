---
# SCRIPT SQL COMPLETO: Sistema de Asignación de Salones
- Fecha: 24 de Octubre de 2025
- Motor: MySQL 8.0+
---

### 1. Crear y Usar Base de Datos
```sql
CREATE DATABASE IF NOT EXISTS sistema_asignacion_salones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_asignacion_salones;
```

### 2. Tablas Auxiliares para Épica 8 (Conflictos y Sugerencias - HU16-17)
```sql
CREATE TABLE CONFLICTOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asignacion_id INT,
    tipo_conflicto ENUM('sobrecupo', 'horario_colision', 'disponibilidad_prof', 'restriccion_uso') NOT NULL,
    descripcion TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asignacion_id) REFERENCES ASIGNACION(id) ON DELETE CASCADE,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE SUGERENCIAS_ALTERNATIVAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conflicto_id INT,
    sugerencia TEXT NOT NULL COMMENT 'Ej: Salon alternativo: ID X',
    prioridad INT DEFAULT 1 CHECK (prioridad BETWEEN 1 AND 5),
    FOREIGN KEY (conflicto_id) REFERENCES CONFLICTOS(id) ON DELETE CASCADE,
    INDEX idx_prioridad (prioridad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3. Tablas Principales
- **Tabla Base: USUARIO** (Épica 1: HU1-2)
```sql
CREATE TABLE USUARIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL COMMENT 'Hasheado con bcrypt',
    rol ENUM('admin', 'superadmin', 'coord', 'prof', 'sec') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **ADMINISTRADOR** (Épica 1, HU15)
```sql
CREATE TABLE ADMINISTRADOR (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nivel_acceso ENUM('bajo', 'medio', 'alto') DEFAULT 'medio' NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **SUPERADMINISTRADOR** (Épica 10: HU19)
```sql
CREATE TABLE SUPERADMINISTRADOR (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,  -- 1:1
    api_keys TEXT COMMENT 'Encriptado',
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **COORDINADOR** (Épicas 2,4,5,6,8)
```sql
CREATE TABLE COORDINADOR (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    especialidad VARCHAR(50) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **COORDINADOR_ACADEMICO** (subtipo, Épica 2,4)
```sql
CREATE TABLE COORDINADOR_ACADEMICO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coordinador_id INT NOT NULL,
    foco_academico VARCHAR(50) NOT NULL CHECK (foco_academico IN ('basico', 'avanzado', 'especial')),
    FOREIGN KEY (coordinador_id) REFERENCES COORDINADOR(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **COORDINADOR_INFRAESTRUCTURA** (subtipo, Épica 3)
```sql
CREATE TABLE COORDINADOR_INFRAESTRUCTURA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coordinador_id INT NOT NULL,
    area_mantenimiento VARCHAR(50) NOT NULL,
    FOREIGN KEY (coordinador_id) REFERENCES COORDINADOR(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **SECRETARIA** (Épica 1,9)
```sql
CREATE TABLE SECRETARIA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    departamento ENUM('acad', 'infra', 'gen') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **SECRETARIA_ACADEMICA** (subtipo, Épica 2)
```sql
CREATE TABLE SECRETARIA_ACADEMICA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    secretaria_id INT NOT NULL,
    contacto_familias VARCHAR(100) CHECK (contacto_familias LIKE '%@%.%'),
    FOREIGN KEY (secretaria_id) REFERENCES SECRETARIA(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **SECRETARIA_INFRAESTRUCTURA** (subtipo, Épica 3)
```sql
CREATE TABLE SECRETARIA_INFRAESTRUCTURA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    secretaria_id INT NOT NULL,
    alertas_mantenimiento BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (secretaria_id) REFERENCES SECRETARIA(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **PROFESOR** (Épica 4: HU7-8)
```sql
CREATE TABLE PROFESOR (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    especialidad VARCHAR(50) UNIQUE NOT NULL,
    hoja_vida TEXT,
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **PROFESOR_INVITADO** (subtipo, Épica 4)
```sql
CREATE TABLE PROFESOR_INVITADO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesor_id INT NOT NULL,
    fecha_expiracion DATE NOT NULL CHECK (fecha_expiracion > CURDATE()),
    FOREIGN KEY (profesor_id) REFERENCES PROFESOR(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **GRUPO** (Épica 2: HU3-4)
```sql
CREATE TABLE GRUPO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    nivel INT DEFAULT 1 CHECK (nivel >= 1),
    numEstudiantes INT NOT NULL CHECK (numEstudiantes > 0),
    caracteristicas TEXT,
    coordinador_id INT NOT NULL,
    FOREIGN KEY (coordinador_id) REFERENCES COORDINADOR(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_coordinador (coordinador_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **SALON** (Épica 3: HU5-6)
```sql
CREATE TABLE SALON (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    recursos TEXT,
    ubicacion VARCHAR(50) NOT NULL,
    coordinador_infra_id INT NOT NULL,
    FOREIGN KEY (coordinador_infra_id) REFERENCES COORDINADOR_INFRAESTRUCTURA(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_infra (coordinador_infra_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **ASIGNACION** (Épicas 5-6,8: HU9-12,16-17)
```sql
CREATE TABLE ASIGNACION (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    grupo_id INT NOT NULL,
    salon_id INT NOT NULL,
    profesor_id INT NOT NULL,
    horario_id INT NOT NULL,
    FOREIGN KEY (grupo_id) REFERENCES GRUPO(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (salon_id) REFERENCES SALON(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES PROFESOR(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (horario_id) REFERENCES HORARIO(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY uk_asignacion (grupo_id, fecha),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **HORARIO** (Épica 7: HU13)
```sql
CREATE TABLE HORARIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    periodo DATE NOT NULL,
    coordinador_id INT NOT NULL,
    FOREIGN KEY (coordinador_id) REFERENCES COORDINADOR(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_periodo (periodo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **REPORTE** (Épica 7: HU15)
```sql
CREATE TABLE REPORTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('uso_recursos', 'estadisticas') NOT NULL,
    fechaGeneracion DATETIME DEFAULT CURRENT_TIMESTAMP,
    admin_id INT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES ADMINISTRADOR(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **RESTRICCION** (Épica 8: HU17)
```sql
CREATE TABLE RESTRICCION (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('capacidad', 'horario') NOT NULL,
    descripcion TEXT,
    asignacion_id INT,
    coordinador_id INT NOT NULL,
    es_activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (asignacion_id) REFERENCES ASIGNACION(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (coordinador_id) REFERENCES COORDINADOR(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **AUDITORIA** (Épica 9: HU18)
```sql
CREATE TABLE AUDITORIA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    accion ENUM('create', 'update', 'delete') NOT NULL,
    usuario_id INT NOT NULL,
    tabla_afectada VARCHAR(50),
    descripcion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES USUARIO(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

- **PARAMETRO** (Épica 10: HU19)
```sql
CREATE TABLE PARAMETRO (
    clave VARCHAR(50) PRIMARY KEY,
    valor TEXT NOT NULL,
    admin_id INT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES ADMINISTRADOR(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4. Triggers (Expandidos para Todas las Épicas/HU)
```sql
DELIMITER //
-- Épica 1: Auditoría en USUARIO
CREATE TRIGGER trg_usuario_insert AFTER INSERT ON USUARIO FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.id, 'create', 'USUARIO', CONCAT('Nueva cuenta: ', NEW.email));
END //

CREATE TRIGGER trg_usuario_update AFTER UPDATE ON USUARIO FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.id, 'update', 'USUARIO', CONCAT('Cuenta actualizada: ', NEW.email));
END //

CREATE TRIGGER trg_usuario_delete AFTER DELETE ON USUARIO FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (OLD.id, 'delete', 'USUARIO', CONCAT('Cuenta eliminada: ', OLD.email));
END //

-- Épica 2: En GRUPO
CREATE TRIGGER trg_grupo_insert AFTER INSERT ON GRUPO FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.coordinador_id, 'create', 'GRUPO', CONCAT('Grupo creado: ', NEW.nombre));
END //

CREATE TRIGGER trg_grupo_update AFTER UPDATE ON GRUPO FOR EACH ROW
BEGIN
    IF OLD.numEstudiantes != NEW.numEstudiantes THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cambio numEstudiantes requiere revisión (HU4)';
    END IF;
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.coordinador_id, 'update', 'GRUPO', CONCAT('Grupo actualizado: ', NEW.nombre));
END //

-- Épica 3: En SALON
CREATE TRIGGER trg_salon_insert AFTER INSERT ON SALON FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.coordinador_infra_id, 'create', 'SALON', CONCAT('Salón creado: ', NEW.ubicacion));
END //

CREATE TRIGGER trg_salon_update BEFORE UPDATE ON SALON FOR EACH ROW
BEGIN
    DECLARE v_num_est INT DEFAULT 0;
    SELECT SUM(g.numEstudiantes) INTO v_num_est FROM ASIGNACION a JOIN GRUPO g ON a.grupo_id = g.id WHERE a.salon_id = OLD.id;
    IF v_num_est > NEW.capacidad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sobrecupo al actualizar capacidad (HU6)';
    END IF;
END //

CREATE TRIGGER trg_salon_update_audit AFTER UPDATE ON SALON FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.coordinador_infra_id, 'update', 'SALON', CONCAT('Salón actualizado: ', NEW.ubicacion));
END //

-- Épica 4: En PROFESOR
CREATE TRIGGER trg_profesor_insert AFTER INSERT ON PROFESOR FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.usuario_id, 'create', 'PROFESOR', CONCAT('Profesor creado: ', NEW.especialidad));
END //

CREATE TRIGGER trg_profesor_update BEFORE UPDATE ON PROFESOR FOR EACH ROW
BEGIN
    DECLARE v_colision INT DEFAULT 0;
    SELECT COUNT(*) INTO v_colision FROM ASIGNACION WHERE profesor_id = OLD.id AND fecha IN (SELECT fecha FROM ASIGNACION WHERE profesor_id != OLD.id);
    IF v_colision > 0 AND NEW.especialidad != OLD.especialidad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Colisión en disponibilidades al cambiar especialidad (HU8)';
    END IF;
END //

-- Épicas 5-6,8: En ASIGNACION (HU9-12,16-17)
CREATE TRIGGER trg_asignacion_insert_before BEFORE INSERT ON ASIGNACION FOR EACH ROW
BEGIN
    DECLARE v_num_est INT DEFAULT 0;
    DECLARE v_cap INT DEFAULT 0;
    DECLARE v_colision INT DEFAULT 0;

    SELECT numEstudiantes INTO v_num_est FROM GRUPO WHERE id = NEW.grupo_id;
    SELECT capacidad INTO v_cap FROM SALON WHERE id = NEW.salon_id;
    IF v_num_est > v_cap THEN
        INSERT INTO CONFLICTOS (asignacion_id, tipo_conflicto, descripcion) VALUES (0, 'sobrecupo', CONCAT('Sobrecupo: ', v_num_est, ' > ', v_cap));
        INSERT INTO SUGERENCIAS_ALTERNATIVAS (sugerencia, prioridad) VALUES ('Usar salón con mayor capacidad', 1);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Conflicto sobrecupo (HU16)';
    END IF;

    SELECT COUNT(*) INTO v_colision FROM ASIGNACION WHERE profesor_id = NEW.profesor_id AND fecha = NEW.fecha;
    IF v_colision > 0 THEN
        INSERT INTO CONFLICTOS (asignacion_id, tipo_conflicto, descripcion) VALUES (0, 'horario_colision', 'Profesor ocupado en fecha');
        INSERT INTO SUGERENCIAS_ALTERNATIVAS (sugerencia, prioridad) VALUES ('Cambiar fecha o profesor', 2);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Colisión horario (HU12)';
    END IF;

    IF EXISTS (SELECT 1 FROM RESTRICCION r WHERE r.asignacion_id IS NULL AND r.tipo = 'horario' AND r.descripcion LIKE CONCAT('%', NEW.fecha, '%')) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Restricción horaria activa (HU17)';
    END IF;
END //

CREATE TRIGGER trg_asignacion_insert_after AFTER INSERT ON ASIGNACION FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES ((SELECT usuario_id FROM PROFESOR WHERE id = NEW.profesor_id), 'create', 'ASIGNACION', CONCAT('Asignación creada: ID ', NEW.id));
END //

CREATE TRIGGER trg_asignacion_update_before BEFORE UPDATE ON ASIGNACION FOR EACH ROW
BEGIN
    DECLARE v_num_est INT DEFAULT 0;
    DECLARE v_cap INT DEFAULT 0;

    SELECT numEstudiantes INTO v_num_est FROM GRUPO WHERE id = NEW.grupo_id;
    SELECT capacidad INTO v_cap FROM SALON WHERE id = NEW.salon_id;

    IF v_num_est > v_cap THEN
        INSERT INTO CONFLICTOS (asignacion_id, tipo_conflicto, descripcion) VALUES (NEW.id, 'sobrecupo', CONCAT('Sobrecupo al actualizar: ', v_num_est, ' > ', v_cap));
        INSERT INTO SUGERENCIAS_ALTERNATIVAS (sugerencia, prioridad) VALUES ('Reasignar salón mayor', 1);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Conflicto sobrecupo al actualizar (HU12)';
    END IF;

    DECLARE v_param_prox VARCHAR(10) DEFAULT '0';
    SELECT valor INTO v_param_prox FROM PARAMETRO WHERE clave = 'prioridad_proximidad';
    IF CAST(v_param_prox AS UNSIGNED) > 0 AND (SELECT ubicacion FROM SALON WHERE id = NEW.salon_id) NOT LIKE (SELECT ubicacion FROM SALON WHERE id = OLD.salon_id) THEN
        INSERT INTO CONFLICTOS (asignacion_id, tipo_conflicto, descripcion) VALUES (NEW.id, 'proximidad', 'Salón no próximo (HU10)');
    END IF;
END //

CREATE TRIGGER trg_asignacion_update_after AFTER UPDATE ON ASIGNACION FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES ((SELECT usuario_id FROM PROFESOR WHERE id = NEW.profesor_id), 'update', 'ASIGNACION', CONCAT('Asignación actualizada: ID ', NEW.id));
END //

CREATE TRIGGER trg_asignacion_delete_after AFTER DELETE ON ASIGNACION FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (OLD.profesor_id, 'delete', 'ASIGNACION', CONCAT('Asignación eliminada: ID ', OLD.id));
END //

-- Épica 10: En PARAMETRO
CREATE TRIGGER trg_parametro_update BEFORE UPDATE ON PARAMETRO FOR EACH ROW
BEGIN
    IF NEW.clave = 'periodo_academico' AND NEW.valor NOT REGEXP '^[0-9]{4}-[0-9]{4}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Formato inválido período (HU19)';
    END IF;
END //

CREATE TRIGGER trg_parametro_insert_after AFTER INSERT ON PARAMETRO FOR EACH ROW
BEGIN
    INSERT INTO AUDITORIA (usuario_id, accion, tabla_afectada, descripcion)
    VALUES (NEW.admin_id, 'create', 'PARAMETRO', CONCAT('Parámetro creado: ', NEW.clave));
END //
DELIMITER ;
```

### 5. Vistas (Épica 7: HU13-15)
```sql
CREATE VIEW v_horario_semestral AS
SELECT h.periodo, a.fecha, g.nombre AS grupo, s.ubicacion AS salon, p.especialidad AS profesor
FROM HORARIO h JOIN ASIGNACION a ON h.id = a.horario_id
JOIN GRUPO g ON a.grupo_id = g.id JOIN SALON s ON a.salon_id = s.id JOIN PROFESOR p ON a.profesor_id = p.id
ORDER BY h.periodo, a.fecha;

CREATE VIEW v_horario_personal AS
SELECT u.nombre AS usuario, p.especialidad, a.fecha, s.ubicacion AS salon, g.nombre AS grupo
FROM USUARIO u JOIN PROFESOR p ON u.id = p.usuario_id JOIN ASIGNACION a ON p.id = a.profesor_id
JOIN SALON s ON a.salon_id = s.id JOIN GRUPO g ON a.grupo_id = g.id
ORDER BY a.fecha;  -- Filtrar por profesor en app

CREATE VIEW v_reporte_utilizacion AS
SELECT s.ubicacion, COUNT(a.id) AS num_asignaciones, AVG(g.numEstudiantes) AS avg_estudiantes
FROM SALON s LEFT JOIN ASIGNACION a ON s.id = a.salon_id LEFT JOIN GRUPO g ON a.grupo_id = g.id
GROUP BY s.id;
```

### 6. Datos de Prueba (Todos los Roles + Expandidos)
```sql
-- Usuarios Base
INSERT INTO USUARIO (nombre, email, password, rol) VALUES 
('Admin Principal', 'admin1@edu.com', SHA2('adminpass', 256), 'admin'),
('Admin Soporte', 'admin2@edu.com', SHA2('adminpass', 256), 'admin'),
('Super Admin IT', 'superadmin@edu.com', SHA2('superpass', 256), 'superadmin'),
('Coord General', 'coord_gen@edu.com', SHA2('coordpass', 256), 'coord'),
('Coord General 2', 'coord_gen2@edu.com', SHA2('coordpass', 256), 'coord'),
('Sec General', 'sec_gen@edu.com', SHA2('secpass', 256), 'sec'),
('Sec General 2', 'sec_gen2@edu.com', SHA2('secpass', 256), 'sec'),
('Prof Matematicas', 'prof_math@edu.com', SHA2('profpass', 256), 'prof'),
('Prof Fisica', 'prof_phys@edu.com', SHA2('profpass', 256), 'prof'),
('Prof Quimica', 'prof_chem@edu.com', SHA2('profpass', 256), 'prof');

-- Administrador
INSERT INTO ADMINISTRADOR (usuario_id, nivel_acceso) VALUES (1, 'alto'), (2, 'medio');

-- Superadministrador
INSERT INTO SUPERADMINISTRADOR (usuario_id, api_keys) VALUES (3, 'api_key_encrypted_123');

-- Coordinador General
INSERT INTO COORDINADOR (usuario_id, especialidad) VALUES (4, 'Académica'), (5, 'General');

-- Coordinador Académico
INSERT INTO COORDINADOR_ACADEMICO (coordinador_id, foco_academico) VALUES (1, 'basico'), (2, 'avanzado');

-- Coordinador Infraestructura
INSERT INTO COORDINADOR_INFRAESTRUCTURA (coordinador_id, area_mantenimiento) VALUES (1, 'Edificios'), (2, 'Mantenimiento');

-- Secretaria General
INSERT INTO SECRETARIA (usuario_id, departamento) VALUES (6, 'acad'), (7, 'infra');

-- Secretaria Académica
INSERT INTO SECRETARIA_ACADEMICA (secretaria_id, contacto_familias) VALUES (1, 'fam@edu.com'), (2, 'acad_contact@edu.com');

-- Secretaria Infraestructura
INSERT INTO SECRETARIA_INFRAESTRUCTURA (secretaria_id, alertas_mantenimiento) VALUES (2, TRUE);

-- Profesor
INSERT INTO PROFESOR (usuario_id, especialidad, hoja_vida) VALUES 
(8, 'Matemáticas', 'CV álgebra'),
(9, 'Física', 'CV mecánica'),
(10, 'Química', 'CV orgánica');

-- Profesor Invitado
INSERT INTO PROFESOR_INVITADO (profesor_id, fecha_expiracion) VALUES (1, '2025-12-31'), (2, '2025-06-30'), (3, '2025-09-30');

-- Recursos
INSERT INTO GRUPO (nombre, nivel, numEstudiantes, caracteristicas, coordinador_id) VALUES 
('Mat A', 1, 20, 'Básico', 1),
('Fis B', 2, 25, 'Avanzado', 2),
('Quim C', 1, 15, 'Intro', 1);

INSERT INTO SALON (capacidad, recursos, ubicacion, coordinador_infra_id) VALUES 
(30, 'Proyector', 'A-101', 1),
(40, 'PCs', 'B-202', 2),
(25, 'Pizarra', 'C-303', 1);

-- Gestión
INSERT INTO HORARIO (periodo, coordinador_id) VALUES ('2025-01', 1), ('2025-02', 2), ('2025-03', 1);

INSERT INTO ASIGNACION (fecha, grupo_id, salon_id, profesor_id, horario_id) VALUES 
('2025-01-15', 1, 1, 1, 1),
('2025-02-20', 2, 2, 2, 2),
('2025-03-10', 3, 3, 3, 3);

INSERT INTO REPORTE (tipo, admin_id) VALUES ('uso_recursos', 1), ('estadisticas', 2);

INSERT INTO RESTRICCION (tipo, descripcion, asignacion_id, coordinador_id) VALUES 
('capacidad', 'Máx 25', 1, 1),
('horario', 'No viernes PM', 2, 2);

INSERT INTO PARAMETRO (clave, valor, admin_id) VALUES 
('dias_laborables', 'Lun-Vie', 1),
('periodo_academico', '2025-2026', 2);

-- Prueba Conflicto (HU16: Sobrecupo)
INSERT INTO GRUPO (nombre, nivel, numEstudiantes, caracteristicas, coordinador_id) VALUES ('Test Sobrecupo', 1, 45, 'Test', 1);
-- Al asignar a salón cap 30, trigger disparará SIGNAL y log en CONFLICTOS
```

### 7. Queries de Verificación
```sql
SELECT 'Tablas creadas' AS status;
SHOW TABLES;
SELECT * FROM USUARIO;  -- Ver roles
SELECT * FROM v_horario_semestral;  -- HU13
SELECT COUNT(*) FROM CONFLICTOS;  -- Ver si hay conflictos

-- Fin
SELECT 'Script SQL completo ejecutado. Sistema listo para uso.' AS status;
```
