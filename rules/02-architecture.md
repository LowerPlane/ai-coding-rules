# Architecture & Design Rules (Rules 11-18)

Rules for designing maintainable, scalable systems with AI assistance.

---

## Rule 11: Humans Design, AI Implements

**❌ Bad:** Ask AI to design entire system architecture

**✅ Good:** Human creates interfaces/types, AI implements them

### How to Follow

- Human defines domain models and interfaces first
- Human creates API contracts and specifications
- Human determines system boundaries and dependencies
- AI generates implementations based on human design
- Human reviews and refines AI-generated code

### Example

**❌ Bad Approach:**

```markdown
Prompt: "Design and build a complete e-commerce system"
```

This gives AI too much architectural control.

**✅ Good Approach:**

```markdown
## Context
I've designed the architecture. Here are the interfaces:

```typescript
// Human-designed interfaces
interface ProductRepository {
  findById(id: string): Promise<Result<Product, Error>>;
  findAll(filters: ProductFilters): Promise<Result<Product[], Error>>;
  create(data: CreateProductDTO): Promise<Result<Product, Error>>;
  update(id: string, data: UpdateProductDTO): Promise<Result<Product, Error>>;
  delete(id: string): Promise<Result<void, Error>>;
}

interface ProductService {
  getProduct(id: string): Promise<Result<ProductDTO, Error>>;
  listProducts(filters: ProductFilters): Promise<Result<ProductDTO[], Error>>;
  createProduct(data: CreateProductDTO): Promise<Result<ProductDTO, Error>>;
}
```

## Task
Implement ProductRepositoryImpl and ProductServiceImpl following these interfaces.
Use Prisma for database access. Return Result<T, Error> for all operations.
```

### Implementation Guidance

**Human Responsibilities:**
- System architecture decisions
- Data model design
- Interface contracts
- Security requirements
- Performance requirements
- Integration points

**AI Responsibilities:**
- Implementation of defined interfaces
- Boilerplate code generation
- Test generation
- Documentation
- Utility functions

**Review Points:**
- Does implementation match interface contract?
- Are business rules correctly implemented?
- Is error handling comprehensive?
- Are edge cases covered?

---

## Rule 12: One Responsibility Per File

**❌ Bad:** 3000-line file doing everything

**✅ Good:** Small, focused files (< 300 lines each)

### How to Follow

- Each file has a single, clear purpose
- Split by concern: controller, service, repository, types
- Separate validation from business logic
- Keep routes separate from handlers
- Extract utilities to dedicated files
- Maximum 300 lines per file (preferably < 200)

### Example

**❌ Bad Structure:**

```typescript
// user.ts (3000 lines - EVERYTHING in one file)
import express from 'express';
import bcrypt from 'bcrypt';
import { z } from 'zod';

// Validation schemas
const userSchema = z.object({ ... });

// Types
interface User { ... }

// Database queries
class UserRepository { ... }

// Business logic
class UserService { ... }

// HTTP handlers
class UserController { ... }

// Routes
const router = express.Router();
router.post('/users', ...);

// Export everything
export { router, UserService, UserRepository, User };
```

**✅ Good Structure:**

```typescript
// user.types.ts (50 lines)
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateUserDTO {
  email: string;
  password: string;
  name: string;
}

export interface UpdateUserDTO {
  name?: string;
  email?: string;
}

export type UserDTO = Omit<User, 'password'>;

// user.validator.ts (40 lines)
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain uppercase letter")
    .regex(/[0-9]/, "Must contain number")
    .regex(/[^A-Za-z0-9]/, "Must contain special character"),
  name: z.string().min(2).max(100).trim(),
});

export const updateUserSchema = z.object({
  email: z.string().email().max(255).optional(),
  name: z.string().min(2).max(100).trim().optional(),
});

// user.repository.ts (120 lines)
import { PrismaClient } from '@prisma/client';
import type { User, CreateUserDTO, UpdateUserDTO } from './user.types';
import type { Result } from '@/shared/types/result';

export class UserRepository {
  constructor(private db: PrismaClient) {}

  async findById(id: string): Promise<Result<User | null, Error>> {
    try {
      const user = await this.db.user.findUnique({ where: { id } });
      return { success: true, data: user };
    } catch (error) {
      return { success: false, error: error as Error };
    }
  }

  async findByEmail(email: string): Promise<Result<User | null, Error>> {
    try {
      const user = await this.db.user.findUnique({
        where: { email: email.toLowerCase() }
      });
      return { success: true, data: user };
    } catch (error) {
      return { success: false, error: error as Error };
    }
  }

  async create(data: CreateUserDTO): Promise<Result<User, Error>> {
    try {
      const user = await this.db.user.create({ data });
      return { success: true, data: user };
    } catch (error) {
      return { success: false, error: error as Error };
    }
  }

  // ... other methods
}

// user.service.ts (150 lines)
import bcrypt from 'bcrypt';
import type { UserRepository } from './user.repository';
import type { CreateUserDTO, UpdateUserDTO, UserDTO } from './user.types';
import type { Result } from '@/shared/types/result';

export class UserService {
  constructor(
    private repository: UserRepository,
    private logger: Logger
  ) {}

  async createUser(data: CreateUserDTO): Promise<Result<UserDTO, Error>> {
    // Check if user exists
    const existingResult = await this.repository.findByEmail(data.email);
    if (!existingResult.success) {
      return existingResult;
    }
    if (existingResult.data) {
      return {
        success: false,
        error: new Error('Email already exists')
      };
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 12);

    // Create user
    const createResult = await this.repository.create({
      ...data,
      password: hashedPassword,
    });

    if (!createResult.success) {
      this.logger.error('Failed to create user', { error: createResult.error });
      return createResult;
    }

    // Return without password
    const { password, ...userDTO } = createResult.data;
    return { success: true, data: userDTO };
  }

  // ... other methods
}

// user.controller.ts (100 lines)
import type { Request, Response } from 'express';
import type { UserService } from './user.service';
import { createUserSchema } from './user.validator';

export class UserController {
  constructor(private service: UserService) {}

  async create(req: Request, res: Response): Promise<void> {
    // Validate input
    const validation = createUserSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({
        success: false,
        error: 'Validation failed',
        fields: validation.error.flatten().fieldErrors,
      });
      return;
    }

    // Create user
    const result = await this.service.createUser(validation.data);

    if (!result.success) {
      const statusCode = result.error.message === 'Email already exists'
        ? 409
        : 500;
      res.status(statusCode).json({
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

  // ... other methods
}

// user.routes.ts (30 lines)
import { Router } from 'express';
import { UserController } from './user.controller';
import { authMiddleware } from '@/shared/middleware/auth';
import { rateLimiter } from '@/shared/middleware/rate-limit';

export function createUserRoutes(controller: UserController): Router {
  const router = Router();

  router.post(
    '/users',
    rateLimiter,
    controller.create.bind(controller)
  );

  router.get(
    '/users/:id',
    authMiddleware,
    controller.getById.bind(controller)
  );

  // ... other routes

  return router;
}
```

### Implementation Guidance

**When to Split a File:**
- File exceeds 300 lines
- File has multiple distinct responsibilities
- Difficult to find specific code
- Multiple developers need to edit simultaneously

**File Organization Patterns:**
- `*.types.ts` - Type definitions and interfaces
- `*.validator.ts` - Validation schemas
- `*.repository.ts` - Data access layer
- `*.service.ts` - Business logic layer
- `*.controller.ts` - HTTP handling layer
- `*.routes.ts` - Route definitions
- `*.test.ts` - Tests

**See Also:**
- [Rule 45: Group by Feature, Not Type](#) for directory structure
- [Rule 16: Separation of Concerns](#rule-16-separation-of-concerns) for layer boundaries

---

## Rule 13: Interface-First Development

**❌ Bad:** Let AI decide interfaces

**✅ Good:** Define interfaces first, then implement

### How to Follow

- Write interface contracts before implementation
- Use TypeScript interfaces for all public APIs
- Define expected inputs and outputs explicitly
- Document interface contracts with JSDoc
- Implement interfaces with concrete classes
- Use interfaces for dependency injection

### Example

**❌ Bad Approach:**

```typescript
// Prompt: "Create a payment service"
// AI decides everything, inconsistent patterns

class PaymentService {
  async processPayment(amount: number, token: string) {
    // Returns different things in different methods
    // Inconsistent error handling
    // No clear contract
  }
}
```

**✅ Good Approach:**

```typescript
// Step 1: Human defines interfaces
// payment.types.ts

export interface PaymentMethod {
  id: string;
  type: 'card' | 'bank_transfer' | 'wallet';
  last4?: string;
  isDefault: boolean;
}

export interface ChargeRequest {
  amount: number;
  currency: string;
  paymentMethodId: string;
  description?: string;
  metadata?: Record<string, string>;
}

export interface ChargeResult {
  chargeId: string;
  status: 'succeeded' | 'pending' | 'failed';
  amount: number;
  currency: string;
  createdAt: Date;
}

export interface RefundRequest {
  chargeId: string;
  amount?: number; // Partial refund if specified
  reason?: string;
}

export interface RefundResult {
  refundId: string;
  chargeId: string;
  amount: number;
  status: 'succeeded' | 'pending' | 'failed';
  createdAt: Date;
}

// payment.service.interface.ts

import type { Result } from '@/shared/types/result';
import type {
  PaymentMethod,
  ChargeRequest,
  ChargeResult,
  RefundRequest,
  RefundResult
} from './payment.types';

/**
 * Payment service interface for processing payments and refunds
 */
export interface IPaymentService {
  /**
   * Process a payment charge
   * @param request - Charge details
   * @returns Result with charge details or error
   */
  charge(request: ChargeRequest): Promise<Result<ChargeResult, Error>>;

  /**
   * Refund a previous charge
   * @param request - Refund details
   * @returns Result with refund details or error
   */
  refund(request: RefundRequest): Promise<Result<RefundResult, Error>>;

  /**
   * Get payment methods for a customer
   * @param customerId - Customer identifier
   * @returns Result with payment methods or error
   */
  getPaymentMethods(
    customerId: string
  ): Promise<Result<PaymentMethod[], Error>>;

  /**
   * Add a payment method for a customer
   * @param customerId - Customer identifier
   * @param token - Payment method token from provider
   * @returns Result with payment method or error
   */
  addPaymentMethod(
    customerId: string,
    token: string
  ): Promise<Result<PaymentMethod, Error>>;
}

// Step 2: Prompt AI to implement
```

**Prompt to AI:**

```markdown
## Context
- Stack: Node.js + TypeScript + Stripe
- Existing: IPaymentService interface (see above)
- Conventions: Dependency injection, Result<T,E> return types

## Task
Implement PaymentServiceImpl class that implements IPaymentService.

Requirements:
- Use Stripe SDK (already in package.json)
- Inject Stripe client via constructor
- All amounts in cents (smallest currency unit)
- Log all operations with injected logger
- Comprehensive error handling
- Convert Stripe errors to Result<T, Error>

File: src/features/payments/payment.service.impl.ts
```

**AI Implementation:**

```typescript
// payment.service.impl.ts

import Stripe from 'stripe';
import type { Logger } from '@/shared/types/logger';
import type { Result } from '@/shared/types/result';
import type { IPaymentService } from './payment.service.interface';
import type {
  PaymentMethod,
  ChargeRequest,
  ChargeResult,
  RefundRequest,
  RefundResult,
} from './payment.types';

export class PaymentServiceImpl implements IPaymentService {
  constructor(
    private stripe: Stripe,
    private logger: Logger
  ) {}

  async charge(request: ChargeRequest): Promise<Result<ChargeResult, Error>> {
    try {
      this.logger.info('Processing charge', {
        amount: request.amount,
        currency: request.currency
      });

      const charge = await this.stripe.charges.create({
        amount: request.amount,
        currency: request.currency,
        payment_method: request.paymentMethodId,
        description: request.description,
        metadata: request.metadata,
      });

      const result: ChargeResult = {
        chargeId: charge.id,
        status: charge.status as 'succeeded' | 'pending' | 'failed',
        amount: charge.amount,
        currency: charge.currency,
        createdAt: new Date(charge.created * 1000),
      };

      this.logger.info('Charge successful', { chargeId: result.chargeId });
      return { success: true, data: result };
    } catch (error) {
      this.logger.error('Charge failed', { error, request });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async refund(request: RefundRequest): Promise<Result<RefundResult, Error>> {
    try {
      this.logger.info('Processing refund', { chargeId: request.chargeId });

      const refund = await this.stripe.refunds.create({
        charge: request.chargeId,
        amount: request.amount,
        reason: request.reason as Stripe.RefundCreateParams.Reason,
      });

      const result: RefundResult = {
        refundId: refund.id,
        chargeId: refund.charge as string,
        amount: refund.amount,
        status: refund.status as 'succeeded' | 'pending' | 'failed',
        createdAt: new Date(refund.created * 1000),
      };

      this.logger.info('Refund successful', { refundId: result.refundId });
      return { success: true, data: result };
    } catch (error) {
      this.logger.error('Refund failed', { error, request });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async getPaymentMethods(
    customerId: string
  ): Promise<Result<PaymentMethod[], Error>> {
    try {
      const paymentMethods = await this.stripe.paymentMethods.list({
        customer: customerId,
        type: 'card',
      });

      const methods: PaymentMethod[] = paymentMethods.data.map(pm => ({
        id: pm.id,
        type: 'card',
        last4: pm.card?.last4,
        isDefault: false, // Determine from customer default_payment_method
      }));

      return { success: true, data: methods };
    } catch (error) {
      this.logger.error('Failed to get payment methods', { error, customerId });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async addPaymentMethod(
    customerId: string,
    token: string
  ): Promise<Result<PaymentMethod, Error>> {
    try {
      const paymentMethod = await this.stripe.paymentMethods.attach(token, {
        customer: customerId,
      });

      const method: PaymentMethod = {
        id: paymentMethod.id,
        type: 'card',
        last4: paymentMethod.card?.last4,
        isDefault: false,
      };

      return { success: true, data: method };
    } catch (error) {
      this.logger.error('Failed to add payment method', { error, customerId });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }
}
```

### Implementation Guidance

**Benefits of Interface-First:**
- Consistent API contracts across codebase
- Easy to swap implementations (testing, different providers)
- Clear boundaries between layers
- Self-documenting code
- Easier to reason about system design

**When to Use:**
- All service layer code
- Repository/data access layer
- External integrations
- Complex business logic
- Code that will be tested with mocks

**Testing with Interfaces:**

```typescript
// payment.service.test.ts

describe('PaymentServiceImpl', () => {
  let service: IPaymentService; // Use interface, not implementation
  let mockStripe: jest.Mocked<Stripe>;
  let mockLogger: jest.Mocked<Logger>;

  beforeEach(() => {
    mockStripe = createMockStripe();
    mockLogger = createMockLogger();
    service = new PaymentServiceImpl(mockStripe, mockLogger);
  });

  it('should charge payment successfully', async () => {
    const request: ChargeRequest = {
      amount: 5000,
      currency: 'usd',
      paymentMethodId: 'pm_123',
    };

    const result = await service.charge(request);

    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.amount).toBe(5000);
      expect(result.data.status).toBe('succeeded');
    }
  });
});
```

**See Also:**
- [Rule 14: Dependency Injection](#rule-14-dependency-injection-over-hardcoding)
- [Rule 11: Humans Design, AI Implements](#rule-11-humans-design-ai-implements)

---

## Rule 14: Dependency Injection Over Hardcoding

**❌ Bad:** `const db = new Database()` inside service

**✅ Good:** `constructor(private db: Database)`

### How to Follow

- Pass all dependencies via constructor
- Never instantiate dependencies inside classes
- Use interfaces for dependencies (not concrete classes)
- Make all dependencies explicit and visible
- Use dependency injection container for complex apps
- Avoid global singletons

### Example

**❌ Bad (Hardcoded Dependencies):**

```typescript
// user.service.ts - BAD
import { PrismaClient } from '@prisma/client';
import { EmailService } from '../email/email.service';
import { Logger } from '../logger';

export class UserService {
  // Hardcoded dependencies - can't test, can't configure
  private db = new PrismaClient();
  private emailService = new EmailService();
  private logger = new Logger('UserService');

  async createUser(data: CreateUserDTO): Promise<User> {
    // Tightly coupled to specific implementations
    const user = await this.db.user.create({ data });
    await this.emailService.sendWelcome(user.email);
    this.logger.info('User created', { userId: user.id });
    return user;
  }
}

// Hard to test, hard to change implementations
```

**✅ Good (Dependency Injection):**

```typescript
// user.service.ts - GOOD
import type { Database } from '@/shared/types/database';
import type { IEmailService } from '@/features/email/email.service.interface';
import type { Logger } from '@/shared/types/logger';
import type { CreateUserDTO, User } from './user.types';
import type { Result } from '@/shared/types/result';

export class UserService {
  // Dependencies injected via constructor
  constructor(
    private db: Database,
    private emailService: IEmailService,
    private logger: Logger
  ) {}

  async createUser(data: CreateUserDTO): Promise<Result<User, Error>> {
    try {
      // Use injected dependencies
      const user = await this.db.user.create({ data });

      // Email sending failure shouldn't fail user creation
      const emailResult = await this.emailService.sendWelcome(user.email);
      if (!emailResult.success) {
        this.logger.warn('Welcome email failed', {
          userId: user.id,
          error: emailResult.error
        });
      }

      this.logger.info('User created', { userId: user.id });
      return { success: true, data: user };
    } catch (error) {
      this.logger.error('User creation failed', { error, data });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }
}

// Easy to test with mocks
// Easy to swap implementations
// Clear what dependencies are needed
```

**Testing with Dependency Injection:**

```typescript
// user.service.test.ts

describe('UserService', () => {
  let service: UserService;
  let mockDb: jest.Mocked<Database>;
  let mockEmailService: jest.Mocked<IEmailService>;
  let mockLogger: jest.Mocked<Logger>;

  beforeEach(() => {
    // Create mocks
    mockDb = {
      user: {
        create: jest.fn(),
        findUnique: jest.fn(),
      },
    } as any;

    mockEmailService = {
      sendWelcome: jest.fn(),
    } as any;

    mockLogger = {
      info: jest.fn(),
      warn: jest.fn(),
      error: jest.fn(),
    } as any;

    // Inject mocks
    service = new UserService(mockDb, mockEmailService, mockLogger);
  });

  it('should create user successfully', async () => {
    const userData: CreateUserDTO = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'hashedpassword',
    };

    const expectedUser: User = {
      id: 'user-123',
      ...userData,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    // Setup mocks
    mockDb.user.create.mockResolvedValue(expectedUser);
    mockEmailService.sendWelcome.mockResolvedValue({ success: true, data: undefined });

    // Execute
    const result = await service.createUser(userData);

    // Assert
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data).toEqual(expectedUser);
    }
    expect(mockDb.user.create).toHaveBeenCalledWith({ data: userData });
    expect(mockEmailService.sendWelcome).toHaveBeenCalledWith(userData.email);
    expect(mockLogger.info).toHaveBeenCalled();
  });

  it('should handle email failure gracefully', async () => {
    const userData: CreateUserDTO = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'hashedpassword',
    };

    mockDb.user.create.mockResolvedValue({ id: 'user-123', ...userData } as User);
    mockEmailService.sendWelcome.mockResolvedValue({
      success: false,
      error: new Error('Email service down')
    });

    const result = await service.createUser(userData);

    // User creation should still succeed
    expect(result.success).toBe(true);
    // Should log warning about email failure
    expect(mockLogger.warn).toHaveBeenCalledWith(
      'Welcome email failed',
      expect.any(Object)
    );
  });
});
```

**Dependency Injection Container (Advanced):**

```typescript
// container.ts - For complex applications

import { PrismaClient } from '@prisma/client';
import { UserService } from './features/users/user.service';
import { UserRepository } from './features/users/user.repository';
import { EmailServiceImpl } from './features/email/email.service.impl';
import { createLogger } from './shared/logger';

export class Container {
  private static instance: Container;
  private dependencies: Map<string, any> = new Map();

  private constructor() {
    this.registerDependencies();
  }

  static getInstance(): Container {
    if (!Container.instance) {
      Container.instance = new Container();
    }
    return Container.instance;
  }

  private registerDependencies(): void {
    // Register singletons
    const db = new PrismaClient();
    this.dependencies.set('database', db);
    this.dependencies.set('logger', createLogger());

    // Register services
    this.dependencies.set('emailService', new EmailServiceImpl(
      this.get('logger')
    ));

    this.dependencies.set('userRepository', new UserRepository(
      this.get('database')
    ));

    this.dependencies.set('userService', new UserService(
      this.get('database'),
      this.get('emailService'),
      this.get('logger')
    ));
  }

  get<T>(key: string): T {
    const dependency = this.dependencies.get(key);
    if (!dependency) {
      throw new Error(`Dependency not found: ${key}`);
    }
    return dependency as T;
  }
}

// Usage
const container = Container.getInstance();
const userService = container.get<UserService>('userService');
```

### Implementation Guidance

**What to Inject:**
- Database connections
- External service clients (email, SMS, payment)
- Logging services
- Configuration objects
- Cache clients (Redis)
- Other business services

**What NOT to Inject:**
- Simple utilities (pure functions)
- Constants
- Type definitions
- Validation schemas (unless dynamic)

**Prompt Template for AI:**

```markdown
## Context
- All services use dependency injection
- Dependencies passed via constructor
- Use interfaces for dependencies
- No hardcoded instantiation inside classes

## Task
Create OrderService with these dependencies:
- database: Database (interface from @/shared/types/database)
- paymentService: IPaymentService
- inventoryService: IInventoryService
- logger: Logger

Constructor should accept all dependencies.
All dependencies should be readonly private properties.
```

**See Also:**
- [Rule 13: Interface-First Development](#rule-13-interface-first-development)
- [Rule 15: Stateless Services](#rule-15-stateless-services)

---

## Rule 15: Stateless Services

**❌ Bad:** In-memory caches or state in services

**✅ Good:** External state management (Redis, database)

### How to Follow

- No module-level variables for mutable state
- No class-level state that changes over time
- Use external storage for caching (Redis, database)
- Pass all required state as function parameters
- Design services to be horizontally scalable
- Each request should be independent

### Example

**❌ Bad (Stateful Service):**

```typescript
// session.service.ts - BAD
export class SessionService {
  // State stored in memory - breaks in multi-instance deployments
  private activeSessions: Map<string, Session> = new Map();
  private loginAttempts: Map<string, number> = new Map();

  async createSession(userId: string): Promise<Session> {
    const session: Session = {
      id: generateId(),
      userId,
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 3600000),
    };

    // State stored in memory - lost on restart
    this.activeSessions.set(session.id, session);
    return session;
  }

  async getSession(sessionId: string): Promise<Session | null> {
    // Only works on the same instance that created it
    return this.activeSessions.get(sessionId) || null;
  }

  async incrementLoginAttempts(email: string): Promise<number> {
    const attempts = (this.loginAttempts.get(email) || 0) + 1;
    this.loginAttempts.set(email, attempts);

    // Lost on restart, doesn't work across instances
    if (attempts >= 5) {
      throw new Error('Too many login attempts');
    }

    return attempts;
  }

  // Cleanup never happens reliably
  async cleanup(): Promise<void> {
    const now = Date.now();
    for (const [id, session] of this.activeSessions.entries()) {
      if (session.expiresAt.getTime() < now) {
        this.activeSessions.delete(id);
      }
    }
  }
}

// Problems:
// - Can't scale horizontally (sessions on different instances)
// - State lost on restart
// - No persistence
// - Memory leaks if cleanup fails
```

**✅ Good (Stateless Service):**

```typescript
// session.service.ts - GOOD
import type { RedisClient } from '@/shared/types/redis';
import type { Logger } from '@/shared/types/logger';
import type { Session } from './session.types';
import type { Result } from '@/shared/types/result';

export class SessionService {
  // Constants are fine
  private readonly SESSION_TTL = 3600; // 1 hour in seconds
  private readonly MAX_LOGIN_ATTEMPTS = 5;
  private readonly LOGIN_ATTEMPTS_TTL = 900; // 15 minutes

  // Dependencies injected, no mutable state
  constructor(
    private redis: RedisClient,
    private logger: Logger
  ) {}

  async createSession(userId: string): Promise<Result<Session, Error>> {
    try {
      const session: Session = {
        id: generateId(),
        userId,
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + this.SESSION_TTL * 1000),
      };

      // Store in Redis with TTL - works across instances
      await this.redis.setex(
        `session:${session.id}`,
        this.SESSION_TTL,
        JSON.stringify(session)
      );

      this.logger.info('Session created', { sessionId: session.id, userId });
      return { success: true, data: session };
    } catch (error) {
      this.logger.error('Session creation failed', { error, userId });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async getSession(sessionId: string): Promise<Result<Session | null, Error>> {
    try {
      // Read from Redis - works from any instance
      const data = await this.redis.get(`session:${sessionId}`);

      if (!data) {
        return { success: true, data: null };
      }

      const session: Session = JSON.parse(data);

      // Check expiration
      if (new Date(session.expiresAt) < new Date()) {
        await this.redis.del(`session:${sessionId}`);
        return { success: true, data: null };
      }

      return { success: true, data: session };
    } catch (error) {
      this.logger.error('Session retrieval failed', { error, sessionId });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async deleteSession(sessionId: string): Promise<Result<void, Error>> {
    try {
      await this.redis.del(`session:${sessionId}`);
      this.logger.info('Session deleted', { sessionId });
      return { success: true, data: undefined };
    } catch (error) {
      this.logger.error('Session deletion failed', { error, sessionId });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async incrementLoginAttempts(email: string): Promise<Result<number, Error>> {
    try {
      const key = `login_attempts:${email.toLowerCase()}`;

      // Increment in Redis with TTL
      const attempts = await this.redis.incr(key);

      // Set TTL on first attempt
      if (attempts === 1) {
        await this.redis.expire(key, this.LOGIN_ATTEMPTS_TTL);
      }

      this.logger.info('Login attempt recorded', { email, attempts });
      return { success: true, data: attempts };
    } catch (error) {
      this.logger.error('Failed to record login attempt', { error, email });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async isAccountLocked(email: string): Promise<Result<boolean, Error>> {
    try {
      const key = `login_attempts:${email.toLowerCase()}`;
      const attempts = await this.redis.get(key);

      const attemptsCount = attempts ? parseInt(attempts, 10) : 0;
      const isLocked = attemptsCount >= this.MAX_LOGIN_ATTEMPTS;

      return { success: true, data: isLocked };
    } catch (error) {
      this.logger.error('Failed to check account lock', { error, email });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }

  async resetLoginAttempts(email: string): Promise<Result<void, Error>> {
    try {
      const key = `login_attempts:${email.toLowerCase()}`;
      await this.redis.del(key);
      this.logger.info('Login attempts reset', { email });
      return { success: true, data: undefined };
    } catch (error) {
      this.logger.error('Failed to reset login attempts', { error, email });
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Unknown error')
      };
    }
  }
}

// Benefits:
// - Scales horizontally (multiple instances share Redis)
// - Survives restarts (data persisted in Redis)
// - TTL handled automatically by Redis
// - No memory leaks
// - Consistent across all instances
```

**Configuration as Stateless:**

```typescript
// config.ts
import { z } from 'zod';

// Configuration is immutable state - loaded once at startup
const configSchema = z.object({
  database: z.object({
    url: z.string().url(),
    maxConnections: z.number().positive(),
  }),
  redis: z.object({
    url: z.string().url(),
    ttl: z.number().positive(),
  }),
  session: z.object({
    ttl: z.number().positive().default(3600),
    maxLoginAttempts: z.number().positive().default(5),
  }),
});

export type Config = z.infer<typeof configSchema>;

export function loadConfig(): Config {
  const config = configSchema.parse({
    database: {
      url: process.env.DATABASE_URL,
      maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '10', 10),
    },
    redis: {
      url: process.env.REDIS_URL,
      ttl: parseInt(process.env.REDIS_TTL || '3600', 10),
    },
    session: {
      ttl: parseInt(process.env.SESSION_TTL || '3600', 10),
      maxLoginAttempts: parseInt(process.env.MAX_LOGIN_ATTEMPTS || '5', 10),
    },
  });

  return config;
}

// Load once at startup - immutable
export const config = loadConfig();
```

### Implementation Guidance

**Acceptable "State" in Services:**
- Injected dependencies (readonly)
- Configuration constants (readonly)
- Immutable lookup tables
- Static utility methods

**Must Use External Storage:**
- User sessions
- Rate limiting counters
- Feature flags
- Temporary data/caching
- Request deduplication
- Distributed locks

**Stateless Design Benefits:**
- Horizontal scaling (add more instances)
- Zero-downtime deployments
- Easy testing (no hidden state)
- Predictable behavior
- Fault tolerance

**Prompt Template for AI:**

```markdown
## Context
- All services must be stateless
- Use Redis for temporary state (sessions, rate limiting, caching)
- Use database for persistent state
- No module-level or class-level mutable variables
- Design for horizontal scaling

## Task
Create CacheService for product data:
- Use Redis for storage (inject RedisClient)
- TTL of 5 minutes for product cache
- Methods: get, set, delete, exists
- Use Result<T, Error> return types
- No in-memory state
```

**See Also:**
- [Rule 14: Dependency Injection](#rule-14-dependency-injection-over-hardcoding)
- [Rule 18: Configuration as Code](#rule-18-configuration-as-code)

---

## Rule 16: Separation of Concerns

**❌ Bad:** Business logic in controllers

**✅ Good:** Controllers → Services → Repositories

### How to Follow

- Controllers: HTTP handling only (request/response)
- Services: Business logic and orchestration
- Repositories: Data access only (database queries)
- Validators: Input validation only
- Keep each layer focused on its responsibility
- No database queries in controllers
- No HTTP handling in services

### Example

**❌ Bad (Mixed Concerns):**

```typescript
// user.controller.ts - BAD
import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const db = new PrismaClient();

export async function createUser(req: Request, res: Response) {
  // Validation mixed with business logic
  if (!req.body.email || !req.body.password) {
    res.status(400).json({ error: 'Missing fields' });
    return;
  }

  // Database access in controller
  const existing = await db.user.findUnique({
    where: { email: req.body.email },
  });

  // Business logic in controller
  if (existing) {
    res.status(409).json({ error: 'Email exists' });
    return;
  }

  // Password hashing in controller
  const hashedPassword = await bcrypt.hash(req.body.password, 12);

  // Database access in controller
  const user = await db.user.create({
    data: {
      email: req.body.email,
      password: hashedPassword,
      name: req.body.name,
    },
  });

  // Token generation in controller
  const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!);

  // Everything mixed together
  res.status(201).json({ user, token });
}

// Problems:
// - Can't test business logic without HTTP
// - Can't reuse logic elsewhere
// - Hard to maintain
// - Violates single responsibility
```

**✅ Good (Separated Concerns):**

```typescript
// user.validator.ts - VALIDATION LAYER
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string()
    .min(8)
    .regex(/[A-Z]/, "Must contain uppercase")
    .regex(/[0-9]/, "Must contain number"),
  name: z.string().min(2).max(100).trim(),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;

// user.repository.ts - DATA ACCESS LAYER
import type { PrismaClient, User } from '@prisma/client';
import type { CreateUserDTO } from './user.types';
import type { Result } from '@/shared/types/result';

export class UserRepository {
  constructor(private db: PrismaClient) {}

  async findByEmail(email: string): Promise<Result<User | null, Error>> {
    try {
      const user = await this.db.user.findUnique({
        where: { email: email.toLowerCase() },
      });
      return { success: true, data: user };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Database error')
      };
    }
  }

  async create(data: CreateUserDTO): Promise<Result<User, Error>> {
    try {
      const user = await this.db.user.create({ data });
      return { success: true, data: user };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Database error')
      };
    }
  }

  async findById(id: string): Promise<Result<User | null, Error>> {
    try {
      const user = await this.db.user.findUnique({ where: { id } });
      return { success: true, data: user };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error : new Error('Database error')
      };
    }
  }
}

// user.service.ts - BUSINESS LOGIC LAYER
import bcrypt from 'bcrypt';
import type { UserRepository } from './user.repository';
import type { CreateUserInput } from './user.validator';
import type { UserDTO, CreateUserDTO } from './user.types';
import type { Logger } from '@/shared/types/logger';
import type { Result } from '@/shared/types/result';

export class UserService {
  constructor(
    private repository: UserRepository,
    private logger: Logger
  ) {}

  async createUser(input: CreateUserInput): Promise<Result<UserDTO, Error>> {
    // Business logic: Check if user exists
    const existingResult = await this.repository.findByEmail(input.email);
    if (!existingResult.success) {
      return existingResult;
    }

    if (existingResult.data) {
      this.logger.warn('User registration attempted with existing email', {
        email: input.email,
      });
      return {
        success: false,
        error: new Error('Email already exists'),
      };
    }

    // Business logic: Hash password
    const hashedPassword = await bcrypt.hash(input.password, 12);

    // Business logic: Prepare data
    const createData: CreateUserDTO = {
      email: input.email.toLowerCase(),
      password: hashedPassword,
      name: input.name,
    };

    // Data access: Create user
    const createResult = await this.repository.create(createData);
    if (!createResult.success) {
      this.logger.error('User creation failed', { error: createResult.error });
      return createResult;
    }

    // Business logic: Remove sensitive data
    const { password, ...userDTO } = createResult.data;

    this.logger.info('User created successfully', { userId: userDTO.id });
    return { success: true, data: userDTO };
  }

  async getUserById(id: string): Promise<Result<UserDTO | null, Error>> {
    const result = await this.repository.findById(id);

    if (!result.success) {
      return result;
    }

    if (!result.data) {
      return { success: true, data: null };
    }

    // Remove sensitive data
    const { password, ...userDTO } = result.data;
    return { success: true, data: userDTO };
  }
}

// auth.service.ts - AUTHENTICATION BUSINESS LOGIC
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import type { UserRepository } from '../users/user.repository';
import type { Logger } from '@/shared/types/logger';
import type { Result } from '@/shared/types/result';

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export class AuthService {
  constructor(
    private userRepository: UserRepository,
    private config: { jwtSecret: string; tokenExpiry: string },
    private logger: Logger
  ) {}

  async login(
    email: string,
    password: string
  ): Promise<Result<AuthTokens, Error>> {
    // Get user
    const userResult = await this.userRepository.findByEmail(email);
    if (!userResult.success) {
      return userResult;
    }

    if (!userResult.data) {
      this.logger.warn('Login attempt for non-existent user', { email });
      return {
        success: false,
        error: new Error('Invalid credentials'),
      };
    }

    // Verify password
    const isValid = await bcrypt.compare(password, userResult.data.password);
    if (!isValid) {
      this.logger.warn('Login attempt with invalid password', {
        userId: userResult.data.id
      });
      return {
        success: false,
        error: new Error('Invalid credentials'),
      };
    }

    // Generate tokens
    const accessToken = jwt.sign(
      { userId: userResult.data.id },
      this.config.jwtSecret,
      { expiresIn: this.config.tokenExpiry }
    );

    const refreshToken = jwt.sign(
      { userId: userResult.data.id, type: 'refresh' },
      this.config.jwtSecret,
      { expiresIn: '7d' }
    );

    this.logger.info('User logged in successfully', {
      userId: userResult.data.id
    });

    return {
      success: true,
      data: { accessToken, refreshToken },
    };
  }
}

// user.controller.ts - HTTP LAYER
import type { Request, Response } from 'express';
import type { UserService } from './user.service';
import type { AuthService } from '../auth/auth.service';
import { createUserSchema } from './user.validator';
import type { Logger } from '@/shared/types/logger';

export class UserController {
  constructor(
    private userService: UserService,
    private authService: AuthService,
    private logger: Logger
  ) {}

  async create(req: Request, res: Response): Promise<void> {
    // HTTP concern: Validate request body
    const validation = createUserSchema.safeParse(req.body);
    if (!validation.success) {
      res.status(400).json({
        success: false,
        error: 'Validation failed',
        fields: validation.error.flatten().fieldErrors,
      });
      return;
    }

    // HTTP concern: Call service
    const userResult = await this.userService.createUser(validation.data);

    // HTTP concern: Handle service result
    if (!userResult.success) {
      const statusCode = userResult.error.message === 'Email already exists'
        ? 409
        : 500;

      res.status(statusCode).json({
        success: false,
        error: userResult.error.message,
      });
      return;
    }

    // HTTP concern: Generate auth tokens
    const tokenResult = await this.authService.login(
      validation.data.email,
      validation.data.password
    );

    if (!tokenResult.success) {
      // User created but token generation failed
      this.logger.error('Token generation failed after user creation', {
        userId: userResult.data.id,
      });
      res.status(500).json({
        success: false,
        error: 'Registration successful but login failed',
      });
      return;
    }

    // HTTP concern: Send response
    res.status(201).json({
      success: true,
      data: {
        user: userResult.data,
        tokens: tokenResult.data,
      },
    });
  }

  async getById(req: Request, res: Response): Promise<void> {
    const { id } = req.params;

    const result = await this.userService.getUserById(id);

    if (!result.success) {
      res.status(500).json({
        success: false,
        error: 'Failed to retrieve user',
      });
      return;
    }

    if (!result.data) {
      res.status(404).json({
        success: false,
        error: 'User not found',
      });
      return;
    }

    res.status(200).json({
      success: true,
      data: result.data,
    });
  }
}
```

### Implementation Guidance

**Layer Responsibilities:**

**Controllers (HTTP Layer):**
- Parse request parameters
- Validate input format
- Call appropriate service methods
- Transform service results to HTTP responses
- Set HTTP status codes
- Handle HTTP-specific concerns (cookies, headers)

**Services (Business Logic Layer):**
- Implement business rules
- Orchestrate multiple repositories
- Handle complex workflows
- Transform data between layers
- Business-level error handling
- Logging business events

**Repositories (Data Access Layer):**
- Execute database queries
- Map between database and domain models
- Handle database-specific errors
- No business logic
- Return raw data

**Validators:**
- Input format validation
- Type checking
- Format constraints
- No business logic

**Prompt Template for AI:**

```markdown
## Context
- Strict separation of concerns
- Controllers: HTTP only
- Services: Business logic
- Repositories: Data access
- Validators: Input validation
- Use Result<T, Error> return types throughout

## Task
Create Order feature with these layers:

1. order.validator.ts - Zod schemas for validation
2. order.repository.ts - Database queries with Prisma
3. order.service.ts - Business logic (create order, calculate totals)
4. order.controller.ts - HTTP handlers

Dependencies to inject:
- OrderRepository
- ProductService (to verify product availability)
- PaymentService (to process payment)
- Logger
```

**See Also:**
- [Rule 12: One Responsibility Per File](#rule-12-one-responsibility-per-file)
- [Rule 13: Interface-First Development](#rule-13-interface-first-development)

---

## Rule 17: Return Types Over Throwing

**❌ Bad:** `throw new Error()` in business logic

**✅ Good:** `return Result.error(error)`

### How to Follow

- Use Result<T, E> type for functions that can fail
- Reserve `throw` for truly exceptional cases
- Make errors explicit in function signatures
- Force callers to handle errors
- Provide detailed error information
- Use discriminated unions for type safety

### Example

**❌ Bad (Throwing Errors):**

```typescript
// user.service.ts - BAD
export class UserService {
  async createUser(data: CreateUserDTO): Promise<User> {
    // Caller doesn't know this can throw
    const existing = await this.repository.findByEmail(data.email);

    // Throws - forces try-catch everywhere
    if (existing) {
      throw new Error('Email already exists');
    }

    const hashedPassword = await bcrypt.hash(data.password, 12);

    // This can also throw - not clear from signature
    const user = await this.repository.create({
      ...data,
      password: hashedPassword,
    });

    return user;
  }

  async getUserById(id: string): Promise<User> {
    const user = await this.repository.findById(id);

    // Throws - mixing null checks with exceptions
    if (!user) {
      throw new Error('User not found');
    }

    return user;
  }
}

// Usage - forced to use try-catch
try {
  const user = await userService.createUser(data);
  // Success case
} catch (error) {
  // What errors can happen? No idea from type signature
  // Could be validation, duplicate email, database error, etc.
  if (error.message === 'Email already exists') {
    // Handle duplicate
  } else {
    // Handle other errors?
  }
}
```

**✅ Good (Result Types):**

```typescript
// result.type.ts - Shared type
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Helper functions
export const ok = <T>(data: T): Result<T, never> => ({
  success: true,
  data,
});

export const err = <E>(error: E): Result<never, E> => ({
  success: false,
  error,
});

// user.errors.ts - Explicit error types
export class UserNotFoundError extends Error {
  constructor(userId: string) {
    super(`User not found: ${userId}`);
    this.name = 'UserNotFoundError';
  }
}

export class EmailAlreadyExistsError extends Error {
  constructor(email: string) {
    super(`Email already exists: ${email}`);
    this.name = 'EmailAlreadyExistsError';
  }
}

export class InvalidPasswordError extends Error {
  constructor() {
    super('Invalid password');
    this.name = 'InvalidPasswordError';
  }
}

export type UserServiceError =
  | UserNotFoundError
  | EmailAlreadyExistsError
  | InvalidPasswordError
  | Error; // Generic database errors

// user.service.ts - GOOD
import type { Result } from '@/shared/types/result';
import { ok, err } from '@/shared/types/result';
import {
  EmailAlreadyExistsError,
  UserNotFoundError,
  type UserServiceError,
} from './user.errors';

export class UserService {
  constructor(
    private repository: UserRepository,
    private logger: Logger
  ) {}

  async createUser(
    data: CreateUserDTO
  ): Promise<Result<UserDTO, UserServiceError>> {
    // Check existing - error is explicit in return type
    const existingResult = await this.repository.findByEmail(data.email);

    if (!existingResult.success) {
      this.logger.error('Database error checking existing user', {
        error: existingResult.error,
      });
      return err(existingResult.error);
    }

    if (existingResult.data) {
      this.logger.warn('Duplicate email registration attempt', {
        email: data.email,
      });
      return err(new EmailAlreadyExistsError(data.email));
    }

    // Hash password
    try {
      const hashedPassword = await bcrypt.hash(data.password, 12);

      const createResult = await this.repository.create({
        ...data,
        password: hashedPassword,
      });

      if (!createResult.success) {
        this.logger.error('Database error creating user', {
          error: createResult.error,
        });
        return err(createResult.error);
      }

      const { password, ...userDTO } = createResult.data;
      this.logger.info('User created', { userId: userDTO.id });

      return ok(userDTO);
    } catch (error) {
      // Only truly unexpected errors
      this.logger.error('Unexpected error in createUser', { error });
      return err(error instanceof Error ? error : new Error('Unknown error'));
    }
  }

  async getUserById(id: string): Promise<Result<UserDTO, UserServiceError>> {
    const result = await this.repository.findById(id);

    if (!result.success) {
      return err(result.error);
    }

    if (!result.data) {
      return err(new UserNotFoundError(id));
    }

    const { password, ...userDTO } = result.data;
    return ok(userDTO);
  }

  async verifyPassword(
    email: string,
    password: string
  ): Promise<Result<UserDTO, UserServiceError>> {
    const userResult = await this.repository.findByEmail(email);

    if (!userResult.success) {
      return err(userResult.error);
    }

    if (!userResult.data) {
      // Don't reveal whether user exists
      return err(new InvalidPasswordError());
    }

    const isValid = await bcrypt.compare(password, userResult.data.password);

    if (!isValid) {
      this.logger.warn('Invalid password attempt', { email });
      return err(new InvalidPasswordError());
    }

    const { password: _, ...userDTO } = userResult.data;
    return ok(userDTO);
  }
}

// Usage - Type-safe error handling
const result = await userService.createUser(data);

if (!result.success) {
  // TypeScript knows result.error is UserServiceError
  if (result.error instanceof EmailAlreadyExistsError) {
    return res.status(409).json({
      success: false,
      error: 'Email already exists',
    });
  }

  if (result.error instanceof UserNotFoundError) {
    return res.status(404).json({
      success: false,
      error: 'User not found',
    });
  }

  // Generic error
  return res.status(500).json({
    success: false,
    error: 'Internal server error',
  });
}

// TypeScript knows result.data is UserDTO
const user = result.data;
res.status(201).json({
  success: true,
  data: user,
});
```

**Advanced Pattern with Detailed Error Types:**

```typescript
// error.types.ts - Structured errors
export interface ValidationError {
  type: 'validation';
  fields: Record<string, string[]>;
}

export interface NotFoundError {
  type: 'not_found';
  resource: string;
  id: string;
}

export interface ConflictError {
  type: 'conflict';
  message: string;
  field?: string;
}

export interface DatabaseError {
  type: 'database';
  message: string;
  code?: string;
}

export type ServiceError =
  | ValidationError
  | NotFoundError
  | ConflictError
  | DatabaseError;

// Helper functions for creating errors
export const validationError = (
  fields: Record<string, string[]>
): ValidationError => ({
  type: 'validation',
  fields,
});

export const notFoundError = (resource: string, id: string): NotFoundError => ({
  type: 'not_found',
  resource,
  id,
});

export const conflictError = (
  message: string,
  field?: string
): ConflictError => ({
  type: 'conflict',
  message,
  field,
});

export const databaseError = (
  message: string,
  code?: string
): DatabaseError => ({
  type: 'database',
  message,
  code,
});

// Usage in service
async createUser(
  data: CreateUserDTO
): Promise<Result<UserDTO, ServiceError>> {
  const existingResult = await this.repository.findByEmail(data.email);

  if (!existingResult.success) {
    return err(databaseError('Failed to check existing user'));
  }

  if (existingResult.data) {
    return err(conflictError('Email already exists', 'email'));
  }

  // ... rest of implementation
}

// Type-safe error handling in controller
const result = await userService.createUser(data);

if (!result.success) {
  const error = result.error;

  switch (error.type) {
    case 'validation':
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        fields: error.fields,
      });

    case 'not_found':
      return res.status(404).json({
        success: false,
        error: `${error.resource} not found`,
      });

    case 'conflict':
      return res.status(409).json({
        success: false,
        error: error.message,
        field: error.field,
      });

    case 'database':
      this.logger.error('Database error', { error });
      return res.status(500).json({
        success: false,
        error: 'Internal server error',
      });
  }
}

// Success case
res.status(201).json({
  success: true,
  data: result.data,
});
```

### Implementation Guidance

**When to Use Result Types:**
- Service layer methods
- Repository layer methods
- Any function with expected failure modes
- External API calls
- File system operations
- Validation logic

**When Throwing is OK:**
- Programming errors (null pointer, type errors)
- Configuration errors at startup
- Framework/library internal errors
- Truly exceptional, unrecoverable situations

**Benefits:**
- Errors explicit in type signature
- Compiler forces error handling
- No silent failures
- Better error documentation
- Easier testing
- Type-safe error handling

**Prompt Template for AI:**

```markdown
## Context
- Use Result<T, E> for all methods that can fail
- Define specific error types (not just Error)
- Result type: { success: true; data: T } | { success: false; error: E }
- Helpers: ok(data), err(error)

## Task
Create ProductService with Result return types:

Methods:
- getProduct(id): Result<Product, ProductError>
- createProduct(data): Result<Product, ProductError>
- updateStock(id, quantity): Result<Product, ProductError>

Error types:
- ProductNotFoundError
- InsufficientStockError
- InvalidProductDataError

All methods return Result, no throwing.
```

**See Also:**
- [Rule 35: Handle Errors Gracefully](#)
- [Rule 5: Define Success and Error Scenarios](#)

---

## Rule 18: Configuration as Code

**❌ Bad:** Magic numbers and strings throughout code

**✅ Good:** Centralized configuration with validation

### How to Follow

- Define configuration schema with validation (Zod)
- Validate environment variables on startup
- Use typed configuration objects
- Centralize all configuration in one place
- Use constants for business rules
- Document all configuration options
- Fail fast on invalid configuration

### Example

**❌ Bad (Magic Values):**

```typescript
// Scattered throughout codebase
// auth.service.ts
const token = jwt.sign(payload, 'my-secret-key', { expiresIn: '15m' });

// user.service.ts
const hash = await bcrypt.hash(password, 10);

// email.service.ts
await sendEmail({
  from: 'noreply@example.com',
  to: user.email,
  // ...
});

// session.service.ts
await redis.setex(`session:${id}`, 3600, data);

// rate-limit.middleware.ts
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
});

// Problems:
// - Values hardcoded everywhere
// - Can't change without code changes
// - Different values for dev/prod require code changes
// - No validation
// - No documentation
```

**✅ Good (Configuration as Code):**

```typescript
// config/config.schema.ts
import { z } from 'zod';

export const configSchema = z.object({
  // Environment
  env: z.enum(['development', 'staging', 'production']),
  port: z.number().int().positive().default(3000),

  // Database
  database: z.object({
    url: z.string().url(),
    maxConnections: z.number().int().positive().default(10),
    ssl: z.boolean().default(false),
    logging: z.boolean().default(false),
  }),

  // Redis
  redis: z.object({
    url: z.string().url(),
    sessionTTL: z.number().int().positive().default(3600), // 1 hour
    cacheTTL: z.number().int().positive().default(300), // 5 minutes
  }),

  // Authentication
  auth: z.object({
    jwtSecret: z.string().min(32, 'JWT secret must be at least 32 characters'),
    accessTokenExpiry: z.string().default('15m'),
    refreshTokenExpiry: z.string().default('7d'),
    bcryptRounds: z.number().int().min(10).max(15).default(12),
    maxLoginAttempts: z.number().int().positive().default(5),
    lockoutDuration: z.number().int().positive().default(900), // 15 minutes
  }),

  // Email
  email: z.object({
    provider: z.enum(['sendgrid', 'ses', 'smtp']),
    from: z.string().email(),
    apiKey: z.string().optional(),
    smtp: z.object({
      host: z.string().optional(),
      port: z.number().int().positive().optional(),
      user: z.string().optional(),
      password: z.string().optional(),
    }).optional(),
  }),

  // Rate Limiting
  rateLimit: z.object({
    windowMs: z.number().int().positive().default(15 * 60 * 1000), // 15 min
    maxRequests: z.number().int().positive().default(100),
    authEndpoints: z.object({
      windowMs: z.number().int().positive().default(15 * 60 * 1000),
      maxRequests: z.number().int().positive().default(5),
    }),
  }),

  // Business Rules
  business: z.object({
    minOrderAmount: z.number().positive().default(10),
    maxOrderAmount: z.number().positive().default(10000),
    defaultCurrency: z.string().length(3).default('USD'),
    taxRate: z.number().min(0).max(1).default(0.08), // 8%
    shippingFee: z.number().positive().default(5),
  }),

  // Feature Flags
  features: z.object({
    enableNewCheckout: z.boolean().default(false),
    enableEmailVerification: z.boolean().default(true),
    enableTwoFactor: z.boolean().default(false),
  }),

  // Logging
  logging: z.object({
    level: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
    pretty: z.boolean().default(false),
  }),
});

export type Config = z.infer<typeof configSchema>;

// config/config.loader.ts
import { configSchema, type Config } from './config.schema';

export function loadConfig(): Config {
  // Load from environment variables
  const rawConfig = {
    env: process.env.NODE_ENV || 'development',
    port: parseInt(process.env.PORT || '3000', 10),

    database: {
      url: process.env.DATABASE_URL,
      maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '10', 10),
      ssl: process.env.DB_SSL === 'true',
      logging: process.env.DB_LOGGING === 'true',
    },

    redis: {
      url: process.env.REDIS_URL,
      sessionTTL: parseInt(process.env.REDIS_SESSION_TTL || '3600', 10),
      cacheTTL: parseInt(process.env.REDIS_CACHE_TTL || '300', 10),
    },

    auth: {
      jwtSecret: process.env.JWT_SECRET,
      accessTokenExpiry: process.env.ACCESS_TOKEN_EXPIRY || '15m',
      refreshTokenExpiry: process.env.REFRESH_TOKEN_EXPIRY || '7d',
      bcryptRounds: parseInt(process.env.BCRYPT_ROUNDS || '12', 10),
      maxLoginAttempts: parseInt(process.env.MAX_LOGIN_ATTEMPTS || '5', 10),
      lockoutDuration: parseInt(process.env.LOCKOUT_DURATION || '900', 10),
    },

    email: {
      provider: process.env.EMAIL_PROVIDER || 'sendgrid',
      from: process.env.EMAIL_FROM,
      apiKey: process.env.EMAIL_API_KEY,
      smtp: {
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT ? parseInt(process.env.SMTP_PORT, 10) : undefined,
        user: process.env.SMTP_USER,
        password: process.env.SMTP_PASSWORD,
      },
    },

    rateLimit: {
      windowMs: parseInt(process.env.RATE_LIMIT_WINDOW || '900000', 10),
      maxRequests: parseInt(process.env.RATE_LIMIT_MAX || '100', 10),
      authEndpoints: {
        windowMs: parseInt(process.env.AUTH_RATE_LIMIT_WINDOW || '900000', 10),
        maxRequests: parseInt(process.env.AUTH_RATE_LIMIT_MAX || '5', 10),
      },
    },

    business: {
      minOrderAmount: parseFloat(process.env.MIN_ORDER_AMOUNT || '10'),
      maxOrderAmount: parseFloat(process.env.MAX_ORDER_AMOUNT || '10000'),
      defaultCurrency: process.env.DEFAULT_CURRENCY || 'USD',
      taxRate: parseFloat(process.env.TAX_RATE || '0.08'),
      shippingFee: parseFloat(process.env.SHIPPING_FEE || '5'),
    },

    features: {
      enableNewCheckout: process.env.FEATURE_NEW_CHECKOUT === 'true',
      enableEmailVerification: process.env.FEATURE_EMAIL_VERIFICATION !== 'false',
      enableTwoFactor: process.env.FEATURE_TWO_FACTOR === 'true',
    },

    logging: {
      level: process.env.LOG_LEVEL || 'info',
      pretty: process.env.LOG_PRETTY === 'true',
    },
  };

  // Validate configuration
  try {
    const config = configSchema.parse(rawConfig);
    console.log('✅ Configuration loaded and validated successfully');
    return config;
  } catch (error) {
    console.error('❌ Configuration validation failed:');
    console.error(error);
    process.exit(1); // Fail fast
  }
}

// Export singleton
export const config = loadConfig();
```

**Usage in Services:**

```typescript
// auth.service.ts
import { config } from '@/config/config.loader';

export class AuthService {
  async login(email: string, password: string): Promise<Result<AuthTokens, Error>> {
    // Use configuration values
    const accessToken = jwt.sign(
      { userId: user.id },
      config.auth.jwtSecret,
      { expiresIn: config.auth.accessTokenExpiry }
    );

    const refreshToken = jwt.sign(
      { userId: user.id, type: 'refresh' },
      config.auth.jwtSecret,
      { expiresIn: config.auth.refreshTokenExpiry }
    );

    return ok({ accessToken, refreshToken });
  }

  async hashPassword(password: string): Promise<string> {
    // Use configured rounds
    return bcrypt.hash(password, config.auth.bcryptRounds);
  }
}

// order.service.ts
import { config } from '@/config/config.loader';

export class OrderService {
  async validateOrder(order: CreateOrderDTO): Promise<Result<void, ServiceError>> {
    // Use business rule configuration
    if (order.total < config.business.minOrderAmount) {
      return err(validationError({
        total: [`Minimum order amount is ${config.business.minOrderAmount}`],
      }));
    }

    if (order.total > config.business.maxOrderAmount) {
      return err(validationError({
        total: [`Maximum order amount is ${config.business.maxOrderAmount}`],
      }));
    }

    return ok(undefined);
  }

  async calculateTotal(subtotal: number): Promise<OrderTotal> {
    return {
      subtotal,
      tax: subtotal * config.business.taxRate,
      shipping: config.business.shippingFee,
      total: subtotal + (subtotal * config.business.taxRate) + config.business.shippingFee,
      currency: config.business.defaultCurrency,
    };
  }
}

// Feature flags usage
// user.controller.ts
import { config } from '@/config/config.loader';

export class UserController {
  async register(req: Request, res: Response): Promise<void> {
    const result = await this.userService.createUser(req.body);

    if (!result.success) {
      // ... handle error
    }

    // Use feature flag
    if (config.features.enableEmailVerification) {
      await this.emailService.sendVerificationEmail(result.data.email);
    }

    res.status(201).json({
      success: true,
      data: result.data,
    });
  }
}
```

### Implementation Guidance

**Configuration Best Practices:**
- Validate all configuration on startup
- Fail fast if configuration is invalid
- Use environment variables for secrets
- Use .env.example to document all options
- Different configs for dev/staging/prod
- Never commit .env files
- Type-safe configuration access

**What to Configure:**
- External service credentials
- Connection strings
- Rate limits
- Business rules (minimum amounts, fees, etc.)
- Feature flags
- Timeouts and retry policies
- Logging levels

**What NOT to Configure:**
- Application logic
- Validation rules (should be in code)
- Type definitions
- Complex algorithms

**Prompt Template for AI:**

```markdown
## Context
- Centralized configuration with Zod validation
- Configuration loaded from environment variables
- Fail fast on invalid configuration
- Typed configuration object
- Existing config at @/config/config.loader

## Task
Add payment provider configuration:

Add to config schema:
- payment.provider (stripe | paypal)
- payment.stripeSecretKey (string, required if provider=stripe)
- payment.stripeWebhookSecret (string)
- payment.paypalClientId (string, required if provider=paypal)
- payment.paypalClientSecret (string)
- payment.currency (3-letter code, default USD)
- payment.refundPolicy (number of days, default 30)

Update config.loader.ts to load from environment variables.
Use appropriate Zod validation for each field.
```

**See Also:**
- [Rule 19: Never Hardcode Secrets](#)
- [Rule 15: Stateless Services](#rule-15-stateless-services)

---

## Summary: Architecture & Design Best Practices

**✅ Do:**
- Let humans design interfaces and architecture
- Keep files small and focused (< 300 lines)
- Define interfaces before implementations
- Inject all dependencies via constructor
- Design stateless, horizontally scalable services
- Separate concerns (Controller → Service → Repository)
- Use Result types for expected failures
- Centralize configuration with validation

**❌ Don't:**
- Let AI design system architecture
- Create 1000+ line files doing everything
- Hardcode dependencies inside classes
- Store mutable state in services
- Mix business logic with HTTP handling
- Throw errors for expected failure cases
- Scatter magic numbers throughout code
- Skip configuration validation

**Key Principles:**
1. **Human-Led Design** - AI implements, humans architect
2. **Single Responsibility** - Each file/class does one thing
3. **Explicit Contracts** - Interfaces define clear boundaries
4. **Dependency Injection** - Dependencies passed, not created
5. **Stateless Design** - Horizontal scaling by default
6. **Layered Architecture** - Clear separation of concerns
7. **Explicit Errors** - Result types over exceptions
8. **Validated Configuration** - Fail fast on invalid config

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [01-prompts.md](./01-prompts.md) - Prompt engineering rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Workflow checklist
