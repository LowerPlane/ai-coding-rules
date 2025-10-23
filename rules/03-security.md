# Security Rules (Rules 19-28)

Rules for writing secure code with AI assistance.

---

## Rule 19: Never Hardcode Secrets

**❌ Bad:** `const API_KEY = 'sk_live_abc123xyz789'`

**✅ Good:** `const API_KEY = process.env.STRIPE_API_KEY`

### How to Follow

- Store all secrets in environment variables
- Validate secrets on application startup
- Never commit .env files to version control
- Use .env.example to document required variables
- Rotate secrets regularly

### Example

```typescript
// ❌ BAD: Hardcoded secrets
const stripe = new Stripe('sk_live_abc123xyz789');
const dbPassword = 'super_secret_password';
const jwtSecret = 'my-secret-key';

// ✅ GOOD: Environment variables with validation
import { z } from 'zod';

const envSchema = z.object({
  STRIPE_API_KEY: z.string().min(32).startsWith('sk_'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  ENCRYPTION_KEY: z.string().length(64), // 32 bytes hex
});

// Validate on startup
const env = envSchema.parse(process.env);

const stripe = new Stripe(env.STRIPE_API_KEY);
const jwtSecret = env.JWT_SECRET;
```

### .env.example Template

```bash
# API Keys
STRIPE_API_KEY=sk_test_your_test_key_here
SENDGRID_API_KEY=SG.your_api_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_SECRET=your_32_char_minimum_secret_here
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_SECRET=your_refresh_token_secret_here

# Encryption
ENCRYPTION_KEY=your_64_char_hex_encryption_key_here
```

> **⚠️ WARNING**: Never commit .env files. Add to .gitignore immediately:
> ```
> .env
> .env.local
> .env.*.local
> ```

---

## Rule 20: AI Cannot Write Security-Critical Code Alone

**❌ Bad:** "AI, implement payment processing with Stripe"

**✅ Good:** Human designs security flow, AI helps with integration boilerplate

### How to Follow

**Never Let AI Generate Alone:**
- Payment processing logic
- Encryption/decryption implementations
- Password hashing algorithms
- OAuth/SSO flows
- Session management
- Access control systems
- Cryptographic key generation

**AI Can Help With:**
- Input validation schemas
- Rate limiting configuration
- CORS setup
- Security header middleware
- Audit logging boilerplate

### Example: Payment Processing

```typescript
// ❌ BAD: Letting AI design payment flow
// "AI, create a payment processing system"

// ✅ GOOD: Human designs, AI implements boilerplate

// HUMAN DESIGNS:
/**
 * Payment Processing Flow (Human-Designed)
 *
 * 1. Validate payment intent on server
 * 2. Verify user authorization
 * 3. Create idempotent payment record
 * 4. Call Stripe API (official SDK only)
 * 5. Handle webhooks for async confirmation
 * 6. Never trust client-side amounts
 */

// AI IMPLEMENTS (with strict guidelines):
interface PaymentIntent {
  userId: string;
  amount: number;
  currency: string;
  idempotencyKey: string;
}

// Human-reviewed payment service
class PaymentService {
  constructor(
    private stripe: Stripe, // Official SDK only
    private db: Database,
    private logger: Logger
  ) {}

  async createPayment(intent: PaymentIntent): Promise<Result<Payment, Error>> {
    // Human validates this logic
    // AI generates boilerplate
  }
}
```

### Security Checklist for AI Code

```markdown
Before accepting AI-generated security code:

Critical Components (HUMAN MUST REVIEW):
- [ ] Authentication logic
- [ ] Authorization checks
- [ ] Password handling
- [ ] Token generation/validation
- [ ] Encryption operations
- [ ] Payment processing
- [ ] Data sanitization

Safe for AI (with review):
- [ ] Input validation schemas
- [ ] Rate limiting setup
- [ ] Logging configuration
- [ ] Error messages (non-sensitive)
- [ ] API client initialization (using official SDKs)
```

> **⚠️ CRITICAL**: Never deploy AI-generated security code without expert human review. When in doubt, consult a security professional.

---

## Rule 21: Validate All Inputs

**❌ Bad:** Trust user input directly

**✅ Good:** Validate with schema before any processing

### How to Follow

- Use validation libraries (Zod, Joi, Yup)
- Validate at system boundaries (API endpoints, message handlers)
- Reject invalid input early
- Provide specific error messages
- Validate type, format, length, and business rules

### Example

```typescript
// ❌ BAD: No validation
app.post('/api/users', async (req, res) => {
  const user = await db.users.create(req.body); // DANGEROUS!
  res.json(user);
});

// ✅ GOOD: Comprehensive validation
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .max(255, 'Email too long')
    .toLowerCase()
    .trim(),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),

  name: z.string()
    .min(2, 'Name too short')
    .max(100, 'Name too long')
    .trim()
    .regex(/^[a-zA-Z\s-']+$/, 'Invalid characters in name'),

  age: z.number()
    .int('Age must be an integer')
    .positive('Age must be positive')
    .min(18, 'Must be at least 18 years old')
    .max(120, 'Invalid age'),

  phoneNumber: z.string()
    .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number')
    .optional(),

  role: z.enum(['user', 'admin', 'moderator'])
    .default('user'),
});

type CreateUserInput = z.infer<typeof createUserSchema>;

app.post('/api/users', async (req, res) => {
  try {
    // Validate input
    const validatedData = createUserSchema.parse(req.body);

    // Now safe to use
    const user = await userService.create(validatedData);

    res.status(201).json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: error.errors.map(e => ({
          field: e.path.join('.'),
          message: e.message,
        })),
      });
    }

    throw error;
  }
});
```

### Validation Checklist

```typescript
// Complete validation example
const comprehensiveSchema = z.object({
  // Email validation
  email: z.string().email().max(255).toLowerCase().trim(),

  // URL validation
  website: z.string().url().max(2048).optional(),

  // Enum validation
  status: z.enum(['active', 'pending', 'suspended']),

  // Number ranges
  quantity: z.number().int().min(1).max(1000),

  // String length
  description: z.string().min(10).max(5000).trim(),

  // Date validation
  birthDate: z.string().datetime().or(z.date()),

  // Array validation
  tags: z.array(z.string()).min(1).max(10),

  // Nested object validation
  address: z.object({
    street: z.string().max(200),
    city: z.string().max(100),
    zipCode: z.string().regex(/^\d{5}(-\d{4})?$/),
  }),

  // Custom validation
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/)
    .refine(
      async (username) => {
        const exists = await db.users.exists({ username });
        return !exists;
      },
      { message: 'Username already taken' }
    ),
});
```

> **⚠️ OWASP Reference**: This prevents [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/) attacks.

---

## Rule 22: Use Parameterized Queries Only

**❌ Bad:** String concatenation in SQL queries

**✅ Good:** Parameterized queries or ORM methods

### How to Follow

- **NEVER** concatenate user input into SQL
- Use ORM query builders (Prisma, TypeORM, Sequelize)
- Use parameterized queries for raw SQL
- Validate input even with parameterized queries
- Use prepared statements

### Example

```typescript
// ❌ BAD: SQL Injection vulnerability
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;

  // DANGEROUS! User can inject: 1 OR 1=1
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  const user = await db.raw(query);

  // ALSO DANGEROUS! Template literals don't help
  const query2 = `SELECT * FROM users WHERE email = '${req.query.email}'`;

  res.json(user);
});

// ❌ BAD: Dynamic query building
const buildQuery = (filters: any) => {
  let query = 'SELECT * FROM products WHERE 1=1';

  if (filters.category) {
    query += ` AND category = '${filters.category}'`; // DANGEROUS!
  }

  if (filters.minPrice) {
    query += ` AND price >= ${filters.minPrice}`; // DANGEROUS!
  }

  return query;
};

// ✅ GOOD: ORM (Prisma)
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      email: true,
      name: true,
      // Never select password hash in API responses
    },
  });

  res.json(user);
});

// ✅ GOOD: Parameterized query (PostgreSQL)
app.get('/api/users/search', async (req, res) => {
  const { email } = req.query;

  // Parameterized query - safe from SQL injection
  const result = await db.query(
    'SELECT id, email, name FROM users WHERE email = $1',
    [email]
  );

  res.json(result.rows);
});

// ✅ GOOD: Query builder
app.get('/api/products', async (req, res) => {
  const { category, minPrice, maxPrice } = req.query;

  // Build query safely
  let query = db('products').select('*');

  if (category) {
    query = query.where('category', '=', category); // Parameterized
  }

  if (minPrice) {
    query = query.where('price', '>=', Number(minPrice)); // Parameterized
  }

  if (maxPrice) {
    query = query.where('price', '<=', Number(maxPrice)); // Parameterized
  }

  const products = await query;
  res.json(products);
});
```

### Advanced: Dynamic Filters with Type Safety

```typescript
// ✅ BEST: Type-safe query builder
interface ProductFilters {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  inStock?: boolean;
}

const filterSchema = z.object({
  category: z.string().max(50).optional(),
  minPrice: z.number().positive().optional(),
  maxPrice: z.number().positive().optional(),
  inStock: z.boolean().optional(),
});

async function getProducts(filters: ProductFilters) {
  // Validate filters first
  const validated = filterSchema.parse(filters);

  // Build query with Prisma (always parameterized)
  const products = await prisma.product.findMany({
    where: {
      ...(validated.category && { category: validated.category }),
      ...(validated.inStock !== undefined && { inStock: validated.inStock }),
      ...(validated.minPrice || validated.maxPrice ? {
        price: {
          ...(validated.minPrice && { gte: validated.minPrice }),
          ...(validated.maxPrice && { lte: validated.maxPrice }),
        },
      } : {}),
    },
  });

  return products;
}
```

### Prompt Template for AI

```markdown
When generating database queries:

REQUIREMENTS:
- Use Prisma/TypeORM query builder (NEVER raw SQL with concatenation)
- If raw SQL is required, use parameterized queries with $1, $2, etc.
- Validate all inputs with Zod before querying
- Never use template literals with user input
- Never concatenate strings to build queries

EXAMPLE:
// Use Prisma
await prisma.user.findMany({ where: { email: userEmail } });

// If raw SQL needed
await db.query('SELECT * FROM users WHERE email = $1', [userEmail]);
```

> **⚠️ OWASP Reference**: This prevents [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/) (SQL Injection).

---

## Rule 23: Sanitize All Output

**❌ Bad:** Display user input directly in HTML

**✅ Good:** Sanitize based on output context (HTML, URL, JavaScript)

### How to Follow

- Use DOMPurify for HTML sanitization
- Use template engines with auto-escaping (React, Vue, EJS)
- Encode output based on context
- Never trust data from database either
- Set proper Content-Security-Policy headers

### Example

```typescript
// ❌ BAD: XSS vulnerability
app.get('/search', (req, res) => {
  const query = req.query.q;

  // DANGEROUS! User can inject: <script>alert('XSS')</script>
  res.send(`<h1>Results for: ${query}</h1>`);
});

// ❌ BAD: Inserting database content without sanitization
app.get('/profile/:id', async (req, res) => {
  const user = await db.users.findOne({ id: req.params.id });

  // DANGEROUS! User bio might contain malicious scripts
  res.send(`
    <div class="profile">
      <h1>${user.name}</h1>
      <div class="bio">${user.bio}</div>
    </div>
  `);
});

// ✅ GOOD: React (auto-escapes by default)
function SearchResults({ query, results }: Props) {
  return (
    <div>
      {/* React automatically escapes this */}
      <h1>Results for: {query}</h1>

      <ul>
        {results.map(result => (
          <li key={result.id}>
            {/* Auto-escaped */}
            <h2>{result.title}</h2>
            <p>{result.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

// ⚠️ CAREFUL: dangerouslySetInnerHTML requires sanitization
import DOMPurify from 'isomorphic-dompurify';

function RichContent({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
    ALLOWED_ATTR: [],
  });

  return (
    <div dangerouslySetInnerHTML={{ __html: sanitized }} />
  );
}

// ✅ GOOD: Backend with template engine
import ejs from 'ejs';

app.get('/search', async (req, res) => {
  const query = req.query.q as string;
  const results = await searchService.search(query);

  // EJS auto-escapes <%= %> tags
  const html = await ejs.renderFile('search.ejs', {
    query,      // Auto-escaped
    results,    // Auto-escaped
  });

  res.send(html);
});

// search.ejs template
// <h1>Results for: <%= query %></h1>  <!-- Auto-escaped -->
```

### Context-Specific Encoding

```typescript
// ✅ GOOD: Different contexts need different encoding

import DOMPurify from 'isomorphic-dompurify';

class OutputEncoder {
  // HTML context
  static html(input: string): string {
    return DOMPurify.sanitize(input);
  }

  // HTML attribute context
  static htmlAttribute(input: string): string {
    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }

  // URL parameter context
  static url(input: string): string {
    return encodeURIComponent(input);
  }

  // JavaScript context
  static javascript(input: string): string {
    return JSON.stringify(input).slice(1, -1); // Remove quotes
  }
}

// Usage
app.get('/profile/:id', async (req, res) => {
  const user = await db.users.findOne({ id: req.params.id });

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>${OutputEncoder.htmlAttribute(user.name)}'s Profile</title>
      </head>
      <body>
        <h1>${OutputEncoder.html(user.name)}</h1>

        <!-- Rich content (user bio) -->
        <div class="bio">
          ${OutputEncoder.html(user.bio)}
        </div>

        <!-- Link with user input -->
        <a href="/search?q=${OutputEncoder.url(user.favoriteTag)}">
          Search
        </a>

        <script>
          // JavaScript context
          const userName = '${OutputEncoder.javascript(user.name)}';
          console.log('User:', userName);
        </script>
      </body>
    </html>
  `;

  res.send(html);
});
```

### Content Security Policy

```typescript
// ✅ GOOD: Set CSP headers
import helmet from 'helmet';

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"], // No inline scripts
      styleSrc: ["'self'", "'unsafe-inline'"], // Styles from same origin
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'],
      fontSrc: ["'self'", 'https://fonts.gstatic.com'],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  })
);

// Additional security headers
app.use(helmet.xssFilter());
app.use(helmet.noSniff());
app.use(helmet.frameguard({ action: 'deny' }));
```

> **⚠️ OWASP Reference**: This prevents [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/) (XSS attacks).

---

## Rule 24: Implement Rate Limiting

**❌ Bad:** No rate limits on public endpoints

**✅ Good:** Rate limit all endpoints, especially auth and expensive operations

### How to Follow

- Use rate limiting middleware (express-rate-limit, rate-limiter-flexible)
- Different limits for different endpoint types
- Store limits in Redis for distributed systems
- Return 429 status with Retry-After header
- Log rate limit violations

### Example

```typescript
// ❌ BAD: No rate limiting
app.post('/api/login', async (req, res) => {
  // Vulnerable to brute force attacks
  const user = await authService.login(req.body);
  res.json(user);
});

app.post('/api/send-email', async (req, res) => {
  // Can be abused to send spam
  await emailService.send(req.body);
  res.json({ success: true });
});

// ✅ GOOD: Comprehensive rate limiting
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Strict rate limit for authentication
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:',
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: {
    error: 'Too many login attempts. Please try again in 15 minutes.',
  },
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  // Increment on failed attempts only
  skip: (req, res) => res.statusCode < 400,
});

// Normal rate limit for API endpoints
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:api:',
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: {
    error: 'Too many requests. Please try again later.',
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Very strict for expensive operations
const expensiveLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:expensive:',
  }),
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // 10 requests per hour
  message: {
    error: 'Rate limit exceeded for this operation.',
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Apply to routes
app.post('/api/login', authLimiter, loginHandler);
app.post('/api/register', authLimiter, registerHandler);
app.post('/api/forgot-password', authLimiter, forgotPasswordHandler);

app.use('/api/', apiLimiter); // All API routes

app.post('/api/reports/generate', expensiveLimiter, generateReportHandler);
app.post('/api/send-email', expensiveLimiter, sendEmailHandler);
```

### Advanced: Per-User Rate Limiting

```typescript
// ✅ BEST: Different limits for authenticated users
import { RateLimiterRedis } from 'rate-limiter-flexible';

const redis = new Redis(process.env.REDIS_URL);

// Anonymous users: strict limits
const anonymousLimiter = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'rl:anon',
  points: 10, // Number of requests
  duration: 60, // Per 60 seconds
  blockDuration: 300, // Block for 5 minutes if exceeded
});

// Authenticated users: more generous
const authenticatedLimiter = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'rl:auth',
  points: 100,
  duration: 60,
  blockDuration: 60,
});

// Premium users: even more generous
const premiumLimiter = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'rl:premium',
  points: 1000,
  duration: 60,
  blockDuration: 30,
});

// Middleware
const rateLimitMiddleware = async (req, res, next) => {
  try {
    const user = req.user; // From auth middleware
    const ip = req.ip;

    let limiter: RateLimiterRedis;
    let key: string;

    if (!user) {
      // Anonymous user - use IP address
      limiter = anonymousLimiter;
      key = ip;
    } else if (user.plan === 'premium') {
      limiter = premiumLimiter;
      key = `user:${user.id}`;
    } else {
      limiter = authenticatedLimiter;
      key = `user:${user.id}`;
    }

    const rateLimitResult = await limiter.consume(key);

    // Add rate limit info to response headers
    res.set({
      'X-RateLimit-Limit': limiter.points,
      'X-RateLimit-Remaining': rateLimitResult.remainingPoints,
      'X-RateLimit-Reset': new Date(Date.now() + rateLimitResult.msBeforeNext).toISOString(),
    });

    next();
  } catch (error) {
    if (error instanceof Error) {
      // Rate limit exceeded
      const retryAfter = Math.ceil(error.msBeforeNext / 1000);

      res.set('Retry-After', String(retryAfter));
      res.status(429).json({
        error: 'Too many requests',
        retryAfter,
      });

      // Log suspicious activity
      logger.warn('Rate limit exceeded', {
        ip: req.ip,
        userId: req.user?.id,
        endpoint: req.path,
      });
    } else {
      next(error);
    }
  }
};

app.use('/api/', rateLimitMiddleware);
```

### Rate Limiting Best Practices

```typescript
// Rate limit configuration by endpoint type
const RATE_LIMITS = {
  // Authentication endpoints (most strict)
  auth: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5,
    message: 'Too many authentication attempts',
  },

  // Password reset (prevent enumeration)
  passwordReset: {
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3,
    message: 'Too many password reset requests',
  },

  // API endpoints (moderate)
  api: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,
    message: 'API rate limit exceeded',
  },

  // Search endpoints (prevent scraping)
  search: {
    windowMs: 60 * 1000, // 1 minute
    max: 30,
    message: 'Too many search requests',
  },

  // File uploads (prevent abuse)
  upload: {
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 20,
    message: 'Upload limit exceeded',
  },

  // Export/reports (expensive operations)
  export: {
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 5,
    message: 'Export limit exceeded',
  },
};
```

> **⚠️ OWASP Reference**: This prevents [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/).

---

## Rule 25: Hash Passwords Correctly

**❌ Bad:** MD5, SHA-1, SHA-256, or plain text

**✅ Good:** bcrypt with cost factor 12+, or Argon2

### How to Follow

- **NEVER** use MD5, SHA-1, or plain SHA-256 for passwords
- Use bcrypt with cost factor 12 or higher
- Or use Argon2 (winner of Password Hashing Competition)
- Never implement your own hashing algorithm
- Add pepper (server-side secret) for additional security
- Use timing-safe comparison

### Example

```typescript
// ❌ BAD: Insecure password hashing
import crypto from 'crypto';

// NEVER DO THIS!
const md5Hash = crypto.createHash('md5').update(password).digest('hex');
const sha1Hash = crypto.createHash('sha1').update(password).digest('hex');
const sha256Hash = crypto.createHash('sha256').update(password).digest('hex');

// STILL INSECURE - no salt
const hash = crypto.createHash('sha256').update(password).digest('hex');

// ❌ BAD: Weak bcrypt cost factor
const weakHash = await bcrypt.hash(password, 4); // Too weak!

// ✅ GOOD: bcrypt with proper cost factor
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12; // Cost factor (2^12 iterations)

async function hashPassword(password: string): Promise<string> {
  // bcrypt automatically generates salt
  const hash = await bcrypt.hash(password, SALT_ROUNDS);
  return hash;
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  // Timing-safe comparison built-in
  const isValid = await bcrypt.compare(password, hash);
  return isValid;
}

// Usage
const passwordHash = await hashPassword('user_password_123');
// Returns: $2b$12$randomSaltAndHash...

const isValid = await verifyPassword('user_password_123', passwordHash);
// Returns: true or false

// ✅ BETTER: Argon2 (more secure)
import argon2 from 'argon2';

async function hashPasswordArgon2(password: string): Promise<string> {
  const hash = await argon2.hash(password, {
    type: argon2.argon2id, // Hybrid mode (memory-hard + data-dependent)
    memoryCost: 65536,     // 64 MB
    timeCost: 3,           // Number of iterations
    parallelism: 4,        // Number of threads
  });
  return hash;
}

async function verifyPasswordArgon2(password: string, hash: string): Promise<boolean> {
  try {
    const isValid = await argon2.verify(hash, password);

    // Check if parameters need updating
    if (isValid && argon2.needsRehash(hash)) {
      // Rehash with new parameters
      const newHash = await hashPasswordArgon2(password);
      await db.users.updatePasswordHash(newHash);
    }

    return isValid;
  } catch (error) {
    return false;
  }
}
```

### Complete User Registration Example

```typescript
// ✅ BEST: Complete secure user registration
import { z } from 'zod';
import bcrypt from 'bcrypt';
import { randomBytes } from 'crypto';

const registerSchema = z.object({
  email: z.string().email().max(255).toLowerCase(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  name: z.string().min(2).max(100).trim(),
});

class AuthService {
  private readonly SALT_ROUNDS = 12;
  private readonly PEPPER = process.env.PASSWORD_PEPPER!; // Server-side secret

  async register(input: unknown): Promise<Result<User, Error>> {
    // 1. Validate input
    const validated = registerSchema.parse(input);

    // 2. Check if user exists
    const existingUser = await db.users.findByEmail(validated.email);
    if (existingUser) {
      return { success: false, error: 'Email already registered' };
    }

    // 3. Add pepper to password
    const pepperedPassword = validated.password + this.PEPPER;

    // 4. Hash password
    const passwordHash = await bcrypt.hash(pepperedPassword, this.SALT_ROUNDS);

    // 5. Generate email verification token
    const verificationToken = randomBytes(32).toString('hex');
    const verificationTokenHash = await bcrypt.hash(verificationToken, 10);

    // 6. Create user
    const user = await db.users.create({
      email: validated.email,
      name: validated.name,
      passwordHash, // Store hash, never plain password
      verificationTokenHash,
      verificationTokenExpiry: new Date(Date.now() + 24 * 60 * 60 * 1000),
      isVerified: false,
    });

    // 7. Send verification email
    await emailService.sendVerificationEmail(user.email, verificationToken);

    // 8. Return user (without sensitive data)
    return {
      success: true,
      data: {
        id: user.id,
        email: user.email,
        name: user.name,
        isVerified: user.isVerified,
      },
    };
  }

  async login(email: string, password: string): Promise<Result<User, Error>> {
    // 1. Find user
    const user = await db.users.findByEmail(email);
    if (!user) {
      // Don't reveal whether user exists
      await bcrypt.hash(password, this.SALT_ROUNDS); // Timing-safe dummy hash
      return { success: false, error: 'Invalid credentials' };
    }

    // 2. Add pepper
    const pepperedPassword = password + this.PEPPER;

    // 3. Verify password
    const isValid = await bcrypt.compare(pepperedPassword, user.passwordHash);

    if (!isValid) {
      // Log failed attempt
      await db.auditLog.create({
        userId: user.id,
        action: 'login_failed',
        ip: req.ip,
      });

      return { success: false, error: 'Invalid credentials' };
    }

    // 4. Check if password needs rehashing (cost factor increased)
    if (this.needsRehash(user.passwordHash)) {
      const newHash = await bcrypt.hash(pepperedPassword, this.SALT_ROUNDS);
      await db.users.update(user.id, { passwordHash: newHash });
    }

    return { success: true, data: user };
  }

  private needsRehash(hash: string): boolean {
    const rounds = bcrypt.getRounds(hash);
    return rounds < this.SALT_ROUNDS;
  }
}
```

### Password Hashing Checklist

```markdown
✅ Password Security Checklist:

Algorithm:
- [ ] Using bcrypt with cost factor 12+ OR Argon2
- [ ] NOT using MD5, SHA-1, SHA-256
- [ ] NOT implementing custom hashing

Security:
- [ ] Unique salt per password (bcrypt does this automatically)
- [ ] Server-side pepper (additional secret)
- [ ] Timing-safe comparison
- [ ] Rate limiting on login endpoint
- [ ] Account lockout after N failed attempts

Best Practices:
- [ ] Never store plain text passwords
- [ ] Never log passwords (even in debug mode)
- [ ] Rehash on login if cost factor increased
- [ ] Don't reveal if email exists during login
- [ ] Generic error message: "Invalid credentials"
```

> **⚠️ OWASP Reference**: This prevents [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/).

---

## Rule 26: Secure JWT Tokens

**❌ Bad:** Long-lived tokens, weak secrets, stored in localStorage

**✅ Good:** Short-lived access tokens, strong secrets, httpOnly cookies for refresh tokens

### How to Follow

- Access tokens: 15 minutes max
- Refresh tokens: 7 days, rotate on use
- Secret: minimum 32 characters (256 bits)
- Store refresh tokens in httpOnly cookies
- Implement token revocation
- Validate all claims

### Example

```typescript
// ❌ BAD: Insecure JWT implementation
import jwt from 'jsonwebtoken';

// INSECURE: Weak secret
const token = jwt.sign({ userId: '123' }, 'secret', { expiresIn: '30d' });

// INSECURE: Long-lived token
const longToken = jwt.sign({ userId: '123' }, process.env.JWT_SECRET, {
  expiresIn: '365d', // One year!
});

// INSECURE: Storing in localStorage (vulnerable to XSS)
localStorage.setItem('token', token);

// ✅ GOOD: Secure JWT implementation
import jwt from 'jsonwebtoken';
import { randomBytes } from 'crypto';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

interface RefreshTokenPayload {
  userId: string;
  tokenId: string; // Unique ID for revocation
}

class TokenService {
  private readonly ACCESS_TOKEN_SECRET = process.env.JWT_SECRET!; // Min 32 chars
  private readonly REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET!;
  private readonly ACCESS_TOKEN_EXPIRY = '15m';
  private readonly REFRESH_TOKEN_EXPIRY = '7d';

  constructor() {
    // Validate secrets on startup
    if (this.ACCESS_TOKEN_SECRET.length < 32) {
      throw new Error('JWT_SECRET must be at least 32 characters');
    }
    if (this.REFRESH_TOKEN_SECRET.length < 32) {
      throw new Error('REFRESH_TOKEN_SECRET must be at least 32 characters');
    }
  }

  generateAccessToken(payload: TokenPayload): string {
    return jwt.sign(
      {
        sub: payload.userId,        // Subject (user ID)
        email: payload.email,
        role: payload.role,
        type: 'access',             // Token type
      },
      this.ACCESS_TOKEN_SECRET,
      {
        expiresIn: this.ACCESS_TOKEN_EXPIRY,
        issuer: 'your-app.com',
        audience: 'your-app.com',
      }
    );
  }

  generateRefreshToken(userId: string): { token: string; tokenId: string } {
    const tokenId = randomBytes(32).toString('hex');

    const token = jwt.sign(
      {
        sub: userId,
        tokenId,
        type: 'refresh',
      },
      this.REFRESH_TOKEN_SECRET,
      {
        expiresIn: this.REFRESH_TOKEN_EXPIRY,
        issuer: 'your-app.com',
        audience: 'your-app.com',
      }
    );

    return { token, tokenId };
  }

  verifyAccessToken(token: string): TokenPayload {
    const decoded = jwt.verify(token, this.ACCESS_TOKEN_SECRET, {
      issuer: 'your-app.com',
      audience: 'your-app.com',
    }) as any;

    if (decoded.type !== 'access') {
      throw new Error('Invalid token type');
    }

    return {
      userId: decoded.sub,
      email: decoded.email,
      role: decoded.role,
    };
  }

  verifyRefreshToken(token: string): RefreshTokenPayload {
    const decoded = jwt.verify(token, this.REFRESH_TOKEN_SECRET, {
      issuer: 'your-app.com',
      audience: 'your-app.com',
    }) as any;

    if (decoded.type !== 'refresh') {
      throw new Error('Invalid token type');
    }

    return {
      userId: decoded.sub,
      tokenId: decoded.tokenId,
    };
  }
}

// Login endpoint
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  // Authenticate user
  const user = await authService.login(email, password);
  if (!user.success) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Generate tokens
  const tokenService = new TokenService();

  const accessToken = tokenService.generateAccessToken({
    userId: user.data.id,
    email: user.data.email,
    role: user.data.role,
  });

  const { token: refreshToken, tokenId } = tokenService.generateRefreshToken(
    user.data.id
  );

  // Store refresh token in database for revocation
  await db.refreshTokens.create({
    tokenId,
    userId: user.data.id,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    userAgent: req.headers['user-agent'],
    ip: req.ip,
  });

  // Set refresh token in httpOnly cookie
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,      // Prevents XSS
    secure: true,        // HTTPS only
    sameSite: 'strict',  // CSRF protection
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    path: '/api/auth/refresh',       // Limited scope
  });

  // Return access token
  res.json({
    accessToken,
    expiresIn: 900, // 15 minutes in seconds
    tokenType: 'Bearer',
  });
});

// Refresh token endpoint
app.post('/api/auth/refresh', async (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (!refreshToken) {
    return res.status(401).json({ error: 'Refresh token required' });
  }

  try {
    const tokenService = new TokenService();
    const decoded = tokenService.verifyRefreshToken(refreshToken);

    // Check if token is revoked
    const storedToken = await db.refreshTokens.findOne({
      tokenId: decoded.tokenId,
      userId: decoded.userId,
    });

    if (!storedToken || storedToken.revoked) {
      return res.status(401).json({ error: 'Token revoked' });
    }

    // Get user
    const user = await db.users.findOne({ id: decoded.userId });

    // Generate new access token
    const accessToken = tokenService.generateAccessToken({
      userId: user.id,
      email: user.email,
      role: user.role,
    });

    // Rotate refresh token
    const { token: newRefreshToken, tokenId: newTokenId } =
      tokenService.generateRefreshToken(user.id);

    // Revoke old refresh token
    await db.refreshTokens.update(storedToken.id, { revoked: true });

    // Store new refresh token
    await db.refreshTokens.create({
      tokenId: newTokenId,
      userId: user.id,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      userAgent: req.headers['user-agent'],
      ip: req.ip,
    });

    // Set new refresh token cookie
    res.cookie('refreshToken', newRefreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000,
      path: '/api/auth/refresh',
    });

    res.json({
      accessToken,
      expiresIn: 900,
      tokenType: 'Bearer',
    });
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Logout endpoint (revoke refresh token)
app.post('/api/auth/logout', async (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (refreshToken) {
    try {
      const tokenService = new TokenService();
      const decoded = tokenService.verifyRefreshToken(refreshToken);

      // Revoke token
      await db.refreshTokens.update(
        { tokenId: decoded.tokenId },
        { revoked: true }
      );
    } catch (error) {
      // Token already invalid, ignore
    }
  }

  // Clear cookie
  res.clearCookie('refreshToken', { path: '/api/auth/refresh' });
  res.json({ success: true });
});

// Protected endpoint middleware
const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1]; // Bearer <token>

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  try {
    const tokenService = new TokenService();
    const payload = tokenService.verifyAccessToken(token);

    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
};

// Use in routes
app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({ message: 'Protected data', user: req.user });
});
```

### JWT Security Checklist

```markdown
✅ JWT Security Checklist:

Token Configuration:
- [ ] Access token expiry: 15 minutes or less
- [ ] Refresh token expiry: 7 days or less
- [ ] JWT secret: minimum 32 characters (256 bits)
- [ ] Different secrets for access and refresh tokens
- [ ] Validate issuer and audience claims

Storage:
- [ ] Access token: memory or sessionStorage (not localStorage)
- [ ] Refresh token: httpOnly, secure, sameSite cookie
- [ ] Never store tokens in localStorage (XSS vulnerable)

Security:
- [ ] Refresh token rotation on each use
- [ ] Token revocation support (database storage)
- [ ] Rate limiting on token endpoints
- [ ] Log token issuance and validation
- [ ] Logout revokes refresh token

Claims:
- [ ] Include user ID, email, role
- [ ] Include token type (access/refresh)
- [ ] Include unique token ID for refresh tokens
- [ ] Set issuer and audience
- [ ] Never include sensitive data (password, SSN, etc.)
```

> **⚠️ OWASP Reference**: This prevents [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/).

---

## Rule 27: Apply Defense in Depth

**❌ Bad:** Single security layer

**✅ Good:** Multiple overlapping security controls

### How to Follow

- Layer security controls (don't rely on one)
- Authentication + authorization + validation
- Rate limiting + input validation + output encoding
- Fail securely (deny by default)
- Log security events at each layer

### Example

```typescript
// ❌ BAD: Single layer of security
app.post('/api/admin/users/:id/delete', async (req, res) => {
  // Only checks authentication - INSECURE!
  if (!req.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  await db.users.delete(req.params.id);
  res.json({ success: true });
});

// ✅ GOOD: Defense in Depth (Multiple Layers)
import rateLimit from 'express-rate-limit';
import { z } from 'zod';

// Layer 1: Rate limiting
const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: 'Too many requests',
});

// Layer 2: Authentication
const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    logger.warn('Missing authentication token', { ip: req.ip });
    return res.status(401).json({ error: 'Authentication required' });
  }

  try {
    const user = await tokenService.verify(token);
    req.user = user;
    next();
  } catch (error) {
    logger.warn('Invalid token', { error, ip: req.ip });
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Layer 3: Role-based authorization
const requireRole = (...allowedRoles: string[]) => {
  return (req, res, next) => {
    if (!req.user) {
      logger.error('requireRole called without authentication');
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      logger.warn('Insufficient permissions', {
        userId: req.user.id,
        userRole: req.user.role,
        requiredRoles: allowedRoles,
        endpoint: req.path,
      });
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
};

// Layer 4: Input validation
const deleteUserSchema = z.object({
  params: z.object({
    id: z.string().uuid('Invalid user ID'),
  }),
  body: z.object({
    reason: z.string().min(10).max(500),
    confirmDelete: z.literal(true),
  }),
});

// Layer 5: Business logic validation
const validateDeletion = async (req, res, next) => {
  const userId = req.params.id;

  // Prevent deleting yourself
  if (userId === req.user.id) {
    return res.status(400).json({ error: 'Cannot delete your own account' });
  }

  // Check if user has active subscriptions
  const hasActiveSubscriptions = await db.subscriptions.exists({
    userId,
    status: 'active',
  });

  if (hasActiveSubscriptions) {
    return res.status(400).json({
      error: 'Cannot delete user with active subscriptions',
    });
  }

  next();
};

// Layer 6: Audit logging
const auditLog = (action: string) => {
  return async (req, res, next) => {
    await db.auditLog.create({
      action,
      userId: req.user?.id,
      ip: req.ip,
      userAgent: req.headers['user-agent'],
      requestBody: req.body,
      timestamp: new Date(),
    });

    next();
  };
};

// Apply all layers
app.post(
  '/api/admin/users/:id/delete',
  strictLimiter,                      // Layer 1: Rate limiting
  authenticate,                        // Layer 2: Authentication
  requireRole('admin', 'superadmin'), // Layer 3: Role authorization
  validateRequest(deleteUserSchema),   // Layer 4: Input validation
  validateDeletion,                    // Layer 5: Business rules
  auditLog('user_deletion'),          // Layer 6: Audit logging
  async (req, res) => {
    try {
      const { id } = req.params;
      const { reason } = req.body;

      // Soft delete
      await db.users.update(id, {
        deleted: true,
        deletedAt: new Date(),
        deletedBy: req.user.id,
        deletionReason: reason,
      });

      // Additional cleanup
      await db.sessions.revokeAll(id);
      await db.refreshTokens.revokeAll(id);

      res.json({ success: true });
    } catch (error) {
      logger.error('User deletion failed', { error, userId: req.params.id });
      res.status(500).json({ error: 'Deletion failed' });
    }
  }
);
```

### Defense in Depth Checklist

```markdown
✅ Defense in Depth Layers:

Layer 1: Network Security
- [ ] Rate limiting on all endpoints
- [ ] DDoS protection (Cloudflare, AWS Shield)
- [ ] Firewall rules
- [ ] HTTPS only (TLS 1.3)

Layer 2: Authentication
- [ ] Token validation
- [ ] Session management
- [ ] Multi-factor authentication (MFA)
- [ ] Account lockout after failed attempts

Layer 3: Authorization
- [ ] Role-based access control (RBAC)
- [ ] Resource-level permissions
- [ ] Attribute-based access control (ABAC)
- [ ] Principle of least privilege

Layer 4: Input Validation
- [ ] Schema validation (Zod)
- [ ] Type checking (TypeScript)
- [ ] Length limits
- [ ] Format validation
- [ ] Business rule validation

Layer 5: Output Encoding
- [ ] HTML sanitization
- [ ] Context-specific encoding
- [ ] Content Security Policy (CSP)
- [ ] CORS configuration

Layer 6: Data Security
- [ ] Parameterized queries
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Sensitive data masking in logs

Layer 7: Monitoring & Logging
- [ ] Audit logging
- [ ] Security event monitoring
- [ ] Anomaly detection
- [ ] Alert system
```

---

## Rule 28: Log Security Events

**❌ Bad:** No logging or log everything including secrets

**✅ Good:** Log security-relevant events only, never sensitive data

### How to Follow

- Log authentication events (success and failure)
- Log authorization failures
- Log data modifications
- Never log passwords, tokens, or PII
- Include context (user ID, IP, timestamp)
- Use structured logging

### Example

```typescript
// ❌ BAD: Logging sensitive data
logger.info('User login', {
  email: user.email,
  password: password,           // NEVER LOG!
  passwordHash: user.password,  // NEVER LOG!
  creditCard: user.creditCard,  // NEVER LOG!
  ssn: user.ssn,               // NEVER LOG!
});

// ❌ BAD: No logging
app.post('/api/login', async (req, res) => {
  const user = await authService.login(req.body);
  res.json(user);
  // No logging of security event!
});

// ✅ GOOD: Secure structured logging
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'security.log', level: 'warn' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Security event types
enum SecurityEvent {
  LOGIN_SUCCESS = 'login_success',
  LOGIN_FAILED = 'login_failed',
  LOGOUT = 'logout',
  PASSWORD_RESET_REQUESTED = 'password_reset_requested',
  PASSWORD_CHANGED = 'password_changed',
  PERMISSION_DENIED = 'permission_denied',
  RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded',
  SUSPICIOUS_ACTIVITY = 'suspicious_activity',
  TOKEN_REVOKED = 'token_revoked',
  MFA_ENABLED = 'mfa_enabled',
  MFA_DISABLED = 'mfa_disabled',
  DATA_EXPORT = 'data_export',
  ADMIN_ACTION = 'admin_action',
}

interface SecurityLogContext {
  event: SecurityEvent;
  userId?: string;
  email?: string;
  ip: string;
  userAgent?: string;
  resource?: string;
  action?: string;
  result: 'success' | 'failure';
  reason?: string;
  metadata?: Record<string, any>;
}

class SecurityLogger {
  private static maskEmail(email: string): string {
    const [name, domain] = email.split('@');
    return `${name[0]}***@${domain}`;
  }

  private static maskIP(ip: string): string {
    // Mask last octet for IPv4
    const parts = ip.split('.');
    if (parts.length === 4) {
      return `${parts[0]}.${parts[1]}.${parts[2]}.***`;
    }
    return '***';
  }

  static log(context: SecurityLogContext): void {
    const logData = {
      timestamp: new Date().toISOString(),
      event: context.event,
      userId: context.userId,
      // Optionally mask email for privacy
      email: context.email ? this.maskEmail(context.email) : undefined,
      ip: this.maskIP(context.ip),
      userAgent: context.userAgent,
      resource: context.resource,
      action: context.action,
      result: context.result,
      reason: context.reason,
      metadata: context.metadata,
    };

    if (context.result === 'failure') {
      logger.warn('Security event', logData);
    } else {
      logger.info('Security event', logData);
    }
  }
}

// Usage in login endpoint
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await authService.login(email, password);

    if (!user.success) {
      // Log failed login
      SecurityLogger.log({
        event: SecurityEvent.LOGIN_FAILED,
        email,
        ip: req.ip,
        userAgent: req.headers['user-agent'],
        result: 'failure',
        reason: 'Invalid credentials',
      });

      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Log successful login
    SecurityLogger.log({
      event: SecurityEvent.LOGIN_SUCCESS,
      userId: user.data.id,
      email: user.data.email,
      ip: req.ip,
      userAgent: req.headers['user-agent'],
      result: 'success',
    });

    const token = tokenService.generate(user.data);
    res.json({ token });
  } catch (error) {
    logger.error('Login error', {
      error: error.message,
      stack: error.stack,
      ip: req.ip,
    });

    res.status(500).json({ error: 'Internal error' });
  }
});
```

### Security Logging Checklist

```markdown
✅ ALWAYS Log:
- [ ] Login attempts (success and failure)
- [ ] Logout events
- [ ] Password changes/resets
- [ ] Permission denied errors (403)
- [ ] Authentication failures (401)
- [ ] Rate limit violations
- [ ] Token revocations
- [ ] Admin actions
- [ ] Data exports
- [ ] Suspicious patterns
- [ ] MFA enable/disable
- [ ] Account lockouts

❌ NEVER Log:
- [ ] Passwords (plain or hashed)
- [ ] API keys or secrets
- [ ] JWT tokens
- [ ] Credit card numbers
- [ ] Social Security Numbers
- [ ] Personal health information
- [ ] Full session tokens
- [ ] Encryption keys

📝 Log Context (Include):
- [ ] Timestamp (ISO 8601)
- [ ] Event type
- [ ] User ID (if authenticated)
- [ ] IP address (optionally masked)
- [ ] User agent
- [ ] Resource accessed
- [ ] Action performed
- [ ] Result (success/failure)
- [ ] Failure reason (if applicable)

🔍 Monitoring:
- [ ] Centralized log aggregation
- [ ] Real-time alerting
- [ ] Anomaly detection
- [ ] Regular log review
- [ ] Log retention policy (90+ days)
- [ ] Secure log storage
```

> **⚠️ OWASP Reference**: This supports [A09:2021 – Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/).

---

## Summary: Security Best Practices

✅ **Do:**
- Store secrets in environment variables
- Let humans review security-critical code
- Validate all inputs with schemas
- Use parameterized queries or ORMs
- Sanitize output based on context
- Implement rate limiting on all endpoints
- Use bcrypt (cost 12+) or Argon2 for passwords
- Short-lived JWTs with refresh token rotation
- Apply defense in depth (multiple security layers)
- Log security events (without sensitive data)

❌ **Don't:**
- Hardcode secrets in code
- Let AI generate payment/auth logic alone
- Trust any user input
- Concatenate strings in SQL queries
- Display unsanitized user content
- Skip rate limiting
- Use MD5, SHA-1, or weak hashing
- Create long-lived tokens
- Rely on single security control
- Log passwords, tokens, or PII

---

## Security Checklist Summary

```markdown
🔒 Pre-Deployment Security Checklist:

Secrets Management:
- [ ] All secrets in environment variables
- [ ] No secrets in version control
- [ ] Secrets validated on startup
- [ ] .env files in .gitignore

Input Security:
- [ ] All inputs validated with schemas
- [ ] Parameterized queries only
- [ ] No string concatenation in SQL
- [ ] File upload restrictions

Output Security:
- [ ] HTML sanitization with DOMPurify
- [ ] Context-specific encoding
- [ ] Content Security Policy headers
- [ ] CORS properly configured

Authentication:
- [ ] Rate limiting on auth endpoints
- [ ] bcrypt (12+) or Argon2 for passwords
- [ ] Account lockout after failed attempts
- [ ] Secure session management

Authorization:
- [ ] Role-based access control
- [ ] Resource-level permissions
- [ ] Principle of least privilege
- [ ] Defense in depth applied

Tokens:
- [ ] Access tokens: 15 min expiry
- [ ] Refresh tokens: httpOnly cookies
- [ ] Token revocation implemented
- [ ] Strong secrets (32+ chars)

Logging:
- [ ] Security events logged
- [ ] Sensitive data never logged
- [ ] Centralized log aggregation
- [ ] Real-time alerting configured

Code Review:
- [ ] Human reviewed security code
- [ ] No AI-generated auth/payment logic
- [ ] Security tests passing
- [ ] OWASP Top 10 vulnerabilities checked
```

---

## OWASP Top 10 Reference

These rules help prevent vulnerabilities from the [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/):

- **A01: Broken Access Control** → Rules 20, 27
- **A02: Cryptographic Failures** → Rules 19, 25, 26
- **A03: Injection** → Rules 21, 22, 23
- **A04: Insecure Design** → Rules 20, 27
- **A05: Security Misconfiguration** → Rules 19, 23, 26
- **A07: Identification and Authentication Failures** → Rules 24, 25, 26
- **A09: Security Logging and Monitoring Failures** → Rule 28

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [01-prompts.md](./01-prompts.md) - Prompt engineering rules
- [02-architecture.md](./02-architecture.md) - Architecture rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Workflow checklist
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Security vulnerabilities
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/) - Security best practices
