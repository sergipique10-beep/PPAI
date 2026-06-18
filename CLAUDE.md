# PPAI — Guia para Claude Code

Este archivo define como Claude Code debe trabajar en proyectos de PPAI. Leerlo completo antes de comenzar cualquier tarea.

---

## Stack tecnologico

| Capa | Tecnologia |
|------|-----------|
| Frontend web | Angular + TypeScript |
| Frontend mobile | Ionic + Capacitor + TypeScript |
| App nativa | Android Studio |
| Backend | Python + FastAPI |
| Base de datos (prod) | PostgreSQL en VH Cloud |
| Base de datos (dev) | Supabase |
| Autenticacion | Firebase Auth |
| Runtime Node | NVM — usar la version del archivo `.nvmrc` del proyecto |

---

## Convenciones de codigo

### TypeScript / Angular / Ionic

- Componentes: `PascalCase` con sufijo → `UserProfileComponent`
- Servicios: `PascalCase` con sufijo → `AuthService`
- Guards: `PascalCase` con sufijo → `AuthGuard`
- Pipes: `PascalCase` con sufijo → `DateFormatPipe`
- Variables y funciones: `camelCase` → `getUserById()`
- Constantes: `UPPER_SNAKE_CASE` → `MAX_RETRY_COUNT`
- Archivos: `kebab-case` → `user-profile.component.ts`
- Interfaces: prefijo `I` → `IUserProfile`
- Enums: `PascalCase` → `UserRole`

### Python / FastAPI

- Archivos y modulos: `snake_case` → `user_service.py`
- Variables y funciones: `snake_case` → `get_user_by_id()`
- Clases: `PascalCase` → `UserService`
- Modelos Pydantic (request): sufijo `Request` → `UserCreateRequest`
- Modelos Pydantic (response): sufijo `Response` → `UserResponse`
- Constantes: `UPPER_SNAKE_CASE` → `MAX_RETRY_COUNT`
- Routers: sufijo `_router` → `auth_router.py`

---

## Estructura de carpetas

### Frontend (Angular/Ionic)

```
src/
├── app/
│   ├── core/              ← servicios singleton, guards, interceptors, modelos globales
│   ├── shared/            ← componentes, pipes y directivas reutilizables entre features
│   ├── features/          ← un modulo por funcionalidad de negocio
│   │   └── [feature]/
│   │       ├── components/
│   │       ├── pages/
│   │       ├── services/
│   │       └── [feature].module.ts
│   └── app.module.ts
├── assets/
└── environments/
    ├── environment.ts
    └── environment.prod.ts
```

### Backend (FastAPI)

```
app/
├── api/
│   └── routers/           ← un archivo por dominio (auth_router.py, user_router.py)
├── core/
│   ├── config.py          ← variables de entorno via pydantic-settings
│   ├── dependencies.py    ← dependencias de FastAPI (get_db, verify_token, etc.)
│   └── middleware.py      ← middleware global (CORS, logging)
├── models/                ← modelos Pydantic de request y response
├── services/              ← logica de negocio (sin acceso directo a DB)
├── db/
│   ├── connection.py      ← pool de conexion a PostgreSQL
│   ├── migrations/        ← migraciones SQL versionadas
│   └── queries/           ← queries SQL organizadas por dominio
└── main.py
```

---

## Git workflow

- **Branches:** `feature/nombre-en-kebab`, `fix/nombre-en-kebab`, `chore/nombre-en-kebab`
- **Commits:** Conventional Commits
  - `feat: descripcion` — nueva funcionalidad
  - `fix: descripcion` — correccion de bug
  - `chore: descripcion` — tareas de mantenimiento
  - `docs: descripcion` — documentacion
  - `refactor: descripcion` — refactorizacion sin cambio de comportamiento
  - `test: descripcion` — tests
- **Flujo:** branch → PR → `develop` → (release) → `main`
- **Regla:** nunca hacer push directo a `main` ni a `develop`

---

## Reglas de arquitectura

1. **Firebase es el unico responsable de auth.** No almacenar passwords, tokens de sesion ni datos de credenciales en PostgreSQL.
2. **Todo endpoint de FastAPI que requiera autenticacion debe validar el token de Firebase** usando la dependencia `verify_token` de `core/dependencies.py`.
3. **Angular consume FastAPI via REST.** No hay acceso directo del frontend a la base de datos.
4. **Supabase solo en `dev`/`testing`.** La variable `ENVIRONMENT` en `.env` debe ser `dev` para habilitar Supabase.
5. **Variables de entorno en `.env`.** Nunca hardcodear URLs, keys ni credenciales en el codigo.
6. **Un router por dominio en FastAPI.** No agrupar endpoints no relacionados en el mismo router.

---

## Modo de escritura de codigo — Lazy Senior (Ponytail)

Antes de escribir cualquier codigo, detenerse en el primer escalon que aplique:

1. ¿Necesita existir? → Omitirlo (YAGNI)
2. ¿Lo da la stdlib? → Usarla.
3. ¿Es una feature nativa de la plataforma? → Usarla.
4. ¿Ya lo resuelve una dependencia instalada? → Usarla.
5. ¿Se puede hacer en una linea? → Hacerlo en una linea.
6. Solo entonces: escribir el minimo codigo que funcione.

**Reglas:**

- Sin abstracciones que no fueron pedidas explicitamente.
- Sin dependencias nuevas si se puede evitar.
- Sin boilerplate que nadie pidio.
- Borrar sobre agregar. Aburrido sobre ingenioso. La menor cantidad de archivos posible.
- Cuestionar pedidos complejos: "¿Realmente necesitas X, o alcanza con Y?"
- Marcar simplificaciones intencionales con un comentario `# ponytail:`. Si el atajo tiene un techo conocido (lock global, scan O(n²), heuristica naive), el comentario nombra el techo y el camino de mejora.
- Cuando dos enfoques de stdlib tienen el mismo tamano, elegir el que maneja bien los edge cases. Lazy es menos codigo, no el algoritmo mas fragil.

**Self-check obligatorio:** la logica no trivial deja UN check ejecutable atras — lo minimo que falla si la logica se rompe (un assert o un archivo de test minimo, sin frameworks ni fixtures). Las one-liners triviales no necesitan test.

**No se aplica lazy a:** validacion de input en limites de confianza, manejo de errores que previene perdida de datos, seguridad, accesibilidad, ni nada pedido explicitamente.

---

## Agentes especializados

Disponibles en `.claude/skills/`. Invocar con:

| Comando | Cuando usarlo |
|---------|--------------|
| `/arquitectura` | Decisiones de diseno de sistema, nuevos modulos, contratos entre capas |
| `/backend` | Endpoints FastAPI, servicios Python, validacion Firebase, queries PostgreSQL |
| `/frontend` | Componentes Angular, paginas Ionic, servicios, guards, consumo de API |
| `/database` | Esquemas PostgreSQL, migraciones, queries, configuracion Supabase dev |
| `/mobile` | Capacitor plugins, builds Android, permisos nativos, signing APK |
| `/seguridad` | Revision de endpoints sin proteccion, validacion de tokens, datos expuestos |

---

## Entorno local — arranque rapido

### Frontend
```bash
nvm use                  # usa la version de .nvmrc
npm install
ng serve                 # Angular en http://localhost:4200
# o para Ionic:
ionic serve
```

### Backend
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # completar variables
uvicorn app.main:app --reload
```

### Base de datos (dev con Supabase)
```bash
supabase start           # requiere Supabase CLI
```
