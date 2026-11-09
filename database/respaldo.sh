#!/usr/bin/env bash
# Respaldo y restauración de la base de datos del inventario (RNF-RESP-01).
# Uso:  DB_PASSWORD=... ./database/respaldo.sh respaldar
#       DB_PASSWORD=... ./database/respaldo.sh restaurar archivo.sql.gz
set -euo pipefail
DB_NAME="${DB_NAME:-inventario_rg_beauty}"
DB_USER="${DB_USER:-inventario_app}"
DB_HOST="${DB_HOST:-localhost}"
export MYSQL_PWD="${DB_PASSWORD:?Defina DB_PASSWORD}"

case "${1:-}" in
  respaldar)
    mkdir -p respaldos
    archivo="respaldos/inventario_$(date +%Y%m%d_%H%M%S).sql.gz"
    mysqldump -h "$DB_HOST" -u "$DB_USER" --single-transaction --skip-add-locks --skip-lock-tables --routines "$DB_NAME" | gzip > "$archivo"
    chmod 600 "$archivo"
    echo "Respaldo creado: $archivo"
    ;;
  restaurar)
    archivo="${2:?Indique el archivo a restaurar}"
    gunzip -c "$archivo" | mysql -h "$DB_HOST" -u "$DB_USER" "$DB_NAME"
    echo "Base restaurada desde: $archivo"
    ;;
  *)
    echo "Uso: $0 respaldar | restaurar archivo.sql.gz"; exit 1 ;;
esac
