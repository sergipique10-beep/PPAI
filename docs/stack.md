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
