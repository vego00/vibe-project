#!/bin/bash

HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/prepare-commit-msg"
TEMPLATE_FILE=".git/commit-template.txt"

echo "Creating Git hook..."

# 1) Ensure .git/hooks exists
if [ ! -d "$HOOK_DIR" ]; then
    echo "❌ No .git/hooks directory found! Are you in the project root?"
    exit 1
fi

# 2) Create default commit template if not exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Creating default commit template..."
    cat <<EOF > "$TEMPLATE_FILE"
#ISSUE : [TYPE]

Description:
- What changed:
- Why:

Test:
- How to test:

Additional Notes:
EOF
fi

# 3) Create prepare-commit-msg hook
cat <<'EOF' > "$HOOK_FILE"
#!/bin/sh

BRANCH_NAME=$(git branch --show-current)
ISSUE_KEY=$(echo "$BRANCH_NAME" | grep -oE '[A-Z]+-[0-9]+')

TEMPLATE_FILE=".git/commit-template.txt"
MSG_FILE="$1"

# If commit message already exists (like git commit -m "msg"), do nothing
if [ -s "$MSG_FILE" ]; then
    exit 0
fi

# Copy template into commit message
if [ -f "$TEMPLATE_FILE" ]; then
    cp "$TEMPLATE_FILE" "$MSG_FILE"
fi

# Replace placeholder with branch issue key
if [ -n "$ISSUE_KEY" ]; then
    sed -i "s/#ISSUE/$ISSUE_KEY/" "$MSG_FILE"
fi
EOF

# 4) Make hook executable
chmod +x "$HOOK_FILE"

echo "✅ Git hook successfully installed at $HOOK_FILE"
echo "➡ Commit template: $TEMPLATE_FILE"
