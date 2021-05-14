#!/bin/bash
#
# Vault k/v secret engine backup
#

set -e

_log() {
    printf "$(date): $1\n"
}

OPTS=""

[[ -z ${VAULT_TOKEN} ]] && {
    _log "VAULT_TOKEN environment missing, exit."
    exit 1
}

[[ -z ${VAULT_ADDR} ]] && {
    _log "VAULT_ADDR environment missing, exit."
    exit 1
}

[[ "${DEBUG}" -eq "1" ]] && {
    _log "DEBUG is enable"
    OPTS="${OPTS} --debug"
}

BACKUP_DIR=${BACKUP_DIR:-/backup}
BACKUP_ROTATE=${BACKUP_ROTATE:-30} # days
BASE_NAME=${BASE_NAME:-backup}

[[ ! -d ${BACKUP_DIR} ]] && {
    _log "Create directory ${BACKUP_DIR}"
    mkdir -p ${BACKUP_DIR}
}

t_name=$(date  +"%Y-%m-%d_%H-%M")
data_file="${BACKUP_DIR}/${BASE_NAME}_${t_name}.data"
key_file="${BACKUP_DIR}/${BASE_NAME}_${t_name}.key"
cmd="vmb ${OPTS} ${data_file} --backup-key ${key_file}"

_log "Running Vault kv backup from ${VAULT_ADDR}:"
_log "${cmd}"

${cmd}

_log "Clean old backups & keys"
find ${BACKUP_DIR} -type f -name "*.data" -mtime +${BACKUP_ROTATE} -delete
find ${BACKUP_DIR} -type f -name "*.key" -mtime +${BACKUP_ROTATE} -delete

_log "Done"
