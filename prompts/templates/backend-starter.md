# Backend API Starter Template

Use this template when generating backend API endpoints with AI assistance.

---

## Context

**Stack:**
- Runtime: Node.js 20.x
- Framework: Express.js 4.18+ / Fastify 4.x / Nest.js 10.x
- Language: TypeScript 5.x
- Database: PostgreSQL 15+ / MongoDB 6.x
- ORM: Prisma 5.x / TypeORM 0.3.x
- Validation: Zod 3.x
- Authentication: JWT (jsonwebtoken 9.x)

**Existing Code:**
- User authentication system implemented
- Database connection established
- Middleware: auth, error handling, logging
- Base repository pattern for data access

**Conventions:**
- Async/await (no callbacks)
- Result<T, E> return types for error handling
- Dependency injection pattern
- Feature-based folder structure
- 90%+ test coverage required

---

## Task

Create a REST API endpoint for [DESCRIBE FEATURE]

### Specific Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

---

## API Specification

### Endpoint
```
METHOD /api/v1/resource
```

### Request

**Headers:**
```json
{
  "Authorization": "Bearer {jwt_token}",
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "field1": "string",
  "field2": "number",
  "field3": "boolean"
}
```

### Response

**Success (200/201):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "field1": "value",
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
```

**Validation Error (400):**
```json
{
  "success": false,
  "error": "Validation failed",
  "fields": {
    "field1": "Error message",
    "field2": "Error message"
  }
}
```

**Unauthorized (401):**
```json
{
  "success": false,
  "error": "Unauthorized"
}
```

**Not Found (404):**
```json
{
  "success": false,
  "error": "Resource not found"
}
```

**Server Error (500):**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Validation Rules

Use Zod schema:

```typescript
const schema = z.object({
  field1: z.string()
    .min(2, "Minimum 2 characters")
    .max(100, "Maximum 100 characters")
    .trim(),

  field2: z.number()
    .int("Must be integer")
    .positive("Must be positive")
    .min(1)
    .max(1000),

  field3: z.boolean(),

  email: z.string().email("Invalid email").max(255),

  // Optional field
  field4: z.string().optional(),

  // Enum
  status: z.enum(['active', 'inactive', 'pending']),

  // Array
  tags: z.array(z.string()).min(1).max(10),
});
```

---

## Output Format

### File Structure
```
src/features/[feature-name]/
├── [feature].controller.ts     # HTTP handling
├── [feature].service.ts        # Business logic
├── [feature].repository.ts     # Data access
├── [feature].types.ts          # TypeScript types
├── [feature].validator.ts      # Zod schemas
└── __tests__/
    ├── [feature].controller.test.ts
    ├── [feature].service.test.ts
    └── [feature].repository.test.ts
```

### Code Style

**Controller:**
```typescript
import { Request, Response } from 'express';
import { UserService } from './user.service';
import { createUserSchema } from './user.validator';

export class UserController {
  constructor(private userService: UserService) {}

  async create(req: Request, res: Response): Promise<void> {
    // Validate
    const validation = createUserSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({
        success: false,
        error: 'Validation failed',
        fields: validation.error.flatten().fieldErrors,
      });
      return;
    }

    // Business logic
    const result = await this.userService.create(validation.data);

    if (!result.success) {
      res.status(500).json({
        success: false,
        error: result.error.message,
      });
      return;
    }

    res.status(201).json({
      success: true,
      data: result.data,
    });
  }
}
```

**Service:**
```typescript
import { UserRepository } from './user.repository';
import { CreateUserDTO, User } from './user.types';
import { Result } from '@/utils/result';

export class UserService {
  constructor(private repository: UserRepository) {}

  async create(data: CreateUserDTO): Promise<Result<User, Error>> {
    try {
      // Business logic
      const user = await this.repository.create(data);
      return { success: true, data: user };
    } catch (error) {
      return { success: false, error: error as Error };
    }
  }
}
```

---

## Security Requirements

**CRITICAL - Never Skip:**

1. **Input Validation**
   - Validate ALL inputs with Zod schema
   - Sanitize strings (trim, escape)
   - Limit array/string sizes

2. **SQL Injection Prevention**
   - Use parameterized queries only
   - NEVER concatenate user input into SQL
   - Use ORM methods (Prisma, TypeORM)

3. **Authentication**
   - Verify JWT token on all protected endpoints
   - Check token expiration
   - Validate user permissions

4. **Rate Limiting**
   - Apply rate limits: 100 req/15min for API
   - Stricter for auth endpoints: 5 req/15min

5. **No Secrets in Code**
   - All secrets in environment variables
   - Validate secrets on startup

---

## Testing Requirements

**Coverage: 90%+ required**

### Test Scenarios

1. **Happy Path**
   ```typescript
   it('should create user with valid data', async () => {
     const userData = { email: 'test@example.com', name: 'Test' };
     const result = await service.create(userData);
     expect(result.success).toBe(true);
     expect(result.data.email).toBe(userData.email);
   });
   ```

2. **Validation Errors**
   ```typescript
   it('should return error for invalid email', async () => {
     const result = await service.create({ email: 'invalid' });
     expect(result.success).toBe(false);
   });
   ```

3. **Edge Cases**
   ```typescript
   it('should handle duplicate email', async () => {
     // Test duplicate handling
   });

   it('should handle database errors', async () => {
     // Test error handling
   });
   ```

4. **Security**
   ```typescript
   it('should reject requests without auth token', async () => {
     // Test authentication
   });
   ```

---

## Dependencies

**Use existing packages only:**
- express / fastify / @nestjs/core
- zod (validation)
- jsonwebtoken (JWT)
- bcrypt (password hashing)
- prisma / typeorm (database)

**DO NOT install new packages without approval**

---

## Example Usage

### Prompt Example

```markdown
## Context
- Stack: Express.js 4.18 + TypeScript + Prisma + PostgreSQL
- Existing: User auth, database connection, error middleware
- Conventions: Async/await, Result<T,E>, dependency injection

## Task
Create POST /api/v1/products endpoint for adding products

## Requirements
- Product has: name, description, price, category, stock
- Only admins can create products
- Validate all inputs
- Check duplicate product names
- Return 201 with product on success

## Validation
- name: 2-200 chars, required
- description: 10-2000 chars, required
- price: positive number with 2 decimals
- category: enum ['electronics', 'clothing', 'food']
- stock: non-negative integer

## Security
- Require JWT auth + admin role
- Validate all inputs with Zod
- Rate limit: 20 requests per hour

## Tests
- Happy path with valid product
- Validation errors for each field
- Duplicate name rejection
- Non-admin rejection
- Database error handling

Generate: controller, service, repository, types, validator, tests
```

---

## Checklist

Before submitting AI-generated code:

- [ ] All inputs validated with Zod
- [ ] Parameterized queries (no string concatenation)
- [ ] Authentication middleware applied
- [ ] Rate limiting configured
- [ ] Error handling complete
- [ ] Tests cover all scenarios (90%+)
- [ ] No hardcoded secrets
- [ ] Functions under 50 lines
- [ ] TypeScript strict mode passes
- [ ] JSDoc comments on public methods

---

**See also:**
- [Rule 21: Validate All Inputs](../../README.md#rule-21-validate-all-inputs)
- [Rule 22: Parameterized Queries](../../README.md#rule-22-use-parameterized-queries-only)
- [Rule 37: Test Everything](../../README.md#rule-37-test-everything-ai-generates)
- [DAILY_CHECKLIST.md](../../DAILY_CHECKLIST.md)
