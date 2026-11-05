#!/usr/bin/env sh
# Installs the pre-commit privacy guard. Run once after cloning:
#   sh scripts/install-hooks.sh
set -e
root=$(git rev-parse --show-toplevel)
hook="$root/.git/hooks/pre-commit"
cat > "$hook" <<'HOOK'
#!/usr/bin/env sh
# Blocks commits containing personal data. Bypass with: git commit --no-verify
exec python3 "$(git rev-parse --show-toplevel)/scripts/check_private.py"
HOOK
chmod +x "$hook"
echo "Installed pre-commit guard at .git/hooks/pre-commit"
