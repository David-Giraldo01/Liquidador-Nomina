"""
Configuración de ejemplo para PostgreSQL.

Instrucciones:
1. Copia este archivo con el nombre secret_config.py
   en esta misma carpeta.
2. Reemplaza los valores de ejemplo con tus datos de Render.
3. Para HOST, usa el servidor de External Database URL:
   la parte después de @ y antes de /, sin el puerto.
4. No publiques secret_config.py: contiene tu contraseña
   y está excluido mediante .gitignore.

Este archivo de ejemplo sí se puede subir a GitHub.
"""

HOST = "TU_SERVIDOR_EXTERNO"
PORT = 5432
DATABASE = "TU_BASE_DE_DATOS"
USER = "TU_USUARIO"
PASSWORD = "TU_PASSWORD"
SSLMODE = "require"