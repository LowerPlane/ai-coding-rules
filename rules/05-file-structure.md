# File Structure & Review Rules (Rules 43-50)

Rules for organizing code and reviewing AI-generated outputs.

---

## File Organization (Rules 43-46)

### Rule 43: Consistent File Structure

**❌ Bad:** Random file placement with no clear organization

**✅ Good:** Standard, predictable project structure

### How to Follow

- Establish a clear directory hierarchy
- Group related files together
- Use consistent naming conventions
- Document your structure in README.md
- Keep structure shallow (max 4-5 levels deep)

### Example

```
❌ BAD: Random, inconsistent structure
/project/
  user-stuff.js
  UserController.ts
  user_service.tsx
  userRepo.js
  test-user.spec.js
  helpers.js
  utils/
    user-utils.js
  components/
    UserThing.tsx

✅ GOOD: Consistent, predictable structure
/project/
  /src/
    /features/
      /users/
        user.controller.ts
        user.service.ts
        user.repository.ts
        user.types.ts
        user.validator.ts
        user.test.ts
    /shared/
      /types/
      /utils/
      /errors/
```

### Directory Structure Templates

```typescript
// Backend API Structure
/project/
  /src/
    /features/
      /users/
        user.controller.ts       // HTTP layer
        user.service.ts          // Business logic
        user.repository.ts       // Data access
        user.types.ts            // TypeScript types
        user.validator.ts        // Input validation
        user.test.ts             // Tests
        index.ts                 // Public exports
      /products/
        product.controller.ts
        product.service.ts
        product.repository.ts
        product.types.ts
        product.validator.ts
        product.test.ts
        index.ts
    /shared/
      /types/
        result.ts               // Result<T,E> type
        pagination.ts           // Common types
      /utils/
        logger.ts
        crypto.ts
      /errors/
        app-error.ts
        error-handler.ts
      /middleware/
        auth.ts
        rate-limit.ts
        validate.ts
      /config/
        database.ts
        env.ts
    /infrastructure/
      /database/
        connection.ts
        migrations/
        seeds/
      /cache/
        redis.ts
    app.ts                      // App setup
    server.ts                   // Entry point
  /tests/
    /integration/
    /e2e/
  /scripts/
  /docs/
  package.json
  tsconfig.json
  .env.example

// Frontend React Structure
/project/
  /src/
    /features/
      /auth/
        /components/
          LoginForm.tsx
          RegisterForm.tsx
        /hooks/
          useAuth.ts
        /api/
          auth-api.ts
        /types/
          auth.types.ts
        index.ts
      /products/
        /components/
          ProductList.tsx
          ProductCard.tsx
        /hooks/
          useProducts.ts
        /api/
          products-api.ts
        /types/
          product.types.ts
        index.ts
    /shared/
      /components/
        Button.tsx
        Input.tsx
        Modal.tsx
      /hooks/
        useLocalStorage.ts
        useDebounce.ts
      /utils/
        format.ts
        validation.ts
      /types/
        common.types.ts
    /layouts/
      MainLayout.tsx
      AuthLayout.tsx
    /routes/
      routes.tsx
    App.tsx
    main.tsx
  /public/
  /tests/
  package.json
  vite.config.ts
```

### Naming Conventions

```typescript
// File naming patterns
user.controller.ts        // ✅ Descriptive suffix
user.service.ts          // ✅ Descriptive suffix
user.types.ts            // ✅ Descriptive suffix
user.test.ts             // ✅ Descriptive suffix

UserController.ts        // ❌ PascalCase for files
usercontroller.ts        // ❌ No separator
user_controller.ts       // ❌ Snake case (unless Python)

// Component naming (React)
Button.tsx               // ✅ PascalCase for components
useAuth.ts               // ✅ camelCase for hooks
auth-api.ts              // ✅ kebab-case for utilities

// Constants
constants.ts             // ✅ Single file for small apps
/constants/
  http-status.ts         // ✅ Grouped by domain
  error-codes.ts
  validation-rules.ts
```

### Prompt Template for AI

```markdown
When generating files, follow this structure:

PROJECT STRUCTURE:
/src/
  /features/[feature-name]/
    [feature].controller.ts
    [feature].service.ts
    [feature].repository.ts
    [feature].types.ts
    [feature].validator.ts
    [feature].test.ts

NAMING RULES:
- Files: kebab-case with descriptive suffix (user.service.ts)
- Components: PascalCase (UserProfile.tsx)
- Hooks: camelCase with 'use' prefix (useAuth.ts)
- Types: kebab-case with .types.ts suffix
- Tests: same name as file with .test.ts suffix

EXAMPLE:
Generate user registration feature in /src/features/users/ following this structure.
```

---

## Rule 44: AI Code in Separate Directory

**❌ Bad:** AI generates directly to /src/, mixing with human code

**✅ Good:** AI generates to /ai-generated/, review, then merge

### How to Follow

1. AI outputs to `/ai-generated/[feature]/`
2. Run automated checks (linting, tests)
3. Human reviews code thoroughly
4. Merge to `/src/` only after approval
5. Document the merge in commit message

### Example

```
❌ BAD: Direct generation to source
/src/
  /features/
    /users/
      user.service.ts          // AI generated, no review
      user.controller.ts       // AI generated, no review

✅ GOOD: Staged review process
/ai-generated/
  /users/
    user.service.ts            // AI generates here first
    user.controller.ts
    user.repository.ts
    user.test.ts
    PROMPT.md                  // Original prompt
    REVIEW.md                  // Review notes

After review and approval:
/src/
  /features/
    /users/
      user.service.ts          // Merged after review
      user.controller.ts       // Merged after review
```

### Workflow

```bash
# Step 1: AI generates code
# Prompt: "Generate user service in /ai-generated/users/"

# Step 2: Run automated checks
npm run lint:ai-code ai-generated/users/
npm run test ai-generated/users/

# Step 3: Human review
# - Check security
# - Verify business logic
# - Test edge cases
# - Document in REVIEW.md

# Step 4: Merge to source (if approved)
mv ai-generated/users/* src/features/users/

# Step 5: Commit with proper message
git add src/features/users/
git commit -m "feat(users): add user service

Generated with AI assistance.
Prompt: See ai-generated/users/PROMPT.md
Review: Approved by @username
Security: Validated input/output handling
Tests: 95% coverage, all passing"

# Step 6: Clean up
rm -rf ai-generated/users/
```

### Review Workflow Script

```bash
#!/bin/bash
# tools/review-ai-code.sh

FEATURE_DIR=$1

if [ -z "$FEATURE_DIR" ]; then
  echo "Usage: ./tools/review-ai-code.sh ai-generated/feature-name"
  exit 1
fi

echo "📋 Reviewing AI-generated code in $FEATURE_DIR"
echo "================================================"

# 1. Run linter (stricter rules for AI code)
echo "1️⃣ Running linter..."
npm run lint:ai-code "$FEATURE_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Linting failed. Fix errors before proceeding."
  exit 1
fi
echo "✅ Linting passed"

# 2. Run tests
echo ""
echo "2️⃣ Running tests..."
npm test "$FEATURE_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Fix errors before proceeding."
  exit 1
fi
echo "✅ Tests passed"

# 3. Check test coverage
echo ""
echo "3️⃣ Checking test coverage..."
npm run test:coverage "$FEATURE_DIR"
COVERAGE=$(npm run test:coverage "$FEATURE_DIR" | grep "All files" | awk '{print $10}' | sed 's/%//')
if [ "$COVERAGE" -lt 90 ]; then
  echo "⚠️  Coverage is ${COVERAGE}% (target: 90%+)"
else
  echo "✅ Coverage: ${COVERAGE}%"
fi

# 4. Security scan
echo ""
echo "4️⃣ Running security checks..."
npm run security:scan "$FEATURE_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Security issues found. Fix before proceeding."
  exit 1
fi
echo "✅ Security checks passed"

# 5. Check for secrets
echo ""
echo "5️⃣ Checking for hardcoded secrets..."
./tools/check-secrets.sh "$FEATURE_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Potential secrets found. Review and remove."
  exit 1
fi
echo "✅ No hardcoded secrets detected"

# 6. Generate review checklist
echo ""
echo "6️⃣ Generating review checklist..."
cat > "$FEATURE_DIR/REVIEW.md" << EOF
# Code Review Checklist

## Automated Checks
- [x] Linting passed
- [x] Tests passed
- [x] Coverage >= 90%
- [x] Security scan passed
- [x] No hardcoded secrets

## Manual Review (Human Required)

### Security
- [ ] Input validation present
- [ ] Output sanitization applied
- [ ] SQL injection prevented
- [ ] XSS protection implemented
- [ ] Authentication/authorization correct
- [ ] Rate limiting appropriate
- [ ] Error messages don't leak info

### Code Quality
- [ ] Functions < 50 lines
- [ ] No TypeScript 'any' types
- [ ] Proper error handling
- [ ] Meaningful variable names
- [ ] Comments explain 'why', not 'what'
- [ ] No duplicate code
- [ ] Follows DRY principle

### Business Logic
- [ ] Implements requirements correctly
- [ ] Handles edge cases
- [ ] Validates business rules
- [ ] Returns proper error codes
- [ ] Logging is appropriate

### Tests
- [ ] Tests cover happy path
- [ ] Tests cover error scenarios
- [ ] Tests cover edge cases
- [ ] Tests are readable
- [ ] Tests follow AAA pattern

### Documentation
- [ ] Functions have JSDoc comments
- [ ] Complex logic is explained
- [ ] API endpoints documented
- [ ] Types/interfaces documented

## Review Notes
<!-- Add your review notes here -->

## Decision
- [ ] Approved for merge
- [ ] Needs changes (see notes)
- [ ] Rejected (see notes)

**Reviewer:**
**Date:**
**Security Level:** [ ] Low [ ] Medium [ ] High [ ] Critical
EOF

echo "✅ Review checklist created: $FEATURE_DIR/REVIEW.md"

echo ""
echo "================================================"
echo "✅ All automated checks passed!"
echo "📝 Next step: Complete manual review in $FEATURE_DIR/REVIEW.md"
echo "💡 After approval, run: ./tools/merge-ai-code.sh $FEATURE_DIR"
```

### Merge Script

```bash
#!/bin/bash
# tools/merge-ai-code.sh

FEATURE_DIR=$1

if [ -z "$FEATURE_DIR" ]; then
  echo "Usage: ./tools/merge-ai-code.sh ai-generated/feature-name"
  exit 1
fi

# Check if review is complete
if [ ! -f "$FEATURE_DIR/REVIEW.md" ]; then
  echo "❌ No REVIEW.md found. Run review-ai-code.sh first."
  exit 1
fi

# Check if approved
if ! grep -q "\[x\] Approved for merge" "$FEATURE_DIR/REVIEW.md"; then
  echo "❌ Code not approved in REVIEW.md"
  exit 1
fi

# Extract feature name
FEATURE_NAME=$(basename "$FEATURE_DIR")

# Merge to source
echo "📦 Merging $FEATURE_NAME to src/features/"
mkdir -p "src/features/$FEATURE_NAME"
cp -r "$FEATURE_DIR"/* "src/features/$FEATURE_NAME/"

# Archive review materials
mkdir -p "docs/ai-generated-reviews/$FEATURE_NAME"
mv "$FEATURE_DIR/PROMPT.md" "docs/ai-generated-reviews/$FEATURE_NAME/"
mv "$FEATURE_DIR/REVIEW.md" "docs/ai-generated-reviews/$FEATURE_NAME/"

# Clean up
rm -rf "$FEATURE_DIR"

echo "✅ Merged successfully!"
echo "📝 Review materials archived to docs/ai-generated-reviews/$FEATURE_NAME"
echo "💡 Next step: git add and commit with proper message"
```

### .gitignore Configuration

```bash
# .gitignore

# AI-generated code (not yet reviewed)
ai-generated/

# Exception: Keep prompts and reviews for tracking
!ai-generated/**/PROMPT.md
!ai-generated/**/REVIEW.md
```

---

## Rule 45: Group by Feature, Not Type

**❌ Bad:** Group by technical layer (/controllers/, /services/, /models/)

**✅ Good:** Group by business feature (/users/, /products/, /orders/)

### How to Follow

- Each feature is a self-contained module
- Related files are co-located
- Easy to delete entire features
- Clear ownership boundaries
- Reduces cognitive load

### Example

```
❌ BAD: Grouped by type (hard to maintain)
/src/
  /controllers/
    user.controller.ts
    product.controller.ts
    order.controller.ts
    payment.controller.ts
  /services/
    user.service.ts
    product.service.ts
    order.service.ts
    payment.service.ts
  /models/
    user.model.ts
    product.model.ts
    order.model.ts
    payment.model.ts
  /validators/
    user.validator.ts
    product.validator.ts
    order.validator.ts

Problems:
- Hard to find all user-related code
- Difficult to understand feature scope
- Can't delete feature without touching multiple dirs
- No clear ownership
- Merge conflicts frequent

✅ GOOD: Grouped by feature (maintainable)
/src/
  /features/
    /users/
      user.controller.ts
      user.service.ts
      user.repository.ts
      user.types.ts
      user.validator.ts
      user.test.ts
      index.ts              // Public exports
    /products/
      product.controller.ts
      product.service.ts
      product.repository.ts
      product.types.ts
      product.validator.ts
      product.test.ts
      index.ts
    /orders/
      order.controller.ts
      order.service.ts
      order.repository.ts
      order.types.ts
      order.validator.ts
      order.test.ts
      /subfeatures/          // Nested if needed
        /order-items/
        /order-tracking/
      index.ts

Benefits:
- All related code in one place
- Easy to understand feature scope
- Can delete entire feature directory
- Clear ownership per feature
- Fewer merge conflicts
```

### Feature Module Template

```typescript
// src/features/users/index.ts
// Public API of the feature

export { UserController } from './user.controller';
export { UserService } from './user.service';
export { UserRepository } from './user.repository';
export type { User, CreateUserDTO, UpdateUserDTO } from './user.types';
export { userValidator } from './user.validator';

// Internal exports (not exported)
// - user.test.ts
// - user.helper.ts (if any)
```

```typescript
// src/features/users/user.types.ts
// All types for this feature

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

export enum UserRole {
  USER = 'user',
  ADMIN = 'admin',
  MODERATOR = 'moderator',
}

export interface CreateUserDTO {
  email: string;
  password: string;
  name: string;
}

export interface UpdateUserDTO {
  email?: string;
  name?: string;
}

export interface UserFilters {
  role?: UserRole;
  search?: string;
  createdAfter?: Date;
}
```

### Feature Boundaries

```typescript
// ✅ GOOD: Features communicate through public APIs
// src/features/orders/order.service.ts

import { UserService } from '@/features/users';
import { ProductService } from '@/features/products';

export class OrderService {
  constructor(
    private userService: UserService,      // ✅ Use public API
    private productService: ProductService // ✅ Use public API
  ) {}

  async createOrder(userId: string, productIds: string[]) {
    // Use public APIs only
    const user = await this.userService.findById(userId);
    const products = await this.productService.findByIds(productIds);

    // Create order logic...
  }
}

// ❌ BAD: Reaching into internal implementation
import { UserRepository } from '@/features/users/user.repository';

export class OrderService {
  constructor(
    private userRepository: UserRepository // ❌ Skip service layer
  ) {}
}
```

### Frontend Feature Structure

```typescript
// React feature structure
/src/
  /features/
    /products/
      /components/
        ProductList.tsx        // Feature-specific components
        ProductCard.tsx
        ProductFilters.tsx
      /hooks/
        useProducts.ts         // Feature-specific hooks
        useProductFilters.ts
      /api/
        products-api.ts        // API calls for this feature
      /types/
        product.types.ts       // Types for this feature
      /utils/
        product-utils.ts       // Feature-specific utilities
      /constants/
        product-constants.ts
      index.ts                 // Public exports

// Usage from other features
import { ProductList, useProducts } from '@/features/products';
```

---

## Rule 46: Shared Code in Common Directory

**❌ Bad:** Duplicate utilities across features

**✅ Good:** Shared code in /shared/ or /common/

### How to Follow

- Identify truly reusable code
- Extract to /shared/ directory
- Organize by purpose (types, utils, errors)
- Avoid feature-specific code in shared
- Use consistent naming

### Example

```
❌ BAD: Duplicated code across features
/src/
  /features/
    /users/
      user.service.ts
      logger.ts              // ❌ Duplicated
      result.ts              // ❌ Duplicated
      date-utils.ts          // ❌ Duplicated
    /products/
      product.service.ts
      logger.ts              // ❌ Duplicated
      result.ts              // ❌ Duplicated
      date-utils.ts          // ❌ Duplicated

✅ GOOD: Shared code extracted
/src/
  /shared/
    /types/
      result.ts              // Result<T,E> type
      pagination.ts          // Pagination types
      api-response.ts        // API response types
    /utils/
      logger.ts              // Logging utility
      date-utils.ts          // Date formatting
      crypto.ts              // Encryption utilities
      validation.ts          // Common validators
    /errors/
      app-error.ts           // Base error class
      error-codes.ts         // Error code constants
      error-handler.ts       // Global error handler
    /constants/
      http-status.ts         // HTTP status codes
      regex.ts               // Common regex patterns
      limits.ts              // Rate limits, size limits
    /middleware/
      auth.ts                // Authentication middleware
      rate-limit.ts          // Rate limiting
      validate.ts            // Request validation
      error.ts               // Error handling middleware
    /config/
      env.ts                 // Environment variables
      database.ts            // Database config
      redis.ts               // Redis config
  /features/
    /users/
      user.service.ts        // Uses shared utilities
    /products/
      product.service.ts     // Uses shared utilities
```

### Shared Types Example

```typescript
// src/shared/types/result.ts
/**
 * Result type for operations that can fail
 * Avoids throwing exceptions for expected errors
 */
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

export const ok = <T>(data: T): Result<T, never> => ({
  success: true,
  data,
});

export const err = <E>(error: E): Result<never, E> => ({
  success: false,
  error,
});

// Usage in features
import { Result, ok, err } from '@/shared/types/result';

export class UserService {
  async findById(id: string): Promise<Result<User, string>> {
    const user = await this.repository.findById(id);

    if (!user) {
      return err('User not found');
    }

    return ok(user);
  }
}
```

```typescript
// src/shared/types/pagination.ts
export interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

export const createPaginatedResponse = <T>(
  data: T[],
  total: number,
  params: PaginationParams
): PaginatedResponse<T> => {
  const totalPages = Math.ceil(total / params.limit);

  return {
    data,
    pagination: {
      page: params.page,
      limit: params.limit,
      total,
      totalPages,
      hasNext: params.page < totalPages,
      hasPrev: params.page > 1,
    },
  };
};
```

### When to Use Shared vs Feature-Specific

```typescript
// ✅ GOOD: Truly reusable → shared
/shared/
  /utils/
    date-utils.ts         // Used by all features
    logger.ts             // Used by all features
    crypto.ts             // Used by all features

// ✅ GOOD: Feature-specific → keep in feature
/features/
  /products/
    /utils/
      product-formatter.ts  // Only used by products
      price-calculator.ts   // Only used by products

// ❌ BAD: Feature-specific in shared
/shared/
  /utils/
    user-email-sender.ts   // ❌ Only used by users feature

// ❌ BAD: Generic util duplicated
/features/
  /users/
    date-utils.ts          // ❌ Should be in shared
  /products/
    date-utils.ts          // ❌ Should be in shared
```

---

## Review & Approval (Rules 47-50)

### Rule 47: Human Always Reviews First

**❌ Bad:** Deploy AI code directly to production

**✅ Good:** Human review + approval required for all AI code

### How to Follow

1. AI generates code in isolated directory
2. Automated checks run (lint, tests, security)
3. Human reviews for logic and security
4. Approval required before merge
5. Deploy only after approval

### Example Workflow

```markdown
Step 1: AI Generation
- AI generates code in /ai-generated/[feature]/
- Original prompt saved to PROMPT.md
- AI provides self-review notes

Step 2: Automated Checks
- Linting (stricter rules for AI code)
- Unit tests (90%+ coverage required)
- Security scan (check for secrets, vulnerabilities)
- Type checking (no 'any' types)
- Complexity analysis (max cyclomatic complexity)

Step 3: Human Review
- Security validation
- Business logic verification
- Edge case handling
- Error handling completeness
- Performance considerations
- Documentation quality

Step 4: Approval
- Reviewer signs off in REVIEW.md
- Code merged to source
- Commit message documents AI involvement

Step 5: Deployment
- CI/CD pipeline runs additional checks
- Staging deployment first
- Production deployment after validation
```

---

## Rule 48: Use Code Review Checklist

**❌ Bad:** Ad-hoc, inconsistent reviews

**✅ Good:** Standardized checklist for every review

### How to Follow

- Create standardized checklist
- Customize by security level
- Track completion percentage
- Archive completed reviews
- Update checklist based on learnings

### Example Checklists by Security Level

```markdown
# LOW SECURITY (UI Components, Formatters)

## Quick Review Checklist

- [ ] Tests passing (>=80% coverage)
- [ ] No TypeScript 'any' types
- [ ] Functions < 50 lines
- [ ] No code duplication
- [ ] Proper error handling
- [ ] Documentation present

Time estimate: 10-15 minutes
```

```markdown
# MEDIUM SECURITY (API Endpoints, Business Logic)

## Standard Review Checklist

Security:
- [ ] Input validation with schema
- [ ] Output sanitization
- [ ] Authentication checked
- [ ] Authorization correct
- [ ] No SQL injection risk
- [ ] Rate limiting present

Quality:
- [ ] Tests passing (>=90% coverage)
- [ ] Edge cases tested
- [ ] Error handling complete
- [ ] No TypeScript 'any' types
- [ ] Functions < 50 lines
- [ ] No code duplication

Documentation:
- [ ] JSDoc on public functions
- [ ] API endpoints documented
- [ ] Business logic explained

Time estimate: 30-45 minutes
```

```markdown
# HIGH SECURITY (Authentication, Payments)

## Thorough Review Checklist

Security (Critical):
- [ ] No hardcoded secrets
- [ ] Input validation comprehensive
- [ ] Output sanitization complete
- [ ] Authentication implementation correct
- [ ] Authorization granular
- [ ] SQL injection prevented
- [ ] XSS protection implemented
- [ ] Rate limiting strict
- [ ] Security logging complete

Code Quality:
- [ ] Tests passing (>=95% coverage)
- [ ] All paths tested
- [ ] All error scenarios tested
- [ ] No TypeScript 'any' types
- [ ] Functions < 30 lines
- [ ] Complexity < 10

Business Logic:
- [ ] Requirements met completely
- [ ] Business rules correct
- [ ] Edge cases handled
- [ ] Transactions appropriate

Documentation:
- [ ] Complete JSDoc
- [ ] Security considerations documented
- [ ] API fully documented

Compliance:
- [ ] OWASP Top 10 checked
- [ ] PCI DSS if payment-related
- [ ] GDPR if EU users

Time estimate: 60-120 minutes
Requires: Senior developer + security review
```

---

## Rule 49: AI Code Gets Stricter Linting

**❌ Bad:** Same linting rules for human and AI code

**✅ Good:** Stricter rules for AI-generated code

### How to Follow

- Create separate ESLint config for AI code
- Lower complexity thresholds
- Stricter line limits
- More aggressive checks
- Zero tolerance for warnings

### Example Configuration

```javascript
// .eslintrc.js
module.exports = {
  root: true,
  extends: ['@your-org/eslint-config'],

  // Standard rules for human code
  rules: {
    'max-lines-per-function': ['warn', 100],
    complexity: ['warn', 15],
    'max-depth': ['warn', 4],
  },

  // Stricter rules for AI-generated code
  overrides: [
    {
      files: ['ai-generated/**/*.ts', 'ai-generated/**/*.tsx'],
      rules: {
        // Complexity (STRICTER)
        complexity: ['error', 10],              // vs 15 for human
        'max-lines-per-function': ['error', 50], // vs 100 for human
        'max-depth': ['error', 3],              // vs 4 for human
        'max-params': ['error', 3],
        'max-lines': ['error', 300],

        // TypeScript (STRICTER)
        '@typescript-eslint/no-explicit-any': 'error',
        '@typescript-eslint/explicit-function-return-type': 'error',
        '@typescript-eslint/explicit-module-boundary-types': 'error',

        // Code Quality (STRICTER)
        'no-console': 'error',                  // vs warn for human
        'no-debugger': 'error',
        'no-var': 'error',
        'prefer-const': 'error',
        'no-magic-numbers': ['error', {
          ignore: [0, 1, -1],
          ignoreArrayIndexes: true,
        }],

        // Security (ENFORCED)
        'no-eval': 'error',
        'no-implied-eval': 'error',
        'no-new-func': 'error',

        // Comments (REQUIRED)
        'require-jsdoc': ['error', {
          require: {
            FunctionDeclaration: true,
            MethodDefinition: true,
            ClassDeclaration: true,
          },
        }],
      },
    },
  ],
};
```

### package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint src/",
    "lint:ai-code": "eslint ai-generated/ --max-warnings 0",
    "lint:fix": "eslint src/ --fix",
    "lint:ai-fix": "eslint ai-generated/ --fix"
  }
}
```

---

## Rule 50: Document AI Generation

**❌ Bad:** No record of AI involvement

**✅ Good:** Document prompts, outputs, and reviews

### How to Follow

- Add @generated tag to AI code
- Include original prompt reference
- Document review date and reviewer
- Track AI model/version used
- Archive prompts for reproducibility

### Example Documentation

```typescript
/**
 * User Service
 *
 * Handles user management operations including creation, updates,
 * and authentication.
 *
 * @generated AI
 * @aiModel Claude 3.5 Sonnet
 * @prompt prompts/user-service.md
 * @generatedDate 2025-01-15
 * @reviewedBy John Doe <john@example.com>
 * @reviewedDate 2025-01-16
 * @securityLevel HIGH
 * @testCoverage 95%
 */
export class UserService {
  /**
   * Creates a new user account
   *
   * @param data - User registration data
   * @returns Result with created user or error
   *
   * @generated AI
   * @humanReviewed 2025-01-16
   */
  async create(data: CreateUserDTO): Promise<Result<User, Error>> {
    // Implementation...
  }

  /**
   * Custom validation logic added by human reviewer
   *
   * @humanAdded 2025-01-16
   * @reason Handle specific business rule for enterprise accounts
   */
  private validateEnterpriseAccount(data: CreateUserDTO): boolean {
    // Human-added logic...
  }
}
```

### Commit Message Template

```bash
# When committing AI-generated code

git commit -m "feat(users): add user service with CRUD operations

Implemented user management service with create, read, update, and
delete operations. Includes comprehensive validation, error handling,
and security measures.

AI-Generated: Yes
Model: Claude 3.5 Sonnet
Prompt: docs/ai-generated-reviews/users/PROMPT.md
Review: docs/ai-generated-reviews/users/REVIEW.md
Reviewed-by: John Doe <john@example.com>
Security-level: HIGH
Test-coverage: 96.8%

Changes:
- Add UserService class with DI
- Add Zod validation schemas
- Add comprehensive test suite
- Add JSDoc documentation

Security notes:
- Password hashing with bcrypt (cost 12)
- Input validation on all methods
- Soft delete implementation
- No sensitive data in responses"
```

---

## Summary: File Structure & Review Best Practices

✅ **Do:**
- Use consistent, predictable file structure
- Stage AI code in separate directory first
- Group files by feature, not type
- Extract shared code to /shared/
- Always review AI code before merging
- Use standardized review checklists
- Apply stricter linting to AI code
- Document AI generation thoroughly
- Archive prompts and reviews

❌ **Don't:**
- Place files randomly
- Generate directly to source
- Group by technical layer
- Duplicate utilities across features
- Deploy AI code without review
- Use ad-hoc review processes
- Apply same linting rules
- Skip documentation
- Lose prompt history

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│         FILE STRUCTURE & REVIEW RULES              │
├─────────────────────────────────────────────────────┤
│ STRUCTURE:                                          │
│  ✓ /features/[feature]/ (not /controllers/)       │
│  ✓ /shared/ for common code                       │
│  ✓ Consistent naming conventions                  │
│  ✓ Max 4-5 directory levels                       │
│                                                     │
│ AI CODE WORKFLOW:                                   │
│  1. Generate to /ai-generated/[feature]/          │
│  2. Run automated checks                          │
│  3. Human review (use checklist)                  │
│  4. Merge to /src/ after approval                 │
│  5. Document in commit message                    │
│                                                     │
│ REVIEW REQUIREMENTS:                                │
│  ✓ Security checklist complete                    │
│  ✓ Code quality verified                          │
│  ✓ Tests >= 90% coverage                          │
│  ✓ Business logic validated                       │
│  ✓ Documentation reviewed                         │
│                                                     │
│ LINTING:                                            │
│  AI Code: Stricter rules, 0 warnings              │
│  Human Code: Standard rules                       │
│  Complexity: AI max 10, Human max 15              │
│  Lines: AI max 50, Human max 100                  │
│                                                     │
│ DOCUMENTATION:                                      │
│  ✓ @generated AI tag                              │
│  ✓ Original prompt saved                          │
│  ✓ Review notes archived                          │
│  ✓ Human changes tracked                          │
└─────────────────────────────────────────────────────┘
```

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [01-prompts.md](./01-prompts.md) - Prompt engineering rules
- [02-architecture.md](./02-architecture.md) - Architecture rules
- [03-security.md](./03-security.md) - Security rules
- [04-testing.md](./04-testing.md) - Testing rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Workflow checklist
