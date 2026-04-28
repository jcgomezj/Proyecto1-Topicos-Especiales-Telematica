#!/bin/bash
set -e

echo "Configurando Kong API Gateway..."

# Esperar a que Kong esté listo
echo "Esperando a que Kong esté disponible..."
sleep 10

# Configurar Kong en modo DB-less (usando declarative config)
KONG_ADMIN="http://localhost:8001"

# Crear servicio para monolith
curl -s -X POST $KONG_ADMIN/services \
  --data name=monolith \
  --data url=http://monolith:8000

curl -s -X POST $KONG_ADMIN/services/monolith/routes \
  --data name=monolith-route \
  --data paths=/monolith \
  --data strip_path=true

# Crear servicio para auth_service
curl -s -X POST $KONG_ADMIN/services \
  --data name=auth-service \
  --data url=http://auth_service:8001

curl -s -X POST $KONG_ADMIN/services/auth-service/routes \
  --data name=auth-route \
  --data paths=/auth \
  --data strip_path=true

# Crear servicio para user_service
curl -s -X POST $KONG_ADMIN/services \
  --data name=user-service \
  --data url=http://user_service:8002

curl -s -X POST $KONG_ADMIN/services/user-service/routes \
  --data name=user-route \
  --data paths=/users \
  --data strip_path=true

# Crear servicio para group_service
curl -s -X POST $KONG_ADMIN/services \
  --data name=group-service \
  --data url=http://group_service:8003

curl -s -X POST $KONG_ADMIN/services/group-service/routes \
  --data name=group-route \
  --data paths=/groups \
  --data strip_path=true

# Crear servicio para messaging_service
curl -s -X POST $KONG_ADMIN/services \
  --data name=messaging-service \
  --data url=http://messaging_service:8004

curl -s -X POST $KONG_ADMIN/services/messaging-service/routes \
  --data name=messaging-route \
  --data paths=/messages \
  --data strip_path=true

# Crear servicio para file_service
curl -s -X POST $KONG_ADMIN/services \
  --data name=file-service \
  --data url=http://file_service:8005

curl -s -X POST $KONG_ADMIN/services/file-service/routes \
  --data name=file-route \
  --data paths=/files \
  --data strip_path=true

echo "Configuración de Kong completada!"
echo ""
echo "Rutas configuradas:"
echo "  /monolith -> monolith:8000"
echo "  /auth -> auth_service:8001"
echo "  /users -> user_service:8002"
echo "  /groups -> group_service:8003"
echo "  /messages -> messaging_service:8004"
echo "  /files -> file_service:8005"