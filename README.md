# AI Coding Rules - Complete Reference

**A mostly reasonable approach to AI-assisted development**

> **Note**: This guide assumes you are using Claude Code, GPT-4, or similar LLMs for code generation.

---

## Philosophy

AI is a **creative amplifier**, not a replacement. This guide provides:

- **Structured prompts** for consistent, high-quality outputs
- **Safety guardrails** to prevent AI-generated technical debt
- **Review workflows** for human oversight
- **Scalable patterns** for teams of any size

### Core Beliefs

> AI coding without rules is chaos. Rules without AI are slow. Together, they create velocity.

1. **Human-Directed, AI-Implemented**: Humans own architecture, AI fills implementation
2. **Test Everything**: 100% of AI code must include tests
3. **Explainability First**: If you can't explain it in 60 seconds, refactor it
4. **Version Control Everything**: Prompts, outputs, and iterations tracked

---

## What's in This Repository

This repository contains:

### 📖 Core Documentation
- **README.md** (this file) - All 54 rules in one reference
- **RULES_ONE_PAGE.md** - Printable quick reference card
- **INDEX.md** - Complete navigation index
- **DAILY_CHECKLIST.md** - 31-step workflow for AI coding tasks
- **CLAUDE.md** - Guidance for Claude Code AI assistant

### 📋 Detailed Rule Documents ([rules/](./rules/))
- **01-prompts.md** ✅ Complete - Prompt Engineering (Rules 1-10)
- **02-architecture.md** ✅ Complete - Architecture & Design (Rules 11-18)
- **03-security.md** ✅ Complete - Security (Rules 19-28)
- **04-testing.md** ✅ Complete - Code Quality & Testing (Rules 29-42)
- **05-file-structure.md** ✅ Complete - File Org & Review (Rules 43-50)
- **06-version-control.md** ✅ Complete - Version Control (Rules 51-54)
- **07-10-*.md** 📝 Placeholders - Frontend, Backend, Growth, Integrations

### 📝 Prompt Templates ([prompts/templates/](./prompts/templates/))
- **backend-starter.md** ✅ Complete - REST API template
- **frontend-component.md** ✅ Complete - UI component template
- **integration-builder.md** ✅ Complete - Third-party integration template
- **growth-playbook.md** ✅ Complete - Marketing/SEO template

### 🔄 Workflows ([workflows/](./workflows/))
- **api-generator.md** ✅ Complete - REST API generation (30-60 min)
- **landing-page-builder.md** ✅ Complete - Landing pages (45 min)
- **slack-bot-builder.md** ✅ Complete - Slack integration (60 min)
- **seo-content-generator.md** ✅ Complete - SEO content (30 min)

### 💡 Examples ([examples/](./examples/))
- Real-world projects built following these rules
- Includes prompts used and review notes

### 🛠️ Tools ([tools/](./tools/))
- **lint-ai-code.js** - Stricter linting for AI-generated code
- **pre-commit-hook.sh** - Git hook for security checks
- **prompt-validator.py** - Validate prompt templates

---

## Table of Contents

1. [Prompt Engineering Rules](#prompt-engineering-rules)
2. [Architecture & Design Rules](#architecture--design-rules)
3. [Security Rules](#security-rules)
4. [Code Quality Rules](#code-quality-rules)
5. [Testing Rules](#testing-rules)
6. [File Organization Rules](#file-organization-rules)
7. [Review & Approval Rules](#review--approval-rules)
8. [Version Control Rules](#version-control-rules)

---

## Prompt Engineering Rules

### Rule 1: Never Use Generic Prompts
**❌ Bad:** "Build me a login page"
**✅ Good:** "Create a React login component using TypeScript, React Hook Form for validation, Tailwind CSS for styling, with email/password fields, 'remember me' checkbox, loading states, and error display"

**How to Follow:**
- Include specific technologies
- List all required features
- Specify styling approach
- Define validation rules
- Mention edge cases

---

### Rule 2: Always Provide Context Before Task
**❌ Bad:** "Write an API endpoint"
**✅ Good:** Provide stack details (Express, PostgreSQL, JWT auth) THEN describe endpoint

**How to Follow:**
```markdown
## Context
- Stack: [Runtime/Framework/Database]
- Existing: [What's already built]
- Conventions: [Your coding style]

## Task
[What to build]
```

---

### Rule 3: Specify Output Format Explicitly
**❌ Bad:** "Generate a user service"
**✅ Good:** "Generate user.service.ts with TypeScript, JSDoc comments, Result<T,E> return types, and dependency injection"

**How to Follow:**
- Specify file names and extensions
- Request documentation format (JSDoc, inline comments)
- Define return types and error handling
- Specify code organization (classes vs functions)

---

### Rule 4: Include Validation Requirements
**❌ Bad:** "Validate the input"
**✅ Good:** "Use Zod schema: email (valid format), password (min 8 chars, uppercase, lowercase, number, special char), name (2-100 chars, trimmed)"

**How to Follow:**
- Specify validation library
- List all field requirements
- Define min/max constraints
- Include format requirements (email, phone, etc.)
- Specify error messages

---

### Rule 5: Define Success and Error Scenarios
**❌ Bad:** "Handle errors"
**✅ Good:** "Return 201 with user object on success, 400 with field-specific errors on validation failure, 409 on duplicate email, 500 on database errors"

**How to Follow:**
- List all possible HTTP status codes
- Define error response structure
- Specify success response format
- Include edge case handling

---

### Rule 6: Specify Dependencies Explicitly
**❌ Bad:** "Use a validation library"
**✅ Good:** "Use Zod v3.21.0 (already in package.json), do NOT install new packages"

**How to Follow:**
- List available dependencies with versions
- Prohibit installing new packages without asking
- Specify preferred libraries for common tasks
- Include existing utility functions to reuse

---

### Rule 7: Request Tests Upfront
**❌ Bad:** "Write some tests later"
**✅ Good:** "Generate tests covering: happy path, validation errors, database errors, duplicate submissions. Target 90%+ coverage."

**How to Follow:**
- Always request tests in initial prompt
- Specify test framework (Jest, Vitest, etc.)
- List required test scenarios
- Set coverage targets

---

### Rule 8: Provide Style Guidelines
**❌ Bad:** Let AI choose coding style
**✅ Good:** "Use functional components, prefer const over let, explicit return types, max 50 lines per function"

**How to Follow:**
- Specify naming conventions
- Define function/component style
- Set complexity limits
- Include formatting preferences

---

### Rule 9: Use Example-Driven Prompts
**❌ Bad:** "Make it work like a shopping cart"
**✅ Good:** "Implement shopping cart: addItem(productId, quantity), removeItem(productId), updateQuantity(productId, quantity), calculateTotal() returns {subtotal, tax, total}"

**How to Follow:**
- Provide input/output examples
- Show example function signatures
- Include sample data structures
- Demonstrate expected behavior

---

### Rule 10: Break Complex Tasks Into Steps
**❌ Bad:** "Build an e-commerce platform"
**✅ Good:** "Phase 1: Product listing. Phase 2: Cart management. Phase 3: Checkout. Generate Phase 1 first."

**How to Follow:**
- Identify logical phases
- Request one phase at a time
- Review each phase before proceeding
- Build incrementally

---

## Architecture & Design Rules

### Rule 11: Humans Design, AI Implements
**❌ Bad:** Ask AI to design entire system architecture
**✅ Good:** Human creates interfaces/types, AI implements them

**How to Follow:**
1. Human defines domain models and interfaces
2. Human creates API contracts
3. AI generates implementations
4. Human reviews and refines

---

### Rule 12: One Responsibility Per File
**❌ Bad:** 3000-line file doing everything
**✅ Good:** Small, focused files (< 300 lines each)

**How to Follow:**
- Split by concern: controller, service, repository
- Separate validation from business logic
- Keep routes separate from handlers
- Extract utilities to separate files

---

### Rule 13: Interface-First Development
**❌ Bad:** Let AI decide interfaces
**✅ Good:** Define interfaces first, then implement

**How to Follow:**
```typescript
// Human creates
interface UserService {
  createUser(data: CreateUserDTO): Promise<Result<User, Error>>;
}

// AI implements
class UserServiceImpl implements UserService {
  // Implementation
}
```

---

### Rule 14: Dependency Injection Over Hardcoding
**❌ Bad:** `const db = new Database()` inside service
**✅ Good:** `constructor(private db: Database)`

**How to Follow:**
- Pass dependencies as constructor params
- Never instantiate dependencies inside classes
- Use interfaces for dependencies
- Make dependencies explicit

---

### Rule 15: Stateless Services
**❌ Bad:** In-memory caches in services
**✅ Good:** External state management (Redis, database)

**How to Follow:**
- No module-level variables for state
- Use external storage (Redis, DB)
- Pass state as parameters
- Design for horizontal scaling

---

### Rule 16: Separation of Concerns
**❌ Bad:** Business logic in controllers
**✅ Good:** Controllers → Services → Repositories

**How to Follow:**
```
Controllers: HTTP handling only
Services: Business logic
Repositories: Data access only
Validators: Input validation only
```

---

### Rule 17: Return Types Over Throwing
**❌ Bad:** `throw new Error()` in business logic
**✅ Good:** `return Result.error(error)`

**How to Follow:**
```typescript
// Use Result types
type Result<T, E> =
  | { success: true; data: T }
  | { success: false; error: E };

// Return results
return { success: false, error: 'User not found' };
```

---

### Rule 18: Configuration as Code
**❌ Bad:** Magic numbers and strings throughout code
**✅ Good:** Centralized configuration with validation

**How to Follow:**
- Define config schema with Zod
- Validate environment variables on startup
- Use constants for business rules
- Document all config options

---

## Security Rules

### Rule 19: Never Hardcode Secrets
**❌ Bad:** `const API_KEY = 'sk_live_abc123'`
**✅ Good:** `const API_KEY = process.env.STRIPE_API_KEY`

**How to Follow:**
- All secrets in environment variables
- Validate secrets on startup (Zod schema)
- Never commit .env files
- Use .env.example for documentation

---

### Rule 20: AI Cannot Write Security-Critical Code Alone
**❌ Bad:** Let AI generate payment processing logic
**✅ Good:** Human designs, AI helps with boilerplate

**How to Follow:**
**Never Let AI Generate:**
- Payment processing logic
- Encryption implementations
- Password hashing algorithms (use libraries only)
- OAuth flows (use official SDKs)

**AI Can Help With:**
- Input validation boilerplate
- Rate limiting setup
- CSRF token integration

---

### Rule 21: Validate All Inputs
**❌ Bad:** Trust user input
**✅ Good:** Validate with schema (Zod/Joi) before processing

**How to Follow:**
```typescript
const schema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
});

// Validate before use
const data = schema.parse(req.body);
```

---

### Rule 22: Use Parameterized Queries Only
**❌ Bad:** `` `SELECT * FROM users WHERE id = ${userId}` ``
**✅ Good:** `db.query('SELECT * FROM users WHERE id = ?', [userId])`

**How to Follow:**
- Never concatenate user input into SQL
- Use ORM methods (Prisma, TypeORM)
- Use parameterized queries for raw SQL
- Explicitly prohibit string concatenation in prompts

---

### Rule 23: Sanitize All Output
**❌ Bad:** `res.send(`<h1>Results for: ${query}</h1>`)`
**✅ Good:** `res.send(`<h1>Results for: ${DOMPurify.sanitize(query)}</h1>`)`

**How to Follow:**
- Use DOMPurify for HTML sanitization
- Use template engines with auto-escaping
- Encode output based on context (HTML, URL, JavaScript)
- Never trust data from database either

---

### Rule 24: Implement Rate Limiting
**❌ Bad:** No rate limits
**✅ Good:** Rate limit all public endpoints

**How to Follow:**
```typescript
// Strict for auth endpoints
authLimiter: 5 requests per 15 minutes

// Normal for API endpoints
apiLimiter: 100 requests per 15 minutes

// Very strict for expensive operations
reportLimiter: 2 requests per hour
```

---

### Rule 25: Hash Passwords Correctly
**❌ Bad:** MD5, SHA-1, or custom hashing
**✅ Good:** bcrypt with cost factor 12+

**How to Follow:**
```typescript
import bcrypt from 'bcrypt';

// Hash
const hash = await bcrypt.hash(password, 12);

// Verify
const valid = await bcrypt.compare(password, hash);
```

---

### Rule 26: Secure JWT Tokens
**❌ Bad:** Long-lived tokens, weak secrets
**✅ Good:** Short-lived access tokens, strong secrets, refresh token rotation

**How to Follow:**
- Access tokens: 15 minutes
- Refresh tokens: 7 days, rotate on use
- Secret: minimum 32 characters
- Store refresh tokens in httpOnly cookies

---

### Rule 27: Apply Defense in Depth
**❌ Bad:** Single security layer
**✅ Good:** Multiple security layers

**How to Follow:**
```typescript
app.post('/api/sensitive', [
  rateLimiter,           // Layer 1
  authMiddleware,        // Layer 2
  requireRole('admin'),  // Layer 3
  validateRequest,       // Layer 4
  auditLogger,          // Layer 5
], handler);
```

---

### Rule 28: Log Security Events
**❌ Bad:** No logging or log everything
**✅ Good:** Log security-relevant events only

**How to Follow:**
**Always Log:**
- Failed login attempts
- Permission denied errors
- API key usage
- Data modifications
- Suspicious patterns

**Never Log:**
- Passwords (even hashed)
- API keys or secrets
- Credit card numbers
- Personal identification

---

## Code Quality Rules

### Rule 29: Explicit Over Implicit
**❌ Bad:** `function process(data) { ... }`
**✅ Good:** `function processUserData(data: UserData): ProcessedResult { ... }`

**How to Follow:**
- Use TypeScript for type safety
- Add explicit return types
- Name functions descriptively
- Avoid ambiguous names (data, result, temp)

---

### Rule 30: Small Functions
**❌ Bad:** 200-line functions
**✅ Good:** Functions under 50 lines

**How to Follow:**
- One function, one purpose
- Extract complex logic to separate functions
- Use early returns
- Limit nesting depth to 3 levels

---

### Rule 31: No Magic Numbers
**❌ Bad:** `if (user.age > 18)`
**✅ Good:** `if (user.age > MINIMUM_AGE)`

**How to Follow:**
```typescript
const MINIMUM_AGE = 18;
const MAX_LOGIN_ATTEMPTS = 5;
const TOKEN_EXPIRY_HOURS = 24;

// Use constants
if (user.age > MINIMUM_AGE) { ... }
```

---

### Rule 32: Meaningful Variable Names
**❌ Bad:** `const d = new Date()`, `const temp = x + y`
**✅ Good:** `const currentDate = new Date()`, `const totalPrice = basePrice + tax`

**How to Follow:**
- Use full words, not abbreviations
- Be specific: `userEmail` not `email`
- Use conventions: `isValid`, `hasPermission`, `shouldRetry`
- Avoid single letters except in loops

---

### Rule 33: DRY (Don't Repeat Yourself)
**❌ Bad:** Copy-paste code in multiple places
**✅ Good:** Extract to reusable function/utility

**How to Follow:**
- If code appears 3+ times, extract it
- Create utility functions
- Use higher-order functions
- Leverage inheritance/composition

---

### Rule 34: Comment Why, Not What
**❌ Bad:** `// Increment counter`
`counter++;`

**✅ Good:** `// Retry mechanism requires incremental backoff`
`counter++;`

**How to Follow:**
- Don't comment obvious code
- Explain business logic
- Document edge cases
- Note performance optimizations
- Link to relevant issues/tickets

---

### Rule 35: Handle Errors Gracefully
**❌ Bad:** Empty catch blocks
**✅ Good:** Specific error handling with logging

**How to Follow:**
```typescript
try {
  await operation();
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validation failed', { error });
    return { success: false, error: 'Invalid input' };
  }

  logger.error('Unexpected error', { error, stack: error.stack });
  return { success: false, error: 'Internal error' };
}
```

---

### Rule 36: Use TypeScript Strictly
**❌ Bad:** `any` types everywhere
**✅ Good:** Explicit types for everything

**How to Follow:**
```typescript
// tsconfig.json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "noUncheckedIndexedAccess": true
}
```

---

## Testing Rules

### Rule 37: Test Everything AI Generates
**❌ Bad:** Deploy AI code without tests
**✅ Good:** 90%+ test coverage before merge

**How to Follow:**
- Request tests in initial prompt
- Cover happy path + edge cases
- Test error scenarios
- Verify business rules

---

### Rule 38: Test Business Logic, Not Framework
**❌ Bad:** Test Express.js internals
**✅ Good:** Test your business logic

**How to Follow:**
- Focus on service layer tests
- Mock external dependencies
- Test pure functions thoroughly
- Integration tests for critical paths only

---

### Rule 39: Arrange-Act-Assert Pattern
**❌ Bad:** Mixed test logic
**✅ Good:** Clear AAA structure

**How to Follow:**
```typescript
it('should create user with valid data', async () => {
  // Arrange
  const userData = { email: 'test@example.com', name: 'Test' };

  // Act
  const result = await userService.create(userData);

  // Assert
  expect(result.success).toBe(true);
  expect(result.data.email).toBe(userData.email);
});
```

---

### Rule 40: Test Edge Cases
**❌ Bad:** Only test happy path
**✅ Good:** Test boundaries and edge cases

**How to Follow:**
- Empty inputs ([], null, undefined, "")
- Boundary values (0, -1, MAX_INT)
- Invalid types
- Concurrent operations
- Network failures

---

### Rule 41: Use Descriptive Test Names
**❌ Bad:** `it('works', ...)`
**✅ Good:** `it('should return 400 when email is invalid', ...)`

**How to Follow:**
- Start with "should"
- Describe behavior, not implementation
- Include expected outcome
- Make failures obvious

---

### Rule 42: Mock External Services
**❌ Bad:** Call real APIs in tests
**✅ Good:** Mock all external dependencies

**How to Follow:**
```typescript
// Mock external services
jest.mock('./paymentService');
jest.mock('./emailService');

// Test with mocks
const mockPaymentService = {
  charge: jest.fn().mockResolvedValue({ success: true }),
};
```

---

## File Organization Rules

### Rule 43: Consistent File Structure
**❌ Bad:** Random file placement
**✅ Good:** Standard project structure

**How to Follow:**
```
/src/
  /features/
    /users/
      user.controller.ts
      user.service.ts
      user.repository.ts
      user.types.ts
      user.validator.ts
      user.test.ts
```

---

### Rule 44: AI Code in Separate Directory
**❌ Bad:** AI generates directly to /src/
**✅ Good:** AI generates to /ai-generated/, review, then merge

**How to Follow:**
1. AI outputs to `/ai-generated/feature/`
2. Run linting and tests
3. Human reviews
4. Merge to `/src/` after approval

---

### Rule 45: Group by Feature, Not Type
**❌ Bad:** `/controllers/`, `/services/`, `/models/`
**✅ Good:** `/features/users/`, `/features/products/`

**How to Follow:**
- Each feature is self-contained
- Related files are together
- Easy to delete entire features
- Clear ownership boundaries

---

### Rule 46: Shared Code in Common Directory
**❌ Bad:** Duplicate utilities across features
**✅ Good:** Shared code in `/shared/` or `/common/`

**How to Follow:**
```
/src/
  /shared/
    /types/
    /utils/
    /errors/
    /constants/
  /features/
    /users/
    /products/
```

---

## Review & Approval Rules

### Rule 47: Human Always Reviews First
**❌ Bad:** Deploy AI code directly to production
**✅ Good:** Human review + approval required

**How to Follow:**
1. AI generates code
2. Automated checks (lint, tests)
3. Human reviews for logic and security
4. Approval required for merge
5. Deploy after approval

---

### Rule 48: Use Code Review Checklist
**❌ Bad:** Ad-hoc reviews
**✅ Good:** Standardized checklist

**How to Follow:**
**Security Checklist:**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS protection implemented

**Quality Checklist:**
- [ ] Functions under 50 lines
- [ ] Test coverage > 90%
- [ ] No TypeScript `any` types
- [ ] Error handling complete

---

### Rule 49: AI Code Gets Stricter Linting
**❌ Bad:** Same rules for human and AI code
**✅ Good:** Stricter rules for AI-generated code

**How to Follow:**
```javascript
// .eslintrc.js
overrides: [
  {
    files: ['ai-generated/**/*.ts'],
    rules: {
      complexity: ['error', 10],  // Stricter
      'max-lines-per-function': ['error', 50],  // Stricter
    },
  },
],
```

---

### Rule 50: Document AI Generation
**❌ Bad:** No record of AI involvement
**✅ Good:** Document prompts and AI outputs

**How to Follow:**
```typescript
/**
 * User Service
 *
 * @generated AI
 * @prompt "Create user service with CRUD operations"
 * @date 2025-01-15
 * @reviewed-by John Doe
 */
```

---

## Version Control Rules

### Rule 51: Meaningful Commit Messages
**❌ Bad:** `git commit -m "fix stuff"`
**✅ Good:** `git commit -m "feat(auth): add JWT token refresh endpoint"`

**How to Follow:**
```
Format: <type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Test additions

Example:
feat(users): add email verification endpoint
fix(auth): resolve token expiration bug
docs(api): update authentication documentation
```

---

### Rule 52: Small, Focused Commits
**❌ Bad:** 1000 lines changed in single commit
**✅ Good:** Logical, reviewable commits

**How to Follow:**
- One feature per commit
- Separate refactoring from features
- Commit working code only
- Keep related changes together

---

### Rule 53: Tag AI-Generated Commits
**❌ Bad:** No indication of AI involvement
**✅ Good:** Tag commits with AI indicator

**How to Follow:**
```bash
git commit -m "feat(api): add user registration endpoint

Generated with Claude Code assistance.
Prompt: See prompts/user-registration.md
Human review: Approved by @johndoe"
```

---

### Rule 54: Branch Strategy for AI Code
**❌ Bad:** Commit AI code directly to main
**✅ Good:** Use feature branches with review

**How to Follow:**
```bash
# AI generates code
git checkout -b ai/user-registration

# Review and test
npm run lint:ai-code
npm test

# Create PR for human review
git push origin ai/user-registration
# Open PR with "AI-Generated" label
```

---

## Summary: The 10 Most Critical Rules

**Must-Follow Rules (Never Skip These):**

1. ✅ **Rule 2**: Always provide context before task
2. 🔒 **Rule 19**: Never hardcode secrets
3. 🔒 **Rule 20**: AI cannot write security-critical code alone
4. 🔒 **Rule 22**: Use parameterized queries only
5. ✅ **Rule 37**: Test everything AI generates
6. 📁 **Rule 44**: AI code in separate directory first
7. 👁️ **Rule 47**: Human always reviews first
8. 🏗️ **Rule 11**: Humans design, AI implements
9. 🔒 **Rule 21**: Validate all inputs
10. ⚡ **Rule 30**: Keep functions small (< 50 lines)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│           AI CODING RULES - QUICK REF              │
├─────────────────────────────────────────────────────┤
│ BEFORE PROMPTING:                                   │
│  ☐ Define context (stack, existing code)          │
│  ☐ Specify output format                          │
│  ☐ List dependencies                              │
│  ☐ Include validation rules                       │
│                                                     │
│ AFTER GENERATION:                                   │
│  ☐ Run lint:ai-code                               │
│  ☐ Run tests (90%+ coverage)                      │
│  ☐ Security review                                │
│  ☐ Human code review                              │
│  ☐ Merge to source                                │
│                                                     │
│ NEVER LET AI:                                       │
│  ✗ Generate payment processing                     │
│  ✗ Implement encryption                           │
│  ✗ Design system architecture                     │
│  ✗ Go directly to production                      │
│                                                     │
│ ALWAYS:                                             │
│  ✓ Validate all inputs                            │
│  ✓ Use parameterized queries                      │
│  ✓ Test everything                                │
│  ✓ Review before merge                            │
└─────────────────────────────────────────────────────┘
```

---

## Getting Started

### Quick Start (5 minutes)

1. **Read the philosophy** (above) to understand the approach
2. **Review [RULES_ONE_PAGE.md](./RULES_ONE_PAGE.md)** - Printable reference
3. **Check [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)** - Use for every AI coding task
4. **Try a template** - Use [backend-starter.md](./prompts/templates/backend-starter.md) for your next API

### For Your First AI-Generated Feature

1. **Plan** - Define requirements clearly (you, not AI)
2. **Prompt** - Use [rules/01-prompts.md](./rules/01-prompts.md) or a template
3. **Generate** - Let AI create code in `/ai-generated/` directory
4. **Review** - Follow [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)
5. **Test** - Ensure 90%+ coverage
6. **Merge** - Move to `/src/` after human approval

### Setting Up Tools

```bash
# Install pre-commit hook (checks for secrets)
cp tools/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Validate a prompt template
python tools/prompt-validator.py prompts/templates/backend-starter.md

# Lint AI-generated code (stricter rules)
node tools/lint-ai-code.js ai-generated/my-feature
```

---

## Resources

### In This Repository
- [rules/01-prompts.md](./rules/01-prompts.md) - Detailed prompt engineering guide
- [prompts/templates/](./prompts/templates/) - Reusable prompt templates
- [workflows/](./workflows/) - Step-by-step workflows
- [examples/](./examples/) - Real-world example projects
- [tools/](./tools/) - Validation and linting scripts

### External Resources
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Security reference
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/) - Security best practices

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- Report issues or suggest improvements
- Add new rules or update existing ones
- Create templates for other stacks/frameworks
- Share example projects with prompts and review notes
- Improve tools and automation

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

**Remember: AI is a powerful tool, but humans remain responsible for architecture, security, and final decisions.**

**Last Updated:** 2025-10-15 | **Version:** 1.0 | **Rules:** 54