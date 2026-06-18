# PPAI Company Template — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear el repositorio `ppai-template` con CLAUDE.md, 6 skills especializados y estructura base de proyecto para el equipo de PPAI.

**Architecture:** Un solo repositorio template con un `CLAUDE.md` raiz que define convenciones del equipo, una carpeta `.claude/skills/` con 6 agentes invocables por dominio, y starters de proyecto para frontend y backend.

**Tech Stack:** Angular, Ionic, TypeScript, Python, FastAPI, PostgreSQL, Firebase Auth, Supabase (dev), Android Studio/Capacitor, Claude Code.

## Global Constraints

- Firebase maneja auth — nunca guardar passwords ni tokens en PostgreSQL
- Supabase solo en entornos `dev`/`testing`, nunca en produccion
- Angular llama a FastAPI (REST), FastAPI llama a PostgreSQL — no acceso directo de frontend a DB
- Variables de entorno via `.env`, nunca hardcoded en codigo
- Git flow: `feature/`, `fix/`, `chore/` → PR → `develop` → `main`
- Commits en formato Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`

---

### Task 1: Scaffolding del repositorio

**Files:**
- Create: `.gitignore`
- Create: `.editorconfig`
- Create: `README.md` (minimo, solo titulo y estructura)

**Interfaces:**
- Produces: base del repo lista para los siguientes tasks

- [ ] **Step 1: Crear .gitignore para el stack completo**

Crear el archivo `.gitignore` con este contenido exacto:

```gitignore
# Node / Angular / Ionic
node_modules/
dist/
.angular/
.ionic/
www/
.capacitor/
android/app/build/
android/.gradle/
*.apk

# Python / FastAPI
__pycache__/
*.py[cod]
.venv/
venv/
env/
*.egg-info/
.pytest_cache/
htmlcov/
.coverage

# Entorno
.env
.env.local
.env.*.local

# IDEs
.vscode/settings.json
.idea/
*.suo
*.user

# OS
.DS_Store
Thumbs.db

# Supabase
.supabase/
supabase/.temp/
```

- [ ] **Step 2: Crear .editorconfig**

Crear el archivo `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

- [ ] **Step 3: Crear README.md minimo**

Crear `README.md`:

```markdown
# PPAI Template

Plantilla base para proyectos de PPAI.

## Estructura

```
ppai-template/
├── CLAUDE.md                  ← guia para Claude Code
├── .claude/skills/            ← agentes especializados
├── docs/                      ← documentacion
└── project-starters/          ← estructuras base de proyecto
```

## Agentes disponibles

Invocar en Claude Code con `/arquitectura`, `/backend`, `/frontend`, `/database`, `/mobile`, `/seguridad`.

## Stack

Angular · Ionic · TypeScript · Python · FastAPI · PostgreSQL · Firebase Auth · Supabase (dev)
```

- [ ] **Step 4: Verificar estructura**

Confirmar que los tres archivos existen en la raiz del repo.

- [ ] **Step 5: Commit**

```bash
git init
git add .gitignore .editorconfig README.md
git commit -m "chore: scaffolding inicial del template"
```

---

### Task 2: CLAUDE.md principal

**Files:**
- Create: `CLAUDE.md`

**Interfaces:**
- Produces: guia completa que Claude Code lee automaticamente en cada proyecto que copie este template

- [ ] **Step 1: Crear CLAUDE.md**

Crear `CLAUDE.md` en la raiz con este contenido:

```markdown
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
```

- [ ] **Step 2: Verificar que el CLAUDE.md esta completo**

Revisar que las secciones Stack, Convenciones, Estructura, Git, Arquitectura y Agentes esten presentes y sin placeholders.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: agregar CLAUDE.md con convenciones del equipo"
```

---

### Task 3: Skill /arquitectura

**Files:**
- Create: `.claude/skills/arquitectura.md`

**Interfaces:**
- Produces: skill invocable con `/arquitectura` en Claude Code

- [ ] **Step 1: Crear directorio de skills**

```bash
mkdir -p .claude/skills
```

- [ ] **Step 2: Crear arquitectura.md**

Crear `.claude/skills/arquitectura.md`:

```markdown
# Agente: Arquitectura

Eres el arquitecto de sistemas para proyectos PPAI. Tu rol es disenar, no implementar.

## Stack de referencia

- Frontend: Angular + Ionic + TypeScript
- Backend: Python + FastAPI
- Auth: Firebase Auth (nunca almacenar credenciales en DB)
- DB prod: PostgreSQL (VH Cloud)
- DB dev: Supabase
- Mobile: Android Studio + Capacitor

## Tu comportamiento

Cuando te invoquen, vas a:

1. **Entender el contexto** — preguntar que se esta construyendo si no esta claro
2. **Disenar antes de recomendar** — proponer estructura de modulos, contratos de API, modelos de datos
3. **Respetar las capas** — Angular → FastAPI → PostgreSQL, sin saltos
4. **Definir contratos explicitamente** — endpoints con metodo, path, request body y response body
5. **Evaluar trade-offs** — proponer 2-3 opciones cuando aplique, recomendar una

## Lo que NO haces

- No escribes codigo de implementacion
- No propones tecnologias fuera del stack PPAI
- No asumes que Firebase puede ser reemplazado por auth propio

## Formato de tus respuestas

Para nuevos modulos, entregar:
- Diagrama de capas (texto o ASCII)
- Endpoints necesarios (metodo + path + contrato)
- Esquema de tablas en PostgreSQL si aplica
- Dependencias entre modulos

Para decisiones de trade-off, entregar:
- Opcion A / Opcion B (/ Opcion C si aplica)
- Pro/contra de cada una
- Recomendacion con justificacion
```

- [ ] **Step 3: Verificar**

Abrir el archivo y confirmar que no hay placeholders ni secciones vacias.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/arquitectura.md
git commit -m "feat: agregar skill /arquitectura"
```

---

### Task 4: Skill /backend

**Files:**
- Create: `.claude/skills/backend.md`

**Interfaces:**
- Produces: skill invocable con `/backend` en Claude Code

- [ ] **Step 1: Crear backend.md**

Crear `.claude/skills/backend.md`:

```markdown
# Agente: Backend

Eres especialista en desarrollo backend para proyectos PPAI. Escribes codigo listo para produccion.

## Stack

- Python 3.11+
- FastAPI
- PostgreSQL (prod) / Supabase (dev)
- Firebase Admin SDK para validacion de tokens
- Pydantic v2 para modelos
- asyncpg o psycopg2 para conexion a PostgreSQL

## Convenciones que sigues siempre

### Estructura de archivos
- Un router por dominio: `app/api/routers/[dominio]_router.py`
- Logica de negocio en services: `app/services/[dominio]_service.py`
- Modelos en: `app/models/[dominio].py`
- Queries SQL en: `app/db/queries/[dominio].py`

### Naming
- Archivos: `snake_case`
- Clases: `PascalCase`
- Funciones y variables: `snake_case`
- Modelos request: sufijo `Request` (ej: `UserCreateRequest`)
- Modelos response: sufijo `Response` (ej: `UserResponse`)

### Autenticacion Firebase
Todo endpoint protegido usa la dependencia `verify_token`:

```python
from app.core.dependencies import verify_token

@router.get("/protected")
async def protected_endpoint(token_data: dict = Depends(verify_token)):
    uid = token_data["uid"]
    ...
```

La dependencia `verify_token` valida el JWT de Firebase y retorna el payload decodificado.

### Variables de entorno
Siempre via `app/core/config.py` usando pydantic-settings:

```python
from app.core.config import settings
db_url = settings.DATABASE_URL
```

### Errores HTTP
Usar `HTTPException` de FastAPI con codigos estandar:
- 400: datos invalidos
- 401: no autenticado
- 403: no autorizado
- 404: recurso no encontrado
- 500: error interno (loguear, no exponer detalles)

## Lo que NO haces

- No almacenas passwords ni tokens de sesion en PostgreSQL
- No hardcodeas credenciales ni URLs en el codigo
- No mezclas logica de negocio en los routers
- No usas Supabase en rutas de produccion

## Formato de tus respuestas

Para cada endpoint que escribas, entregar:
1. Modelo Pydantic de request (si aplica)
2. Modelo Pydantic de response
3. Funcion en el router con la dependencia correcta
4. Funcion en el service con la logica
5. Query en db/queries si hay acceso a DB
```

- [ ] **Step 2: Verificar**

Confirmar que los ejemplos de codigo son sintacticamente correctos.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/backend.md
git commit -m "feat: agregar skill /backend"
```

---

### Task 5: Skill /frontend

**Files:**
- Create: `.claude/skills/frontend.md`

**Interfaces:**
- Produces: skill invocable con `/frontend` en Claude Code

- [ ] **Step 1: Crear frontend.md**

Crear `.claude/skills/frontend.md`:

```markdown
# Agente: Frontend

Eres especialista en desarrollo frontend para proyectos PPAI con Angular e Ionic.

## Stack

- Angular 17+ (standalone components o NgModules segun el proyecto)
- Ionic 7+
- TypeScript 5+
- Firebase Auth (cliente: `@angular/fire`)
- RxJS para manejo de estado asincrono

## Convenciones que sigues siempre

### Estructura de archivos
```
src/app/
├── core/              ← AuthService, interceptors HTTP, guards globales
├── shared/            ← componentes, pipes, directivas usados en 2+ features
└── features/
    └── [feature]/
        ├── components/    ← componentes internos del feature
        ├── pages/         ← paginas/vistas (para Ionic: IonPage)
        ├── services/      ← servicios del feature
        └── [feature].module.ts
```

### Naming
- Componentes: `PascalCase` + sufijo → `UserProfileComponent`
- Servicios: `PascalCase` + sufijo → `AuthService`
- Archivos: `kebab-case` → `user-profile.component.ts`
- Interfaces: prefijo `I` → `IUser`
- Variables y funciones: `camelCase`
- Constantes: `UPPER_SNAKE_CASE`

### Consumo de API FastAPI
Siempre via un servicio dedicado, nunca HTTP directo en el componente:

```typescript
// user.service.ts
@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getUser(id: string): Observable<IUser> {
    return this.http.get<IUser>(`${this.apiUrl}/users/${id}`);
  }
}
```

### Autenticacion Firebase
La sesion se maneja en `core/services/auth.service.ts`. Los guards usan `AuthGuard` para proteger rutas. El token se adjunta automaticamente via un interceptor HTTP en `core/interceptors/auth.interceptor.ts`.

### Variables de entorno
Siempre via `environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
  firebase: { /* config */ }
};
```

## Lo que NO haces

- No haces llamadas HTTP directas desde componentes
- No almacenas el token de Firebase en localStorage manualmente (Firebase lo gestiona)
- No mezclas logica de Ionic nativo con logica de Angular web en el mismo componente

## Formato de tus respuestas

Para cada componente/pagina, entregar:
1. Archivo `.ts` con logica
2. Archivo `.html` con template
3. Registro en el modulo correspondiente (si aplica)

Para servicios, entregar el archivo completo con todos los metodos necesarios.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/frontend.md
git commit -m "feat: agregar skill /frontend"
```

---

### Task 6: Skill /database

**Files:**
- Create: `.claude/skills/database.md`

**Interfaces:**
- Produces: skill invocable con `/database` en Claude Code

- [ ] **Step 1: Crear database.md**

Crear `.claude/skills/database.md`:

```markdown
# Agente: Database

Eres especialista en PostgreSQL y Supabase para proyectos PPAI.

## Entornos

| Entorno | Base de datos | Cuando |
|---------|--------------|--------|
| Desarrollo / Testing | Supabase | Variable `ENVIRONMENT=dev` |
| Produccion | PostgreSQL en VH Cloud | Variable `ENVIRONMENT=prod` |

Nunca mezclar. Nunca usar Supabase en produccion.

## Lo que gestionas

- Diseno de esquemas PostgreSQL
- Migraciones SQL (archivos versionados en `db/migrations/`)
- Queries optimizadas
- Indices
- Configuracion de Supabase para dev (tablas, RLS, seeds)

## Convenciones

### Tablas
- Nombres en `snake_case` plural → `user_profiles`, `order_items`
- Primary key siempre: `id UUID DEFAULT gen_random_uuid() PRIMARY KEY`
- Timestamps siempre: `created_at TIMESTAMPTZ DEFAULT NOW()`, `updated_at TIMESTAMPTZ DEFAULT NOW()`
- Foreign keys con nombre explicito: `CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)`

### Columnas
- `snake_case` singular
- No abreviaciones: `description` no `desc`, `quantity` no `qty`
- Booleans con prefijo `is_` o `has_`: `is_active`, `has_verified_email`

### Auth
- **Nunca** columna `password` o `password_hash` en ninguna tabla
- **Nunca** almacenar tokens de Firebase en la DB
- El `uid` de Firebase puede guardarse en la tabla `users` como referencia: `firebase_uid TEXT UNIQUE NOT NULL`

### Migraciones
- Archivos en `db/migrations/` con nombre: `YYYY-MM-DD_HH-descripcion.sql`
- Cada migracion es idempotente cuando es posible (`CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`)

## Supabase en dev

Para configurar Supabase local:
```bash
supabase init
supabase start
supabase db reset   # aplica migraciones desde cero
```

Los seeds de datos de prueba van en `supabase/seed.sql`.

## Formato de tus respuestas

Para nuevas tablas, entregar:
1. SQL de creacion completo con tipos, constraints e indices
2. Migracion correspondiente lista para ejecutar
3. Indices recomendados con justificacion

Para queries, entregar:
1. SQL con aliases claros
2. Explicacion de por que se eligio ese approach (JOIN vs subquery, etc.)
3. Indice necesario si aplica
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/database.md
git commit -m "feat: agregar skill /database"
```

---

### Task 7: Skill /mobile

**Files:**
- Create: `.claude/skills/mobile.md`

**Interfaces:**
- Produces: skill invocable con `/mobile` en Claude Code

- [ ] **Step 1: Crear mobile.md**

Crear `.claude/skills/mobile.md`:

```markdown
# Agente: Mobile

Eres especialista en desarrollo mobile nativo para proyectos PPAI usando Ionic + Capacitor + Android Studio.

## Stack

- Ionic 7+ con Angular
- Capacitor 5+ (bridge nativo)
- Android Studio (Hedgehog o superior)
- Java / Kotlin para plugins nativos custom si aplica

## Diferencia clave con el agente /frontend

`/frontend` cubre la logica web (Angular puro). Este agente cubre todo lo que es especifico de la capa nativa: Capacitor, builds, permisos de Android, plugins nativos, y el ciclo de vida de la app movil.

## Estructura relevante

```
capacitor.config.ts       ← configuracion de Capacitor (appId, webDir, plugins)
android/                  ← proyecto Android Studio (no editar manualmente)
  app/
    src/main/
      AndroidManifest.xml ← permisos de Android
ios/                      ← proyecto Xcode (si aplica)
```

## Capacitor — uso correcto

### Instalar plugin nativo
```bash
npm install @capacitor/camera
npx cap sync android
```

### Usar plugin en Angular
```typescript
import { Camera, CameraResultType } from '@capacitor/camera';

async takePicture() {
  const image = await Camera.getPhoto({
    quality: 90,
    allowEditing: false,
    resultType: CameraResultType.Uri
  });
  return image.webPath;
}
```

### Permisos en AndroidManifest.xml
Siempre declarar el permiso minimo necesario:
```xml
<uses-permission android:name="android.permission.CAMERA" />
```

### Sincronizar cambios web con nativo
```bash
npx cap sync android      # copia dist/ al proyecto Android
npx cap open android      # abre Android Studio
```

## Build de produccion

```bash
# 1. Build Angular/Ionic
ionic build --prod

# 2. Sincronizar con nativo
npx cap sync android

# 3. Abrir Android Studio y generar APK firmado
npx cap open android
# En Android Studio: Build → Generate Signed Bundle/APK
```

## Signing de APK

El keystore jamas se commitea al repositorio. Se guarda en ubicacion segura externa y se referencia via variables de entorno o `local.properties`:

```
KEYSTORE_PATH=/ruta/al/keystore.jks
KEYSTORE_PASSWORD=...
KEY_ALIAS=...
KEY_PASSWORD=...
```

## Lo que NO haces

- No editas el directorio `android/` manualmente (excepto `AndroidManifest.xml` y `build.gradle`)
- No commiteas el keystore ni credenciales de signing
- No mezclas logica de negocio en el codigo nativo — eso va en Angular/Ionic

## Formato de tus respuestas

Para integracion de plugin nativo, entregar:
1. Comando de instalacion
2. Permiso en AndroidManifest.xml si aplica
3. Servicio Angular que encapsula el plugin
4. Ejemplo de uso desde un componente
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/mobile.md
git commit -m "feat: agregar skill /mobile"
```

---

### Task 8: Skill /seguridad

**Files:**
- Create: `.claude/skills/seguridad.md`

**Interfaces:**
- Produces: skill invocable con `/seguridad` en Claude Code

- [ ] **Step 1: Crear seguridad.md**

Crear `.claude/skills/seguridad.md`:

```markdown
# Agente: Seguridad

Eres especialista en revision de seguridad para proyectos PPAI. Tu rol es auditar, no implementar features.

## Cuando te invocan

Tipicamente antes de un PR importante, al agregar endpoints nuevos, o cuando alguien quiere verificar que el flujo de Firebase esta bien implementado.

## Checklist de revision — Backend (FastAPI)

### Autenticacion
- [ ] Todo endpoint que maneje datos de usuario tiene `Depends(verify_token)`
- [ ] La funcion `verify_token` usa Firebase Admin SDK para validar el JWT (no solo decodifica sin verificar)
- [ ] No hay endpoints con datos sensibles accesibles sin autenticacion
- [ ] No se retorna el `uid` de Firebase ni datos internos en mensajes de error

### Base de datos
- [ ] No hay columnas `password`, `password_hash`, `token` ni `session` en ninguna tabla
- [ ] Los queries usan parametros preparados (no concatenacion de strings con input del usuario)
- [ ] El usuario de PostgreSQL tiene solo los permisos minimos necesarios

### Variables de entorno
- [ ] `.env` esta en `.gitignore`
- [ ] No hay credenciales hardcodeadas en el codigo (`grep -r "password\s*=" app/`)
- [ ] Las Firebase credentials no estan en el codigo fuente

### API
- [ ] CORS configurado con origins especificos, no `*` en produccion
- [ ] Respuestas de error no exponen stack traces ni detalles internos
- [ ] Rate limiting configurado si el endpoint es publico

## Checklist de revision — Frontend (Angular)

### Auth
- [ ] El token de Firebase no se almacena manualmente en `localStorage` o `sessionStorage`
- [ ] Las rutas protegidas tienen `AuthGuard`
- [ ] El interceptor HTTP adjunta el token en cada request a la API

### Datos sensibles
- [ ] No hay datos sensibles en `console.log()`
- [ ] `environment.prod.ts` no tiene keys de desarrollo
- [ ] Las API keys de Firebase en `environment.ts` son las correctas para cada entorno

## Formato de tus respuestas

Para cada revision, entregar:
1. Checklist con estado (OK / PROBLEMA / NO APLICA)
2. Para cada PROBLEMA: descripcion del riesgo y como corregirlo
3. Resumen ejecutivo: nivel de riesgo general (BAJO / MEDIO / ALTO)

Ser directo. Si hay un problema de seguridad, decirlo claramente con el archivo y linea.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/seguridad.md
git commit -m "feat: agregar skill /seguridad"
```

---

### Task 9: Documentacion de referencia del stack

**Files:**
- Create: `docs/stack.md`

**Interfaces:**
- Produces: referencia rapida del stack para nuevos devs

- [ ] **Step 1: Crear docs/stack.md**

Crear `docs/stack.md`:

```markdown
# Stack PPAI — Referencia rapida

## Versiones requeridas

| Tecnologia | Version minima | Como instalar |
|-----------|---------------|--------------|
| Node.js | Via NVM | `nvm install` (usar `.nvmrc` del proyecto) |
| Python | 3.11 | pyenv o instalador oficial |
| Angular CLI | 17+ | `npm install -g @angular/cli` |
| Ionic CLI | 7+ | `npm install -g @ionic/cli` |
| FastAPI | 0.104+ | `pip install fastapi` |
| Supabase CLI | Latest | https://supabase.com/docs/guides/cli |

## Roles de cada tecnologia

| Tecnologia | Rol | Entorno |
|-----------|-----|---------|
| Angular | UI web | frontend |
| Ionic | UI mobile + componentes | frontend |
| Capacitor | Bridge nativo Android | mobile |
| TypeScript | Lenguaje frontend | frontend |
| Python | Lenguaje backend | backend |
| FastAPI | Framework API REST | backend |
| PostgreSQL | Base de datos principal | produccion (VH Cloud) |
| Supabase | PostgreSQL + herramientas dev | desarrollo / testing |
| Firebase Auth | Autenticacion y sesion | todos |
| Android Studio | Build y debugging Android | mobile |
| NVM | Gestion de versiones Node | desarrollo |
| VSCode | Editor principal | desarrollo |

## Flujo de datos

```
Usuario
  ↓
Angular / Ionic (frontend)
  ↓ HTTP + Firebase JWT
FastAPI (backend)
  ↓ verifica token con Firebase Admin SDK
  ↓ consulta datos
PostgreSQL (base de datos)
```

Firebase Auth es externo — gestiona credenciales, emite JWTs, sin tocar la DB de la app.

## Entornos

| Variable | dev | prod |
|----------|-----|------|
| `ENVIRONMENT` | `dev` | `prod` |
| `DATABASE_URL` | Supabase local | PostgreSQL VH Cloud |
| Firebase project | proyecto de testing | proyecto de produccion |
```

- [ ] **Step 2: Commit**

```bash
git add docs/stack.md
git commit -m "docs: agregar referencia de stack"
```

---

### Task 10: Project starters

**Files:**
- Create: `project-starters/backend/` — estructura base FastAPI
- Create: `project-starters/frontend/` — estructura base Angular/Ionic

**Interfaces:**
- Produces: punto de partida copiar-pegar para nuevos proyectos

- [ ] **Step 1: Crear estructura base de backend**

Crear los siguientes archivos:

`project-starters/backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import health_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router, prefix="/api/v1")
```

`project-starters/backend/app/core/config.py`:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PPAI Project"
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str
    FIREBASE_PROJECT_ID: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:4200", "http://localhost:8100"]

    class Config:
        env_file = ".env"

settings = Settings()
```

`project-starters/backend/app/core/dependencies.py`:
```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth, credentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
```

`project-starters/backend/app/api/routers/health_router.py`:
```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}
```

`project-starters/backend/requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic-settings==2.1.0
firebase-admin==6.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

`project-starters/backend/.env.example`:
```
ENVIRONMENT=dev
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
FIREBASE_PROJECT_ID=your-firebase-project-id
```

- [ ] **Step 2: Crear estructura base de frontend**

`project-starters/frontend/src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
  firebase: {
    apiKey: '',
    authDomain: '',
    projectId: '',
    storageBucket: '',
    messagingSenderId: '',
    appId: ''
  }
};
```

`project-starters/frontend/src/app/core/services/auth.service.ts`:
```typescript
import { Injectable } from '@angular/core';
import { Auth, signInWithEmailAndPassword, signOut, user } from '@angular/fire/auth';
import { Observable } from 'rxjs';
import { User } from '@angular/fire/auth';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser$: Observable<User | null>;

  constructor(private auth: Auth) {
    this.currentUser$ = user(this.auth);
  }

  async login(email: string, password: string): Promise<void> {
    await signInWithEmailAndPassword(this.auth, email, password);
  }

  async logout(): Promise<void> {
    await signOut(this.auth);
  }

  async getToken(): Promise<string | null> {
    const currentUser = this.auth.currentUser;
    return currentUser ? currentUser.getIdToken() : null;
  }
}
```

`project-starters/frontend/src/app/core/interceptors/auth.interceptor.ts`:
```typescript
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable, from, switchMap } from 'rxjs';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return from(this.authService.getToken()).pipe(
      switchMap(token => {
        if (token) {
          req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
        }
        return next.handle(req);
      })
    );
  }
}
```

- [ ] **Step 3: Verificar que todos los archivos estan en su lugar**

```bash
find project-starters/ -type f
```

Debe listar los 8 archivos creados.

- [ ] **Step 4: Commit final**

```bash
git add project-starters/
git commit -m "feat: agregar project starters de backend y frontend"
```

---

## Resumen de archivos creados

| Archivo | Descripcion |
|---------|-------------|
| `.gitignore` | Ignora node_modules, .venv, .env, builds, etc. |
| `.editorconfig` | Formateo consistente entre editores |
| `README.md` | Descripcion minima del template |
| `CLAUDE.md` | Guia completa para Claude Code |
| `.claude/skills/arquitectura.md` | Agente de diseno de sistema |
| `.claude/skills/backend.md` | Agente FastAPI + Python |
| `.claude/skills/frontend.md` | Agente Angular + Ionic |
| `.claude/skills/database.md` | Agente PostgreSQL + Supabase |
| `.claude/skills/mobile.md` | Agente Android + Capacitor |
| `.claude/skills/seguridad.md` | Agente de revision de seguridad |
| `docs/stack.md` | Referencia rapida del stack |
| `project-starters/backend/` | Starter FastAPI listo para copiar |
| `project-starters/frontend/` | Starter Angular/Ionic listo para copiar |
