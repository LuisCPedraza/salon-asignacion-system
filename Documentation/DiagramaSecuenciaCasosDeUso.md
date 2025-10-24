# Diagramas de Secuencia para Casos de Uso por Rol

## Introducción
Estos diagramas de secuencia ilustran las interacciones clave de cada rol con el sistema, enfocándose en sus **actividades principales** y **restricciones específicas**. Cada diagrama usa sintaxis Mermaid para renderizarse en GitHub. Las restricciones se representan como notas o guards (condiciones) en las flechas. Todos los roles inician con autenticación (UC2), como se detalló previamente.

### 1. Secretaría (General)

- **Actividades Principales**: Apoya en creación de cuentas, gestiona solicitudes de cambios en horarios, genera/distribuye reportes básicos y mantiene auditoría rutinaria.  

- **Restricciones Específicas**: Acceso limitado a lectura/edición básica (no asignaciones ni configs globales). Depende de aprobaciones superiores. Solo visualiza datos no sensibles.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>S: Ingresar Como:
    participant S as Secretaría
    participant Sys as Sistema
    participant A as Aprobador (Superior)

    S->>Sys: Iniciar Sesión (UC2)
    Sys->>S: Acceso concedido (limitado)
    Note over S,Sys: Restricción: Solo lectura/edición básica

    S->>Sys: Crear/Actualizar Cuenta (UC1, soporte)
    Sys->>A: Solicitar Aprobación
    A->>Sys: Aprobar
    Sys->>S: Confirmación

    S->>Sys: Generar Reporte Básico (UC15)
    Sys->>S: Reporte (no sensibles)
    Note over S,Sys: Restricción: Sin asignaciones

    S->>Sys: Registrar en Auditoría (UC18)
    Sys->>S: Historial actualizado
```
### 2. Superadministrador

- **Actividades Principales**: Gestiona backups/restauraciones, integra con herramientas externas (ej: LMS), monitorea rendimiento global y aprueba cambios estructurales.

- **Restricciones Específicas**: Acceso exclusivo y auditado (solo para IT/directivos). No interfiere en operaciones diarias. Requiere logs avanzados con doble verificación.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>SA: Ingresar Como:
    participant SA as Superadministrador
    participant Sys as Sistema
    participant Log as Logs Avanzados

    SA->>Sys: Iniciar Sesión (UC2)
    Sys->>SA: Acceso exclusivo
    Note over SA,Sys: Restricción: Auditado con doble verificación

    SA->>Sys: Gestionar Backup/Restauración (UC19 extendido)
    Sys->>Log: Registrar Acción
    Log->>SA: Confirmación auditada

    SA->>Sys: Integrar Herramienta Externa (UC19)
    Sys->>SA: Integración completada
    Note over SA,Sys: Restricción: No operaciones diarias

    SA->>Sys: Monitorear Rendimiento (UC18)
    Sys->>SA: Métricas globales
```
### 3. Administrador

- **Actividades Principales**: Crea/gestiona cuentas, genera reportes de recursos/estadísticas, visualiza historial/auditoría y configura parámetros generales (períodos, días laborables).

- **Restricciones Específicas**: Acceso total pero controlado por rol (no ejecución de asignaciones). Debe registrar todas las acciones para auditoría.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>Admin: Ingresar Como:
    participant Admin as Administrador
    participant Sys as Sistema
    participant Audit as Auditoría

    Admin->>Sys: Iniciar Sesión (UC2)
    Sys->>Admin: Acceso total (controlado)
    Note over Admin,Sys: Restricción: Registrar acciones

    Admin->>Sys: Crear/Gestionar Cuentas (UC1)
    Sys->>Audit: Registrar Acción
    Audit->>Admin: Confirmación

    Admin->>Sys: Generar Reportes (UC15)
    Sys->>Admin: Estadísticas recursos

    Admin->>Sys: Configurar Parámetros (UC19)
    Sys->>Audit: Log de cambio
    Note over Admin,Sys: Restricción: Sin asignaciones
```
### 4. Profesor

- **Actividades Principales**: Inicia sesión, visualiza horario personal y salones asignados, actualiza su disponibilidad horaria y preferencias.

- **Restricciones Específicas**: Acceso solo a datos personales (no edición global). Dependiente de asignaciones de coordinadores; no ve horarios ajenos.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>P: Ingresar Como:
    participant P as Profesor
    participant Sys as Sistema

    P->>Sys: Iniciar Sesión (UC2)
    Sys->>P: Acceso personal
    Note over P,Sys: Restricción: Solo datos propios

    P->>Sys: Visualizar Horario Personal (UC14)
    Sys->>P: Horario y salones

    P->>Sys: Actualizar Disponibilidad (UC8)
    alt Dependiente de Coordinador
        Sys->>P: Validación pendiente
    else
        Sys->>P: Actualizado
    end
    Note over P,Sys: Restricción: No edición global
```
### 5. Secretaría de Infraestructura

- **Actividades Principales**: Actualiza disponibilidades de salones (ej: por mantenimiento), genera reportes de uso de recursos físicos y notifica restricciones.

- **Restricciones Específicas**: Enfocado solo en datos de salones/infraestructura; no accede a horarios académicos o grupos. Requiere aprobación para cambios.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>SI: Ingresar Como:
    participant SI as Secretaría Infra
    participant Sys as Sistema
    participant A as Aprobador

    SI->>Sys: Iniciar Sesión (UC2)
    Sys->>SI: Acceso infra
    Note over SI,Sys: Restricción: Solo salones

    SI->>Sys: Actualizar Disponibilidad Salones (UC6)
    Sys->>A: Solicitar Aprobación
    A->>Sys: Aprobar
    Sys->>SI: Actualizado

    SI->>Sys: Generar Reporte Recursos (UC15)
    Sys->>SI: Reporte físico
    Note over SI,Sys: Restricción: Sin académicos
```
### 6. Coordinador Académico

- **Actividades Principales**: Registra/edita grupos y profesores (enfoque en datos académicos como niveles/especialidades), coordina preferencias pedagógicas y aprueba horarios propuestos.

- **Restricciones Específicas**: No gestiona infraestructura física; reporta a coordinador general. Limitado a filtros académicos, sin configs globales.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>CA: Ingresar Como:
    participant CA as Coord. Académico
    participant Sys as Sistema
    participant CG as Coord. General

    CA->>Sys: Iniciar Sesión (UC2)
    Sys->>CA: Acceso académico
    Note over CA,Sys: Restricción: Sin infra/configs

    CA->>Sys: Registrar/Editar Grupos (UC3)
    Sys->>CA: Confirmación

    CA->>Sys: Aprobar Horarios (UC13)
    Sys->>CG: Reportar
    CG->>CA: Feedback

    CA->>Sys: Editar Profesores (UC7)
    Note over CA,Sys: Restricción: Filtros académicos solo
```
### 7. Secretaria Académica

- **Actividades Principales**: Maneja registros administrativos de grupos/profesores, distribuye horarios a estudiantes/familias y exporta a calendarios externos.

- **Restricciones Específicas**: No asigna salones ni edita disponibilidades; solo datos no sensibles. Acceso temporal a info de estudiantes (con privacidad GDPR-like).

```mermaid
sequenceDiagram
actor Usuario
Usuario->>SAca: Ingresar Como:
    participant SAca as Sec. Académica
    participant Sys as Sistema

    SAca->>Sys: Iniciar Sesión (UC2)
    Sys->>SAca: Acceso admin académico
    Note over SAca,Sys: Restricción: Datos no sensibles

    SAca->>Sys: Manejar Registros Grupos/Profesores (UC3/UC7)
    Sys->>SAca: Actualizado

    SAca->>Sys: Distribuir/Exportar Horarios (UC13/UC14)
    Sys->>SAca: Export completado
    Note over SAca,Sys: Restricción: Acceso temporal estudiantes
```
### 8. Profesor Invitado

- **Actividades Principales**: Visualiza horarios temporales y salones asignados, reporta disponibilidades limitadas y recibe notificaciones por email/SMS.

- **Restricciones Específicas**: Acceso caduco (expira automáticamente); sin edición profunda ni gestión de recursos. Solo para sesiones puntuales.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>PI: Ingresar Como:
    participant PI as Prof. Invitado
    participant Sys as Sistema

    PI->>Sys: Iniciar Sesión Temporal (UC2)
    Sys->>PI: Acceso caduco
    Note over PI,Sys: Restricción: Expira automáticamente

    PI->>Sys: Visualizar Horarios Temporales (UC14)
    Sys->>PI: Horarios y salones

    PI->>Sys: Reportar Disponibilidad Limitada (UC8)
    Sys->>PI: Notificación enviada (email/SMS)
    Note over PI,Sys: Restricción: Sin edición profunda
```
### 9. Coordinador (General)

- **Actividades Principales**: Registra/edita grupos/profesores, ejecuta asignaciones automáticas/manuales, visualiza horarios/conflictos y establece restricciones.

- **Restricciones Específicas**: Dependiente de disponibilidades reales; no configs globales (eso es de admin). Acceso amplio pero no ilimitado a datos sensibles.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>C: Ingresar Como:
    participant C as Coordinador
    participant Sys as Sistema

    C->>Sys: Iniciar Sesión (UC2)
    Sys->>C: Acceso general
    Note over C,Sys: Restricción: Dependiente disponibilidades

    C->>Sys: Registrar Grupos/Profesores (UC3/UC7)
    Sys->>C: Confirmado

    C->>Sys: Ejecutar Asignación Automática (UC9)
    Sys->>C: Resultados (con conflictos UC12)

    C->>Sys: Establecer Restricciones (UC17)
    Note over C,Sys: Restricción: Sin configs globales
```
### 10. Coordinador de Infraestructura

- **Actividades Principales**: Registra/gestiona salones (capacidad, recursos, ubicación) y configura su disponibilidad horaria/restricciones de uso.

- **Restricciones Específicas**: Enfocado solo en recursos físicos; no ve/edita datos académicos. Cambios requieren validación para evitar conflictos.

```mermaid
sequenceDiagram
actor Usuario
Usuario->>CI: Ingresar Como:
    participant CI as Coord. Infra
    participant Sys as Sistema
    participant V as Validador

    CI->>Sys: Iniciar Sesión (UC2)
    Sys->>CI: Acceso infra
    Note over CI,Sys: Restricción: Solo físicos

    CI->>Sys: Registrar Salones (UC5)
    Sys->>CI: Confirmado

    CI->>Sys: Configurar Disponibilidad (UC6)
    Sys->>V: Validar Conflicto
    V->>Sys: Aprobado
    Sys->>CI: Actualizado
    Note over CI,Sys: Restricción: Sin académicos
```










