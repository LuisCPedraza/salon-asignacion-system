# Diagrama de Clases: Sistema de Asignación de Salones

## Introducción
Este diagrama de clases modela el sistema en programación orientada a objetos (POO), basado en el diagrama de casos de uso (UC1-UC19) y los diagramas de secuencia por rol. Incluye clases principales para usuarios/roles (herencia de una clase base `Usuario`), recursos (Grupos, Salones, Profesores) y entidades de gestión (Asignaciones, Horarios, Reportes). 

- **Atributos**: Propiedades clave (ej: ID, nombre, capacidad).
- **Métodos**: Operaciones detalladas, incorporando operaciones CRUD (Create/Read/Update/Delete) donde aplican (ej: createGrupo, readGrupo, etc.), derivadas de actividades de roles. Restricciones implícitas en `verificarPermisos()`.
- **Relaciones**: Herencia (generalización), asociaciones (composición/agregación), dependencias para flujos como autenticación y auditoría.
- **Identificación de Actores**: Los actores (roles del diagrama de casos de uso) se representan como clases hijas de `Usuario`, marcadas con estereotipos `<<actor>>` para identificación rápida. Agrupados lógicamente en comentarios.

El diseño promueve encapsulación, polimorfismo (métodos sobrescritos por rol) y bajo acoplamiento. Se asume un lenguaje como Java/C# para POO.

## Diagrama Mermaid
```mermaid
classDiagram
    %% Clase Base Usuario (base para todos los actores/roles)
    class Usuario {
        -int id
        -String nombre
        -String email
        -String password
        -String rol
        +void iniciarSesion(String creds)
        +boolean verificarPermisos(String accion)
        +void actualizarPerfil()
        +void create(Entidad e)
        +Entidad read(int id)
        +void update(Entidad e)
        +void delete(int id)
    }

    %% Clase Abstracta para Recursos
    class Recurso {
        <<abstract>>
        -int id
        -String tipo
        +String getTipo()
    }

    %% Actores/Roles (herencia de Usuario, con <<actor>> para identificación rápida)
    class Administrador {
        <<actor>>
        +void crearCuenta(Usuario nuevo)
        +void generarReporte(Recurso r)
        +void configurarParametros(Parametro p)
        +void visualizarHistorial(Auditoria a)
        +void createCuenta(Usuario u) // CRUD: Create cuenta
        +Usuario readCuenta(int id) // CRUD: Read cuenta
        +void updateCuenta(Usuario u) // CRUD: Update cuenta
        +void deleteCuenta(int id) // CRUD: Delete cuenta
    }

    class Superadministrador {
        <<actor>>
        +void gestionarBackup()
        +void integrarExterno(String api)
        +void monitorearRendimiento()
        +void createBackup() // CRUD-like: Create backup
        +Backup readBackup(int id)
        +void updateBackup(Backup b)
        +void deleteBackup(int id)
    }

    class Coordinador {
        <<actor>>
        +void registrarGrupo(Grupo g)
        +void ejecutarAsignacionAutomatica()
        +void realizarAsignacionManual(Asignacion a)
        +void visualizarConflictos()
        +void establecerRestricciones(Restriccion r)
        +void createGrupo(Grupo g) // CRUD: Create grupo
        +Grupo readGrupo(int id) // CRUD: Read grupo
        +void updateGrupo(Grupo g) // CRUD: Update grupo
        +void deleteGrupo(int id) // CRUD: Delete grupo
        +void createProfesor(ProfesorEntity p) // CRUD: Create profesor
        +ProfesorEntity readProfesor(int id)
        +void updateProfesor(ProfesorEntity p)
        +void deleteProfesor(int id)
    }

    class CoordinadorAcademico {
        <<actor>>
        +void editarDatosAcademicos(ProfesorEntity p)
        +void aprobarHorario(Horario h)
        +void createAsignacion(Asignacion a) // CRUD: Create asignación académica
        +Asignacion readAsignacion(int id)
        +void updateAsignacion(Asignacion a)
        +void deleteAsignacion(int id)
    }

    class CoordinadorInfraestructura {
        <<actor>>
        +void registrarSalon(Salon s)
        +void configurarDisponibilidad(HorarioSalon hs)
        +void createSalon(Salon s) // CRUD: Create salón
        +Salon readSalon(int id) // CRUD: Read salón
        +void updateSalon(Salon s) // CRUD: Update salón
        +void deleteSalon(int id) // CRUD: Delete salón
    }

    class Profesor {
        <<actor>>
        +void visualizarHorarioPersonal(Horario h)
        +void actualizarDisponibilidad(Horario h)
        +Horario readHorarioPersonal(int id) // CRUD: Read horario personal
        +void updateDisponibilidad(Horario h) // CRUD: Update disponibilidad
    }

    class ProfesorInvitado {
        <<actor>>
        +void visualizarHorarioTemporal(Horario h)
        +void reportarDisponibilidadLimitada()
        +Horario readHorarioTemporal(int id) // CRUD: Read temporal
    }

    class Secretaria {
        <<actor>>
        +void gestionarSolicitudes(Cambio c)
        +void distribuirReportes(Reporte rep)
        +void registrarAuditoria(Auditoria a)
        +void createSolicitud(Cambio c) // CRUD: Create solicitud
        +Cambio readSolicitud(int id)
        +void updateSolicitud(Cambio c)
        +void deleteSolicitud(int id)
    }

    class SecretariaAcademica {
        <<actor>>
        +void manejarRegistros(Grupo g)
        +void exportarHorarios()
        +void createRegistro(Grupo g) // CRUD: Create registro académico
        +Grupo readRegistro(int id)
        +void updateRegistro(Grupo g)
        +void deleteRegistro(int id)
    }

    class SecretariaInfraestructura {
        <<actor>>
        +void actualizarDisponibilidadSalon(Salon s)
        +void notificarRestricciones()
        +void updateDisponibilidadSalon(Salon s) // CRUD: Update disponibilidad infra
        +Salon readDisponibilidad(int id)
    }

    %% Entidades de Recursos (herencia de Recurso)
    class Grupo {
        -String nombre
        -int nivel
        -int numEstudiantes
        -String caracteristicas
        +void editarDetalles()
    }

    class Salon {
        -int capacidad
        -String recursos
        -String ubicacion
        +void gestionarDisponibilidad(Horario h)
    }

    class ProfesorEntity {
        -String especialidad
        -String hojaVida
        +void gestionarDisponibilidad(Horario h)
    }

    %% Entidades de Gestión
    class Asignacion {
        -int id
        -Date fecha
        -Grupo grupo
        -Salon salon
        -ProfesorEntity profesor
        +void validarConflictos()
        +void sugerirAlternativas()
        +void createAsignacion(Asignacion a) // CRUD: Create asignación
        +Asignacion readAsignacion(int id)
        +void updateAsignacion(Asignacion a)
        +void deleteAsignacion(int id)
    }

    class Horario {
        -int id
        -Date periodo
        -List~Asignacion~ asignaciones
        +void visualizarSemestral()
        +void visualizarPersonal(Usuario u)
        +void createHorario(Horario h) // CRUD: Create horario
        +Horario readHorario(int id)
        +void updateHorario(Horario h)
        +void deleteHorario(int id)
    }

    class Reporte {
        -int id
        -String tipo
        -Date fechaGeneracion
        +void generarEstadisticas(Recurso r)
        +void createReporte(Reporte r) // CRUD: Create reporte
        +Reporte readReporte(int id)
        +void updateReporte(Reporte r)
        +void deleteReporte(int id)
    }

    class Restriccion {
        -int id
        -String tipo
        -String descripcion
        +void aplicar(Asignacion a)
        +void createRestriccion(Restriccion r) // CRUD: Create restricción
        +Restriccion readRestriccion(int id)
        +void updateRestriccion(Restriccion r)
        +void deleteRestriccion(int id)
    }

    class Auditoria {
        -int id
        -Date timestamp
        -Usuario usuario
        -String accion
        +void registrarCambio(Asignacion a)
        +void visualizarHistorial()
        +void createAuditoria(Auditoria a) // CRUD: Create auditoría
        +Auditoria readAuditoria(int id)
        +void updateAuditoria(Auditoria a)
        +void deleteAuditoria(int id)
    }

    class Parametro {
        -String clave
        -String valor
        +void configurarGlobal()
        +void createParametro(Parametro p) // CRUD: Create parámetro
        +Parametro readParametro(String clave)
        +void updateParametro(Parametro p)
        +void deleteParametro(String clave)
    }

    %% Relaciones (usando sintaxis Mermaid oficial)
    Usuario <|-- Administrador
    Usuario <|-- Superadministrador
    Usuario <|-- Coordinador
    Usuario <|-- CoordinadorAcademico
    Usuario <|-- CoordinadorInfraestructura
    Usuario <|-- Profesor
    Usuario <|-- ProfesorInvitado
    Usuario <|-- Secretaria
    Usuario <|-- SecretariaAcademica
    Usuario <|-- SecretariaInfraestructura

    Coordinador ..> CoordinadorAcademico : depende
    Coordinador ..> CoordinadorInfraestructura : depende
    Secretaria ..> SecretariaAcademica : depende
    Secretaria ..> SecretariaInfraestructura : depende

    Recurso <|-- Grupo
    Recurso <|-- Salon
    Recurso <|-- ProfesorEntity

    %% Composición con multiplicidad
    Asignacion *-- "1" Grupo : contiene
    Asignacion *-- "1" Salon : contiene
    Asignacion *-- "1" ProfesorEntity : contiene
    Horario *-- "1..*" Asignacion : contiene

    Usuario o-- "1..*" Auditoria : registra
    Reporte ..> Recurso : usa
    Restriccion ..> Asignacion : aplica
    Parametro ..> Administrador : configura
