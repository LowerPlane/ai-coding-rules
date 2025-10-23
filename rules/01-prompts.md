# Prompt Engineering Rules (Rules 1-10)

Rules for crafting effective prompts for AI coding assistants.

---

## Rule 1: Never Use Generic Prompts

**❌ Bad:** "Build me a login page"

**✅ Good:** "Create a React login component using TypeScript, React Hook Form for validation, Tailwind CSS for styling, with email/password fields, 'remember me' checkbox, loading states, and error display"

### How to Follow

- Include specific technologies
- List all required features
- Specify styling approach
- Define validation rules
- Mention edge cases

### Example

```markdown
Create a user authentication form with:
- Stack: React 18 + TypeScript + Tailwind CSS
- Features: Email/password fields, "remember me", forgot password link
- Validation: Email format, password min 8 chars
- States: Loading, error display, success redirect
- Style: Mobile-responsive, accessible (WCAG 2.1 AA)
```

---

## Rule 2: Always Provide Context Before Task

**❌ Bad:** "Write an API endpoint"

**✅ Good:** Provide stack details (Express, PostgreSQL, JWT auth) THEN describe endpoint

### How to Follow

Use this template:

```markdown
## Context
- Stack: Express.js 4.18 + TypeScript + PostgreSQL
- Existing: User model, auth middleware, database connection
- Conventions: Async/await, Result<T,E> return types

## Task
Create POST /api/users endpoint for user registration
```

### Example

```markdown
## Context
- Stack: Next.js 14 App Router + Prisma + PostgreSQL
- Existing: Auth system with NextAuth.js, User schema
- Database: Prisma ORM with existing migrations
- Conventions: Server actions, Zod validation

## Task
Add user profile update functionality
```

---

## Rule 3: Specify Output Format Explicitly

**❌ Bad:** "Generate a user service"

**✅ Good:** "Generate user.service.ts with TypeScript, JSDoc comments, Result<T,E> return types, and dependency injection"

### How to Follow

- Specify file names and extensions
- Request documentation format (JSDoc, inline comments)
- Define return types and error handling
- Specify code organization (classes vs functions)

### Example

```markdown
Generate UserService class:
- File: src/services/user.service.ts
- Format: TypeScript class with dependency injection
- Documentation: JSDoc comments for all public methods
- Return type: Promise<Result<User, Error>>
- Error handling: Try-catch with specific error types
- Style: Functional methods, no side effects
```

---

## Rule 4: Include Validation Requirements

**❌ Bad:** "Validate the input"

**✅ Good:** "Use Zod schema: email (valid format), password (min 8 chars, uppercase, lowercase, number, special char), name (2-100 chars, trimmed)"

### How to Follow

- Specify validation library (Zod, Joi, Yup)
- List all field requirements
- Define min/max constraints
- Include format requirements
- Specify error messages

### Example

```typescript
// Include in prompt:
const userSchema = z.object({
  email: z.string().email("Invalid email format").max(255),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain uppercase")
    .regex(/[0-9]/, "Must contain number")
    .regex(/[^A-Za-z0-9]/, "Must contain special character"),
  name: z.string().min(2).max(100).trim(),
  age: z.number().int().positive().min(18).max(120)
});
```

---

## Rule 5: Define Success and Error Scenarios

**❌ Bad:** "Handle errors"

**✅ Good:** "Return 201 with user object on success, 400 with field-specific errors on validation failure, 409 on duplicate email, 500 on database errors"

### How to Follow

- List all possible HTTP status codes
- Define error response structure
- Specify success response format
- Include edge case handling

### Example

```markdown
## Response Scenarios

Success (201):
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}

Validation Error (400):
{
  "success": false,
  "error": "Validation failed",
  "fields": {
    "email": "Invalid email format",
    "password": "Password too weak"
  }
}

Duplicate (409):
{
  "success": false,
  "error": "Email already exists"
}

Server Error (500):
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Rule 6: Specify Dependencies Explicitly

**❌ Bad:** "Use a validation library"

**✅ Good:** "Use Zod v3.21.0 (already in package.json), do NOT install new packages"

### How to Follow

- List available dependencies with versions
- Prohibit installing new packages without asking
- Specify preferred libraries for common tasks
- Include existing utility functions to reuse

### Example

```markdown
## Available Dependencies
- zod: ^3.21.0 (use for validation)
- bcrypt: ^5.1.0 (use for password hashing)
- jsonwebtoken: ^9.0.0 (use for JWT tokens)
- express-rate-limit: ^6.7.0 (use for rate limiting)

## DO NOT INSTALL
- Any new packages without explicit approval
- Alternative validation libraries (we use Zod)
- Alternative auth libraries (we use JWT)

## Existing Utilities
- src/utils/result.ts (Result<T,E> type)
- src/utils/logger.ts (structured logging)
- src/middleware/auth.ts (JWT verification)
```

---

## Rule 7: Request Tests Upfront

**❌ Bad:** "Write some tests later"

**✅ Good:** "Generate tests covering: happy path, validation errors, database errors, duplicate submissions. Target 90%+ coverage."

### How to Follow

- Always request tests in initial prompt
- Specify test framework (Jest, Vitest, etc.)
- List required test scenarios
- Set coverage targets

### Example

```markdown
## Test Requirements

Framework: Jest + Supertest
Coverage: > 90%

Test Scenarios:
1. Happy Path
   - Valid user registration
   - Returns 201 with user object

2. Validation Errors
   - Invalid email format (400)
   - Weak password (400)
   - Missing required fields (400)

3. Business Logic
   - Duplicate email (409)
   - Email case-insensitive check

4. Error Handling
   - Database connection failure (500)
   - External service timeout (500)

Test File: src/services/__tests__/user.service.test.ts
```

---

## Rule 8: Provide Style Guidelines

**❌ Bad:** Let AI choose coding style

**✅ Good:** "Use functional components, prefer const over let, explicit return types, max 50 lines per function"

### How to Follow

- Specify naming conventions
- Define function/component style
- Set complexity limits
- Include formatting preferences

### Example

```markdown
## Style Guidelines

Naming:
- camelCase for variables and functions
- PascalCase for classes and components
- UPPER_SNAKE_CASE for constants
- Prefix booleans with is/has/should

Code Style:
- Prefer const over let, never var
- Explicit return types on all functions
- Max 50 lines per function
- Max nesting depth: 3 levels
- Early returns for error cases

TypeScript:
- Strict mode enabled
- No any types
- Explicit type annotations
- Use interfaces over types for objects

Comments:
- JSDoc for public functions
- Inline comments for complex logic only
- TODO with ticket number
```

---

## Rule 9: Use Example-Driven Prompts

**❌ Bad:** "Make it work like a shopping cart"

**✅ Good:** "Implement shopping cart: addItem(productId, quantity), removeItem(productId), updateQuantity(productId, quantity), calculateTotal() returns {subtotal, tax, total}"

### How to Follow

- Provide input/output examples
- Show example function signatures
- Include sample data structures
- Demonstrate expected behavior

### Example

```markdown
## Shopping Cart Service

```typescript
interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartTotal {
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
}

class CartService {
  addItem(productId: string, quantity: number): Result<CartItem, Error>
  removeItem(productId: string): Result<void, Error>
  updateQuantity(productId: string, quantity: number): Result<CartItem, Error>
  calculateTotal(): CartTotal
  clear(): void
}
```

Example Usage:
```typescript
const cart = new CartService();
cart.addItem('prod-123', 2); // Add 2 items
cart.updateQuantity('prod-123', 5); // Update to 5
const total = cart.calculateTotal();
// Returns: { subtotal: 99.95, tax: 8.00, shipping: 5.00, total: 112.95 }
```
```

---

## Rule 10: Break Complex Tasks Into Steps

**❌ Bad:** "Build an e-commerce platform"

**✅ Good:** "Phase 1: Product listing. Phase 2: Cart management. Phase 3: Checkout. Generate Phase 1 first."

### How to Follow

- Identify logical phases
- Request one phase at a time
- Review each phase before proceeding
- Build incrementally

### Example

```markdown
## E-commerce Platform - Phased Approach

### Phase 1: Product Catalog (Start Here)
- Product model and schema
- GET /api/products (list with pagination)
- GET /api/products/:id (single product)
- Basic filtering (category, price range)
- Tests for product endpoints

### Phase 2: Shopping Cart (After Phase 1 Review)
- Cart model (user-specific)
- Add/remove/update cart items
- Cart persistence
- Calculate totals
- Tests for cart operations

### Phase 3: Checkout (After Phase 2 Review)
- Order creation
- Payment integration prep
- Order confirmation
- Email notifications
- Tests for checkout flow

Generate Phase 1 only. We'll review before proceeding to Phase 2.
```

---

## Summary: Prompt Engineering Best Practices

✅ **Do:**
- Be specific with technologies and requirements
- Provide full context upfront
- Specify output format and file names
- Include validation rules explicitly
- Define all success/error scenarios
- List available dependencies
- Request tests in initial prompt
- Provide style guidelines
- Use examples liberally
- Break complex tasks into phases

❌ **Don't:**
- Use vague or generic requests
- Assume AI knows your stack
- Leave output format ambiguous
- Skip validation requirements
- Forget error handling scenarios
- Let AI choose dependencies
- Defer testing to later
- Ignore code style
- Request everything at once

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [02-architecture.md](./02-architecture.md) - Architecture rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Workflow checklist
