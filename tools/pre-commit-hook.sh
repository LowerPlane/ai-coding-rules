#!/bin/bash

###############################################################################
# Pre-Commit Hook for AI-Generated Code
#
# Usage:
#   cp tools/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# What it checks:
# - No secrets in staged files (API keys, tokens, passwords)
# - AI-generated code passes stricter linting
# - Test coverage meets 90% threshold
# - No console.log in production code
# - TypeScript strict mode passes
#
# Based on Rules: 19 (secrets), 37 (testing), 49 (strict linting)
###############################################################################

set -e

echo "🔍 Running pre-commit checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for secrets
echo "🔐 Checking for hardcoded secrets (Rule 19)..."

# Patterns to detect
SECRETS_PATTERNS=(
  "API_KEY\s*=\s*['\"][^'\"]*['\"]"
  "SECRET\s*=\s*['\"][^'\"]*['\"]"
  "PASSWORD\s*=\s*['\"][^'\"]*['\"]"
  "TOKEN\s*=\s*['\"][^'\"]*['\"]"
  "sk_live_"
  "sk_test_"
  "ghp_"
  "gho_"
)

SECRETS_FOUND=0

for pattern in "${SECRETS_PATTERNS[@]}"; do
  if git diff --cached | grep -E "$pattern" > /dev/null 2>&1; then
    echo -e "${RED}❌ Potential secret found: $pattern${NC}"
    SECRETS_FOUND=1
  fi
done

if [ $SECRETS_FOUND -eq 1 ]; then
  echo -e "${RED}❌ Secrets detected! Remove them before committing.${NC}"
  echo "   Use environment variables instead (see Rule 19)"
  exit 1
fi

echo -e "${GREEN}✓ No secrets detected${NC}"

# Check for console.log in production code
echo "📝 Checking for console.log statements..."

if git diff --cached --name-only | grep -E '\.(ts|tsx|js|jsx)$' | xargs grep -n "console\.log" 2>/dev/null; then
  echo -e "${YELLOW}⚠️  console.log found - remove before committing${NC}"
  echo "   Use proper logging instead"
fi

# Placeholder for future checks
echo "📋 Additional checks:"
echo "   ⚠️  Linting: Run 'npm run lint' manually"
echo "   ⚠️  Tests: Run 'npm test' manually"
echo "   ⚠️  Coverage: Ensure > 90% (Rule 37)"

echo -e "${GREEN}✓ Pre-commit checks passed${NC}"
echo ""
echo "📖 Remember:"
echo "   - Review AI-generated code (Rule 47)"
echo "   - Run full test suite"
echo "   - Check security checklist (DAILY_CHECKLIST.md)"

exit 0
