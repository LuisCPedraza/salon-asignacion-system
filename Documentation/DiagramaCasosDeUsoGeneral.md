# Diagrama de Casos de Uso: Sistema de Asignación de Salones

## Introducción
Este diagrama de casos de uso modela el Sistema de Asignación de Salones para un centro educativo, integrando roles principales y adicionales para una gestión robusta de recursos, asignaciones y reportes. Utiliza un flujo vertical para claridad.

## Descripciones de Casos de Uso
A continuación, una breve descripción de cada caso de uso (UC), agrupados por épica para referencia:

### Épica 1: Usuarios y Autenticación
- **UC1: Crear/Gestionar Cuentas**: Permite a administradores y secretarias crear, editar o eliminar cuentas de usuarios con roles específicos para control de acceso.
- **UC2: Iniciar Sesión**: Autentica a usuarios (todos los roles) para acceder a funcionalidades según permisos.

### Épica 2: Grupos
- **UC3: Registrar/Editar Grupos**: Registra o modifica detalles de grupos de estudiantes (nombre, nivel, tamaño, características especiales) por coordinadores académicos o generales.

### Épica 3: Salones
- **UC5: Registrar/Gestionar Salones**: Añade o actualiza info de salones (capacidad, recursos, ubicación) por coordinadores de infraestructura.
- **UC6: Gestionar Disponibilidad**: Configura horarios y restricciones de uso de salones.

### Épica 4: Profesores
- **UC7: Registrar/Gestionar Profesores**: Registra o edita perfiles de profesores (datos personales, especialidades, CV) por coordinadores.
- **UC8: Gestionar Disponibilidad**: Actualiza horarios y preferencias de profesores (compartido con ellos mismos).

### Épica 5: Asignación Automática
- **UC9: Ejecutar Algoritmo Automático**: Lanza asignaciones óptimas considerando disponibilidades y preferencias (incluye UC10).
- **UC10: Configurar Parámetros**: Define prioridades para el algoritmo (ej: proximidad de salones).

### Épica 6: Asignación Manual
- **UC11: Asignaciones Manuales**: Asigna grupos a salones vía interfaz drag-and-drop (incluye visualización de conflictos en UC12).
- **UC12: Visualizar Conflictos**: Muestra en tiempo real sobrecupos o colisiones de horarios.

### Épica 7: Visualización y Reportes
- **UC13: Horario Semestral**: Visualiza el horario completo de asignaciones por coordinadores.
- **UC14: Horario Personal**: Muestra horarios individuales de profesores o invitados.
- **UC15: Generar Reportes**: Crea estadísticas de uso de recursos por administradores o secretarias.

### Épica 8: Conflictos
- **UC16: Notificaciones y Alternativas**: Alerta sobre conflictos y sugiere soluciones (extiende UC17).
- **UC17: Establecer Restricciones**: Define reglas específicas para recursos o usuarios.

### Épica 9: Historial
- **UC18: Visualizar Historial**: Revisa cambios en asignaciones y auditoría de usuarios.

### Épica 10: Configuración
- **UC19: Parámetros Generales**: Configura aspectos globales como períodos académicos o días laborables por administradores.

## Diagrama Mermaid
```mermaid
flowchart TD
    %% Título
    Title[📋 Diagrama de Casos de Uso General: Sistema de Asignación de Salones]

    %% Actores Actualizados (con adicionales incorporados)
    Admin[👨‍💼 Administrador]
    SuperAdmin[🔧 Superadministrador]
    Coord[👨‍🏫 Coordinador]
    CoordAcad[📚 Coordinador Académico]
    CoordInfra[🏗️ Coordinador de Infraestructura]
    Prof[👨‍🏫 Profesor]
    ProfInv[👤 Profesor Invitado]
    Secre[💼 Secretaria]
    SecreAcad[📖 Secretaria Académica]
    SecreInfra[🔨 Secretaria de Infraestructura]

    %% Subgráficos (mismos que antes, abreviados para espacio)
    subgraph Épica1 ["🛡️ Usuarios y Autenticación"]
        UC1(("Crear/Gestionar Cuentas"))
        UC2(("Iniciar Sesión"))
    end

    subgraph Épica2 ["👥 Grupos"]
        UC3(("Registrar/Editar Grupos"))
    end

    subgraph Épica3 ["🏫 Salones"]
        UC5(("Registrar/Gestionar Salones"))
        UC6(("Gestionar Disponibilidad"))
    end

    subgraph Épica4 ["👨‍🏫 Profesores"]
        UC7(("Registrar/Gestionar Profesores"))
        UC8(("Gestionar Disponibilidad"))
    end

    subgraph Épica5 ["🤖 Asignación Automática"]
        UC9(("Ejecutar Algoritmo"))
        UC10(("Configurar Parámetros"))
    end

    subgraph Épica6 ["✋ Asignación Manual"]
        UC11(("Asignaciones Manuales"))
        UC12(("Visualizar Conflictos"))
    end

    subgraph Épica7 ["📊 Visualización y Reportes"]
        UC13(("Horario Semestral"))
        UC14(("Horario Personal"))
        UC15(("Generar Reportes"))
    end

    subgraph Épica8 ["⚠️ Conflictos"]
        UC16(("Notificaciones y Alternativas"))
        UC17(("Establecer Restricciones"))
    end

    subgraph Épica9 ["📜 Historial"]
        UC18(("Visualizar Historial"))
    end

    subgraph Épica10 ["⚙️ Configuración"]
        UC19(("Parámetros Generales"))
    end

    %% Relaciones Principales (enfocadas) - Corrección: Todos conectados a UC2
    Admin --> UC2
    SuperAdmin --> UC2
    Coord --> UC2
    CoordAcad --> UC2
    CoordInfra --> UC2
    Prof --> UC2
    ProfInv --> UC2
    Secre --> UC2
    SecreAcad --> UC2
    SecreInfra --> UC2

    Admin --> UC1
    Admin --> UC15
    Admin --> UC18
    Admin --> UC19
    SuperAdmin --> UC1
    SuperAdmin --> UC18
    SuperAdmin --> UC19

    Coord --> UC3
    Coord --> UC7
    Coord --> UC9
    Coord --> UC11
    Coord --> UC13
    Coord --> UC16
    CoordAcad --> UC3
    CoordAcad --> UC7
    CoordAcad --> UC13
    CoordInfra --> UC5
    CoordInfra --> UC6

    Prof --> UC14
    Prof --> UC8
    ProfInv --> UC14

    Secre --> UC15
    Secre --> UC18
    SecreAcad --> UC3
    SecreAcad --> UC15
    SecreInfra --> UC5
    SecreInfra --> UC15

    %% Relaciones entre casos
    UC9 -.->|<<include>>| UC10
    UC11 -.->|<<include>>| UC12
    UC16 -.->|<<extend>>| UC17

    %% Estilos
    classDef actorFill fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef usecaseFill fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef epicFill fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px
    classDef titleFill fill:#fff3e0,stroke:#ef6c00,stroke-width:2px,color:#000

    class Admin,SuperAdmin,Coord,CoordAcad,CoordInfra,Prof,ProfInv,Secre,SecreAcad,SecreInfra actorFill
    class UC1,UC2,UC3,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14,UC15,UC16,UC17,UC18,UC19 usecaseFill
    class Title titleFill
```

### Roles en el Sistema de Asignación de Salones

Todos estos roles deben **iniciar sesión** (UC2) para acceder al sistema, con restricciones basadas en permisos (RBAC). A continuación, detallo **qué hace cada uno** (actividades principales) y **sus restricciones específicas**.

| Rol                          | Actividades Principales (Qué Hace) | Restricciones Específicas |
|------------------------------|-----------------------------------|---------------------------|
| **Secretaría** (General)    | Apoya en creación de cuentas, gestiona solicitudes de cambios en horarios, genera/distribuye reportes básicos y mantiene auditoría rutinaria. | Acceso limitado a lectura/edición básica (no asignaciones ni configs globales). Depende de aprobaciones superiores. Solo visualiza datos no sensibles. |
| **Superadministrador**      | Gestiona backups/restauraciones, integra con herramientas externas (ej: LMS), monitorea rendimiento global y aprueba cambios estructurales. | Acceso exclusivo y auditado (solo para IT/directivos). No interfiere en operaciones diarias. Requiere logs avanzados con doble verificación. |
| **Administrador**           | Crea/gestiona cuentas, genera reportes de recursos/estadísticas, visualiza historial/auditoría y configura parámetros generales (períodos, días laborables). | Acceso total pero controlado por rol (no ejecución de asignaciones). Debe registrar todas las acciones para auditoría. |
| **Profesor**                | Inicia sesión, visualiza horario personal y salones asignados, actualiza su disponibilidad horaria y preferencias. | Acceso solo a datos personales (no edición global). Dependiente de asignaciones de coordinadores; no ve horarios ajenos. |
| **Secretaría de Infraestructura** | Actualiza disponibilidades de salones (ej: por mantenimiento), genera reportes de uso de recursos físicos y notifica restricciones. | Enfocado solo en datos de salones/infraestructura; no accede a horarios académicos o grupos. Requiere aprobación para cambios. |
| **Coordinador Académico**   | Registra/edita grupos y profesores (enfoque en datos académicos como niveles/especialidades), coordina preferencias pedagógicas y aprueba horarios propuestos. | No gestiona infraestructura física; reporta a coordinador general. Limitado a filtros académicos, sin configs globales. |
| **Secretaria Académica**    | Maneja registros administrativos de grupos/profesores, distribuye horarios a estudiantes/familias y exporta a calendarios externos. | No asigna salones ni edita disponibilidades; solo datos no sensibles. Acceso temporal a info de estudiantes (con privacidad GDPR-like). |
| **Profesor Invitado**       | Visualiza horarios temporales y salones asignados, reporta disponibilidades limitadas y recibe notificaciones por email/SMS. | Acceso caduco (expira automáticamente); sin edición profunda ni gestión de recursos. Solo para sesiones puntuales. |
| **Coordinador** (General)   | Registra/edita grupos/profesores, ejecuta asignaciones automáticas/manuales, visualiza horarios/conflictos y establece restricciones. | Dependiente de disponibilidades reales; no configs globales (eso es de admin). Acceso amplio pero no ilimitado a datos sensibles. |
| **Coordinador de Infraestructura** | Registra/gestiona salones (capacidad, recursos, ubicación) y configura su disponibilidad horaria/restricciones de uso. | Enfocado solo en recursos físicos; no ve/edita datos académicos. Cambios requieren validación para evitar conflictos. |
