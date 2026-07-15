#!/usr/bin/env bash
set -Eeuo pipefail

backup_dir="${NORMORDIS_BACKUP_DIR:-/mnt/normordis-backup/backups/repos/normordis-formats}"
backup_file=''
restore_dir=''
list_only=false
force=false

usage() {
  cat <<'EOF'
Uso: full-repo-restore.sh [opções]

  --backup-file FICHEIRO  ZIP a restaurar; por omissão usa o mais recente
  --backup-dir PASTA      pasta de backups
  --restore-dir PASTA     destino do restauro
  --list                  listar backups disponíveis
  --force                 permitir extrair sobre uma pasta não vazia
EOF
}

while (($#)); do
  case "$1" in
    --backup-file|--backup-dir|--restore-dir)
      option=$1
      (($# >= 2)) || { printf 'Falta o valor de %s.\n' "$option" >&2; exit 2; }
      case "$option" in
        --backup-file) backup_file=$2 ;;
        --backup-dir) backup_dir=$2 ;;
        --restore-dir) restore_dir=$2 ;;
      esac
      shift
      ;;
    --list) list_only=true ;;
    --force) force=true ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Opção desconhecida: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

list_backups() {
  [[ -d "$backup_dir" ]] || { printf 'Pasta de backup não encontrada: %s\n' "$backup_dir"; return; }
  mapfile -t backups < <(
    find "$backup_dir" -maxdepth 1 -type f -name 'normordis-formats-*.zip' -printf '%T@ %p\n' \
      | sort -rn | cut -d' ' -f2-
  )
  ((${#backups[@]})) || { printf 'Nenhum backup encontrado em %s\n' "$backup_dir"; return; }
  printf 'Backups disponíveis em %s:\n' "$backup_dir"
  printf '  %s\n' "${backups[@]}"
}

if $list_only; then list_backups; exit 0; fi
[[ -n "$restore_dir" ]] || { printf 'É necessário indicar --restore-dir.\n' >&2; exit 2; }
command -v unzip >/dev/null 2>&1 || { printf 'O comando unzip é necessário.\n' >&2; exit 1; }

if [[ -z "$backup_file" ]]; then
  [[ -d "$backup_dir" ]] || { printf 'Pasta de backup não encontrada: %s\n' "$backup_dir" >&2; exit 1; }
  backup_file="$(find "$backup_dir" -maxdepth 1 -type f -name 'normordis-formats-*.zip' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -n 1 | cut -d' ' -f2-)"
fi
[[ -n "$backup_file" && -f "$backup_file" ]] || { printf 'Backup não encontrado: %s\n' "${backup_file:-$backup_dir}" >&2; exit 1; }

if [[ -d "$restore_dir" && -n "$(find "$restore_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]] && ! $force; then
  printf 'O destino não está vazio. Usa --force para confirmar a sobreposição: %s\n' "$restore_dir" >&2
  exit 1
fi

mkdir -p "$restore_dir"
printf '>>> [RESTORE] A testar %s...\n' "$backup_file"
unzip -tq "$backup_file" >/dev/null
printf '>>> [RESTORE] A extrair %s para %s...\n' "$backup_file" "$restore_dir"
unzip -q "$backup_file" -d "$restore_dir"

if [[ -d "$restore_dir/.git" ]]; then
  linked_worktrees=()
  while IFS= read -r -d '' git_file; do
    linked_worktrees+=("$(dirname -- "$git_file")")
  done < <(find "$restore_dir" -mindepth 2 -type f -name .git -print0)

  if ((${#linked_worktrees[@]})); then
    printf '>>> [RESTORE] A reparar %d worktree(s) ligado(s)...\n' "${#linked_worktrees[@]}"
    git -C "$restore_dir" worktree repair "${linked_worktrees[@]}" >/dev/null
  else
    git -C "$restore_dir" worktree repair >/dev/null
  fi
  git -C "$restore_dir" fsck --no-progress --no-dangling
fi

file_count="$(find "$restore_dir" -type f | wc -l | tr -d ' ')"
printf '>>> [RESTORE] Concluído: %s ficheiros em %s\n' "$file_count" "$restore_dir"
