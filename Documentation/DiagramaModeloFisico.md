# Diagrama del Modelo Físico: Sistema de Asignación de Salones
## Descripción General
El **Modelo Físico** representa la implementación concreta de la BD en MySQL InnoDB, con detalles de almacenamiento (motores, particiones, índices compuestos, claves candidatas, optimizaciones). 

Deriva del relacional, enfocándose en eficiencia (ej: clustering por fecha para HU13). 

Diferencia: Técnico para rendimiento (ej: PARTITION BY RANGE en AUDITORIA para HU18 logs grandes).
**Atractivo Visual:** Graph LR horizontal, subgraphs temáticos, emojis, colores (azul: tablas, morado: índices, verde: particiones), flechas para relaciones físicas.
## Descripciones Detalladas

- **Tablas**: ENGINE=InnoDB, CHARSET=utf8mb4, detalles físicos (ej: AUTO_INCREMENT PK).
- **Índices**: Clustered/secondary para queries (ej: fecha en ASIGNACION HU12).
- **Particiones**: Por fecha/nivel (ej: HORARIO by periodo HU19).
- **Relaciones Físicas**: FK con ON DELETE, optimizaciones (ej: INDEXED FK).
- **Cumplimiento**: Optimizado para épicas (ej: FULLTEXT en RESTRICCION para HU17 búsquedas).

## Diagrama Mermaid (Modelo Físico - Corregido)

```mermaid
graph LR
    subgraph "Capa de Tablas Clave ENGINE=InnoDB CHARSET=utf8mb4"
        T1[👤 USUARIO\nClave Primaria: id AUTO_INCREMENT\nÍndice: email UNIQUE]:::table
        T2[👨‍💼 ADMINISTRADOR\nClave Primaria: id AUTO_INCREMENT\nClave Foránea: usuario_id CASCADE]:::table
        T3[🏗️ COORDINADOR\nClave Primaria: id AUTO_INCREMENT\nÍndice: especialidad]:::table
        T4[👥 GRUPO\nClave Primaria: id AUTO_INCREMENT\nPartición por RANGE de nivel\nVerificación: numEstudiantes mayor 0]:::table
        T5[🏫 SALON\nClave Primaria: id AUTO_INCREMENT\nFULLTEXT: recursos\nÍndice: ubicacion]:::table
        T6[👨‍🏫 PROFESOR\nClave Primaria: id AUTO_INCREMENT\nÚnica: especialidad]:::table
        T7[📅 ASIGNACION\nClave Primaria: id AUTO_INCREMENT\nÍndice Agrupado: fecha\nÚnica: grupo_id fecha]:::table
        T8[⚠️ RESTRICCION\nClave Primaria: id AUTO_INCREMENT\nÍndice: tipo descripcion]:::table
        T9[📜 AUDITORIA\nClave Primaria: id AUTO_INCREMENT\nPartición por RANGE de timestamp\nÍndice: usuario_id timestamp]:::table
    end

    subgraph "Optimizaciones Físicas Indices y Particiones"
        I1[🔍 Índices Secundarios\nEj fecha en ASIGNACION - HU12]:::index
        I2[📊 Particiones\nEj HORARIO por periodo - HU19\nRANGE 2024-01 2025-01]:::partition
        I3[🔒 Restricciones Físicas\nEj ON DELETE CASCADE en Claves Foráneas\nVerificación en capacidades - HU6]:::constraint
    end

    subgraph "Flujos Físicos Relaciones Optimizadas"
        F1[Joins Clave Foránea: USUARIO → Roles\nINDEXED para búsqueda rápida]:::flow
        F2[Joins Clave Foránea: Recursos → Asignación\nCASCADE para integridad - HU4]:::flow
        F3[Optimización Consulta: SELECT con ÍNDICE\nEj: Horarios por fecha - HU13]:::flow
    end

    %% Relaciones Físicas
    T1 ---|"1:N Clave Foránea CASCADE"| T2
    T1 ---|"1:N Clave Foránea"| T3
    T3 ---|"1:N Clave Foránea"| T4
    T3 ---|"1:N Clave Foránea"| T5
    T6 ---|"1:N Clave Foránea"| T7
    T4 ---|"1:N Clave Foránea RESTRICT"| T7
    T5 ---|"1:N Clave Foránea RESTRICT"| T7
    T7 ---|"1:N Clave Foránea CASCADE"| T8
    T1 ---|"1:N Clave Foránea RESTRICT"| T9
    T7 ---|"1:N Clave Foránea"| T9

    T7 -.->|"Índice Agrupado"| I1
    T9 -.->|"Partición RANGE"| I2
    T1 -.->|"Verificación Única"| I3

    F1 -.->|"Joins Rápidos"| T1
    F2 -.->|"Integridad"| T7
    F3 -.->|"Rendimiento Consulta"| T9

    %% Estilos para Atractivo Visual
    classDef table fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,color:#000
    classDef index fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,color:#000
    classDef partition fill:#e8f5e8,stroke:#388e3c,stroke-width:3px,color:#000
    classDef constraint fill:#fff3e0,stroke:#ef6c00,stroke-width:3px,color:#000
    classDef flow fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,color:#000,dashed

    linkStyle default stroke:#42a5f5,stroke-width:2px
```
