# Diagrama de Modelo Relacional: Sistema de Asignación de Salones

## Descripción General
El **Modelo Relacional** representa la implementación física del ERD en tablas de base de datos relacionales (ej: SQL), con énfasis en claves primarias (PK), claves foráneas (FK), índices y restricciones de integridad. Basado en el ERD moderno previo, este diagrama usa notación Mermaid (`erDiagram`) para mostrar tablas como entidades, atributos con tipos/detalles (PK/FK destacados) y relaciones con cardinalidades (Crow's Foot). 

Para robustez, se aplica normalización 3NF (evitando redundancias, ej: roles como tablas separadas con FK a USUARIO), triggers implícitos para auditoría y vistas sugeridas para reportes. Visualmente, tablas agrupadas (roles arriba, recursos medio, gestión abajo) con relaciones etiquetadas para flujo claro (L→R). Esto facilita la generación de scripts SQL (ej: CREATE TABLE) y asegura escalabilidad (ej: índices en FK para joins rápidos).

**Corrección aplicada**: Se simplificaron definiciones de atributos para compatibilidad con Mermaid (eliminando constraints inline como "NOT NULL" o enums detallados, que causaban errores de parse). Constraints se mueven a notas por tabla. Esto mantiene la robustez sin romper el renderizado.

Diferencia con ERD: Más orientado a BD (tipos de datos explícitos, constraints como NOT NULL), menos abstracto.

## Descripciones por Roles (en Tablas Relacionales)
Cada rol se modela como tabla hija de `USUARIO` (FK para herencia), con atributos/relaciones específicas. Restricciones se implementan vía CHECK constraints o triggers.

- **Administrador**: Tabla para acceso global; FK a USUARIO, relaciona con REPORTE/PARAMETRO (1:N). Constraints: nivel_acceso = 'alto' (CHECK).
- **Superadministrador**: Tabla exclusiva; FK a USUARIO, 1:1 con PARAMETRO. Constraints: api_keys ENCRYPTED (via app logic).
- **Coordinador (General)**: Tabla para gestión; FK a USUARIO, 1:N con GRUPO/HORARIO. Constraints: especialidad NOT NULL.
- **Coordinador Académico**: Subtabla; FK a COORDINADOR, 1:N con HORARIO. Constraints: foco_academico IN ('acad1', 'acad2').
- **Coordinador de Infraestructura**: Subtabla; FK a COORDINADOR, 1:N con SALON. Constraints: area_mantenimiento NOT NULL.
- **Profesor**: Tabla recurso; FK a USUARIO, 1:N con ASIGNACION. Constraints: hoja_vida TEXT, especialidad UNIQUE.
- **Profesor Invitado**: Subtabla; FK a PROFESOR, temporal. Constraints: fecha_expiracion > CURRENT_DATE (CHECK).
- **Secretaria (General)**: Tabla soporte; FK a USUARIO, 1:N con AUDITORIA. Constraints: departamento IN ('acad', 'infra').
- **Secretaria Académica**: Subtabla; FK a SECRETARIA, 1:N con GRUPO. Constraints: contacto_familias EMAIL (CHECK).
- **Secretaria de Infraestructura**: Subtabla; FK a SECRETARIA, 1:N con SALON. Constraints: alertas_mantenimiento BOOLEAN DEFAULT TRUE.

## Diagrama Mermaid (Modelo Relacional - Tablas con Relaciones)
```mermaid
erDiagram
    %% Tabla Base Usuario (arriba)
    USUARIO {
        int id PK
        string nombre
        string email
        string password
        string rol
    }
    note for USUARIO "Constraints: email UNIQUE, password HASHED, rol ENUM('admin','superadmin','coord','prof','sec')"

    %% Tablas de Roles (agrupadas)
    ADMINISTRADOR {
        int id PK
        int usuario_id FK
        string nivel_acceso
    }
    note for ADMINISTRADOR "Constraints: nivel_acceso ENUM('bajo','medio','alto') DEFAULT 'medio'"

    SUPERADMINISTRADOR {
        int id PK
        int usuario_id FK
        string api_keys
    }
    note for SUPERADMINISTRADOR "Constraints: api_keys ENCRYPTED"

    COORDINADOR {
        int id PK
        int usuario_id FK
        string especialidad
    }
    note for COORDINADOR "Constraints: especialidad NOT NULL"

    COORDINADOR_ACADEMICO {
        int id PK
        int coordinador_id FK
        string foco_academico
    }
    note for COORDINADOR_ACADEMICO "Constraints: foco_academico NOT NULL"

    COORDINADOR_INFRAESTRUCTURA {
        int id PK
        int coordinador_id FK
        string area_mantenimiento
    }
    note for COORDINADOR_INFRAESTRUCTURA "Constraints: area_mantenimiento NOT NULL"

    SECRETARIA {
        int id PK
        int usuario_id FK
        string departamento
    }
    note for SECRETARIA "Constraints: departamento ENUM('acad','infra','gen') NOT NULL"

    SECRETARIA_ACADEMICA {
        int id PK
        int secretaria_id FK
        string contacto_familias
    }
    note for SECRETARIA_ACADEMICA "Constraints: contacto_familias EMAIL CHECK"

    SECRETARIA_INFRAESTRUCTURA {
        int id PK
        int secretaria_id FK
        boolean alertas_mantenimiento
    }
    note for SECRETARIA_INFRAESTRUCTURA "Constraints: DEFAULT TRUE"

    PROFESOR {
        int id PK
        int usuario_id FK
        string especialidad
        text hoja_vida
    }
    note for PROFESOR "Constraints: especialidad UNIQUE"

    PROFESOR_INVITADO {
        int id PK
        int profesor_id FK
        date fecha_expiracion
    }
    note for PROFESOR_INVITADO "Constraints: fecha_expiracion > CURRENT_DATE CHECK"

    %% Tablas de Recursos (medio)
    GRUPO {
        int id PK
        string nombre
        int nivel
        int numEstudiantes
        string caracteristicas
        int coordinador_id FK
    }
    note for GRUPO "Constraints: numEstudiantes > 0, INDEX on coordinador_id"

    SALON {
        int id PK
        int capacidad
        string recursos
        string ubicacion
        int coordinador_infra_id FK
    }
    note for SALON "Constraints: capacidad > 0, INDEX on coordinador_infra_id"

    %% Tablas de Gestión (abajo)
    ASIGNACION {
        int id PK
        date fecha
        int grupo_id FK
        int salon_id FK
        int profesor_id FK
        int horario_id FK
    }
    note for ASIGNACION "Constraints: UNIQUE (grupo_id, fecha), ON DELETE RESTRICT"

    HORARIO {
        int id PK
        date periodo
        int coordinador_id FK
    }
    note for HORARIO "Constraints: INDEX on periodo"

    REPORTE {
        int id PK
        string tipo
        datetime fechaGeneracion
        int admin_id FK
    }
    note for REPORTE "Constraints: tipo ENUM('uso_recursos','estadisticas'), DEFAULT CURRENT_TIMESTAMP"

    RESTRICCION {
        int id PK
        string tipo
        string descripcion
        int asignacion_id FK
        int coordinador_id FK
    }
    note for RESTRICCION "Constraints: tipo ENUM('capacidad','horario'), ON DELETE CASCADE"

    AUDITORIA {
        int id PK
        datetime timestamp
        string accion
        int usuario_id FK
    }
    note for AUDITORIA "Constraints: accion ENUM('create','update','delete'), TRIGGER AFTER ops"

    PARAMETRO {
        string clave PK
        string valor
        int admin_id FK
    }
    note for PARAMETRO "Constraints: valor NOT NULL"

    %% Relaciones (con constraints para integridad)
    USUARIO ||--o{ ADMINISTRADOR : "es (1:N)"
    USUARIO ||--|| SUPERADMINISTRADOR : "es (1:1)"
    USUARIO ||--o{ COORDINADOR : "es (1:N)"
    COORDINADOR ||--o{ COORDINADOR_ACADEMICO : "especializa (1:N)"
    COORDINADOR ||--o{ COORDINADOR_INFRAESTRUCTURA : "especializa (1:N)"
    USUARIO ||--o{ SECRETARIA : "es (1:N)"
    SECRETARIA ||--o{ SECRETARIA_ACADEMICA : "especializa (1:N)"
    SECRETARIA ||--o{ SECRETARIA_INFRAESTRUCTURA : "especializa (1:N)"
    USUARIO ||--o{ PROFESOR : "es (1:N)"
    PROFESOR ||--o{ PROFESOR_INVITADO : "especializa (1:N)"

    COORDINADOR ||--o{ GRUPO : "gestiona (1:N)"
    COORDINADOR_INFRAESTRUCTURA ||--o{ SALON : "gestiona (1:N)"
    COORDINADOR ||--o{ HORARIO : "aprueba (1:N)"
    ADMINISTRADOR ||--o{ REPORTE : "genera (1:N)"
    COORDINADOR ||--o{ RESTRICCION : "establece (1:N)"
    USUARIO ||--o{ AUDITORIA : "registra (1:N)"
    ADMINISTRADOR ||--o{ PARAMETRO : "configura (1:N)"

    GRUPO ||--o{ ASIGNACION : "participa (1:N)"
    SALON ||--o{ ASIGNACION : "asignado (1:N)"
    PROFESOR ||--o{ ASIGNACION : "imparte (1:N)"
    HORARIO ||--o{ ASIGNACION : "contiene (1:N)"
    ASIGNACION ||--o{ RESTRICCION : "sujeta (1:N)"

    %% Notas para implementación
    %% Ej: VIEW v_horarios AS SELECT * FROM HORARIO JOIN ASIGNACION ON ...
    %% Constraints: FOREIGN KEY... ON DELETE CASCADE/RESTRICT para integridad.
    %% Índices: Para queries frecuentes (ej: por fecha en ASIGNACION).
