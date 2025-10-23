# Code Quality & Testing Rules (Rules 29-42)

Rules for writing clean, testable code with AI assistance.

---

## Code Quality Rules (29-36)

### Rule 29: Explicit Over Implicit

**❌ Bad:** `function process(data) { ... }`

**✅ Good:** `function processUserData(data: UserData): ProcessedResult { ... }`

### How to Follow

- Use TypeScript for type safety
- Add explicit return types to all functions
- Name functions and variables descriptively
- Avoid ambiguous names (data, result, temp, obj)
- Make function purposes obvious from signatures

### Example

**❌ Bad (Implicit, Unclear):**

```typescript
// What does this function do? What are the types?
function process(data) {
  const result = data.map(x => x * 2);
  return result;
}

function handle(req, res) {
  // What is req? What shape is the response?
  const data = req.body;
  const result = service.do(data);
  res.send(result);
}

// Unclear variable names
function calc(a, b) {
  const c = a + b;
  const d = c * 0.08;
  return c + d;
}
```

**✅ Good (Explicit, Clear):**

```typescript
// Clear purpose, explicit types
function doubleNumbers(numbers: number[]): number[] {
  return numbers.map(num => num * 2);
}

// Explicit types for request/response
interface CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

interface CreateUserResponse {
  success: boolean;
  data?: UserDTO;
  error?: string;
}

async function createUserHandler(
  req: Request<{}, {}, CreateUserRequest>,
  res: Response<CreateUserResponse>
): Promise<void> {
  const userData: CreateUserRequest = req.body;
  const result: Result<UserDTO, Error> = await userService.createUser(userData);

  if (!result.success) {
    res.status(400).json({
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

// Descriptive variable names
function calculateOrderTotal(
  subtotal: number,
  taxRate: number
): OrderTotal {
  const taxAmount = subtotal * taxRate;
  const total = subtotal + taxAmount;

  return {
    subtotal,
    taxAmount,
    total,
  };
}
```

### Prompt Template for AI

```markdown
## Code Style Requirements

All code must be explicit:
- TypeScript with explicit return types
- No `any` types
- Descriptive function names (verb + noun pattern)
- Descriptive variable names (no abbreviations)
- Clear interfaces for all data structures
- JSDoc comments for public functions

Example:
```typescript
/**
 * Creates a new user account with email verification
 * @param userData - User registration data
 * @returns Result with user DTO or error
 */
async function createUserAccount(
  userData: CreateUserDTO
): Promise<Result<UserDTO, UserServiceError>> {
  // Implementation
}
```
```

---

## Rule 30: Small Functions

**❌ Bad:** 200-line functions doing multiple things

**✅ Good:** Functions under 50 lines with single responsibility

### How to Follow

- One function, one purpose
- Maximum 50 lines per function
- Extract complex logic into separate functions
- Use early returns to reduce nesting
- Limit nesting depth to 3 levels maximum
- If function needs comments to explain sections, split it

### Example

**❌ Bad (Large, Complex Function):**

```typescript
// 150+ lines, multiple responsibilities
async function processOrder(orderId: string) {
  // Get order
  const order = await db.orders.findOne({ id: orderId });
  if (!order) {
    throw new Error('Order not found');
  }

  // Validate inventory
  for (const item of order.items) {
    const product = await db.products.findOne({ id: item.productId });
    if (!product) {
      throw new Error(`Product not found: ${item.productId}`);
    }
    if (product.stock < item.quantity) {
      throw new Error(`Insufficient stock for ${product.name}`);
    }
  }

  // Calculate totals
  let subtotal = 0;
  for (const item of order.items) {
    const product = await db.products.findOne({ id: item.productId });
    subtotal += product.price * item.quantity;
  }
  const taxRate = 0.08;
  const tax = subtotal * taxRate;
  const shipping = subtotal > 50 ? 0 : 5;
  const total = subtotal + tax + shipping;

  // Process payment
  const paymentResult = await stripe.charges.create({
    amount: total * 100,
    currency: 'usd',
    source: order.paymentMethodId,
  });

  if (paymentResult.status !== 'succeeded') {
    throw new Error('Payment failed');
  }

  // Update inventory
  for (const item of order.items) {
    await db.products.update(
      { id: item.productId },
      { $inc: { stock: -item.quantity } }
    );
  }

  // Send confirmation email
  const emailHtml = `
    <h1>Order Confirmation</h1>
    <p>Thank you for your order!</p>
    <p>Order Total: $${total}</p>
  `;

  await sendEmail({
    to: order.customerEmail,
    subject: 'Order Confirmation',
    html: emailHtml,
  });

  // Update order status
  await db.orders.update(
    { id: orderId },
    {
      status: 'completed',
      subtotal,
      tax,
      shipping,
      total,
      completedAt: new Date(),
    }
  );

  return { success: true, orderId };
}
```

**✅ Good (Small, Focused Functions):**

```typescript
// Each function has single responsibility, under 50 lines

interface OrderProcessingResult {
  orderId: string;
  total: number;
  chargeId: string;
}

async function processOrder(
  orderId: string
): Promise<Result<OrderProcessingResult, Error>> {
  // Orchestrate order processing steps
  const order = await getOrderById(orderId);
  if (!order.success) {
    return order;
  }

  const validationResult = await validateOrderInventory(order.data);
  if (!validationResult.success) {
    return validationResult;
  }

  const totals = await calculateOrderTotals(order.data);
  if (!totals.success) {
    return totals;
  }

  const paymentResult = await processPayment(
    order.data.paymentMethodId,
    totals.data.total
  );
  if (!paymentResult.success) {
    return paymentResult;
  }

  await updateInventory(order.data.items);
  await sendOrderConfirmation(order.data, totals.data);
  await markOrderComplete(orderId, totals.data);

  return ok({
    orderId,
    total: totals.data.total,
    chargeId: paymentResult.data.id,
  });
}

async function getOrderById(
  orderId: string
): Promise<Result<Order, Error>> {
  try {
    const order = await db.orders.findOne({ id: orderId });

    if (!order) {
      return err(new OrderNotFoundError(orderId));
    }

    return ok(order);
  } catch (error) {
    return err(error as Error);
  }
}

async function validateOrderInventory(
  order: Order
): Promise<Result<void, Error>> {
  for (const item of order.items) {
    const product = await db.products.findOne({ id: item.productId });

    if (!product) {
      return err(new ProductNotFoundError(item.productId));
    }

    if (product.stock < item.quantity) {
      return err(new InsufficientStockError(product.name, item.quantity));
    }
  }

  return ok(undefined);
}

interface OrderTotals {
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
}

async function calculateOrderTotals(
  order: Order
): Promise<Result<OrderTotals, Error>> {
  try {
    let subtotal = 0;

    for (const item of order.items) {
      const product = await db.products.findOne({ id: item.productId });
      if (!product) {
        return err(new ProductNotFoundError(item.productId));
      }
      subtotal += product.price * item.quantity;
    }

    const tax = subtotal * config.business.taxRate;
    const shipping = subtotal > config.business.freeShippingThreshold
      ? 0
      : config.business.shippingFee;
    const total = subtotal + tax + shipping;

    return ok({ subtotal, tax, shipping, total });
  } catch (error) {
    return err(error as Error);
  }
}

async function processPayment(
  paymentMethodId: string,
  amount: number
): Promise<Result<ChargeResult, Error>> {
  try {
    const charge = await stripe.charges.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency: 'usd',
      payment_method: paymentMethodId,
    });

    if (charge.status !== 'succeeded') {
      return err(new PaymentFailedError('Payment was not successful'));
    }

    return ok({
      id: charge.id,
      amount: charge.amount / 100,
      status: charge.status,
    });
  } catch (error) {
    return err(new PaymentFailedError((error as Error).message));
  }
}

async function updateInventory(items: OrderItem[]): Promise<void> {
  for (const item of items) {
    await db.products.update(
      { id: item.productId },
      { $inc: { stock: -item.quantity } }
    );
  }
}

async function sendOrderConfirmation(
  order: Order,
  totals: OrderTotals
): Promise<void> {
  const emailContent = generateOrderConfirmationEmail(order, totals);

  await emailService.send({
    to: order.customerEmail,
    subject: 'Order Confirmation',
    html: emailContent,
  });
}

function generateOrderConfirmationEmail(
  order: Order,
  totals: OrderTotals
): string {
  return `
    <h1>Order Confirmation</h1>
    <p>Thank you for your order!</p>
    <p>Order #${order.id}</p>
    <p>Total: $${totals.total.toFixed(2)}</p>
  `;
}

async function markOrderComplete(
  orderId: string,
  totals: OrderTotals
): Promise<void> {
  await db.orders.update(
    { id: orderId },
    {
      status: 'completed',
      ...totals,
      completedAt: new Date(),
    }
  );
}
```

### Benefits of Small Functions

- Easier to test
- Easier to understand
- Easier to reuse
- Easier to debug
- Self-documenting code
- Clear error handling at each step

### Prompt Template for AI

```markdown
## Function Size Requirements

All functions must:
- Be under 50 lines (hard limit)
- Have single responsibility
- Use early returns (no else after return)
- Maximum nesting depth: 3 levels
- Extract complex logic into separate functions

If function needs section comments, split into multiple functions.

Example:
```typescript
// WRONG: One large function
async function processOrder(order: Order) {
  // Get products (20 lines)
  // Calculate totals (15 lines)
  // Process payment (25 lines)
  // Update database (15 lines)
}

// RIGHT: Multiple focused functions
async function processOrder(order: Order) {
  const products = await fetchOrderProducts(order);
  const totals = calculateOrderTotals(products);
  const payment = await processOrderPayment(totals);
  await updateOrderRecord(order.id, payment);
}
```
```

---

## Rule 31: No Magic Numbers

**❌ Bad:** `if (user.age > 18)`, `setTimeout(fn, 3600000)`

**✅ Good:** `if (user.age > MINIMUM_AGE)`, `setTimeout(fn, ONE_HOUR_MS)`

### How to Follow

- Extract all numeric literals to named constants
- Extract string literals to constants
- Use enums for related constants
- Group constants in configuration objects
- Document the meaning of constants

### Example

**❌ Bad (Magic Numbers):**

```typescript
// What do these numbers mean?
function processPayment(amount: number) {
  if (amount < 10) {
    throw new Error('Amount too small');
  }

  if (amount > 10000) {
    throw new Error('Amount too large');
  }

  const fee = amount * 0.029 + 0.30;
  return amount + fee;
}

function isSessionValid(session: Session) {
  const age = Date.now() - session.createdAt;
  return age < 3600000; // What is this number?
}

// String literals everywhere
if (user.status === 'active' && user.role === 'admin') {
  // What are all possible statuses and roles?
}
```

**✅ Good (Named Constants):**

```typescript
// Constants with clear meaning
const PAYMENT_CONSTRAINTS = {
  MINIMUM_AMOUNT: 10, // Minimum payment in USD
  MAXIMUM_AMOUNT: 10_000, // Maximum payment in USD
  STRIPE_FEE_PERCENT: 0.029, // 2.9%
  STRIPE_FEE_FIXED: 0.30, // $0.30
} as const;

const TIME_CONSTANTS = {
  ONE_SECOND_MS: 1_000,
  ONE_MINUTE_MS: 60_000,
  ONE_HOUR_MS: 3_600_000,
  ONE_DAY_MS: 86_400_000,
  SESSION_DURATION_MS: 3_600_000, // 1 hour
} as const;

// Using named constants
function processPayment(amount: number): PaymentResult {
  if (amount < PAYMENT_CONSTRAINTS.MINIMUM_AMOUNT) {
    throw new ValidationError(
      `Minimum payment is $${PAYMENT_CONSTRAINTS.MINIMUM_AMOUNT}`
    );
  }

  if (amount > PAYMENT_CONSTRAINTS.MAXIMUM_AMOUNT) {
    throw new ValidationError(
      `Maximum payment is $${PAYMENT_CONSTRAINTS.MAXIMUM_AMOUNT}`
    );
  }

  const percentageFee = amount * PAYMENT_CONSTRAINTS.STRIPE_FEE_PERCENT;
  const fixedFee = PAYMENT_CONSTRAINTS.STRIPE_FEE_FIXED;
  const totalFee = percentageFee + fixedFee;

  return {
    amount,
    fee: totalFee,
    total: amount + totalFee,
  };
}

function isSessionValid(session: Session): boolean {
  const sessionAge = Date.now() - session.createdAt;
  return sessionAge < TIME_CONSTANTS.SESSION_DURATION_MS;
}

// Enums for related constants
enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
  PENDING = 'pending',
}

enum UserRole {
  USER = 'user',
  ADMIN = 'admin',
  MODERATOR = 'moderator',
  SUPERADMIN = 'superadmin',
}

// Clear, type-safe usage
if (user.status === UserStatus.ACTIVE && user.role === UserRole.ADMIN) {
  // All possible values are visible in autocomplete
}
```

### Business Rules as Constants

```typescript
// Business rules configuration
export const BUSINESS_RULES = {
  order: {
    MINIMUM_ORDER_AMOUNT: 10,
    MAXIMUM_ORDER_AMOUNT: 10_000,
    FREE_SHIPPING_THRESHOLD: 50,
    TAX_RATE: 0.08, // 8%
    DEFAULT_SHIPPING_FEE: 5,
  },

  user: {
    MINIMUM_AGE: 18,
    MINIMUM_PASSWORD_LENGTH: 8,
    MAXIMUM_PASSWORD_LENGTH: 128,
    MAX_LOGIN_ATTEMPTS: 5,
    ACCOUNT_LOCKOUT_DURATION_MS: 15 * 60 * 1000, // 15 minutes
  },

  email: {
    VERIFICATION_TOKEN_EXPIRY_MS: 24 * 60 * 60 * 1000, // 24 hours
    PASSWORD_RESET_EXPIRY_MS: 60 * 60 * 1000, // 1 hour
    MAX_SEND_ATTEMPTS: 3,
  },

  api: {
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
    REQUEST_TIMEOUT_MS: 30_000, // 30 seconds
  },
} as const;

// Usage
function validateOrder(order: CreateOrderDTO): Result<void, ValidationError> {
  if (order.total < BUSINESS_RULES.order.MINIMUM_ORDER_AMOUNT) {
    return err(
      new ValidationError(
        `Minimum order amount is $${BUSINESS_RULES.order.MINIMUM_ORDER_AMOUNT}`
      )
    );
  }

  if (order.total > BUSINESS_RULES.order.MAXIMUM_ORDER_AMOUNT) {
    return err(
      new ValidationError(
        `Maximum order amount is $${BUSINESS_RULES.order.MAXIMUM_ORDER_AMOUNT}`
      )
    );
  }

  return ok(undefined);
}
```

### Prompt Template for AI

```markdown
## Constants Requirements

No magic numbers or strings:
- Extract all numeric literals to named constants
- Extract all string literals (except log messages)
- Use enums for related string constants
- Group related constants in objects
- Add comments explaining what each constant means

Example:
```typescript
// WRONG
if (amount > 100 && age > 18) {
  setTimeout(fn, 3600000);
}

// RIGHT
const LIMITS = {
  MINIMUM_PURCHASE: 100, // Minimum purchase in USD
  MINIMUM_AGE: 18, // Legal age requirement
};

const TIME = {
  ONE_HOUR_MS: 3_600_000,
};

if (amount > LIMITS.MINIMUM_PURCHASE && age > LIMITS.MINIMUM_AGE) {
  setTimeout(fn, TIME.ONE_HOUR_MS);
}
```
```

---

## Rule 32: Meaningful Variable Names

**❌ Bad:** `const d = new Date()`, `const temp = x + y`

**✅ Good:** `const currentDate = new Date()`, `const totalPrice = basePrice + tax`

### How to Follow

- Use full words, avoid abbreviations
- Be specific: `userEmail` not `email`
- Use boolean prefixes: `isValid`, `hasPermission`, `shouldRetry`
- Use verb+noun for functions: `calculateTotal`, `fetchUser`
- Avoid single letters except in small loops
- Name arrays plurally: `users`, `products`
- Avoid generic names: `data`, `info`, `temp`, `obj`

### Example

**❌ Bad (Unclear Names):**

```typescript
// What are these variables?
const d = new Date();
const x = user.a * 0.08;
const temp = calc(a, b);
const data = await fetch();
const result = process(data);

// Unclear function name
function handle(req, res) {
  const obj = req.body;
  const r = service.do(obj);
  res.send(r);
}

// Unclear loop variables
for (const i of arr) {
  for (const j of i.items) {
    const t = j.p * j.q;
    total += t;
  }
}
```

**✅ Good (Clear Names):**

```typescript
// Clear, descriptive names
const currentDate = new Date();
const taxAmount = userSubtotal * TAX_RATE;
const totalPrice = calculateTotalPrice(basePrice, taxAmount);
const userData = await fetchUserData();
const processedResult = processUserData(userData);

// Clear function purpose
async function createUserHandler(
  req: Request<{}, {}, CreateUserRequest>,
  res: Response<CreateUserResponse>
): Promise<void> {
  const registrationData = req.body;
  const userResult = await userService.createUser(registrationData);
  res.status(201).json(userResult);
}

// Clear loop variables
for (const order of orders) {
  for (const orderItem of order.items) {
    const itemTotal = orderItem.price * orderItem.quantity;
    orderTotal += itemTotal;
  }
}

// Boolean naming conventions
const isUserAuthenticated = !!req.user;
const hasAdminPermission = req.user.role === UserRole.ADMIN;
const shouldSendEmail = user.emailVerified && !user.emailOptOut;

if (isUserAuthenticated && hasAdminPermission) {
  // Allow access
}

if (shouldSendEmail) {
  await sendWelcomeEmail(user.email);
}
```

### Function Naming Patterns

```typescript
// Getter functions: get/fetch + noun
async function getUserById(id: string): Promise<User> { }
async function fetchOrderDetails(orderId: string): Promise<Order> { }

// Boolean functions: is/has/should/can + adjective/noun
function isEmailValid(email: string): boolean { }
function hasActiveSubscription(user: User): boolean { }
function shouldRetryRequest(attempt: number): boolean { }
function canUserAccessResource(user: User, resource: Resource): boolean { }

// Action functions: verb + noun
async function createUser(data: CreateUserDTO): Promise<User> { }
async function updateUserProfile(userId: string, data: UpdateProfileDTO): Promise<User> { }
async function deleteOrder(orderId: string): Promise<void> { }
async function calculateOrderTotal(order: Order): Promise<number> { }
async function sendVerificationEmail(email: string): Promise<void> { }

// Transformation functions: verb + from + to
function convertDollarsToCents(dollars: number): number { }
function parseUserDataFromRequest(req: Request): UserData { }
function formatDateToISO(date: Date): string { }
```

### Complex Example

```typescript
// ❌ BAD: Unclear variable names
async function proc(o) {
  const i = o.items;
  let t = 0;

  for (const x of i) {
    const p = await db.findOne({ id: x.id });
    const c = p.price * x.qty;
    t += c;
  }

  const r = t * 0.08;
  const s = t > 50 ? 0 : 5;
  const f = t + r + s;

  return { t, r, s, f };
}

// ✅ GOOD: Clear, descriptive names
interface OrderTotals {
  subtotal: number;
  taxAmount: number;
  shippingFee: number;
  grandTotal: number;
}

async function calculateOrderTotals(order: Order): Promise<OrderTotals> {
  const orderItems = order.items;
  let subtotal = 0;

  for (const orderItem of orderItems) {
    const product = await productRepository.findById(orderItem.productId);
    const itemTotal = product.price * orderItem.quantity;
    subtotal += itemTotal;
  }

  const taxAmount = subtotal * TAX_RATE;
  const shippingFee = subtotal > FREE_SHIPPING_THRESHOLD
    ? 0
    : STANDARD_SHIPPING_FEE;
  const grandTotal = subtotal + taxAmount + shippingFee;

  return {
    subtotal,
    taxAmount,
    shippingFee,
    grandTotal,
  };
}
```

### Prompt Template for AI

```markdown
## Variable Naming Requirements

All variables must:
- Use full words (no abbreviations except standard ones: URL, ID, API)
- Be descriptive and specific
- Use camelCase for variables and functions
- Use PascalCase for classes and types
- Use UPPER_SNAKE_CASE for constants

Naming patterns:
- Booleans: is/has/should/can + descriptor
- Functions: verb + noun (createUser, fetchOrders)
- Collections: plural nouns (users, products, orderItems)
- Single items: singular nouns (user, product, orderItem)

Examples:
```typescript
// WRONG
const d = new Date();
const temp = x + y;
function proc(data) { }

// RIGHT
const currentTimestamp = new Date();
const totalPrice = basePrice + taxAmount;
function processOrderPayment(orderData: OrderData) { }
```
```

---

## Rule 33: DRY (Don't Repeat Yourself)

**❌ Bad:** Copy-paste code in multiple places

**✅ Good:** Extract to reusable function/utility

### How to Follow

- If code appears 3+ times, extract it
- Create utility functions for common operations
- Use higher-order functions for patterns
- Leverage composition over duplication
- Share validation logic
- Reuse type definitions

### Example

**❌ Bad (Repeated Code):**

```typescript
// Email validation repeated in multiple places
app.post('/register', async (req, res) => {
  const { email } = req.body;

  // Email validation
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const emailParts = email.split('@');
  if (emailParts.length !== 2 || !emailParts[1].includes('.')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // ... rest of registration
});

app.post('/update-profile', async (req, res) => {
  const { email } = req.body;

  // Same validation repeated
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const emailParts = email.split('@');
  if (emailParts.length !== 2 || !emailParts[1].includes('.')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // ... rest of update
});

app.post('/invite-user', async (req, res) => {
  const { email } = req.body;

  // Same validation again
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const emailParts = email.split('@');
  if (emailParts.length !== 2 || !emailParts[1].includes('.')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // ... rest of invite
});
```

**✅ Good (DRY, Reusable):**

```typescript
// Shared validation schema
import { z } from 'zod';

export const emailSchema = z.string()
  .email('Invalid email format')
  .max(255, 'Email too long')
  .toLowerCase()
  .trim();

export const userRegistrationSchema = z.object({
  email: emailSchema,
  name: z.string().min(2).max(100).trim(),
  password: z.string().min(8),
});

export const profileUpdateSchema = z.object({
  email: emailSchema.optional(),
  name: z.string().min(2).max(100).trim().optional(),
});

// Reusable validation middleware
function validateRequest<T>(schema: z.ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      const validated = schema.parse(req.body);
      req.body = validated; // Replace with validated data
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      } else {
        next(error);
      }
    }
  };
}

// Use shared validation
app.post('/register',
  validateRequest(userRegistrationSchema),
  registerHandler
);

app.post('/update-profile',
  authenticate,
  validateRequest(profileUpdateSchema),
  updateProfileHandler
);

app.post('/invite-user',
  authenticate,
  requireRole('admin'),
  validateRequest(z.object({ email: emailSchema })),
  inviteUserHandler
);
```

### Utility Functions Example

```typescript
// ❌ BAD: Repeated error handling
async function createUser(data) {
  try {
    const user = await db.users.create(data);
    return { success: true, data: user };
  } catch (error) {
    logger.error('Create user failed', { error });
    return { success: false, error: error.message };
  }
}

async function createProduct(data) {
  try {
    const product = await db.products.create(data);
    return { success: true, data: product };
  } catch (error) {
    logger.error('Create product failed', { error });
    return { success: false, error: error.message };
  }
}

async function createOrder(data) {
  try {
    const order = await db.orders.create(data);
    return { success: true, data: order };
  } catch (error) {
    logger.error('Create order failed', { error });
    return { success: false, error: error.message };
  }
}

// ✅ GOOD: Extracted utility
async function wrapDatabaseOperation<T>(
  operation: () => Promise<T>,
  errorContext: string
): Promise<Result<T, Error>> {
  try {
    const data = await operation();
    return { success: true, data };
  } catch (error) {
    logger.error(`${errorContext} failed`, { error });
    return {
      success: false,
      error: error instanceof Error ? error : new Error('Unknown error'),
    };
  }
}

// Reuse utility
async function createUser(
  data: CreateUserDTO
): Promise<Result<User, Error>> {
  return wrapDatabaseOperation(
    () => db.users.create(data),
    'Create user'
  );
}

async function createProduct(
  data: CreateProductDTO
): Promise<Result<Product, Error>> {
  return wrapDatabaseOperation(
    () => db.products.create(data),
    'Create product'
  );
}

async function createOrder(
  data: CreateOrderDTO
): Promise<Result<Order, Error>> {
  return wrapDatabaseOperation(
    () => db.orders.create(data),
    'Create order'
  );
}
```

### Higher-Order Functions

```typescript
// ❌ BAD: Repeated authorization logic
app.get('/admin/users', async (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  // Handler logic
});

app.post('/admin/products', async (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  // Handler logic
});

app.delete('/admin/orders/:id', async (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  // Handler logic
});

// ✅ GOOD: Reusable middleware
function requireRole(...allowedRoles: UserRole[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      logger.warn('Unauthorized access attempt', {
        userId: req.user.id,
        role: req.user.role,
        requiredRoles: allowedRoles,
      });
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
}

// Use middleware
app.get('/admin/users', requireRole(UserRole.ADMIN), getUsersHandler);
app.post('/admin/products', requireRole(UserRole.ADMIN), createProductHandler);
app.delete('/admin/orders/:id', requireRole(UserRole.ADMIN), deleteOrderHandler);
```

### Prompt Template for AI

```markdown
## DRY Requirements

Avoid code duplication:
- Extract repeated code into utility functions
- Share validation schemas across endpoints
- Use middleware for repeated request logic
- Create higher-order functions for patterns
- Share type definitions across files

If code appears 2+ times, extract it into:
- Utility function in /shared/utils/
- Middleware in /shared/middleware/
- Validation schema in /shared/validators/
- Type definition in /shared/types/

Example:
```typescript
// WRONG: Copy-paste validation
function handler1(req) {
  if (!req.body.email || !isValid(req.body.email)) { ... }
}
function handler2(req) {
  if (!req.body.email || !isValid(req.body.email)) { ... }
}

// RIGHT: Shared validation
const emailSchema = z.string().email();
function validateEmail(schema) { ... }

// Use everywhere
handler1: validateEmail(emailSchema)
handler2: validateEmail(emailSchema)
```
```

---

## Rule 34: Comment Why, Not What

**❌ Bad:** `// Increment counter` → `counter++;`

**✅ Good:** `// Retry mechanism requires exponential backoff` → `delay *= 2;`

### How to Follow

- Don't comment obvious code
- Explain business logic and decisions
- Document edge cases and workarounds
- Note performance optimizations
- Link to tickets/issues for context
- Explain non-obvious algorithms
- Document WHY, not WHAT

### Example

**❌ Bad (Useless Comments):**

```typescript
// Bad: Comments that just repeat the code
// Increment i
i++;

// Set user name
user.name = 'John';

// Call the API
const response = await fetch(url);

// Check if user exists
if (user) {
  // Return user
  return user;
}

// Create a new date
const date = new Date();

// Loop through array
for (const item of items) {
  // Process item
  process(item);
}
```

**✅ Good (Useful Comments):**

```typescript
// Explain WHY, business logic, edge cases

// Stripe requires amounts in cents (smallest currency unit)
const amountInCents = Math.round(amountInDollars * 100);

// Rate limit: 5 attempts per 15 minutes to prevent brute force attacks
// See: https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks
if (loginAttempts >= 5) {
  throw new TooManyAttemptsError();
}

// WORKAROUND: Prisma doesn't support upsert with complex where clauses
// See issue: https://github.com/prisma/prisma/issues/12345
// Manually check existence then update or create
const existingUser = await db.user.findUnique({ where: { email } });
if (existingUser) {
  return db.user.update({ where: { id: existingUser.id }, data });
} else {
  return db.user.create({ data });
}

// Cache for 5 minutes to reduce database load during peak hours
// Average query time: 200ms, cache hit rate: 85%
await redis.setex(cacheKey, 300, JSON.stringify(data));

// Exponential backoff: retry with increasing delays (1s, 2s, 4s, 8s)
// Prevents overwhelming downstream services during incidents
const delay = Math.min(1000 * Math.pow(2, attempt), MAX_DELAY);
await sleep(delay);

// SECURITY: Always use timing-safe comparison to prevent timing attacks
// See: https://en.wikipedia.org/wiki/Timing_attack
const isValid = crypto.timingSafeEqual(
  Buffer.from(providedToken),
  Buffer.from(storedToken)
);

// Edge case: Empty string is technically valid but meaningless for search
// Return early to avoid unnecessary database query
if (searchQuery.trim() === '') {
  return { results: [], total: 0 };
}
```

### JSDoc for Public APIs

```typescript
/**
 * Creates a new user account with email verification
 *
 * This function:
 * 1. Validates user input against schema
 * 2. Checks for duplicate email (case-insensitive)
 * 3. Hashes password with bcrypt (cost factor 12)
 * 4. Generates verification token
 * 5. Sends verification email
 * 6. Returns user without sensitive data
 *
 * @param userData - User registration data
 * @returns Result with created user or error
 *
 * @example
 * ```typescript
 * const result = await createUser({
 *   email: 'user@example.com',
 *   name: 'John Doe',
 *   password: 'SecurePass123!',
 * });
 *
 * if (result.success) {
 *   console.log('User created:', result.data.id);
 * }
 * ```
 *
 * @throws Never throws - returns Result type with error
 *
 * @see {@link UserService} for related operations
 */
async function createUser(
  userData: CreateUserDTO
): Promise<Result<UserDTO, UserServiceError>> {
  // Implementation
}
```

### Complex Algorithm Example

```typescript
/**
 * Calculate optimal shipping route using Dijkstra's algorithm
 *
 * Why Dijkstra: Guarantees shortest path for non-negative edge weights.
 * Our shipping costs are always positive, making this optimal.
 *
 * Performance: O(V²) where V is number of warehouses.
 * For our current scale (< 100 warehouses), this is acceptable.
 * If we exceed 500 warehouses, consider A* algorithm instead.
 *
 * Edge cases handled:
 * - Isolated warehouses (no path): Returns null
 * - Equal-cost paths: Returns first found (deterministic)
 * - Self-loops: Ignored (cost 0 for same warehouse)
 */
function calculateOptimalShippingRoute(
  sourceWarehouse: Warehouse,
  targetWarehouse: Warehouse,
  warehouseNetwork: WarehouseGraph
): ShippingRoute | null {
  // Implementation with minimal inline comments
  // The function name and JSDoc explain WHAT and WHY
}
```

### Prompt Template for AI

```markdown
## Comment Requirements

Comments must explain WHY, not WHAT:
- Don't comment obvious code
- Explain business logic decisions
- Document edge cases and workarounds
- Note performance characteristics
- Link to relevant issues/tickets
- Use JSDoc for public functions

Examples of GOOD comments:
```typescript
// Stripe requires amounts in cents, not dollars
const cents = dollars * 100;

// WORKAROUND: Library bug #123 - double encoding issue
const decoded = decodeURIComponent(decodeURIComponent(input));

// Rate limit to prevent abuse (OWASP recommendation)
if (attempts > 5) throw new RateLimitError();
```

Examples of BAD comments:
```typescript
// Increment i (obvious from code)
i++;

// Create user (function name already says this)
const user = await createUser(data);
```

Add JSDoc to all exported functions with:
- Clear description
- Parameter descriptions
- Return type description
- Example usage if complex
```
```

---

## Rule 35: Handle Errors Gracefully

**❌ Bad:** Empty catch blocks, generic error messages

**✅ Good:** Specific error handling with logging and recovery

### How to Follow

- Never use empty catch blocks
- Log errors with context
- Return specific error messages
- Handle different error types differently
- Provide recovery mechanisms
- Use Result types for expected errors
- Only throw for truly exceptional cases

### Example

**❌ Bad (Poor Error Handling):**

```typescript
// Empty catch blocks - errors silently swallowed
try {
  await processPayment(order);
} catch (error) {
  // Nothing happens!
}

// Generic error handling
try {
  const user = await createUser(data);
} catch (error) {
  res.status(500).json({ error: 'Error' }); // Not helpful!
}

// Catching and re-throwing without adding value
try {
  await updateDatabase();
} catch (error) {
  throw error; // Why catch at all?
}

// Not handling specific errors
try {
  const data = await fetchData();
  const parsed = JSON.parse(data);
} catch (error) {
  // Could be network error OR parse error, handled the same way
  throw new Error('Failed');
}
```

**✅ Good (Comprehensive Error Handling):**

```typescript
import type { Result } from '@/shared/types/result';
import { ok, err } from '@/shared/types/result';

// Handle different error types specifically
async function createUser(
  userData: CreateUserDTO
): Promise<Result<UserDTO, UserServiceError>> {
  try {
    // Validate input
    const validationResult = userSchema.safeParse(userData);
    if (!validationResult.success) {
      return err(new ValidationError(validationResult.error.errors));
    }

    // Check for existing user
    const existingUser = await db.users.findUnique({
      where: { email: userData.email }
    });

    if (existingUser) {
      // Expected error - handle gracefully
      logger.info('Duplicate email registration attempt', {
        email: userData.email,
      });
      return err(new EmailAlreadyExistsError(userData.email));
    }

    // Hash password
    const passwordHash = await bcrypt.hash(userData.password, 12);

    // Create user
    const user = await db.users.create({
      data: {
        ...userData,
        password: passwordHash,
      },
    });

    // Remove sensitive data
    const { password, ...userDTO } = user;
    logger.info('User created successfully', { userId: user.id });

    return ok(userDTO);

  } catch (error) {
    // Handle specific error types
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      // Database constraint violation
      if (error.code === 'P2002') {
        return err(new DuplicateRecordError('User with this email exists'));
      }

      // Foreign key constraint
      if (error.code === 'P2003') {
        return err(new InvalidReferenceError('Invalid reference in user data'));
      }

      // Log database error with context
      logger.error('Database error creating user', {
        error: error.message,
        code: error.code,
        meta: error.meta,
      });

      return err(new DatabaseError('Failed to create user'));
    }

    if (error instanceof Prisma.PrismaClientValidationError) {
      logger.error('Prisma validation error', { error: error.message });
      return err(new ValidationError('Invalid user data format'));
    }

    // Unexpected errors
    logger.error('Unexpected error creating user', {
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      userData: {
        email: userData.email,
        // Don't log sensitive data
      },
    });

    return err(new UnexpectedError('An unexpected error occurred'));
  }
}

// HTTP layer error handling
app.post('/api/users', async (req, res) => {
  const result = await userService.createUser(req.body);

  if (!result.success) {
    const error = result.error;

    // Map service errors to HTTP responses
    if (error instanceof ValidationError) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: error.details,
      });
    }

    if (error instanceof EmailAlreadyExistsError) {
      return res.status(409).json({
        success: false,
        error: 'Email address already registered',
      });
    }

    if (error instanceof DatabaseError) {
      // Don't expose database internals to client
      return res.status(500).json({
        success: false,
        error: 'Unable to create user account. Please try again later.',
      });
    }

    // Generic error response for unexpected errors
    return res.status(500).json({
      success: false,
      error: 'An unexpected error occurred',
    });
  }

  // Success response
  res.status(201).json({
    success: true,
    data: result.data,
  });
});
```

### Prompt Template for AI

```markdown
## Error Handling Requirements

All error handling must:
- Never use empty catch blocks
- Log errors with context (no sensitive data)
- Return Result<T, E> for expected errors
- Handle specific error types differently
- Provide helpful error messages
- Include recovery mechanisms where appropriate

Example:
```typescript
async function operation(): Promise<Result<Data, Error>> {
  try {
    const data = await fetchData();
    return ok(data);
  } catch (error) {
    // Handle specific error types
    if (error instanceof NetworkError) {
      logger.warn('Network error, will retry', { error });
      return err(new TemporaryError('Network unavailable'));
    }

    if (error instanceof ValidationError) {
      logger.info('Validation failed', { error });
      return err(error);
    }

    // Unexpected errors
    logger.error('Unexpected error', {
      error: error.message,
      stack: error.stack,
    });
    return err(new UnexpectedError('Operation failed'));
  }
}
```
```

---

## Rule 36: Use TypeScript Strictly

**❌ Bad:** `any` types everywhere, weak type checking

**✅ Good:** Explicit types with strict mode enabled

### How to Follow

- Enable strict mode in tsconfig.json
- No `any` types (use `unknown` if truly unknown)
- Explicit function return types
- Enable all strict options
- Use type guards for runtime type checking
- Prefer interfaces over types for objects
- Use discriminated unions for variants

### Example

**✅ Good (Strict TypeScript):**

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
  }
}

// Explicit types everywhere
interface ProductData {
  id: string;
  name: string;
  price: number;
}

function processProducts(products: ProductData[]): number[] {
  return products.map((product: ProductData): number => product.price);
}

interface OrderItem {
  productId: string;
  quantity: number;
  price: number;
}

function calculateTotal(items: OrderItem[]): number {
  let total = 0;

  for (const item of items) {
    total += item.price * item.quantity;
  }

  return total;
}
```

### Prompt Template for AI

```markdown
## TypeScript Requirements

All code must use strict TypeScript:
- Enable strict mode in tsconfig.json
- No `any` types (use `unknown` if truly unknown)
- Explicit return types on all functions
- Explicit types on all parameters
- Use interfaces for object shapes
- Use discriminated unions for variants
- Runtime validation before type assertions (use Zod)

tsconfig.json must include:
```json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "noUncheckedIndexedAccess": true,
  "noImplicitReturns": true
}
```

Example:
```typescript
// WRONG
function process(data: any): any {
  return data.map(x => x.value);
}

// RIGHT
interface DataItem {
  id: string;
  value: number;
}

function processData(data: DataItem[]): number[] {
  return data.map((item: DataItem): number => item.value);
}
```
```

---

## Testing Rules (37-42)

### Rule 37: Test Everything AI Generates

**❌ Bad:** Deploy AI code without tests

**✅ Good:** 90%+ test coverage before merge

### How to Follow

- Request tests in initial AI prompt
- Test all public functions
- Cover happy path + error cases
- Test edge cases and boundaries
- Aim for 90%+ code coverage
- Run tests before code review

**See also:** [Rules 38-42 for detailed testing guidelines](#rule-38-test-business-logic-not-framework)

---

## Rule 38: Test Business Logic, Not Framework

**❌ Bad:** Test Express.js/framework internals

**✅ Good:** Test your business logic and service layer

### How to Follow

- Focus tests on service layer (business logic)
- Mock external dependencies (database, APIs)
- Test pure functions thoroughly
- Minimal framework/HTTP testing
- Integration tests only for critical paths

---

## Rule 39: Arrange-Act-Assert Pattern

**❌ Bad:** Mixed test logic, unclear structure

**✅ Good:** Clear AAA structure in every test

### How to Follow

- Arrange: Set up test data and mocks
- Act: Execute the function/method being tested
- Assert: Verify the results
- Keep sections visually separated
- One logical assertion per test

---

## Rule 40: Test Edge Cases

**❌ Bad:** Only test happy path

**✅ Good:** Test boundaries, edge cases, and error conditions

### How to Follow

- Test empty inputs ([], null, undefined, "")
- Test boundary values (0, -1, MAX_INT)
- Test invalid types and formats
- Test concurrent operations
- Test network/external failures
- Test timeout scenarios

---

## Rule 41: Use Descriptive Test Names

**❌ Bad:** `it('works')`, `it('test1')`

**✅ Good:** `it('should return 400 when email is invalid')`

### How to Follow

- Start with "should"
- Describe the behavior being tested
- Include the condition/context
- Make failures self-explanatory
- Be specific, not generic

---

## Rule 42: Mock External Services

**❌ Bad:** Call real APIs, databases in tests

**✅ Good:** Mock all external dependencies

### How to Follow

- Mock database connections
- Mock external APIs (payment, email, SMS)
- Mock file system operations
- Mock network requests
- Mock time/date functions
- Use dependency injection for easier mocking

---

## Summary: Code Quality & Testing Best Practices

**Code Quality (Rules 29-36):**
- Be explicit with types and names
- Keep functions small (< 50 lines)
- No magic numbers or strings
- Use meaningful variable names
- Don't repeat yourself (DRY)
- Comment why, not what
- Handle errors gracefully
- Use strict TypeScript

**Testing (Rules 37-42):**
- Test everything AI generates (90%+ coverage)
- Focus on business logic, not framework
- Use Arrange-Act-Assert pattern
- Test edge cases and boundaries
- Use descriptive test names
- Mock all external services

**Quick Checklist:**
```markdown
Before merging AI-generated code:

Code Quality:
- [ ] All functions under 50 lines
- [ ] No magic numbers (extracted to constants)
- [ ] Explicit TypeScript types everywhere
- [ ] No `any` types
- [ ] Error handling comprehensive
- [ ] Comments explain WHY, not WHAT

Testing:
- [ ] 90%+ test coverage
- [ ] Happy path tested
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] All external dependencies mocked
- [ ] Tests use AAA pattern
- [ ] Test names are descriptive
```

---

**See also:**
- [README.md](../README.md) - All 54 rules
- [01-prompts.md](./01-prompts.md) - Prompt engineering rules
- [02-architecture.md](./02-architecture.md) - Architecture rules
- [03-security.md](./03-security.md) - Security rules
- [DAILY_CHECKLIST.md](../DAILY_CHECKLIST.md) - Workflow checklist
