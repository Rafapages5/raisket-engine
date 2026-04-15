# Extiende la imagen oficial de n8n
# n8n Docker Image
# Trigger: Manual verification of WIF permissions
FROM n8nio/n8n:latest

# Instalar dependencias adicionales de sistema que tu orquestador pueda necesitar.
# Al cambiar de usuario a root temporalmente, se pueden instalar paquetes de alpine o python.
USER root

# Ejemplo de instalación: Si decides incorporar scripts de python a ejecutar localmente por n8n:
# RUN apk add --no-cache python3 py3-pip

# Devolver los permisos de ejecución al usuario 'node' estándar
USER node
