# Diagrama de Flujo de Datos (DFD): Sistema de Asignación de Salones
## Descripción General
DFD que modela flujos de datos por épicas/HU: entidades externas (roles), procesos (funcionalidades), flujos etiquetados y stores (BD). Nivel 0: Contexto global. Nivel 1: Descompuesto. Cubre backlog completo (Épicas 1-10, HU1-19). Visual: Subgraphs agrupados, emojis, colores (azul: entidades, morado: procesos, naranja: stores), flujo vertical.
## Descripciones Detalladas

- Entidades: Roles como fuentes (ej: Coordinador envía "Datos Grupo").
- Procesos: Por épica (ej: P6: Asignación Auto valida disponibilidades).
- Flujos: Etiquetas clave (ej: "Conflicto Log" → D6).
- Stores: Tablas BD (ej: D3: ASIGNACION_BD).
- Cumplimiento: Flujos trazan a HU (ej: P12 para HU16 conflictos/notificaciones).

### Diagrama Mermaid (Nivel 0 y 1)
```mermaid
flowchart TD
    classDef entity fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef store fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef epic fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px

    %% Nivel 0: Contexto
    subgraph Nivel0 ["🌐 Nivel 0: Contexto"]
        E1[👨‍💼 Admin]:::entity
        E2[👨‍🏫 Coord]:::entity
        E3[🏗️ Coord Infra]:::entity
        E4[💼 Sec]:::entity
        E5[👨‍🏫 Prof]:::entity
        P0[Sistema Asignación]:::process
        D0[(🗄️ BD Central)]:::store

        E1 -.->|"Cred/Reportes"| P0
        E2 -.->|"Recursos/Asig"| P0
        E3 -.->|"Salones"| P0
        E4 -.->|"Solic/Audit"| P0
        E5 -.->|"Disp/Horarios"| P0
        P0 -.->|"Datos/Notif"| D0
        D0 -.->|"Respuestas"| P0
        P0 -.->|"Logs/Asig"| E1
        P0 -.->|"Conflictos"| E2
    end

    %% Nivel 1: Descompuesto
    subgraph Nivel1 ["📊 Nivel 1: Por Épicas"]
        subgraph Ep1 ["🛡️ Ép1: Usuarios"]
            P1[Auth]:::process
            P2[Cuentas]:::process
        end
        subgraph Ep234 ["👥 Ép2-4: Recursos"]
            P3[Grupos]:::process
            P4[Salones]:::process
            P5[Profes]:::process
        end
        subgraph Ep56 ["🤖 Ép5-6: Asig"]
            P6[Auto]:::process
            P7[Manual]:::process
            P8[Conflictos]:::process
        end
        subgraph Ep7 ["📊 Ép7: Vis/Rep"]
            P9[Semestral]:::process
            P10[Personal]:::process
            P11[Reportes]:::process
        end
        subgraph Ep8 ["⚠️ Ép8: Conf/Rest"]
            P12[Detección]:::process
            P13[Restricciones]:::process
            P14[Notif/Sug]:::process
        end
        subgraph Ep910 ["📜 Ép9-10: Audit/Config"]
            P15[Historial]:::process
            P16[Parámetros]:::process
        end

        subgraph Stores ["🗄️ Stores (BD)"]
            D1[(D1: Usuario)]:::store
            D2[(D2: Recursos)]:::store
            D3[(D3: Asignación)]:::store
            D4[(D4: Auditoría)]:::store
            D5[(D5: Reportes)]:::store
            D6[(D6: Conflictos)]:::store
        end

        %% Flujos Compactos
        E2 -->|"Datos G"| P3 -->|"Reg G"| D2 <-->|"G Exist"| P3
        E3 -->|"Info S"| P4 -->|"S Disp"| D2 <-->|"Rest S"| P4
        E2 -->|"Datos P"| P5 -->|"Disp P"| D2 <-->|"Profs"| P5
        E2 -->|"Params"| P6 -->|"Asig Opt"| D3 <-->|"Val"| P6
        E2 -->|"Drag"| P7 -->|"Asig Man"| D3 -->|"Conf RT"| P8 -->|"Alerts"| E2
        E2 -->|"Sol H"| P9 <-->|"H Completo"| D3 -->|"Vista S"| E2
        E5 -->|"Sol Pers"| P10 <-->|"H User"| D3 -->|"Vista P"| E5
        E1 -->|"Stats"| P11 <-->|"Datos U"| D3 -->|"Rep Gen"| D5 -->|"Estad"| E1
        P7 -->|"Det Auto"| P12 <-->|"Datos As"| D3 -->|"Conf Log"| D6 -->|"Notif"| P14 -->|"Sugs"| E2
        E2 -->|"Regla"| P13 -->|"Rest App"| D3 <-->|"Val"| P13
        P3 -->|"Log C"| P15 -->|"Hist"| D4 -->|"Audit U"| E1
        E1 -->|"Params G"| P16 -->|"Config Up"| D3 <-->|"Val Per"| P16
    end

    P0 -.-> Nivel1
    note["Flujos: Entidades → Procesos → Stores. Ej: Coord → P3 → D2 (HU3). Compacto: Labels cortos, flujo vertical."]
```
