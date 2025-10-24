# Diagrama Entidad-Relación (ERD): Sistema de Asignación de Salones en Notación Moderna

## Descripción General
La **notación moderna** para ERD (como Crow's Foot o IDEF1X) se centra en cardinalidades claras con símbolos de "patas de cuervo" (|| para uno, o{ para muchos) y líneas directas entre entidades, lo que la hace más visual y escalable para bases de datos relacionales. A diferencia de la **notación clásica (Chen)**, que usa rectángulos para entidades, óvalos para atributos y rombos para relaciones (más teórica y verbosa), la moderna es más compacta, intuitiva y orientada a implementación (ej: SQL). 

**¿Hay diferencia?** Sí, pero sutil en Mermaid: `erDiagram` usa Crow's Foot (moderna) por defecto, por lo que el diagrama anterior ya era moderno. Para resaltar la "moderna", lo refino aquí con etiquetas más precisas, agrupaciones visuales (subgraphs implícitos vía orden) y multiplicidades explícitas (ej: "1..*" para uno-a-muchos opcionales). Esto mejora la legibilidad sin cambiar la estructura. Si usáramos Chen puro, requeriría herramientas externas (no Mermaid nativo), resultando en un diagrama más "académico" pero menos práctico para desarrollo.

El diseño mantiene robustez: entidades con PK/FK, relaciones con labels descriptivos y flujo lógico (roles → recursos → gestión). **Corrección aplicada**: Se eliminaron multiplicidades en comillas (causaban error de parse; Mermaid interpreta "1..*" como texto inválido). En su lugar, se usan símbolos estándar (||--o{ para 1:N) y labels descriptivos para precisión (ej: "(1:N)").

## Descripciones por Roles
Cada rol es una subentidad de `USUARIO` (herencia moderna vía FK), con atributos/relaciones específicas. Esto refleja actividades y restricciones del backlog.

- **Administrador**: Gestiona globalmente; relaciona con Reportes/Parámetros (1:N). Atributos: nivel_acceso. Restricciones: Acceso total, audita.
- **Superadministrador**: Exclusivo para IT; integra/monitorea (1:1 con Parámetros). Atributos: api_keys. Restricciones: Verificación doble.
- **Coordinador (General)**: Gestiona Grupos/Asignaciones (1:N). Atributos: especialidad. Restricciones: Dependiente de disponibilidades.
- **Coordinador Académico**: Subtipo; enfocado en Horarios académicos (1:N). Atributos: foco_academico. Restricciones: Sin infra.
- **Coordinador de Infraestructura**: Subtipo; maneja Salones (1:N). Atributos: area_mantenimiento. Restricciones: Solo físicos.
- **Profesor**: Recurso con disponibilidades; imparte Asignaciones (1:N). Atributos: especialidad, hoja_vida. Restricciones: Datos personales.
- **Profesor Invitado**: Temporal; visualiza horarios (1:N). Atributos: fecha_expiracion. Restricciones: Acceso caduco.
- **Secretaria (General)**: Soporte; gestiona Auditorías/Solicitudes (1:N). Atributos: departamento. Restricciones: Edición básica.
- **Secretaria Académica**: Subtipo; registros de Grupos (1:N). Atributos: contacto_familias. Restricciones: No sensibles.
- **Secretaria de Infraestructura**: Subtipo; actualiza Salones (1:N). Atributos: alertas_mantenimiento. Restricciones: Solo infra.

## Diagrama Mermaid (Notación Moderna - Crow's Foot)
```mermaid
erDiagram
    %% Entidad Base Usuario (arriba para flujo visual)
    USUARIO {
        int id PK
        string nombre
        string email
        string password
        string rol
    }

    %% Subentidades/Roles (agrupadas lógicamente)
    ADMINISTRADOR {
        int id PK
        int usuario_id FK
        string nivel_acceso
    }
    SUPERADMINISTRADOR {
        int id PK
        int usuario_id FK
        string api_keys
    }
    COORDINADOR {
        int id PK
        int usuario_id FK
        string especialidad
    }
    COORDINADOR_ACADEMICO {
        int id PK
        int coordinador_id FK
        string foco_academico
    }
    COORDINADOR_INFRAESTRUCTURA {
        int id PK
        int coordinador_id FK
        string area_mantenimiento
    }
    SECRETARIA {
        int id PK
        int usuario_id FK
        string departamento
    }
    SECRETARIA_ACADEMICA {
        int id PK
        int secretaria_id FK
        string contacto_familias
    }
    SECRETARIA_INFRAESTRUCTURA {
        int id PK
        int secretaria_id FK
        string alertas_mantenimiento
    }
    PROFESOR {
        int id PK
        int usuario_id FK
        string especialidad
        string hoja_vida
    }
    PROFESOR_INVITADO {
        int id PK
        int profesor_id FK
        date fecha_expiracion
    }

    %% Entidades de Recursos (medio)
    GRUPO {
        int id PK
        string nombre
        int nivel
        int numEstudiantes
        string caracteristicas
        int coordinador_id FK
    }
    SALON {
        int id PK
        int capacidad
        string recursos
        string ubicacion
        int coordinador_infra_id FK
    }

    %% Entidades de Gestión (abajo)
    ASIGNACION {
        int id PK
        date fecha
        int grupo_id FK
        int salon_id FK
        int profesor_id FK
        int horario_id FK
    }
    HORARIO {
        int id PK
        date periodo
        int coordinador_id FK
    }
    REPORTE {
        int id PK
        string tipo
        date fechaGeneracion
        int admin_id FK
    }
    RESTRICCION {
        int id PK
        string tipo
        string descripcion
        int asignacion_id FK
        int coordinador_id FK
    }
    AUDITORIA {
        int id PK
        date timestamp
        string accion
        int usuario_id FK
    }
    PARAMETRO {
        string clave PK
        string valor
        int admin_id FK
    }

    %% Relaciones Herencia (1:N para subtipos, moderna y clara)
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

    %% Relaciones Rol-Recurso/Gestión (flujo descendente)
    COORDINADOR ||--o{ GRUPO : "gestiona (1:N)"
    COORDINADOR_INFRAESTRUCTURA ||--o{ SALON : "gestiona (1:N)"
    COORDINADOR ||--o{ HORARIO : "aprueba (1:N)"
    ADMINISTRADOR ||--o{ REPORTE : "genera (1:N)"
    COORDINADOR ||--o{ RESTRICCION : "establece (1:N)"
    USUARIO ||--o{ AUDITORIA : "registra (1:N)"
    ADMINISTRADOR ||--o{ PARAMETRO : "configura (1:N)"

    %% Relaciones Gestión (centrales, con N:M si aplica)
    GRUPO ||--o{ ASIGNACION : "participa (1:N)"
    SALON ||--o{ ASIGNACION : "asignado (1:N)"
    PROFESOR ||--o{ ASIGNACION : "imparte (1:N)"
    HORARIO ||--o{ ASIGNACION : "contiene (1:N)"
    ASIGNACION ||--o{ RESTRICCION : "sujeta (1:N)"

    %% Notas para robustez y visual
    %% PK: Clave Primaria | FK: Clave Foránea
    %% Cardinalidades: ||--o{ (uno a muchos) | ||--|| (uno a uno)
    %% Flujo: Roles (arriba) → Recursos (medio) → Gestión (abajo) para intuición.
