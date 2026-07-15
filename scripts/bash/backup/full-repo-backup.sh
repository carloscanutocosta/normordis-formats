#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
destination="${NORMORDIS_BACKUP_DIR:-/mnt/normordis-backup/backups/repos/normordis-formats}"
keep_last=5

usage() {
  cat <<'EOF'
Uso: full-repo-backup.sh [--dest-dir PASTA] [--keep-last N]
EOF
}

while (($#)); do
  case "$1" in
    --dest-dir)
      (($# >= 2)) || { printf 'Falta a pasta após --dest-dir.\n' >&2; exit 2; }
      destination=$2; shift
      ;;
    --keep-last)
      (($# >= 2)) || { printf 'Falta o número após --keep-last.\n' >&2; exit 2; }
      keep_last=$2; shift
      [[ "$keep_last" =~ ^[0-9]+$ ]] || { printf '%s\n' '--keep-last requer um inteiro não negativo.' >&2; exit 2; }
      ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Opção desconhecida: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

command -v zip >/dev/null 2>&1 || {
  printf 'O comando zip é necessário para criar o backup.\n' >&2
  exit 1
}

destination_parent=$(dirname -- "$destination")
[[ -d "$destination_parent" ]] || {
  printf 'A pasta base de backups não existe: %s\n' "$destination_parent" >&2
  exit 1
}
[[ -w "$destination_parent" ]] || {
  printf 'A pasta base de backups não está gravável: %s\n' "$destination_parent" >&2
  printf 'Confirma que o SSD está montado em modo rw.\n' >&2
  exit 1
}

timestamp="$(date +%Y%m%d-%H%M%S)"
archive="$destination/normordis-formats-$timestamp.zip"
stage="$(mktemp -d "${TMPDIR:-/tmp}/nf-backup.XXXXXX")"
cleanup() { rm -rf "$stage"; }
trap cleanup EXIT
mkdir -p "$destination"

printf '>>> [BACKUP] Origem: %s\n>>> [BACKUP] Destino: %s\n' "$repo_root" "$archive"

tar -C "$repo_root" -cf - \
  --exclude='./build' --exclude='./dist' --exclude='./.cache' \
  --exclude='./.pytest_cache' --exclude='./.mypy_cache' --exclude='./.ruff_cache' \
  --exclude='*/__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
  --exclude='./node_modules' --exclude='./tmp' --exclude='./temp' \
  --exclude='*.log' --exclude='*.tmp' --exclude='*.bak' --exclude='*.swp' \
  --exclude='.DS_Store' --exclude='Thumbs.db' --exclude='Desktop.ini' \
  --exclude='.env' --exclude='.env.*' --exclude='*/.env' --exclude='*/.env.*' \
  --exclude='*.pem' --exclude='*.key' --exclude='*.p12' --exclude='*.pfx' \
  . | tar -C "$stage" -xf -

# Os exemplos versionáveis não contêm credenciais e devem sobreviver ao filtro
# conservador de ficheiros .env*.
while IFS= read -r -d '' example_file; do
  relative_path=${example_file#"$repo_root"/}
  mkdir -p "$stage/$(dirname -- "$relative_path")"
  cp -p -- "$example_file" "$stage/$relative_path"
done < <(find "$repo_root" \
  \( -path "$repo_root/.git" -o -path "$repo_root/build" \
    -o -path "$repo_root/dist" -o -path "$repo_root/.cache" \
    -o -path "$repo_root/.pytest_cache" -o -path "$repo_root/.mypy_cache" \
    -o -path "$repo_root/.ruff_cache" -o -path "$repo_root/node_modules" \) -prune \
  -o -type f -name '.env.example' -print0)

# Preserva ficheiros versionados que vivam em pastas de artefactos excluídas,
# sem reintroduzir material sensível no arquivo.
while IFS= read -r -d '' tracked_file; do
  case "/$tracked_file" in
    */.env|*/.env.*|*.pem|*.key|*.p12|*.pfx) continue ;;
  esac
  [[ -e "$repo_root/$tracked_file" || -L "$repo_root/$tracked_file" ]] || continue
  [[ -e "$stage/$tracked_file" || -L "$stage/$tracked_file" ]] && continue
  mkdir -p "$stage/$(dirname -- "$tracked_file")"
  cp -a -- "$repo_root/$tracked_file" "$stage/$tracked_file"
done < <(git -C "$repo_root" ls-files -z)

(cd "$stage" && zip -qr "$archive" .)
file_count="$(find "$stage" -type f | wc -l | tr -d ' ')"
archive_size="$(du -h "$archive" | awk '{print $1}')"

if ((keep_last > 0)); then
  mapfile -t old_backups < <(
    find "$destination" -maxdepth 1 -type f -name 'normordis-formats-*.zip' -printf '%T@ %p\n' \
      | sort -rn | tail -n "+$((keep_last + 1))" | cut -d' ' -f2-
  )
  if ((${#old_backups[@]})); then
    rm -f -- "${old_backups[@]}"
    printf '>>> [BACKUP] Rotação: %d backup(s) antigo(s) removido(s).\n' "${#old_backups[@]}"
  fi
fi

printf '>>> [BACKUP] Concluído: %s (%s, %s ficheiros)\n' "$archive" "$archive_size" "$file_count"
