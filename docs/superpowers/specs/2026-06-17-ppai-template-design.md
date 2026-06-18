# PPAI Company Template — Design Doc
**Date:** 2026-06-17
**Status:** Approved

---

## Objetivo

Crear un repositorio `ppai-template` que sirva como punto de partida estandarizado para todos los proyectos de la empresa. Incluye un `CLAUDE.md` que guia a Claude Code de forma consistente entre todos los devs del equipo, y 6 agentes especializados por dominio accesibles como skills de Claude Code.

**Equipo objetivo:** 2-5 devs fullstack que trabajan en el mismo stack.

---

## Stack Tecnologico

### Frontend
- Angular
- Ionic
- Android Studio
- TypeScript

### Backend
- Python
- FastAPI
- PostgreSQL (produccion — VH Cloud)

### Gestion de Sesion
- Firebase Auth — delega autenticacion y credenciales, no se almacenan passwords en PostgreSQL

### Entorno de Desarrollo / Testing
- Supabase — solo para desarrollo y testing local
- Visual Studio Code
- NVM (Node Version Manager)

### IA / Dev Tools
- Claude Code — herramienta de desarrollo para el equipo, no integrada en los productos

---

## Estructura del Repositorio

```
ppai-template/
├── CLAUDE.md                     ← guia principal para Claude Code
├── .claude/
│   └── skills/
│       ├── arquitectura.md       ← agente: decisiones de sistema
│       ├── backend.md            ← agente: FastAPI + Python + PostgreSQL
│       ├── frontend.md           ← agente: Angular + Ionic + TypeScript
│       ├── database.md           ← agente: PostgreSQL + Supabase
│       ├── mobile.md             ← agente: Android Studio + Ionic/Capacitor
│       └── seguridad.md          ← agente: auth Firebase, seguridad de API
├── .gitignore                    ← gitignore base para el stack completo
├── .editorconfig                 ← formateo consistente entre editores
├── docs/
│   └── stack.md                  ← referencia rapida del stack
└── project-starters/
    ├── frontend/                 ← estructura base Angular/Ionic
    └── backend/                  ← estructura base FastAPI
```

---

## CLAUDE.md — Contenido

### Identidad del proyecto
- Stack, version de Node (via NVM), version de Python
- Como arrancar el entorno local (frontend y backend)
- Donde vive cada parte del sistema

### Convenciones de Codigo

| Area | Convencion | Ejemplo |
|------|-----------|---------|
| Angular components | PascalCase | `UserProfileComponent` |
| Angular services | PascalCase + sufijo | `AuthService` |
| Angular pipes/guards | PascalCase + sufijo | `AuthGuard`, `DateFormatPipe` |
| Python modules/files | snake_case | `user_service.py` |
| FastAPI routers | snake_case | `auth_router.py` |
| Variables/funciones Python | snake_case | `get_user_by_id()` |
| Variables/funciones TypeScript | camelCase | `getUserById()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Clases Python | PascalCase | `UserService` |
| Modelos Pydantic | PascalCase | `UserCreateRequest` |

### Estructura de Carpetas

**Frontend (Angular/Ionic):**
```
src/
├── app/
│   ├── core/           ← servicios singleton, guards, interceptors
│   ├── shared/         ← componentes, pipes y directivas reutilizables
│   ├── features/       ← modulos por funcionalidad de negocio
│   └── app.module.ts
├── assets/
└── environments/
```

**Backend (FastAPI):**
```
app/
├── api/
│   └── routers/        ← un archivo por dominio (auth_router.py, user_router.py)
├── core/               ← config, dependencias, middleware
├── models/             ← modelos Pydantic (request/response)
├── services/           ← logica de negocio
├── db/                 ← conexion y queries a PostgreSQL
└── main.py
```

### Git Workflow
- **Branch naming:** `feature/nombre-descriptivo`, `fix/nombre-descriptivo`, `chore/nombre-descriptivo`
- **Commit format:** Conventional Commits — `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`
- **Flujo:** feature branch → PR → `develop` → `main` (nunca directo a `main`)
- **PRs:** descripcion clara de que cambia y por que, minimo 1 reviewer

### Reglas de Arquitectura
- Firebase maneja auth — nunca guardar passwords ni tokens de sesion en PostgreSQL
- Supabase solo en entorno `dev`/`testing`, nunca en produccion
- Angular llama a FastAPI (REST), FastAPI llama a PostgreSQL — no hay acceso directo de frontend a DB
- Cada router de FastAPI protege sus endpoints validando el token de Firebase
- Variables de entorno via `.env`, nunca hardcoded en codigo

### Agentes Disponibles
Ver `.claude/skills/` — invocar con `/arquitectura`, `/backend`, `/frontend`, `/database`, `/mobile`, `/seguridad`

---

## Agentes Especializados (Skills)

### `/arquitectura`
**Proposito:** Decisiones de diseno de sistema.
**Cuando usarlo:** Al iniciar un modulo nuevo, al definir contratos entre frontend y backend, al evaluar trade-offs de estructura.
**Comportamiento:** Actua como arquitecto — evalua opciones, propone estructuras de modulos, define endpoints y modelos de datos, revisa que las decisiones respeten el stack. No escribe codigo, diseña.

### `/backend`
**Proposito:** Desarrollo con FastAPI + Python + auth Firebase.
**Cuando usarlo:** Al crear endpoints, servicios, modelos Pydantic, o integraciones con Firebase/PostgreSQL.
**Comportamiento:** Conoce los patrones del proyecto (routers, servicios, dependencias FastAPI, validacion de tokens Firebase, convencion de errores HTTP). Escribe codigo listo para produccion siguiendo convenciones del equipo.

### `/frontend`
**Proposito:** Desarrollo con Angular + Ionic + TypeScript.
**Cuando usarlo:** Al crear componentes, servicios, guards, o al consumir la API FastAPI desde el cliente.
**Comportamiento:** Conoce la estructura de modulos Angular, uso de Ionic components, como consumir la API REST, y como manejar la sesion de Firebase en el cliente. Genera componentes y servicios siguiendo las convenciones.

### `/database`
**Proposito:** PostgreSQL (produccion) y Supabase (dev/testing).
**Cuando usarlo:** Al disenar esquemas, escribir migraciones, optimizar queries, o configurar Supabase para testing.
**Comportamiento:** Distingue explicitamente que va en Supabase (dev) vs PostgreSQL propio (prod). Nunca sugiere guardar datos de sesion/auth porque eso es responsabilidad de Firebase.

### `/mobile`
**Proposito:** Android Studio + Ionic/Capacitor para apps nativas.
**Cuando usarlo:** Al trabajar con Capacitor plugins, builds nativos, permisos de Android, o signing de APK.
**Comportamiento:** Separado de `/frontend` para no mezclar logica web con logica nativa. Conoce el ciclo de build de Ionic a Android, gestion de plugins nativos y configuracion de `capacitor.config.ts`.

### `/seguridad`
**Proposito:** Revision de seguridad de API y auth.
**Cuando usarlo:** Antes de cada PR importante, al agregar endpoints nuevos, o al revisar que el flujo de Firebase esta correctamente implementado.
**Comportamiento:** Verifica que ningun endpoint quede sin proteccion, que los tokens Firebase se validen en cada request, que no haya datos sensibles expuestos en responses, y que las variables de entorno esten correctamente gestionadas.

---

## Decisiones de Diseno

| Decision | Razon |
|----------|-------|
| Un solo repo template (no monorepo) | Equipo pequeno, menor overhead de mantenimiento |
| Skills sobre scripts | Los skills de Claude Code son mas flexibles y no requieren infraestructura adicional |
| Firebase para auth (no custom) | Delega complejidad de seguridad, no hay passwords en DB |
| Supabase solo en dev | Simplifica testing sin riesgo de mezclar datos de prod |
| 6 agentes por dominio | Granularidad suficiente sin fragmentacion excesiva |

---

## Fuera de Alcance (por ahora)
- CI/CD pipeline (agregar cuando el equipo lo necesite)
- Skill de testing dedicado (cubrir en cada agente de dominio)
- Registry privado de packages (innecesario para equipo de 2-5)
- Agentes por feature de negocio especifica
