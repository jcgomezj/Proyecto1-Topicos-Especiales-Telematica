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

## Aplicación desplegada en AWS

| | |
|---|---|
| **URL de la app** | http://3.210.232.100:8000 |
| **Documentación API (Swagger)** | http://3.210.232.100:8000/docs |
| **Proveedor** | AWS EC2 (t3.small, Ubuntu 24.04) |
| **IP** | Elastic IP fija |

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

## Arquitectura Original

```
Cliente (Browser)
      ↓
API REST (FastAPI) — puerto 8000
      ↓
PostgreSQL — puerto 5432
```

## Arquitectura con Microservicios y API Gateway

```
                    ┌─────────────┐
                    │    Kong     │  Puerto 80
                    │ API Gateway │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │  Auth   │      │    User     │    │   File    │
   │ Service │      │   Service   │    │  Service  │
   └─────────┘      └─────────────┘    └───────────┘
                                              │
                                         ┌─────▼─────┐
                                         │   MinIO   │
                                         │  (S3)     │
                                         └───────────┘
```

### Servicios y Rutas

| Servicio | Puerto Directo | Ruta Kong |
|----------|---------------|-----------|
| Kong Gateway | 80 | - |
| Monolith | 8000 | /monolith |
| Auth Service | 8001 | /auth |
| User Service | 8002 | /users |
| Group Service | 8003 | /groups |
| Messaging Service | 8004 | /messages |
| File Service | 8005 | /files |
| MinIO S3 | 9000 | - |
| MinIO Console | 9001 | - |

### Ejecución con Docker Compose

```bash
# Construir y levantar todos los servicios
docker compose up --build -d

# Ver logs
docker compose logs -f

# Detener servicios
docker compose down
```

### Endpoints después de Kong

- **Auth**: `http://localhost/auth/*`
- **Users**: `http://localhost/users/*`
- **Groups**: `http://localhost/groups/*`
- **Messages**: `http://localhost/messages/*`
- **Files**: `http://localhost/files/*`

### Endpoints directos (sin Kong)

- **Auth Service**: http://localhost:8001
- **User Service**: http://localhost:8002
- **Group Service**: http://localhost:8003
- **Messaging Service**: http://localhost:8004
- **File Service**: http://localhost:8005
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

### Kubernetes

Aplicar los manifiestos:

```bash
kubectl apply -f k8s-postgres.yaml
kubectl apply -f k8s-auth-service.yaml
kubectl apply -f k8s-user-service.yaml
kubectl apply -f k8s-minio.yaml
kubectl apply -f k8s-file-service.yaml
kubectl apply -f k8s-kong.yaml
```

### Pruebas del File Service

```bash
# Subir archivo
curl -X POST http://localhost:8005/upload -F "file=@archivo.txt"

# Descargar archivo
curl -o archivo.descargado.txt http://localhost:8005/download/archivo.txt

# Eliminar archivo
curl -X DELETE http://localhost:8005/files/archivo.txt
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
docker compose up --build monolith db
```

### 4. Abrir en el navegador

```
http://localhost:8000
```

---

## Administración del servidor AWS

Para gestionar el servidor en AWS se necesita el archivo `groupsapp-key.pem`.

### Conectarse por SSH

```bash
ssh -i "groupsapp-key.pem" ubuntu@3.210.232.100
```

### Levantar los contenedores (después de reiniciar el lab)

```bash
cd Proyecto1-Topicos-Especiales-Telematica-camilo-auth-users
docker-compose-v2 up -d
```

### Ver estado de los contenedores

```bash
docker ps
```

### Detener todo

```bash
docker-compose-v2 down
```

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
├── auth_service/              # Microservicio de autenticación (próxima entrega)
├── user_service/              # Microservicio de usuarios (próxima entrega)
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
http://3.210.232.100:8000/docs
```

O localmente:

```
http://localhost:8000/docs
```

---


## Uso de IA

En esta entrega se utilizaron herramientas de IA para aspectos operativos puntuales (estructura de Dockerfiles, boilerplate de configuración). El diseño del modelo de datos, la definición de endpoints y la lógica de negocio fueron desarrollados por nosotros.
