# Análisis, Levantamiento de Requerimientos y Diseño del Sistema de Asignación de Salones

## 1. Introducción

El **Sistema de Asignación de Salones** es una aplicación web diseñada para gestionar recursos educativos (grupos, salones, profesores) y programar asignaciones semestrales de manera automática o manual en un centro educativo. Este documento presenta el análisis, levantamiento de requerimientos y diseño del sistema, alineado con el documento *"Proyectos Desarrollo de Software 2.docx"*, que establece un enfoque basado en **DevOps**, **Scrum con Kanban**, **TDD (Desarrollo Dirigido por Pruebas)**, y prioriza la **mantenibilidad**, **modularidad**, **cohesión** y **bajo acoplamiento**.

El sistema se basa en:
- Una **base de datos relacional** (MySQL, motor InnoDB, codificación utf8mb4) optimizada con índices, particiones, triggers y vistas, confirmada al 100% mediante scripts SQL completos para creación, triggers y datos de prueba.
- **Diagramas generados**: 
  - Diagrama de Casos de Uso (general y por rol, con épicas como subgraphs).
  - Diagramas de Secuencia (por rol, con guards para restricciones).
  - Diagrama de Clases (con herencia de `Usuario`, métodos CRUD y relaciones).
  - Diagrama Entidad-Relación (ERD, conceptual y moderno con Crow's Foot).
  - Modelo Relacional (tablas con FK, guards y vistas).
  - Modelo Físico (con ENGINE, particiones, índices y optimizaciones).
  - Diagrama de Flujo de Datos (DFD, niveles 0 y 1 con subgraphs por épica).
- **Backlog de producto** con épicas (HU1-HU19), historias técnicas (TH1-TH4) y criterios de aceptación.

El sistema soporta roles diferenciados (**Administrador**, **Superadministrador**, **Coordinador**, **Coordinador Académico**, **Coordinador de Infraestructura**, **Secretaria**, **Secretaria Académica**, **Secretaria de Infraestructura**, **Profesor**, **Profesor Invitado**) y garantiza **rendimiento** (< 2 segundos por acción), **seguridad** (autenticación, auditoría), **compatibilidad** (navegadores modernos) y **escalabilidad**.

## 2. Levantamiento de Requerimientos

El levantamiento de requerimientos se deriva del backlog de producto del documento, organizado en **requerimientos funcionales** (basados en historias de usuario - HU) y **no funcionales** (criterios de aceptación y historias técnicas - TH).

### 2.1 Requerimientos Funcionales

Los requerimientos funcionales se agrupan en **épicas** según el documento, con flujos validados en los diagramas de secuencia y DFD:

#### Épica 1: Gestión de Usuarios y Autenticación
- **HU1**: Crear, editar, desactivar y visualizar cuentas de usuarios con roles (Administrador, Superadministrador, Coordinador, Profesor, Coordinador de Infraestructura, Secretaria).
- **HU2**: Iniciar sesión con credenciales (email, contraseña) para acceder a funcionalidades según el rol (ver diagrama de secuencia por rol).

#### Épica 2: Gestión de Grupos de Estudiantes
- **HU3**: Registrar grupos con nombre, nivel, número de estudiantes y características específicas.
- **HU4**: Editar, desactivar o visualizar grupos existentes (con triggers para auditoría).

#### Épica 3: Gestión de Salones
- **HU5**: Registrar salones con código, capacidad, ubicación y recursos asociados.
- **HU6**: Gestionar disponibilidad horaria y restricciones específicas de salones (con particiones por ubicación en modelo físico).

#### Épica 4: Gestión de Profesores
- **HU7**: Registrar profesores con información personal, especialidades y enlace a hoja de vida.
- **HU8**: Gestionar disponibilidad horaria y asignaciones especiales de profesores (índices en especialidad para consultas rápidas).

#### Épica 5: Sistema de Asignación Automática
- **HU9**: Ejecutar un algoritmo de asignación automática considerando disponibilidades, capacidades y preferencias (ver diagrama de clases para método `calcularScore()`).
- **HU10**: Configurar parámetros y prioridades para optimizar la asignación automática (almacenados en `PARAMETRO` con triggers de validación).

#### Épica 6: Sistema de Asignación Manual
- **HU11**: Realizar asignaciones manuales mediante una interfaz visual (arrastrar y soltar).
- **HU12**: Visualizar conflictos (e.g., sobrecupos, superposiciones) en tiempo real durante la asignación manual (triggers en `ASIGNACION` para detección inmediata).

#### Épica 7: Visualización y Reportes
- **HU13**: Visualizar el horario semestral completo (vista `v_horario_semestral` en modelo relacional).
- **HU14**: Visualizar horarios personales (para profesores, vista `v_horario_personal`).
- **HU15**: Generar reportes de utilización de recursos y estadísticas (e.g., ocupación de salones, vista `v_reporte_utilizacion`).

#### Épica 8: Gestión de Conflictos y Restricciones
- **HU16**: Notificar conflictos en asignaciones y sugerir alternativas (triggers insertan en `CONFLICTOS` y `SUGERENCIAS_ALTERNATIVAS`).
- **HU17**: Establecer restricciones específicas para grupos, salones o profesores (tabla `RESTRICCION` con guards en triggers).

#### Épica 9: Historial y Auditoría
- **HU18**: Visualizar el historial de cambios y los usuarios responsables (tabla `AUDITORIA` con particiones por timestamp).

#### Épica 10: Configuración del Sistema
- **HU19**: Configurar parámetros generales del sistema (e.g., períodos académicos, horarios laborables, tabla `PARAMETRO` con validaciones CHECK).

### 2.2 Requerimientos No Funcionales

Los requerimientos no funcionales aseguran calidad, rendimiento y mantenibilidad:

- **Rendimiento**: Todas las operaciones (consultas, asignaciones) deben responder en menos de 2 segundos, soportado por índices y particiones en la base de datos (ver modelo físico).
- **Seguridad**: Autenticación segura con hash de contraseñas (bcrypt), auditoría de cambios (triggers en todas las tablas), y respaldos regulares.
- **Usabilidad**: Interfaz intuitiva con mínima capacitación requerida; diseño responsive y accesible (ver diagrama de flujo de datos para procesos de usuario).
- **Compatibilidad**: Soporte para navegadores modernos (Chrome, Firefox, Edge).
- **Mantenibilidad**: Código modular, cohesivo y de bajo acoplamiento; uso de TDD para pruebas unitarias y refactoring continuo (ver diagrama de clases para métodos encapsulados).
- **Escalabilidad**: Base de datos diseñada para manejar grandes volúmenes de datos mediante particiones y optimización de consultas (ver modelo físico).
- **Tecnologías**:
  - Base de datos: MySQL (InnoDB, utf8mb4).
  - Backend: API RESTful para integración con frontend (ver historia técnica TH2).
  - DevOps: Repositorio GitHub con CI/CD (GitHub Actions), despliegue en Render.
  - Frontend: Interfaz web con tecnologías modernas (HTML, CSS, JavaScript).

### 2.3 Priorización Inicial

Basado en el documento, las épicas se priorizan en el siguiente orden para el desarrollo iterativo:
1. Épicas 1, 2, 3 y 4: Gestión básica de usuarios, grupos, salones y profesores (base del sistema, ver diagramas de secuencia por rol).
2. Épicas 10 y 6: Configuración del sistema y asignación manual
