# REST API Generator Workflow

**Complete REST API generation in 30-60 minutes using AI assistance**

---

## Overview

**Time Estimate:** 30-60 minutes
**Difficulty Level:** Intermediate
**Prerequisites:**
- Basic understanding of REST APIs
- Node.js/TypeScript experience
- Database knowledge (PostgreSQL/MongoDB)
- Git workflow familiarity

**What You'll Build:**
A production-ready REST API with:
- CRUD endpoints with validation
- Authentication and authorization
- Comprehensive test coverage (90%+)
- Security best practices
- Database integration
- Documentation

---

## Prerequisites and Setup

### Required Tools
- Node.js 20.x or higher
- Package manager (npm/yarn/pnpm)
- Database (PostgreSQL 15+ or MongoDB 6.x)
- Git
- Code editor with TypeScript support

### Required Knowledge
- REST API principles
- HTTP status codes
- SQL/NoSQL basics
- JWT authentication concepts

### Initial Setup (5 minutes)
```bash
# Create project directory
mkdir my-api && cd my-api

# Initialize project
npm init -y

# Install core dependencies
npm install express typescript zod prisma @types/node @types/express

# Install dev dependencies
npm install -D jest ts-jest @types/jest eslint prettier

# Create directories
mkdir -p src/features ai-generated prompts tests
```

---

## Workflow Steps

### Step 1: Define API Specification (5 minutes)

**Objective:** Create clear API requirements before generating code

**Action:**
Create a specification document defining your API endpoints.

**Prompt to Use:**
```markdown
Help me create an API specification for [YOUR FEATURE].

Requirements:
- Resource: [e.g., users, products, orders]
- Operations: [GET, POST, PUT, DELETE]
- Data fields: [list all fields with types]
- Business rules: [e.g., unique email, min/max values]
- Authentication: [required/optional]

Format the specification with:
- Endpoint paths
- Request/response schemas
- Validation rules
- HTTP status codes
```

**Example Output:**
```
POST /api/v1/products
- Authentication: Required (Admin only)
- Request: { name, description, price, category, stock }
- Response 201: { success, data: { id, ...fields, createdAt } }
- Response 400: { success: false, error, fields }
- Response 401: { success: false, error: "Unauthorized" }
```

**Review Checkpoint:**
- [ ] All endpoints defined
- [ ] Request/response formats clear
- [ ] Validation rules specified
- [ ] Authentication requirements documented

**References:** [Rule 2: Provide Context](../README.md#rule-2-always-provide-context-before-task), [Rule 5: Define Success/Error Scenarios](../README.md#rule-5-define-success-and-error-scenarios)

---

### Step 2: Set Up Database Schema (5 minutes)

**Objective:** Define data models before code generation

**Action:**
Create Prisma schema or database models.

**Prompt to Use:**
```markdown
Generate a Prisma schema for [YOUR RESOURCE] with the following fields:
- [field1]: [type] - [constraints]
- [field2]: [type] - [constraints]

Requirements:
- Use PostgreSQL database
- Add created_at and updated_at timestamps
- Define appropriate indexes for [fields]
- Add unique constraints on [fields]
- Include relationships to [other models]

Follow these conventions:
- snake_case for database columns
- camelCase for Prisma models
- Use UUID for primary keys
```

**Example Prompt:**
```markdown
Generate a Prisma schema for products with:
- id: UUID primary key
- name: String (2-200 chars, unique)
- description: String (10-2000 chars)
- price: Decimal (2 decimal places, positive)
- category: Enum ['electronics', 'clothing', 'food']
- stock: Integer (non-negative)
- created_at and updated_at timestamps

Add indexes on: name, category
Add unique constraint on: name
```

**Review Checkpoint:**
- [ ] Schema matches API specification
- [ ] All constraints defined
- [ ] Indexes added for frequently queried fields
- [ ] Relationships properly defined

**References:** [Rule 13: Interface-First Development](../README.md#rule-13-interface-first-development)

---

### Step 3: Generate TypeScript Types and Interfaces (5 minutes)

**Objective:** Create type-safe data structures

**Action:**
Generate TypeScript types, DTOs, and interfaces.

**Prompt to Use:**
```markdown
Generate TypeScript types for the [RESOURCE] API:

Create these files in src/features/[resource]/:
1. [resource].types.ts - Core domain types
2. [resource].dto.ts - Data Transfer Objects

Requirements:
- Align with Prisma schema
- Separate Create, Update, Response DTOs
- Use strict TypeScript (no 'any' types)
- Add JSDoc comments
- Include Result<T, E> type for responses

Example structure:
- [Resource] interface (domain model)
- Create[Resource]DTO (input validation)
- Update[Resource]DTO (partial updates)
- [Resource]Response (API response)
```

**Example Output Structure:**
```typescript
// product.types.ts
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: ProductCategory;
  stock: number;
  createdAt: Date;
  updatedAt: Date;
}

export enum ProductCategory {
  ELECTRONICS = 'electronics',
  CLOTHING = 'clothing',
  FOOD = 'food'
}

// product.dto.ts
export interface CreateProductDTO {
  name: string;
  description: string;
  price: number;
  category: ProductCategory;
  stock: number;
}
```

**Review Checkpoint:**
- [ ] All types exported
- [ ] No 'any' types used
- [ ] JSDoc comments present
- [ ] DTOs match validation requirements

**References:** [Rule 36: Use TypeScript Strictly](../README.md#rule-36-use-typescript-strictly), [Rule 29: Explicit Over Implicit](../README.md#rule-29-explicit-over-implicit)

---

### Step 4: Generate Validation Schemas (5 minutes)

**Objective:** Create input validation with Zod

**Action:**
Generate Zod schemas for all inputs.

**Prompt to Use:**
```markdown
Generate Zod validation schemas for [RESOURCE] in src/features/[resource]/[resource].validator.ts

Fields to validate:
- [field1]: [validation rules]
- [field2]: [validation rules]

Requirements:
- Use Zod 3.x
- Match the specification exactly
- Include custom error messages
- Export schemas for: create, update, query params

Example validations:
- String: .min().max().trim()
- Email: .email()
- Number: .positive().min().max()
- Enum: .enum([values])
- Array: .array().min().max()

Add these constraints: [list specific business rules]
```

**Example Prompt:**
```markdown
Generate Zod schemas for products:

createProductSchema:
- name: 2-200 chars, required, trimmed
- description: 10-2000 chars, required
- price: positive decimal, 2 decimals, max 999999.99
- category: enum ['electronics', 'clothing', 'food']
- stock: non-negative integer, max 1000000

updateProductSchema:
- All fields optional
- Same validation rules when provided

Include custom error messages for each field
```

**Review Checkpoint:**
- [ ] All validation rules implemented
- [ ] Custom error messages added
- [ ] Matches business requirements
- [ ] Export schemas for reuse

**References:** [Rule 4: Include Validation Requirements](../README.md#rule-4-include-validation-requirements), [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs)

---

### Step 5: Generate Repository Layer (5 minutes)

**Objective:** Create database access layer

**Action:**
Generate repository for data operations.

**Prompt to Use:**
```markdown
Generate a repository class for [RESOURCE] in src/features/[resource]/[resource].repository.ts

Operations needed:
- findAll(filters, pagination)
- findById(id)
- create(data)
- update(id, data)
- delete(id)
- [custom queries]

Requirements:
- Use Prisma client
- Return Result<T, Error> types
- Handle database errors gracefully
- Add proper error logging
- Use transactions for multi-step operations
- Include pagination support (limit, offset)

Database: PostgreSQL with Prisma
Error handling: Catch PrismaClientKnownRequestError
Logging: Use console.error with context
```

**Review Checkpoint:**
- [ ] All CRUD operations implemented
- [ ] Parameterized queries used (Prisma)
- [ ] Error handling complete
- [ ] Pagination implemented
- [ ] Transactions used where needed

**References:** [Rule 22: Use Parameterized Queries Only](../README.md#rule-22-use-parameterized-queries-only), [Rule 17: Return Types Over Throwing](../README.md#rule-17-return-types-over-throwing)

---

### Step 6: Generate Service Layer (10 minutes)

**Objective:** Implement business logic

**Action:**
Generate service class with business rules.

**Prompt to Use:**
```markdown
Generate a service class for [RESOURCE] in src/features/[resource]/[resource].service.ts

Business logic:
- [Rule 1: e.g., check for duplicates before create]
- [Rule 2: e.g., validate stock before update]
- [Rule 3: e.g., soft delete instead of hard delete]

Requirements:
- Inject repository via constructor
- Return Result<T, Error> types
- Validate business rules before database operations
- Log all operations
- Handle edge cases: [list specific cases]
- Use transactions for: [operations]

Class structure:
```typescript
export class [Resource]Service {
  constructor(private repository: [Resource]Repository) {}

  async create(data: Create[Resource]DTO): Promise<Result<[Resource], Error>>
  async findById(id: string): Promise<Result<[Resource], Error>>
  async update(id: string, data: Update[Resource]DTO): Promise<Result<[Resource], Error>>
  async delete(id: string): Promise<Result<void, Error>>
  async findAll(filters?, pagination?): Promise<Result<[Resource][], Error>>
}
```
```

**Review Checkpoint:**
- [ ] Business rules implemented correctly
- [ ] No database access in service (use repository)
- [ ] Error handling comprehensive
- [ ] Functions under 50 lines each
- [ ] Dependency injection used

**References:** [Rule 11: Humans Design, AI Implements](../README.md#rule-11-humans-design-ai-implements), [Rule 16: Separation of Concerns](../README.md#rule-16-separation-of-concerns), [Rule 30: Small Functions](../README.md#rule-30-small-functions)

---

### Step 7: Generate Controller Layer (10 minutes)

**Objective:** Create HTTP request handlers

**Action:**
Generate Express controller.

**Prompt to Use:**
```markdown
Generate an Express controller for [RESOURCE] in src/features/[resource]/[resource].controller.ts

Endpoints:
- POST /api/v1/[resource] - Create new
- GET /api/v1/[resource] - List all (with filters/pagination)
- GET /api/v1/[resource]/:id - Get one
- PUT /api/v1/[resource]/:id - Update
- DELETE /api/v1/[resource]/:id - Delete

Requirements:
- Inject service via constructor
- Validate request body with Zod schemas
- Return proper HTTP status codes:
  - 200: Success (GET, PUT, DELETE)
  - 201: Created (POST)
  - 400: Validation error
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not found
  - 500: Server error
- Use consistent response format: { success, data/error, fields? }
- No business logic in controller (delegate to service)
- Add request logging

Authentication: [Required for all/specific endpoints]
Authorization: [Role requirements]
```

**Review Checkpoint:**
- [ ] All endpoints implemented
- [ ] Input validation before service calls
- [ ] Correct HTTP status codes
- [ ] No business logic in controller
- [ ] Authentication/authorization applied
- [ ] Response format consistent

**References:** [Rule 16: Separation of Concerns](../README.md#rule-16-separation-of-concerns), [Rule 5: Define Success and Error Scenarios](../README.md#rule-5-define-success-and-error-scenarios)

---

### Step 8: Add Security Middleware (5 minutes)

**Objective:** Implement authentication and rate limiting

**Action:**
Generate or integrate security middleware.

**Prompt to Use:**
```markdown
Generate security middleware for the [RESOURCE] API:

1. Authentication middleware (src/middleware/auth.middleware.ts):
   - Verify JWT token from Authorization header
   - Decode user info and attach to req.user
   - Return 401 if token missing/invalid

2. Authorization middleware (src/middleware/role.middleware.ts):
   - Check user role against required roles
   - Return 403 if unauthorized

3. Rate limiting (src/middleware/rate-limit.middleware.ts):
   - API endpoints: 100 requests per 15 minutes
   - Auth endpoints: 5 requests per 15 minutes
   - Create endpoints: 20 requests per hour

Requirements:
- Use express-rate-limit for rate limiting
- Use jsonwebtoken for JWT verification
- Add proper error messages
- Log security events (failed auth, rate limit hits)
```

**Review Checkpoint:**
- [ ] JWT verification implemented
- [ ] Rate limiting configured
- [ ] Role-based access control works
- [ ] Security events logged
- [ ] Error messages don't leak sensitive info

**References:** [Rule 24: Implement Rate Limiting](../README.md#rule-24-implement-rate-limiting), [Rule 26: Secure JWT Tokens](../README.md#rule-26-secure-jwt-tokens), [Rule 27: Apply Defense in Depth](../README.md#rule-27-apply-defense-in-depth)

---

### Step 9: Generate Comprehensive Tests (15 minutes)

**Objective:** Create test suite with 90%+ coverage

**Action:**
Generate tests for all layers.

**Prompt to Use:**
```markdown
Generate comprehensive tests for [RESOURCE] API:

Test files needed:
1. src/features/[resource]/__tests__/[resource].repository.test.ts
2. src/features/[resource]/__tests__/[resource].service.test.ts
3. src/features/[resource]/__tests__/[resource].controller.test.ts
4. src/features/[resource]/__tests__/[resource].integration.test.ts

Test scenarios for each:

Repository tests:
- CRUD operations work correctly
- Database errors are handled
- Transactions work
- Pagination works

Service tests:
- Business rules enforced
- Validation works
- Error handling correct
- Edge cases: [list specific cases]

Controller tests:
- Endpoints return correct status codes
- Request validation works
- Response format consistent
- Authentication required
- Authorization enforced

Integration tests:
- Full request/response cycle
- Database operations complete
- Middleware chain works

Requirements:
- Use Jest + ts-jest
- Follow Arrange-Act-Assert pattern
- Mock external dependencies
- Descriptive test names ("should X when Y")
- Achieve 90%+ code coverage
- Test both success and failure paths
```

**Review Checkpoint:**
- [ ] All layers tested
- [ ] Happy path covered
- [ ] Error scenarios tested
- [ ] Edge cases included
- [ ] Mocks used properly
- [ ] Coverage above 90%
- [ ] Tests are independent

**References:** [Rule 37: Test Everything AI Generates](../README.md#rule-37-test-everything-ai-generates), [Rule 39: Arrange-Act-Assert Pattern](../README.md#rule-39-arrange-act-assert-pattern), [Rule 40: Test Edge Cases](../README.md#rule-40-test-edge-cases)

---

### Step 10: Security Review (10 minutes)

**Objective:** Verify security best practices

**Action:**
Manual security review using checklist.

**Security Checklist:**

**Input Validation:**
- [ ] All inputs validated with Zod schemas
- [ ] String lengths limited
- [ ] Numbers have min/max bounds
- [ ] Arrays have size limits
- [ ] Emails validated with proper regex
- [ ] Enums restricted to valid values

**SQL Injection Prevention:**
- [ ] Using Prisma (parameterized queries)
- [ ] No raw SQL with string concatenation
- [ ] User input never directly in queries

**Authentication & Authorization:**
- [ ] JWT verification on protected endpoints
- [ ] Tokens expire within 1 hour
- [ ] Role checks before operations
- [ ] User can only access own resources

**Secrets Management:**
- [ ] No hardcoded secrets
- [ ] All secrets in environment variables
- [ ] .env in .gitignore
- [ ] .env.example provided

**Rate Limiting:**
- [ ] Applied to all public endpoints
- [ ] Stricter limits on auth endpoints
- [ ] Configured per endpoint type

**Error Handling:**
- [ ] No sensitive data in error messages
- [ ] Stack traces not exposed to clients
- [ ] Errors logged with context
- [ ] Generic messages for users

**Prompt for Security Fixes:**
```markdown
Review the generated code for security issues:

Check for:
1. Hardcoded secrets or credentials
2. Missing input validation
3. SQL injection vulnerabilities
4. Missing authentication/authorization
5. Rate limiting gaps
6. Information leakage in errors

Fix any issues found and explain the security risk.
```

**References:** [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets), [Rule 20: AI Cannot Write Security-Critical Code Alone](../README.md#rule-20-ai-cannot-write-security-critical-code-alone), [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs), [Rule 22: Use Parameterized Queries Only](../README.md#rule-22-use-parameterized-queries-only)

---

### Step 11: Code Quality Review (5 minutes)

**Objective:** Ensure code follows quality standards

**Action:**
Run linting and quality checks.

**Commands to Run:**
```bash
# TypeScript compilation
npm run build

# Linting
npm run lint

# Format check
npm run format:check

# Run tests
npm test

# Coverage report
npm run test:coverage
```

**Quality Checklist:**
- [ ] No TypeScript errors
- [ ] No linting errors
- [ ] Code formatted consistently
- [ ] Functions under 50 lines
- [ ] No 'any' types used
- [ ] Meaningful variable names
- [ ] No magic numbers
- [ ] JSDoc on public methods

**Prompt for Quality Fixes:**
```markdown
Refactor the code to improve quality:

Issues to fix:
- Functions over 50 lines: [list functions]
- 'any' types: [list locations]
- Magic numbers: [list occurrences]
- Poor naming: [list examples]

Requirements:
- Extract long functions into smaller ones
- Replace 'any' with specific types
- Create constants for magic numbers
- Use descriptive names
```

**References:** [Rule 29: Explicit Over Implicit](../README.md#rule-29-explicit-over-implicit), [Rule 30: Small Functions](../README.md#rule-30-small-functions), [Rule 31: No Magic Numbers](../README.md#rule-31-no-magic-numbers), [Rule 36: Use TypeScript Strictly](../README.md#rule-36-use-typescript-strictly)

---

### Step 12: Generate API Documentation (5 minutes)

**Objective:** Document API for consumers

**Action:**
Generate OpenAPI/Swagger documentation.

**Prompt to Use:**
```markdown
Generate OpenAPI 3.0 documentation for the [RESOURCE] API:

Include:
- All endpoints with full paths
- Request/response schemas
- Authentication requirements
- Example requests/responses
- Error response formats
- Rate limiting info

Use this format:
```yaml
openapi: 3.0.0
info:
  title: [Resource] API
  version: 1.0.0
paths:
  /api/v1/[resource]:
    post:
      summary: Create [resource]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]'
      responses:
        '201':
          description: Created successfully
        '400':
          description: Validation error
```

Also generate a README.md for the API with:
- Quick start guide
- Authentication instructions
- Example cURL commands
- Common error codes
```

**Review Checkpoint:**
- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Authentication documented
- [ ] Examples provided
- [ ] Error codes explained

**References:** [Rule 50: Document AI Generation](../README.md#rule-50-document-ai-generation)

---

### Step 13: Integration Testing (5 minutes)

**Objective:** Test the complete API flow

**Action:**
Run integration tests and manual testing.

**Test Scenarios:**

1. **Create Resource:**
```bash
curl -X POST http://localhost:3000/api/v1/products \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 29.99,
    "category": "electronics",
    "stock": 100
  }'
```

2. **Get All Resources:**
```bash
curl http://localhost:3000/api/v1/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

3. **Get One Resource:**
```bash
curl http://localhost:3000/api/v1/products/{id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

4. **Update Resource:**
```bash
curl -X PUT http://localhost:3000/api/v1/products/{id} \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price": 24.99}'
```

5. **Delete Resource:**
```bash
curl -X DELETE http://localhost:3000/api/v1/products/{id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Test Checklist:**
- [ ] Create returns 201 with correct data
- [ ] Get all returns 200 with array
- [ ] Get one returns 200 with object
- [ ] Update returns 200 with updated data
- [ ] Delete returns 200
- [ ] Invalid data returns 400
- [ ] Missing auth returns 401
- [ ] Not found returns 404
- [ ] Rate limiting works

---

### Step 14: Performance Testing (Optional, 5 minutes)

**Objective:** Ensure API performs well

**Action:**
Test response times and database efficiency.

**Prompt to Use:**
```markdown
Generate a performance test script for the [RESOURCE] API:

Test scenarios:
1. Single request response time (should be < 200ms)
2. Concurrent requests handling (100 simultaneous)
3. Database query efficiency (no N+1 queries)
4. Large dataset pagination (10,000+ records)

Use: Artillery.io or Apache Bench

Requirements:
- Test all endpoints
- Measure p50, p95, p99 latency
- Check for memory leaks
- Verify connection pool sizing
```

**Performance Checklist:**
- [ ] Response time < 200ms for simple queries
- [ ] No N+1 query problems
- [ ] Pagination works for large datasets
- [ ] Connection pooling configured
- [ ] Indexes on frequently queried fields

---

### Step 15: Deployment Preparation (5 minutes)

**Objective:** Prepare for production deployment

**Action:**
Set up deployment configuration.

**Deployment Checklist:**

**Environment Variables:**
```bash
# .env.production (template)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
JWT_SECRET=your-secret-key-min-32-chars
JWT_EXPIRES_IN=1h
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
NODE_ENV=production
PORT=3000
```

**Build Process:**
```bash
# Build TypeScript
npm run build

# Run migrations
npx prisma migrate deploy

# Start production
npm start
```

**Health Check Endpoint:**
```markdown
Generate a health check endpoint:

GET /health
Returns:
{
  "status": "ok",
  "timestamp": "2025-10-23T10:00:00Z",
  "database": "connected",
  "uptime": 3600
}

Check:
- Database connection
- Required env vars present
- Memory usage acceptable
```

**Deployment Checklist:**
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Health check endpoint works
- [ ] Logging configured
- [ ] Error monitoring set up (Sentry, etc.)
- [ ] HTTPS enforced
- [ ] CORS configured properly
- [ ] Rate limiting in place

**References:** [Rule 18: Configuration as Code](../README.md#rule-18-configuration-as-code)

---

## Testing Procedures

### Automated Testing
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- product.service.test.ts

# Run in watch mode
npm test -- --watch
```

### Manual Testing Checklist
- [ ] Create operation with valid data
- [ ] Create with invalid data (validation)
- [ ] Create duplicate (business rule)
- [ ] Get all with pagination
- [ ] Get all with filters
- [ ] Get one existing resource
- [ ] Get one non-existent resource
- [ ] Update with valid data
- [ ] Update with invalid data
- [ ] Delete existing resource
- [ ] Delete non-existent resource
- [ ] Test without authentication
- [ ] Test with wrong role
- [ ] Test rate limiting

---

## Example Outputs

### Example Request/Response

**Create Product Request:**
```json
POST /api/v1/products
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with 2.4GHz connectivity",
  "price": 29.99,
  "category": "electronics",
  "stock": 150
}
```

**Success Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with 2.4GHz connectivity",
    "price": 29.99,
    "category": "electronics",
    "stock": 150,
    "createdAt": "2025-10-23T10:30:00Z",
    "updatedAt": "2025-10-23T10:30:00Z"
  }
}
```

**Validation Error (400):**
```json
{
  "success": false,
  "error": "Validation failed",
  "fields": {
    "name": ["String must contain at least 2 character(s)"],
    "price": ["Number must be greater than 0"]
  }
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: TypeScript Errors
**Symptom:** `Property 'X' does not exist on type 'Y'`

**Solution:**
```markdown
Prompt AI to fix:
"Fix TypeScript errors in [file]:
- Add missing properties to interface
- Ensure types are properly imported
- Fix return type mismatches
Use strict TypeScript with no 'any' types"
```

#### Issue 2: Test Failures
**Symptom:** Tests fail with "Cannot find module" or mock errors

**Solution:**
```bash
# Check Jest configuration
npm install -D ts-jest @types/jest

# Update jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts']
};
```

#### Issue 3: Database Connection Fails
**Symptom:** `Can't reach database server`

**Solution:**
1. Check DATABASE_URL in .env
2. Verify database is running
3. Run migrations: `npx prisma migrate dev`
4. Generate Prisma client: `npx prisma generate`

#### Issue 4: Validation Not Working
**Symptom:** Invalid data passes through

**Solution:**
```markdown
Prompt AI:
"Review validation in [resource].validator.ts:
- Ensure all fields have proper constraints
- Check that controller uses safeParse()
- Verify error messages are returned
- Test with invalid data examples"
```

#### Issue 5: Rate Limiting Too Strict
**Symptom:** Users getting 429 Too Many Requests

**Solution:**
```typescript
// Adjust rate limit settings
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200, // Increase from 100
  message: 'Too many requests from this IP'
});
```

#### Issue 6: Authentication Fails
**Symptom:** Always returns 401 Unauthorized

**Solution:**
1. Check JWT_SECRET is set in .env
2. Verify token format: `Bearer <token>`
3. Check token expiration
4. Validate token signature

**Debug Prompt:**
```markdown
"Debug authentication middleware:
- Log the token being received
- Check token verification logic
- Verify JWT_SECRET matches
- Add error logging with details"
```

#### Issue 7: Slow Queries
**Symptom:** API response time > 1 second

**Solution:**
```markdown
"Optimize database queries:
- Add indexes on: [frequently queried fields]
- Use select to limit returned fields
- Implement pagination
- Use database query logging to find slow queries"
```

#### Issue 8: AI Generated Incorrect Logic
**Symptom:** Business rules not working as expected

**Solution:**
1. Review the original prompt
2. Check if requirements were clear
3. Regenerate with more specific prompt
4. Add test cases for the specific scenario
5. Manually fix and add comments explaining logic

---

## Completion Checklist

### Before Merging to Main
- [ ] All tests passing (90%+ coverage)
- [ ] No TypeScript errors
- [ ] No linting errors
- [ ] Security review completed
- [ ] Code quality review passed
- [ ] API documentation generated
- [ ] Integration tests successful
- [ ] Performance acceptable
- [ ] Environment variables documented
- [ ] README updated

### Code Review Checklist
- [ ] No hardcoded secrets
- [ ] Input validation on all endpoints
- [ ] Parameterized queries used
- [ ] Authentication/authorization applied
- [ ] Rate limiting configured
- [ ] Error handling complete
- [ ] Functions under 50 lines
- [ ] No 'any' types
- [ ] JSDoc comments present
- [ ] Business rules correct

### Deployment Checklist
- [ ] Environment variables set
- [ ] Database migrations run
- [ ] Health check working
- [ ] Logging configured
- [ ] Error monitoring active
- [ ] HTTPS enforced
- [ ] CORS configured
- [ ] Backups configured

---

## Time Breakdown

**Setup (5 min):**
- Step 1: API Specification - 5 min

**Development (35 min):**
- Step 2: Database Schema - 5 min
- Step 3: TypeScript Types - 5 min
- Step 4: Validation Schemas - 5 min
- Step 5: Repository Layer - 5 min
- Step 6: Service Layer - 10 min
- Step 7: Controller Layer - 10 min
- Step 8: Security Middleware - 5 min

**Testing & Review (20 min):**
- Step 9: Generate Tests - 15 min
- Step 10: Security Review - 10 min
- Step 11: Code Quality - 5 min

**Documentation & Deployment (10 min):**
- Step 12: API Documentation - 5 min
- Step 13: Integration Testing - 5 min
- Step 15: Deployment Prep - 5 min

**Total: 30-60 minutes** (depending on complexity)

---

## Next Steps

After completing this workflow:

1. **Deploy to Staging:**
   - Test with real data
   - Monitor for errors
   - Get feedback from team

2. **Production Deployment:**
   - Follow deployment checklist
   - Monitor closely for first 24 hours
   - Have rollback plan ready

3. **Ongoing Maintenance:**
   - Add new endpoints as needed
   - Monitor performance metrics
   - Update documentation
   - Refine based on usage patterns

---

## Related Resources

**Templates:**
- [Backend Starter Template](../prompts/templates/backend-starter.md) - Use for detailed prompts
- [Frontend Component Template](../prompts/templates/frontend-component.md) - For API client

**Checklists:**
- [Daily Checklist](../DAILY_CHECKLIST.md) - Complete review checklist
- [Rules One Page](../RULES_ONE_PAGE.md) - Quick reference

**Rules to Review:**
- [Rule 2: Provide Context](../README.md#rule-2-always-provide-context-before-task)
- [Rule 7: Request Tests Upfront](../README.md#rule-7-request-tests-upfront)
- [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs)
- [Rule 37: Test Everything](../README.md#rule-37-test-everything-ai-generates)
- [Rule 47: Human Always Reviews](../README.md#rule-47-human-always-reviews-first)

---

**Last Updated:** 2025-10-23
**Version:** 1.0
**Estimated Time:** 30-60 minutes
