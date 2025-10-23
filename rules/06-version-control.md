# Version Control Rules (Rules 51-54)

Rules for managing AI-generated code in version control systems.

---

## Rule 51: Meaningful Commit Messages

**❌ Bad:** `git commit -m "fix stuff"`

**✅ Good:** `git commit -m "feat(auth): add JWT token refresh endpoint"`

### How to Follow

Use the Conventional Commits format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Scope:** Module or feature affected (auth, users, api, etc.)

**Subject:** Imperative, present tense ("add" not "added" or "adds")

### Examples

```bash
# Feature additions
git commit -m "feat(users): add email verification endpoint"
git commit -m "feat(auth): implement OAuth2 Google login"
git commit -m "feat(api): add pagination to product listing"

# Bug fixes
git commit -m "fix(auth): resolve token expiration edge case"
git commit -m "fix(users): prevent duplicate email registration"
git commit -m "fix(cart): correct tax calculation for multi-state orders"

# Documentation
git commit -m "docs(api): update authentication flow documentation"
git commit -m "docs(readme): add setup instructions for local development"

# Refactoring
git commit -m "refactor(services): extract common validation logic"
git commit -m "refactor(auth): simplify JWT token generation"

# Tests
git commit -m "test(users): add edge cases for user registration"
git commit -m "test(api): increase coverage to 95%"

# Performance
git commit -m "perf(database): add indexes to user queries"
git commit -m "perf(api): implement response caching"
```

### Git Commands

```bash
# Single-line commit
git commit -m "feat(users): add profile update endpoint"

# Multi-line commit with body
git commit -m "feat(auth): add two-factor authentication

Implements TOTP-based 2FA using speakeasy library.
Users can enable 2FA in account settings.
Recovery codes provided during setup."

# Multi-line commit with footer
git commit -m "fix(api): resolve rate limiting bypass issue

The rate limiter was not correctly handling requests from
users behind proxies. Updated to check X-Forwarded-For header.

Closes #123
BREAKING CHANGE: Rate limiter now requires trust proxy setting"
```

### Conventional Commits Full Format

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

**Subject Guidelines:**
- Limit to 50 characters
- Capitalize first letter
- No period at the end
- Use imperative mood

**Body Guidelines:**
- Wrap at 72 characters
- Explain what and why, not how
- Separate from subject with blank line
- Can have multiple paragraphs

**Footer Guidelines:**
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`
- AI-generated tag: `AI-Generated: Claude Code`

### Complete Example

```bash
git commit -m "feat(auth): add JWT token refresh mechanism

Implements automatic token refresh when access token expires.
Refresh tokens are stored in httpOnly cookies for security.
Access tokens have 15-minute expiration, refresh tokens 7 days.

The refresh endpoint validates the refresh token and issues
a new access token and rotated refresh token.

Closes #234
AI-Generated: Claude Code
Reviewed-by: @johndoe"
```

---

## Rule 52: Small, Focused Commits

**❌ Bad:** 1000 lines changed across 20 files in a single commit

**✅ Good:** Logical, reviewable commits with clear scope

### How to Follow

- One logical change per commit
- Separate refactoring from features
- Commit working code only
- Keep related changes together
- Separate formatting from logic changes

### Examples

**❌ Bad - Too Large:**
```bash
# Changes 20 files, mixes concerns
git commit -m "add user system, refactor database, update docs, fix bugs"
```

**✅ Good - Separated:**
```bash
# Commit 1: Foundation
git commit -m "feat(users): add User model and schema"

# Commit 2: Service layer
git commit -m "feat(users): add UserService with CRUD operations"

# Commit 3: API endpoints
git commit -m "feat(users): add user registration endpoint"

# Commit 4: Tests
git commit -m "test(users): add comprehensive user service tests"

# Commit 5: Documentation
git commit -m "docs(users): add API documentation for user endpoints"
```

### Git Commands for Focused Commits

```bash
# Stage specific files
git add src/models/user.model.ts
git commit -m "feat(users): add User model"

# Stage parts of a file (interactive)
git add -p src/services/user.service.ts
git commit -m "feat(users): add createUser method"

# Stage and commit separately
git add src/controllers/user.controller.ts
git commit -m "feat(users): add user registration controller"

git add src/routes/user.routes.ts
git commit -m "feat(users): add user routes"

# Check what will be committed
git status
git diff --staged

# Amend last commit if needed (only if not pushed!)
git add forgotten-file.ts
git commit --amend --no-edit
```

### Commit Size Guidelines

**Good commit size:**
- 1-5 files changed
- 50-200 lines added/modified
- One clear purpose
- Reviewable in < 5 minutes
- Tests pass independently

**When to split commits:**
- Multiple features in one change
- Refactoring mixed with new features
- Formatting changes mixed with logic
- Changes to unrelated modules
- Commits taking > 10 minutes to review

### Example: Feature Development Commits

```bash
# Bad: One massive commit
git add .
git commit -m "add complete user authentication system"
# (500 files changed, 5000 lines)

# Good: Incremental commits
git add src/models/user.model.ts
git commit -m "feat(auth): add User model with password field"

git add src/utils/hash.util.ts
git commit -m "feat(auth): add password hashing utility with bcrypt"

git add src/services/auth.service.ts
git commit -m "feat(auth): add authentication service"

git add src/controllers/auth.controller.ts
git commit -m "feat(auth): add login and register controllers"

git add src/routes/auth.routes.ts
git commit -m "feat(auth): add authentication routes"

git add src/middleware/auth.middleware.ts
git commit -m "feat(auth): add JWT authentication middleware"

git add tests/auth.service.test.ts
git commit -m "test(auth): add authentication service tests"

git add tests/auth.integration.test.ts
git commit -m "test(auth): add authentication integration tests"

git add docs/api/authentication.md
git commit -m "docs(auth): add authentication API documentation"
```

---

## Rule 53: Tag AI-Generated Commits

**❌ Bad:** No indication that AI generated the code

**✅ Good:** Clear tagging of AI involvement with context

### How to Follow

Include AI attribution in commit message footer:
- Specify AI tool used
- Reference prompt or context
- Note human review/approval
- Link to prompt file if available

### Examples

**Basic AI Tag:**
```bash
git commit -m "feat(users): add user registration endpoint

Implements user registration with email verification.
Validates input using Zod schema, hashes password with bcrypt.

AI-Generated: Claude Code
Reviewed-by: @johndoe"
```

**With Prompt Reference:**
```bash
git commit -m "feat(api): add product search endpoint

Implements full-text search across product catalog.
Supports filtering by category, price range, and availability.

AI-Generated: Claude Code
Prompt: See prompts/api/product-search.md
Reviewed-by: @sarahjones
Tested-by: @mikebrown"
```

**With Modifications:**
```bash
git commit -m "feat(payment): add Stripe integration

Integrates Stripe payment processing for checkout flow.
Handles webhooks for payment confirmation.

AI-Generated: Claude Code (with human modifications)
Modified: Updated error handling and added retry logic
Prompt: See prompts/integrations/stripe.md
Security-Review: @securityteam
Reviewed-by: @johndoe"
```

**Partial AI Assistance:**
```bash
git commit -m "feat(analytics): add event tracking service

Implements custom analytics event tracking system.
Batches events and sends to analytics API.

Partially AI-Generated: Claude Code
AI: Service structure and type definitions
Human: Business logic and event validation
Reviewed-by: @analytics-team"
```

### Git Commit Template

Create `.gitmessage` template:

```bash
# .gitmessage
<type>(<scope>): <subject>

[What was changed and why]

[AI generation details]
AI-Generated: [Tool name]
Prompt: [Link to prompt file or description]
Reviewed-by: [@reviewer]

[Optional: Issue references]
Closes #
Refs #
```

Set as default template:
```bash
git config commit.template .gitmessage
```

### Pre-commit Hook for AI Tags

```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

# Check if this is AI-generated code
if grep -q "ai-generated" "$1" 2>/dev/null || \
   git diff --cached --name-only | grep -q "^ai-generated/"; then

  # Ensure AI tag is present
  if ! grep -q "AI-Generated:" "$1"; then
    echo "" >> "$1"
    echo "AI-Generated: [SPECIFY TOOL]" >> "$1"
    echo "Reviewed-by: [@REVIEWER]" >> "$1"
  fi
fi
```

### Directory-Based AI Tagging

```bash
# For code in /ai-generated directory
git commit -m "feat(users): add user service

Generated in ai-generated/ directory for review.

AI-Generated: Claude Code
Status: Awaiting human review
Prompt: Create user service with CRUD operations
Next: Move to src/ after approval"

# After review and merge to src/
git commit -m "feat(users): merge reviewed user service to src

Moved from ai-generated/ after successful review.

Originally-AI-Generated: Claude Code
Reviewed-by: @johndoe
Approved-by: @sarahjones
Tests: Passing (95% coverage)
Security: Approved"
```

---

## Rule 54: Branch Strategy for AI Code

**❌ Bad:** Commit AI code directly to main/master branch

**✅ Good:** Use feature branches with review workflow

### How to Follow

Use branch naming convention:
- `ai/<feature-name>` - AI-generated features
- `ai/fix/<bug-name>` - AI-generated fixes
- `ai/refactor/<scope>` - AI-generated refactoring
- `feature/<feature-name>` - Human-led features
- `fix/<bug-name>` - Human-led fixes

### Branch Workflow

```
main (protected)
  │
  ├── ai/user-registration (AI feature)
  │   ├── ai-generated/ (temporary)
  │   └── src/ (after review)
  │
  ├── ai/fix/auth-bug (AI bugfix)
  │
  └── feature/payment-system (human-led)
```

### Git Commands

```bash
# 1. Create AI feature branch from main
git checkout main
git pull origin main
git checkout -b ai/user-registration

# 2. AI generates code to ai-generated/ directory
# (Claude Code or other AI assistant generates files)

# 3. Stage and commit AI code
git add ai-generated/users/
git commit -m "feat(users): generate user registration service

AI-Generated: Claude Code
Status: Initial generation, awaiting review
Prompt: See prompts/users/registration.md"

# 4. Run tests and linting
npm run lint:ai-code ai-generated/
npm test

# 5. Commit test results
git add ai-generated/users/__tests__/
git commit -m "test(users): add tests for user registration

AI-Generated: Claude Code
Coverage: 94%
All tests passing"

# 6. Push to remote
git push origin ai/user-registration

# 7. Create pull request
gh pr create \
  --title "feat(users): Add user registration (AI-generated)" \
  --label "ai-generated" \
  --label "needs-review" \
  --body "AI-generated user registration feature. See commits for details."

# 8. After review and approval, human moves code to src/
git checkout ai/user-registration
mv ai-generated/users src/features/users
git add src/features/users
git commit -m "feat(users): move approved user code to src

Originally-AI-Generated: Claude Code
Reviewed-by: @johndoe
Approved-by: @sarahjones
Security-Review: Passed
Tests: 94% coverage"

# 9. Merge to main via PR
# (Done through GitHub/GitLab UI with required approvals)

# 10. Clean up
git checkout main
git pull origin main
git branch -d ai/user-registration
git push origin --delete ai/user-registration
```

### Branch Protection Rules

Configure in GitHub/GitLab:

```yaml
# main branch protection
main:
  required_reviews: 2
  required_checks:
    - lint
    - test
    - security-scan
  required_labels:
    - when: contains "AI-Generated"
      require: ["security-review", "code-review"]
  no_direct_commits: true
  no_force_push: true

# AI branch requirements
ai/**:
  required_reviews: 1
  required_checks:
    - lint:ai-code  # Stricter linting
    - test
    - security-scan
    - ai-code-review
  required_labels: ["ai-generated"]
```

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   AI Code Workflow                       │
└─────────────────────────────────────────────────────────┘

main branch (protected)
    │
    ├── 1. Create branch: git checkout -b ai/feature
    │
    ├── 2. AI generates to ai-generated/
    │       ├── Code generation
    │       ├── Tests generation
    │       └── Documentation
    │
    ├── 3. Commit AI code
    │       git commit -m "AI-Generated: ..."
    │
    ├── 4. Run automated checks
    │       ├── Lint (stricter rules)
    │       ├── Tests (90%+ coverage)
    │       ├── Security scan
    │       └── Complexity analysis
    │
    ├── 5. Push and create PR
    │       git push origin ai/feature
    │
    ├── 6. Human review
    │       ├── Code review
    │       ├── Security review
    │       ├── Logic verification
    │       └── Approval
    │
    ├── 7. Move to src/ after approval
    │       mv ai-generated/* src/
    │
    ├── 8. Final commit
    │       git commit -m "Reviewed-by: ..."
    │
    └── 9. Merge to main
            ├── Squash merge (optional)
            ├── Update changelog
            └── Tag release (if applicable)
```

### Example: Complete Feature Flow

```bash
# Day 1: AI Generation
git checkout -b ai/payment-integration
# AI generates code
git add ai-generated/payment/
git commit -m "feat(payment): generate Stripe payment integration

AI-Generated: Claude Code
Prompt: See prompts/payment/stripe-integration.md
Status: Initial generation"

git add ai-generated/payment/__tests__/
git commit -m "test(payment): add payment integration tests

AI-Generated: Claude Code
Coverage: 92%"

git push origin ai/payment-integration

# Create PR with ai-generated label
gh pr create \
  --title "feat(payment): Add Stripe payment integration (AI)" \
  --label "ai-generated" \
  --label "needs-review" \
  --label "needs-security-review"

# Day 2: Review and feedback
# Reviewer comments: "Add error handling for network failures"

git checkout ai/payment-integration
# AI regenerates with improvements
git add ai-generated/payment/payment.service.ts
git commit -m "fix(payment): improve error handling per review

AI-Generated: Claude Code (iteration 2)
Changes: Added retry logic and timeout handling
Reviewer: @johndoe"

git push origin ai/payment-integration

# Day 3: Approval and merge
# After approval, move to src/
mv ai-generated/payment src/features/payment
rm -rf ai-generated/payment

git add src/features/payment
git commit -m "feat(payment): move approved payment code to src

Originally-AI-Generated: Claude Code
Reviewed-by: @johndoe
Security-Review: @securityteam
Approved-by: @techlead
Tests: 92% coverage, all passing
Documentation: Complete"

git push origin ai/payment-integration

# Merge via GitHub UI
# After merge:
git checkout main
git pull origin main
git branch -d ai/payment-integration
```

### Branch Naming Conventions

```bash
# AI-generated features
ai/user-authentication
ai/product-search
ai/email-notifications

# AI-generated fixes
ai/fix/login-timeout
ai/fix/validation-error
ai/fix/memory-leak

# AI-generated refactoring
ai/refactor/user-service
ai/refactor/database-queries
ai/refactor/api-responses

# Human-led work (for comparison)
feature/payment-dashboard
fix/security-vulnerability
refactor/legacy-code
```

### Merge Strategies

**For AI branches:**

```bash
# Option 1: Squash merge (recommended for AI code)
# Combines all AI commits into one clean commit
git merge --squash ai/feature
git commit -m "feat(scope): description

Originally generated across multiple AI iterations.
Final version reviewed and approved.

AI-Generated: Claude Code
Reviewed-by: @reviewer"

# Option 2: Regular merge (preserves AI commit history)
git merge --no-ff ai/feature

# Option 3: Rebase (for linear history)
git checkout ai/feature
git rebase main
git checkout main
git merge --ff-only ai/feature
```

### Release Tagging

```bash
# After merging AI-generated features to main
git checkout main
git pull origin main

# Tag release with AI-generated features noted
git tag -a v1.2.0 -m "Release v1.2.0

Features:
- User registration system (AI-generated, reviewed)
- Email verification (AI-generated, reviewed)
- Password reset flow (human-developed)

AI-Generated: 60% of new code
Review coverage: 100%
Test coverage: 94%"

git push origin v1.2.0
```

---

## Summary: Version Control Best Practices

✅ **Do:**
- Use conventional commit format consistently
- Write clear, descriptive commit messages
- Make small, focused commits (one logical change)
- Tag all AI-generated commits
- Reference prompts in commit messages
- Use AI-specific branch naming (ai/*)
- Require reviews for AI branches
- Move code to src/ only after approval
- Document AI tool and reviewer
- Keep commit history clean and meaningful

❌ **Don't:**
- Make vague commits ("fix stuff", "updates")
- Commit thousands of lines at once
- Mix multiple features in one commit
- Hide AI involvement
- Commit directly to main branch
- Skip code review for AI code
- Merge without human approval
- Forget to tag AI-generated code
- Leave AI code in ai-generated/ permanently
- Force push to protected branches

### Quick Reference

```bash
# Good commit
git commit -m "feat(auth): add JWT refresh token endpoint

Implements automatic token refresh mechanism.
Access tokens expire after 15 minutes.
Refresh tokens rotate on each use.

AI-Generated: Claude Code
Prompt: See prompts/auth/jwt-refresh.md
Reviewed-by: @johndoe
Closes #123"

# Good workflow
git checkout -b ai/new-feature
# AI generates code
git add ai-generated/
git commit -m "feat: initial generation (AI)"
git push origin ai/new-feature
gh pr create --label "ai-generated"
# Review, approve
mv ai-generated/* src/
git commit -m "feat: move reviewed code to src"
# Merge via PR
```

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [01-prompts.md](./01-prompts.md) - Prompt engineering rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Daily workflow checklist
