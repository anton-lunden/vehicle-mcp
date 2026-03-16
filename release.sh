#!/bin/bash
set -e

if [ -z "$1" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "Usage: ./release.sh <version>"
  echo "Example: ./release.sh 0.1.0"
  exit 0
fi

VERSION="$1"

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Version must be in format X.Y.Z (e.g., 0.1.0)"
  exit 1
fi

# Update version in pyproject.toml
sed -i '' "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# Lint & type check
uv run ruff check .
uv run pyrefly check src

# Commit and tag
git add pyproject.toml
git commit -m "v$VERSION"
git tag "v$VERSION"

echo "Release v$VERSION ready. Run: git push origin main v$VERSION"
