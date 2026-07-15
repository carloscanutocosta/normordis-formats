#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# restore.sh — restore a normordis-formats backup produced by backup.sh onto
# a new machine (e.g. a fresh Ubuntu Server install).
#
# Usage:
#   scripts/restore.sh -a ARCHIVE [options]
#   scripts/restore.sh ARCHIVE [target-parent-dir]     (positional form)
#
# Options:
#   -a, --archive FILE   Backup archive to restore (.tar.gz).
#   -d, --dest DIR       Parent directory to extract into. Default: current
#                        directory. The project lands in DIR/normordis-spec.
#   -t, --test           Dry run: verify checksum and list contents, extract
#                        nothing.
#   -f, --force          Overwrite the target project directory if it already
#                        exists.
#   -h, --help           Show this help and exit.
# -----------------------------------------------------------------------------

usage() {
    sed -n '/^# ---/,/^# ---/p' "${BASH_SOURCE[0]}" | sed '1d;$d;s/^# \{0,1\}//'
}

ARCHIVE=""
TARGET_PARENT="."
DRY_RUN=0
FORCE=0
POSITIONAL=()

while [ $# -gt 0 ]; do
    case "$1" in
        -a|--archive)
            ARCHIVE="$2"; shift 2 ;;
        -d|--dest)
            TARGET_PARENT="$2"; shift 2 ;;
        -t|--test|--dry-run)
            DRY_RUN=1; shift ;;
        -f|--force)
            FORCE=1; shift ;;
        -h|--help)
            usage; exit 0 ;;
        -*)
            echo "error: unknown option: $1" >&2; usage >&2; exit 1 ;;
        *)
            POSITIONAL+=("$1"); shift ;;
    esac
done

# Positional fallback: restore.sh ARCHIVE [target-parent-dir]
if [ -z "$ARCHIVE" ] && [ "${#POSITIONAL[@]}" -ge 1 ]; then
    ARCHIVE="${POSITIONAL[0]}"
fi
if [ "${#POSITIONAL[@]}" -ge 2 ]; then
    TARGET_PARENT="${POSITIONAL[1]}"
fi

if [ -z "$ARCHIVE" ]; then
    echo "error: no archive given" >&2
    usage >&2
    exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
    echo "error: backup archive not found: $ARCHIVE" >&2
    exit 1
fi

if [ -f "$ARCHIVE.sha256" ]; then
    echo "==> Verifying checksum"
    ( cd "$(dirname "$ARCHIVE")" && sha256sum -c "$(basename "$ARCHIVE").sha256" )
else
    echo "warning: no .sha256 sidecar found next to archive, skipping integrity check" >&2
fi

ARCHIVE_LISTING="$(tar -tzf "$ARCHIVE")"
PROJECT_NAME="${ARCHIVE_LISTING%%$'\n'*}"
PROJECT_NAME="${PROJECT_NAME%%/*}"

if [ "$DRY_RUN" = 1 ]; then
    echo "==> Dry run: would extract '$PROJECT_NAME' into '$TARGET_PARENT' (nothing will be written)"
    echo "    files in archive: $(printf '%s\n' "$ARCHIVE_LISTING" | wc -l)"
    if [ -f "$ARCHIVE.manifest.txt" ]; then
        echo "    manifest:"
        sed 's/^/      /' "$ARCHIVE.manifest.txt"
    fi
    exit 0
fi

mkdir -p "$TARGET_PARENT"
TARGET_PARENT="$(cd "$TARGET_PARENT" && pwd)"
PROJECT_DIR="$TARGET_PARENT/$PROJECT_NAME"

if [ -e "$PROJECT_DIR" ]; then
    if [ "$FORCE" = 1 ]; then
        echo "==> Removing existing $PROJECT_DIR (--force)"
        rm -rf "$PROJECT_DIR"
    else
        echo "error: $PROJECT_DIR already exists (use -f/--force to overwrite)" >&2
        exit 1
    fi
fi

echo "==> Extracting into $TARGET_PARENT"
tar -xzf "$ARCHIVE" -C "$TARGET_PARENT"

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "error: $PROJECT_DIR does not look like a git repository after extraction" >&2
    exit 1
fi

# Linked worktrees record absolute paths, which will not match this machine.
# Find any nested .git (linked worktrees) and repair their admin links.
mapfile -t LINKED_WORKTREES < <(find "$PROJECT_DIR" -mindepth 2 -name .git -not -path "$PROJECT_DIR/.git" | xargs -r -n1 dirname)

if [ "${#LINKED_WORKTREES[@]}" -gt 0 ]; then
    echo "==> Repairing linked worktree(s):"
    printf '      %s\n' "${LINKED_WORKTREES[@]}"
    git -C "$PROJECT_DIR" worktree repair "${LINKED_WORKTREES[@]}"
else
    git -C "$PROJECT_DIR" worktree repair
fi

echo "==> Verifying repository integrity"
git -C "$PROJECT_DIR" fsck --no-progress || echo "warning: git fsck reported issues, inspect manually" >&2

echo
echo "==> Restore complete: $PROJECT_DIR"
echo "    branches:"
git -C "$PROJECT_DIR" branch -vv | sed 's/^/      /'
echo "    worktrees:"
git -C "$PROJECT_DIR" worktree list | sed 's/^/      /'

UNCOMMITTED="$(git -C "$PROJECT_DIR" status --porcelain)"
if [ -n "$UNCOMMITTED" ]; then
    echo "    uncommitted work restored:"
    echo "$UNCOMMITTED" | sed 's/^/      /'
fi

echo
echo "Next: cd \"$PROJECT_DIR\" && git remote -v   # confirm the remote URL is reachable from here"
