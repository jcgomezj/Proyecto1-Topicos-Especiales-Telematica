# GroupsApp — Sistema de Mensajería Distribuida

Proyecto 1 — ST0263 Tópicos Especiales en Telemática / SI3007 Sistemas Distribuidos  
Universidad EAFIT — 2026-1

## Equipo
- **Camilo** 
- **Santiago** 
- **Posso**

---

## Descripción

GroupsApp es una aplicación de mensajería instantánea similar a WhatsApp/Telegram con arquitectura de microservicios. Permite crear grupos, enviar mensajes, compartir archivos e imágenes, y ver el estado de presencia de los usuarios en tiempo real.

---

## Funcionalidades

- Registro y autenticación de usuarios con JWT
- Creación y gestión de grupos
- Mensajería en grupo con historial
- Estado de mensajes: enviado ✓, entregado ✓✓, leído ✓✓ (verde)
- Subida y descarga de archivos e imágenes
- Estado de presencia online/offline en tiempo real
- Interfaz web tipo WhatsApp

---

## Arquitectura

```
Cliente (Browser)
      ↓
API REST (FastAPI) — puerto 8000
      ↓
PostgreSQL — puerto 5432
```

El monolito contiene todos los módulos:
- `auth` — registro, login, JWT
- `users` — perfiles y presencia
- `groups` — grupos, miembros, canales
- `messages` — mensajes y estado
- `files` — archivos e imágenes

---

## Requisitos

- Docker
- Docker Compose

---

## Cómo correr el proyecto localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/jcgomezj/Proyecto1-Topicos-Especiales-Telematica.git
cd Proyecto1-Topicos-Especiales-Telematica
git checkout camilo/auth-users
```

### 2. Crear el archivo de variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/groupsapp
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Levantar el monolito

```bash
cd monolith
docker compose up --build monolith db
```

### 4. Abrir en el navegador

```
http://localhost:8000
```

---

## Cómo correr con acceso externo (ngrok)

Para que otros usuarios puedan acceder desde sus PCs:

### 1. Instalar ngrok

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

### 2. Configurar token de ngrok

Crear cuenta en [ngrok.com](https://ngrok.com) y obtener el authtoken:

```bash
ngrok config add-authtoken TU_TOKEN
```

### 3. Exponer el puerto

En una terminal separada (con el monolito corriendo):

```bash
ngrok http 8000
```

Compartir la URL generada con los demás usuarios.

---

## Estructura del repositorio

```
Proyecto1-Topicos-Especiales-Telematica/
├── monolith/                  # Aplicación monolítica (Entrega 1)
│   ├── main.py                # Punto de entrada FastAPI
│   ├── database.py            # Conexión PostgreSQL
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── group.py
│   │   └── message.py
│   ├── routes/                # Endpoints REST
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── groups.py
│   │   ├── messages.py
│   │   └── files.py
│   ├── schemas/               # Esquemas Pydantic
│   ├── static/                # Frontend HTML
│   ├── uploads/               # Archivos subidos
│   ├── requirements.txt
│   └── Dockerfile
├── auth_service/              # Microservicio de autenticación
├── user_service/              # Microservicio de usuarios
├── docker-compose.yml
└── .gitignore
```

---

## Endpoints principales

### Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/logout` | Cerrar sesión |

### Users
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/` | Listar usuarios |
| GET | `/users/{id}` | Ver perfil |
| PUT | `/users/{id}` | Actualizar perfil |
| PATCH | `/users/{id}/presence` | Actualizar presencia |

### Groups
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/groups/` | Crear grupo |
| GET | `/groups/` | Listar grupos |
| POST | `/groups/{id}/members` | Agregar miembro |
| GET | `/groups/{id}/members` | Ver miembros |
| POST | `/groups/{id}/channels` | Crear canal |

### Messages
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/messages/` | Enviar mensaje |
| GET | `/messages/group/{id}` | Mensajes de grupo |
| GET | `/messages/direct/{id}/{id}` | Mensajes directos |
| PATCH | `/messages/{id}/status` | Actualizar estado |

### Files
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/files/upload/{message_id}` | Subir archivo |
| GET | `/files/download/{filename}` | Descargar archivo |
| GET | `/files/message/{message_id}` | Archivos de un mensaje |

---

## Documentación interactiva

Con el proyecto corriendo, accede a:

```
http://localhost:8000/docs
```

## Uso de IA

En esta entrega se utilizaron herramientas de IA para aspectos operativos puntuales (estructura de Dockerfiles, boilerplate de configuración). El diseño del modelo de datos, la definición de endpoints y la lógica de negocio fueron desarrollados por nosotros.

