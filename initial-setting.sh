#!/bin/bash

echo "🔄 Setting up Python virtual environment..."
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r requirements.txt

HOOK_PATH=".git/hooks/prepare-commit-msg"

echo "🔧 Creating prepare-commit-msg git hook..."

cat << 'EOF' > $HOOK_PATH
#!/bin/sh

BRANCH_NAME=$(git branch --show-current)
ISSUE_KEY=$(echo $BRANCH_NAME | grep -oE '[A-Z]+-[0-9]+')

# If issue key found, prepend to first line
if [ -n "$ISSUE_KEY" ]; then
  sed -i.bak -e "1s/^/$ISSUE_KEY: /" "$1"
fi
EOF

chmod +x $HOOK_PATH

echo "✅ Git hook created at $HOOK_PATH"
echo "🚀 Now commit from terminal and the issue key will auto-prefix your commit message"
