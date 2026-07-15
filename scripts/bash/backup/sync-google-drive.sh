#!/usr/bin/env bash
set -Eeuo pipefail

source_dir="${NORMORDIS_BACKUP_DIR:-/mnt/normordis-backup/backups/repos/normordis-formats}"
remote="${NORMORDIS_RCLONE_REMOTE:-gdrive:backups/projetos/normordis-formats}"
dry_run=false
keep_last=5

usage() {
  cat <<'EOF'
Uso: sync-google-drive.sh [--source-dir PASTA] [--remote REMOTE]
                            [--keep-last N] [--dry-run]

Copia os backups locais para o Google Drive e mantém os N mais recentes.
Por omissão, usa gdrive:backups/projetos/normordis-formats.
EOF
}

while (($#)); do
  case "$1" in
    --source-dir)
      (($# >= 2)) || { printf 'Falta a pasta após --source-dir.\n' >&2; exit 2; }
      source_dir=$2; shift
      ;;
    --remote)
      (($# >= 2)) || { printf 'Falta o destino após --remote.\n' >&2; exit 2; }
      remote=$2; shift
      ;;
    --keep-last)
      (($# >= 2)) || { printf 'Falta o número após --keep-last.\n' >&2; exit 2; }
      keep_last=$2; shift
      [[ "$keep_last" =~ ^[1-9][0-9]*$ ]] || {
        printf '%s\n' '--keep-last requer um inteiro positivo.' >&2
        exit 2
      }
      ;;
    --dry-run) dry_run=true ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Opção desconhecida: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

command -v rclone >/dev/null 2>&1 || {
  printf 'O comando rclone não está instalado.\n' >&2
  exit 1
}
[[ -d "$source_dir" ]] || {
  printf 'A pasta local de backups não existe: %s\n' "$source_dir" >&2
  exit 1
}

[[ "$remote" == *:* ]] || {
  printf 'Destino rclone inválido (esperado remote:caminho): %s\n' "$remote" >&2
  exit 2
}
remote_name=${remote%%:*}:
rclone listremotes | grep -Fqx -- "$remote_name" || {
  printf 'Remote rclone não configurado: %s\n' "$remote_name" >&2
  exit 1
}

lock_file="${TMPDIR:-/tmp}/normordis-formats-rclone.lock"
exec 9>"$lock_file"
flock -n 9 || {
  printf 'Já existe uma cópia cloud do normordis-formats em execução.\n' >&2
  exit 1
}

printf '>>> [CLOUD] Origem: %s\n>>> [CLOUD] Destino: %s\n' "$source_dir" "$remote"

if ! $dry_run; then
  printf '>>> [CLOUD] A garantir a pasta remota...\n'
  rclone mkdir "$remote"
fi

copy_args=(
  copy "$source_dir" "$remote"
  --immutable
  --checksum
  --check-first
  --transfers 4
  --checkers 8
)
if $dry_run; then
  copy_args+=(--dry-run)
  printf '>>> [CLOUD] Simulação: nenhum ficheiro será enviado.\n'
fi
rclone "${copy_args[@]}"

if ! $dry_run; then
  printf '>>> [CLOUD] A verificar os ficheiros enviados...\n'
  rclone check "$source_dir" "$remote" --one-way
fi

if ! remote_listing="$(rclone lsf "$remote" --files-only)"; then
  if $dry_run; then
    printf '>>> [CLOUD] Retenção não simulada: a pasta remota ainda não existe ou não está acessível.\n'
    printf '>>> [CLOUD] Simulação concluída; retenção configurada: %d backup(s).\n' "$keep_last"
    exit 0
  fi
  printf 'Não foi possível listar o destino remoto para aplicar a retenção: %s\n' "$remote" >&2
  exit 1
fi

mapfile -t remote_backups < <(
  printf '%s\n' "$remote_listing" \
    | grep -E '^normordis-formats-[0-9]{8}-[0-9]{6}[.]zip$' \
    | LC_ALL=C sort -r || true
)

if ((${#remote_backups[@]} > keep_last)); then
  old_backups=("${remote_backups[@]:keep_last}")
  if $dry_run; then
    printf '>>> [CLOUD] Simulação da retenção: %d backup(s) seriam removidos:\n' "${#old_backups[@]}"
    printf '    %s\n' "${old_backups[@]}"
  else
    for backup_name in "${old_backups[@]}"; do
      rclone deletefile "${remote%/}/$backup_name"
      printf '>>> [CLOUD] Retenção: removido %s\n' "$backup_name"
    done
  fi
fi

printf '>>> [CLOUD] Concluído com sucesso; retenção: %d backup(s).\n' "$keep_last"
