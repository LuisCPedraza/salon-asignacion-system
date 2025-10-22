# Diagrama Flujo de Datos
---
## Enfoque para el Diagrama de Flujo de Datos
Un DFD muestra cómo los datos fluyen entre entidades externas, procesos, almacenes de datos, y flujos de datos. Basado en el sistema descrito en el documento, el DFD nivel 0 (diagrama de contexto) y nivel 1 (desglose de procesos principales) cubrirán las funcionalidades clave del sistema de gestión de asignaciones académicas. A continuación, detallo el enfoque:

- Entidades Externas:
	- Administrador: Gestiona usuarios, parámetros del sistema, y auditorías (HU1, HU2, HU19).
	- Coordinador: Configura periodos académicos, grupos, salones, y restricciones; realiza asignaciones manuales (HU3-HU6, HU9-HU12, HU16-HU17).
	- Coordinador de Infraestructura: Gestiona salones y recursos (HU5-HU6).
	- Profesor: Registra disponibilidades y consulta asignaciones (HU7-HU8, HU11).
	- Sistema Externo: Genera reportes de ocupación y detecta conflictos (HU13-HU15).

- Procesos Principales (basados en épicas):
	- Gestión de Usuarios: Autenticación y gestión de roles (HU1-HU2).
	- Gestión de Recursos Académicos: Configuración de periodos, grupos, salones, y profesores (HU3-HU8).
	- Gestión de Asignaciones: Asignaciones automáticas y manuales, validación de restricciones (HU9-HU12, HU16-HU17).
	- Generación de Reportes: Reportes de ocupación y auditorías (HU13-HU15, HU18).
	- Configuración del Sistema: Gestión de parámetros del sistema (HU19).

- Almacenes de Datos:
	- Cada tabla del modelo físico (periodo_academico, usuario, profesor, grupo, salon, recurso, salon_recurso, recurso_disponibilidad, disp_profesor, disp_salon, asignacion, tipo_restriccion, restriccion, auditoria, reporte_ocupacion, parametro_sistema) se representa como un almacé...

### Diagrama Flujo de Datos (Nivel 1 - Corregido y Mejorado)
```mermaid
graph LR
    subgraph "Entidades Externas"
        A[Administrador]:::external
        B[Coordinador]:::external
        CI[Coordinador de Infraestructura]:::external
        P[Profesor]:::external
        SE[Sistema Externo]:::external
    end

    subgraph "Procesos Principales"
        P1[Gestionar Usuarios]:::process
        P2[Gestionar Recursos Académicos]:::process
        P3[Gestionar Asignaciones]:::process
        P4[Generar Reportes]:::process
        P5[Gestionar Salones]:::process
        P6[Configurar Sistema]:::process
    end

    subgraph "Almacenes de Datos"
        D1[(Usuario)]:::store
        D2[(Grupo)]:::store
        D3[(Salon)]:::store
        D4[(Profesor)]:::store
        D5[(Asignacion)]:::store
        D6[(Restriccion)]:::store
        D7[(Auditoria)]:::store
        D8[(ReporteOcupacion)]:::store
        D9[(ParametroSistema)]:::store
    end

    %% Flujos de Datos
    A -.-> P1
    A -.-> P6
    A -.-> P4
    B -.-> P2
    B -.-> P3
    %% Flujo para Coordinador de Infraestructura
    CI -.-> P5
    P -.-> P2
    SE -.-> P4

    P1 <--> D1
    P2 <--> D2
    P2 <--> D3
    P2 <--> D4
    P3 <--> D5
    P3 <--> D6
    P4 <--> D7
    P4 <--> D8
    P5 <--> D3
    P6 <--> D9
    P3 <--> D7

    %% Estilos Mejorados para Diseño Atractivo
    classDef external fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,color:#000
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,shape:circle,color:#000
    classDef store fill:#e8f5e8,stroke:#388e3c,stroke-width:3px,color:#000

    linkStyle default stroke:#42a5f5,stroke-width:2px
