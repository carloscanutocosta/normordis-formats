#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# backup.sh — full, self-contained backup of the normordis-formats project.
#
# Captures everything that cannot be regenerated: the entire .git directory
# (all local branches, tags, stash, reflog, and worktree admin data) plus the
# working tree, including any uncommitted or untracked work. Leaves out only
# build artefacts that tools in this repo can regenerate on demand.
#
# Usage:
#   scripts/backup.sh [options]
#
# Options:
#   -d, --dest DIR     Destination directory for the archive.
#                       Default: /mnt/e/Backup/normordis-formats (falls back
#                       to /mnt/E/Backup/normordis-formats), or $BACKUP_DEST.
#   -s, --source DIR   Project directory to back up. Default: this repo.
#   -t, --test         Dry run: report what would be archived, write nothing.
#   -q, --quiet        Suppress non-essential output.
#   -h, --help         Show this help and exit.
# -----------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '/^# ---/,/^# ---/p' "${BASH_SOURCE[0]}" | sed '1d;$d;s/^# \{0,1\}//'
}

default_dest() {
    for candidate in /mnt/e/Backup/normordis-formats /mnt/E/Backup/normordis-formats; do
        if [ -d "$(dirname "$candidate")" ]; then
            echo "$candidate"
            return
        fi
    done
    echo "/mnt/e/Backup/normordis-formats"
}

SOURCE_DIR=""
DEST=""
DRY_RUN=0
QUIET=0

while [ $# -gt 0 ]; do
    case "$1" in
        -d|--dest)
            DEST="$2"; shift 2 ;;
        -s|--source)
            SOURCE_DIR="$2"; shift 2 ;;
        -t|--test|--dry-run)
            DRY_RUN=1; shift ;;
        -q|--quiet)
            QUIET=1; shift ;;
        -h|--help)
            usage; exit 0 ;;
        *)
            echo "error: unknown option: $1" >&2; usage >&2; exit 1 ;;
    esac
done

PROJECT_DIR="$(cd "${SOURCE_DIR:-$SCRIPT_DIR/..}" && git rev-parse --show-toplevel)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
DEST="${DEST:-${BACKUP_DEST:-$(default_dest)}}"

log() { [ "$QUIET" = 1 ] || echo "$@"; }

# Reconstructible items only: generated build output and interpreter/OS
# cruft. Everything else (.git history, worktrees, uncommitted/untracked
# work) is preserved as-is.
EXCLUDES=(
    --exclude="$PROJECT_NAME/build"
    --exclude="*/__pycache__"
    --exclude="*.pyc"
    --exclude="*/node_modules"
    --exclude=".DS_Store"
    --exclude="Thumbs.db"
    --exclude="*.swp"
    --exclude="*.bak"
)

if [ "$DRY_RUN" = 1 ]; then
    log "==> Dry run: $PROJECT_DIR -> $DEST (nothing will be written)"
    FILE_COUNT="$(tar -cvzf /dev/null -C "$(dirname "$PROJECT_DIR")" "${EXCLUDES[@]}" "$PROJECT_NAME" 2>/dev/null | wc -l)"
    APPROX_BYTES="$(tar -cf - -C "$(dirname "$PROJECT_DIR")" "${EXCLUDES[@]}" "$PROJECT_NAME" | wc -c)"
    log "    files that would be archived: $FILE_COUNT"
    log "    uncompressed size (approx):   $(numfmt --to=iec "$APPROX_BYTES" 2>/dev/null || echo "$APPROX_BYTES bytes")"
    log "    excludes: build/, __pycache__, *.pyc, node_modules, .DS_Store, Thumbs.db, *.swp, *.bak"
    exit 0
fi

mkdir -p "$DEST"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$DEST/normordis-formats-$TIMESTAMP.tar.gz"

log "==> Backing up $PROJECT_DIR"
log "==> Destination: $ARCHIVE"

{
    echo "normordis-formats backup"
    echo "date:      $(date -Is)"
    echo "host:      $(hostname)"
    echo "source:    $PROJECT_DIR"
    echo "git HEAD:  $(git -C "$PROJECT_DIR" rev-parse HEAD 2>/dev/null || echo 'n/a')"
    echo
    echo "remotes:"
    git -C "$PROJECT_DIR" remote -v 2>/dev/null | sed 's/^/  /'
    echo
    echo "branches (local):"
    git -C "$PROJECT_DIR" branch -vv 2>/dev/null | sed 's/^/  /'
    echo
    echo "worktrees:"
    git -C "$PROJECT_DIR" worktree list 2>/dev/null | sed 's/^/  /'
    echo
    echo "uncommitted changes at backup time (also preserved in the archive):"
    git -C "$PROJECT_DIR" status --porcelain 2>/dev/null | sed 's/^/  /'
    echo
    echo "Note: linked worktree paths are absolute and will not match a new"
    echo "machine. restore.sh runs 'git worktree repair' automatically to fix"
    echo "them after extraction."
} > "$ARCHIVE.manifest.txt"

tar -czf "$ARCHIVE" \
    -C "$(dirname "$PROJECT_DIR")" \
    "${EXCLUDES[@]}" \
    "$PROJECT_NAME"

( cd "$DEST" && sha256sum "$(basename "$ARCHIVE")" > "$(basename "$ARCHIVE").sha256" )

SIZE="$(du -h "$ARCHIVE" | cut -f1)"
log "==> Done: $ARCHIVE ($SIZE)"
log "==> Checksum: $ARCHIVE.sha256"
