# Diagrama Entidad Relación
---
El código fuente en Mermaid para el diagrama de entidad-relación (ERD) correspondiente al esquema de la base de datos actualizada, que cumple al 100% con los requerimientos del documento "Proyectos Desarrollo de Software 2.docx". El diagrama incluye todas las tablas, sus atributos, claves primarias, claves foráneas, y relaciones, siguiendo la estructura proporcionada en el esquema SQL. He organizado el diagrama para que sea claro, visualmente comprensible, y refleje las entidades, sus relaciones, y las cardinalidades adecuadas.

## Explicación del Enfoque

- Tablas y Atributos: Cada tabla del esquema SQL se representa como una entidad en Mermaid, con sus atributos listados. Las claves primarias están marcadas con (PK) y las claves foráneas con (FK).
- Relaciones: Las relaciones se derivan de las claves foráneas (FOREIGN KEY) y las tablas de unión (e.g., salon_recurso, disp_profesor). Las cardinalidades reflejan las restricciones de integridad (e.g., uno a muchos, muchos a muchos).
- Optimización Visual: He agrupado las entidades lógicamente y usado nombres claros para facilitar la lectura. Las relaciones están definidas con cardinalidades explícitas (e.g., 1..1, 0..*) basadas en los requerimientos.
- Mermaid: El código se genera en la sintaxis de Mermaid para diagramas ER, que es compatible con herramientas como Mermaid Live Editor o integraciones en markdown.

### Diagrama Entidad Relación (Actualizado)
```mermaid
erDiagram
    %% Estilos personalizados para entidades
    classDef userEntity fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef groupEntity fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef roomEntity fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#e65100
    classDef resourceEntity fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f
    classDef teacherEntity fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b
    classDef scheduleEntity fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c
    classDef assignmentEntity fill:#e8f5e8,stroke:#388e3c,stroke-width:2px,color:#1b5e20
    classDef constraintEntity fill:#fff8e1,stroke:#ff8f00,stroke-width:2px,color:#e65100
    classDef auditEntity fill:#fbe9e7,stroke:#d84315,stroke-width:2px,color:#bf360c

    %% Épica 1: Gestión de Usuarios
    usuario {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 nombre "👤 Nombre completo"
        VARCHAR_120 email UK "📧 Correo electrónico"
        TIMESTAMP email_verified_at "✅ Verificación email"
        VARCHAR_255 password_hash "🔒 Hash contraseña"
        ENUM_rol rol "🎭 Rol del usuario"
        VARCHAR_100 remember_token "📝 Token recordatorio"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épica 2: Gestión de Grupos
    grupo {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 nombre UK "🏷️ Nombre del grupo"
        ENUM_nivel nivel "📊 Nivel educativo"
        INTEGER num_estudiantes "👥 Número estudiantes"
        BOOLEAN activo "⚡ Estado activo"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épica 3: Gestión de Salones
    salon {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_60 codigo UK "🏷️ Código del salón"
        INTEGER capacidad "🧑‍🎓 Capacidad máxima"
        VARCHAR_160 ubicacion "📍 Ubicación física"
        BOOLEAN activo "⚡ Estado activo"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    recurso {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 nombre "🛠️ Nombre del recurso"
        VARCHAR_255 descripcion "📝 Descripción detallada"
        BOOLEAN activo "⚡ Estado activo"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    salon_recurso {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 salon_id FK "🏫 Referencia salón"
        CHAR_36 recurso_id FK "🛠️ Referencia recurso"
        INTEGER cantidad "🔢 Cantidad disponible"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épica 4: Gestión de Profesores
    profesor {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 usuario_id FK "👤 Referencia usuario"
        VARCHAR_255 especialidades "🎯 Áreas de especialización"
        BOOLEAN activo "⚡ Estado activo"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épicas 5-6: Asignaciones y Disponibilidades
    periodo_academico {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 nombre "🏷️ Nombre período"
        DATE fecha_inicio "📅 Fecha inicio"
        DATE fecha_fin "📅 Fecha fin"
        BOOLEAN activo "⚡ Estado activo"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    bloque_horario {
        CHAR_36 id PK "🔑 Identificador único"
        ENUM_dia_semana dia_semana "📅 Día de la semana"
        TIME hora_inicio "⏰ Hora inicio"
        TIME hora_fin "⏰ Hora fin"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    disp_profesor {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 profesor_id FK "👨‍🏫 Referencia profesor"
        CHAR_36 bloque_id FK "⏰ Referencia bloque"
        ENUM_estado estado "📊 Estado disponibilidad"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    disp_salon {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 salon_id FK "🏫 Referencia salón"
        CHAR_36 bloque_id FK "⏰ Referencia bloque"
        ENUM_estado estado "📊 Estado disponibilidad"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    recurso_disponibilidad {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 recurso_id FK "🛠️ Referencia recurso"
        CHAR_36 bloque_id FK "⏰ Referencia bloque"
        ENUM_estado estado "📊 Estado disponibilidad"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    asignacion {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 grupo_id FK "👥 Referencia grupo"
        CHAR_36 salon_id FK "🏫 Referencia salón"
        CHAR_36 profesor_id FK "👨‍🏫 Referencia profesor"
        CHAR_36 bloque_id FK "⏰ Referencia bloque"
        CHAR_36 periodo_id FK "📅 Referencia período"
        ENUM_estado_asignacion estado "📊 Estado asignación"
        ENUM_origen origen "🎯 Origen asignación"
        FLOAT score "⭐ Puntuación optimización"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épicas 7-8: Restricciones y Conflictos
    tipo_restriccion {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 nombre "🏷️ Nombre restricción"
        VARCHAR_255 descripcion "📝 Descripción detallada"
        BOOLEAN activa "⚡ Estado activa"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    restriccion {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 tipo_restriccion_id FK "📏 Referencia tipo"
        CHAR_36 objetivo_id "🎯 ID entidad objetivo"
        VARCHAR_60 objetivo_tipo "🏷️ Tipo entidad objetivo"
        JSON configuracion "⚙️ Configuración parámetros"
        BOOLEAN activa "⚡ Estado activa"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Épicas 9-10: Auditoría y Reportes
    auditoria {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 usuario_id FK "👤 Usuario ejecutor"
        VARCHAR_60 entidad "🏷️ Entidad afectada"
        CHAR_36 entidad_id "🔑 ID entidad afectada"
        JSON cambios_json "📊 Registro de cambios"
        TIMESTAMP created_at "📅 Fecha auditoría"
    }

    reporte_ocupacion {
        CHAR_36 id PK "🔑 Identificador único"
        CHAR_36 periodo_id FK "📅 Referencia período"
        ENUM_tipo_reporte tipo "📊 Tipo de reporte"
        CHAR_36 objetivo_id "🎯 Entidad objetivo"
        FLOAT ocupacion_porcentaje "📈 Porcentaje ocupación"
        INTEGER num_bloques_ocupados "⏰ Bloques ocupados"
        TIMESTAMP created_at "📅 Fecha generación"
    }

    parametro_sistema {
        CHAR_36 id PK "🔑 Identificador único"
        VARCHAR_120 clave UK "🔐 Clave parámetro"
        JSON valor "💾 Valor configuración"
        VARCHAR_60 scope "🌐 Alcance parámetro"
        TIMESTAMP created_at "📅 Creado en"
        TIMESTAMP updated_at "✏️ Actualizado en"
    }

    %% Relaciones con estilos
    usuario ||--|| profesor : "tiene"
    periodo_academico ||--o{ asignacion : "contiene"
    grupo ||--o{ asignacion : "tiene"
    salon ||--o{ asignacion : "asignado_en"
    profesor ||--o{ asignacion : "imparte"
    bloque_horario ||--o{ asignacion : "programado_en"
    salon ||--o{ salon_recurso : "tiene"
    recurso ||--o{ salon_recurso : "pertenece_a"
    profesor ||--o{ disp_profesor : "disponibilidad"
    bloque_horario ||--o{ disp_profesor : "en_bloque"
    salon ||--o{ disp_salon : "disponibilidad"
    bloque_horario ||--o{ disp_salon : "en_bloque"
    recurso ||--o{ recurso_disponibilidad : "disponibilidad"
    bloque_horario ||--o{ recurso_disponibilidad : "en_bloque"
    tipo_restriccion ||--o{ restriccion : "define"
    usuario ||--o{ auditoria : "realiza"
    periodo_academico ||--o{ reporte_ocupacion : "genera"

    %% Aplicar estilos a las entidades
    class usuario,profesor userEntity
    class grupo groupEntity
    class salon,salon_recurso,disp_salon roomEntity
    class recurso,recurso_disponibilidad resourceEntity
    class profesor,disp_profesor teacherEntity
    class periodo_academico,bloque_horario scheduleEntity
    class asignacion assignmentEntity
    class tipo_restriccion,restriccion constraintEntity
    class auditoria,reporte_ocupacion,parametro_sistema auditEntity
