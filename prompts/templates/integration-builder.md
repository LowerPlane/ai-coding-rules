# Integration Builder Template

Use this template when building third-party integrations (Slack, Notion, GitHub, etc.) with AI assistance.

---

## Context

**Stack:**
- Runtime: Node.js 20.x / Python 3.11+ / Deno 1.x
- Framework: Express.js 4.x / Fastify 4.x / FastAPI 0.100+
- Language: TypeScript 5.x / Python with type hints
- Authentication: OAuth 2.0 / API Keys / Webhooks
- Queue: Bull 4.x / Celery 5.x / BullMQ 4.x
- Storage: Redis 7.x (tokens, rate limits)
- Database: PostgreSQL 15+ (audit logs)

**Existing Code:**
- OAuth flow implementation
- Webhook signature verification
- Rate limiter middleware
- Retry mechanism with exponential backoff
- Audit logging system

**Conventions:**
- Async/await for all I/O operations
- Result<T, E> return types for error handling
- Idempotent operations (support retries)
- Comprehensive audit logging
- Environment-based configuration
- 90%+ test coverage required

---

## Task

Create integration with [PLATFORM NAME] for [DESCRIBE FUNCTIONALITY]

### Specific Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

---

## Integration Specification

### Platform Details

**Platform:** Slack / Notion / GitHub / Discord / Zapier / Google Workspace / Microsoft 365

**API Version:** [Version number]

**API Documentation:** [Link to official API docs]

**Rate Limits:**
- Tier 2: 20 requests per minute
- Tier 3: 50 requests per second
- Burst limit: 100 requests

**Authentication Method:**
- OAuth 2.0 (Authorization Code Flow)
- Scopes required: `read:user`, `write:data`, `admin:webhooks`

### Endpoints Used

```typescript
interface PlatformEndpoints {
  // OAuth
  authorize: 'https://platform.com/oauth/authorize';
  token: 'https://platform.com/oauth/token';
  revoke: 'https://platform.com/oauth/revoke';

  // API
  baseUrl: 'https://api.platform.com/v2';
  endpoints: {
    getUser: 'GET /users/{userId}';
    createItem: 'POST /items';
    updateItem: 'PATCH /items/{itemId}';
    deleteItem: 'DELETE /items/{itemId}';
    listItems: 'GET /items';
  };

  // Webhooks
  webhookUrl: 'POST /webhooks';
  webhookEvents: ['item.created', 'item.updated', 'item.deleted'];
}
```

---

## API Specification

### OAuth Flow

**1. Authorization URL:**
```typescript
GET https://platform.com/oauth/authorize
  ?client_id={CLIENT_ID}
  &redirect_uri={REDIRECT_URI}
  &scope=read:user,write:data
  &state={RANDOM_STATE}
  &response_type=code
```

**2. Token Exchange:**
```typescript
POST https://platform.com/oauth/token
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "{AUTH_CODE}",
  "client_id": "{CLIENT_ID}",
  "client_secret": "{CLIENT_SECRET}",
  "redirect_uri": "{REDIRECT_URI}"
}

// Response
{
  "access_token": "xoxp-...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "xoxr-...",
  "scope": "read:user,write:data"
}
```

**3. Token Refresh:**
```typescript
POST https://platform.com/oauth/token
Content-Type: application/json

{
  "grant_type": "refresh_token",
  "refresh_token": "{REFRESH_TOKEN}",
  "client_id": "{CLIENT_ID}",
  "client_secret": "{CLIENT_SECRET}"
}
```

### API Requests

**Headers:**
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json",
  "User-Agent": "YourApp/1.0",
  "X-Request-ID": "{unique_request_id}"
}
```

**Request Example:**
```typescript
POST /api/v2/items
{
  "title": "New Item",
  "description": "Item description",
  "status": "active",
  "metadata": {
    "source": "api"
  }
}
```

**Success Response (201):**
```json
{
  "id": "item_123abc",
  "title": "New Item",
  "description": "Item description",
  "status": "active",
  "created_at": "2025-10-23T10:30:00Z",
  "updated_at": "2025-10-23T10:30:00Z"
}
```

**Error Responses:**

```json
// 400 - Validation Error
{
  "error": "invalid_request",
  "error_description": "Missing required field: title"
}

// 401 - Unauthorized
{
  "error": "invalid_token",
  "error_description": "Token expired or invalid"
}

// 403 - Forbidden
{
  "error": "insufficient_scope",
  "error_description": "Missing required scope: write:data"
}

// 429 - Rate Limited
{
  "error": "rate_limited",
  "error_description": "Too many requests",
  "retry_after": 60
}

// 500 - Server Error
{
  "error": "server_error",
  "error_description": "Internal server error"
}
```

### Webhook Specification

**Webhook Payload:**
```json
{
  "event": "item.created",
  "timestamp": "2025-10-23T10:30:00Z",
  "data": {
    "id": "item_123abc",
    "title": "New Item",
    "status": "active"
  },
  "webhook_id": "webhook_xyz"
}
```

**Webhook Headers:**
```
X-Platform-Signature: sha256=abcdef123456...
X-Platform-Event: item.created
X-Platform-Delivery: delivery_123
X-Platform-Timestamp: 1698059400
```

---

## Validation Rules

Use Zod schema for request/response validation:

```typescript
import { z } from 'zod';

// OAuth Token Response
const tokenResponseSchema = z.object({
  access_token: z.string().min(1),
  token_type: z.literal('Bearer'),
  expires_in: z.number().int().positive(),
  refresh_token: z.string().min(1).optional(),
  scope: z.string(),
});

// API Request Schema
const createItemSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title too long')
    .trim(),

  description: z.string()
    .max(2000, 'Description too long')
    .trim()
    .optional(),

  status: z.enum(['active', 'inactive', 'archived']),

  metadata: z.record(z.string(), z.unknown()).optional(),

  tags: z.array(z.string()).max(10, 'Maximum 10 tags').optional(),
});

// API Response Schema
const itemSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().optional(),
  status: z.enum(['active', 'inactive', 'archived']),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// Webhook Event Schema
const webhookEventSchema = z.object({
  event: z.enum(['item.created', 'item.updated', 'item.deleted']),
  timestamp: z.string().datetime(),
  data: itemSchema,
  webhook_id: z.string(),
});

// Webhook Signature Verification
const webhookHeadersSchema = z.object({
  'x-platform-signature': z.string(),
  'x-platform-event': z.string(),
  'x-platform-delivery': z.string(),
  'x-platform-timestamp': z.string(),
});

type CreateItemDTO = z.infer<typeof createItemSchema>;
type Item = z.infer<typeof itemSchema>;
type WebhookEvent = z.infer<typeof webhookEventSchema>;
```

---

## Output Format

### File Structure

```
src/integrations/platform-name/
├── platform.client.ts          # API client
├── platform.oauth.ts           # OAuth flow
├── platform.webhook.ts         # Webhook handler
├── platform.types.ts           # TypeScript types
├── platform.validator.ts       # Zod schemas
├── platform.service.ts         # Business logic
├── platform.repository.ts      # Token storage
├── platform.queue.ts           # Background jobs
├── platform.retry.ts           # Retry logic
├── platform.ratelimit.ts       # Rate limiting
├── platform.errors.ts          # Custom errors
├── platform.config.ts          # Configuration
└── __tests__/
    ├── platform.client.test.ts
    ├── platform.oauth.test.ts
    ├── platform.webhook.test.ts
    └── platform.integration.test.ts
```

### Code Style

**OAuth Client:**
```typescript
import crypto from 'crypto';
import { z } from 'zod';
import { Result } from '@/utils/result';
import { tokenResponseSchema } from './platform.validator';
import { PlatformConfig } from './platform.config';

/**
 * PlatformOAuth - Handles OAuth 2.0 flow for Platform integration
 */
export class PlatformOAuth {
  constructor(
    private config: PlatformConfig,
    private repository: TokenRepository
  ) {}

  /**
   * Generate authorization URL for OAuth flow
   */
  getAuthorizationUrl(userId: string): string {
    const state = this.generateState(userId);

    const params = new URLSearchParams({
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      scope: this.config.scopes.join(','),
      state,
      response_type: 'code',
    });

    return `${this.config.authorizeUrl}?${params.toString()}`;
  }

  /**
   * Exchange authorization code for access token
   */
  async exchangeCode(
    code: string,
    state: string
  ): Promise<Result<TokenData, Error>> {
    try {
      // Verify state
      const userId = await this.verifyState(state);
      if (!userId) {
        return {
          success: false,
          error: new Error('Invalid state parameter'),
        };
      }

      // Exchange code
      const response = await fetch(this.config.tokenUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grant_type: 'authorization_code',
          code,
          client_id: this.config.clientId,
          client_secret: this.config.clientSecret,
          redirect_uri: this.config.redirectUri,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        return {
          success: false,
          error: new Error(error.error_description || 'Token exchange failed'),
        };
      }

      const data = await response.json();

      // Validate response
      const validation = tokenResponseSchema.safeParse(data);
      if (!validation.success) {
        return {
          success: false,
          error: new Error('Invalid token response'),
        };
      }

      // Store tokens
      await this.repository.saveTokens(userId, {
        accessToken: validation.data.access_token,
        refreshToken: validation.data.refresh_token,
        expiresAt: Date.now() + (validation.data.expires_in * 1000),
        scope: validation.data.scope,
      });

      return {
        success: true,
        data: validation.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error as Error,
      };
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(userId: string): Promise<Result<TokenData, Error>> {
    try {
      const tokens = await this.repository.getTokens(userId);
      if (!tokens?.refreshToken) {
        return {
          success: false,
          error: new Error('No refresh token available'),
        };
      }

      const response = await fetch(this.config.tokenUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grant_type: 'refresh_token',
          refresh_token: tokens.refreshToken,
          client_id: this.config.clientId,
          client_secret: this.config.clientSecret,
        }),
      });

      if (!response.ok) {
        // Refresh token expired, need re-authorization
        await this.repository.deleteTokens(userId);
        return {
          success: false,
          error: new Error('Refresh token expired'),
        };
      }

      const data = await response.json();
      const validation = tokenResponseSchema.safeParse(data);

      if (!validation.success) {
        return {
          success: false,
          error: new Error('Invalid token response'),
        };
      }

      // Update stored tokens
      await this.repository.saveTokens(userId, {
        accessToken: validation.data.access_token,
        refreshToken: validation.data.refresh_token || tokens.refreshToken,
        expiresAt: Date.now() + (validation.data.expires_in * 1000),
        scope: validation.data.scope,
      });

      return {
        success: true,
        data: validation.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error as Error,
      };
    }
  }

  private generateState(userId: string): string {
    const state = crypto.randomBytes(32).toString('hex');
    // Store state with expiration (5 minutes)
    this.repository.saveState(state, userId, 300);
    return state;
  }

  private async verifyState(state: string): Promise<string | null> {
    return this.repository.getState(state);
  }
}
```

**API Client with Rate Limiting:**
```typescript
import { RateLimiter } from './platform.ratelimit';
import { RetryStrategy } from './platform.retry';
import { Result } from '@/utils/result';

/**
 * PlatformClient - API client with rate limiting and retry logic
 */
export class PlatformClient {
  private rateLimiter: RateLimiter;
  private retryStrategy: RetryStrategy;

  constructor(
    private config: PlatformConfig,
    private oauth: PlatformOAuth,
    private auditLog: AuditLogger
  ) {
    this.rateLimiter = new RateLimiter({
      maxRequests: config.rateLimitMax,
      windowMs: config.rateLimitWindow,
    });

    this.retryStrategy = new RetryStrategy({
      maxRetries: 3,
      initialDelay: 1000,
      maxDelay: 10000,
    });
  }

  /**
   * Create item via Platform API
   */
  async createItem(
    userId: string,
    data: CreateItemDTO
  ): Promise<Result<Item, Error>> {
    // Validate input
    const validation = createItemSchema.safeParse(data);
    if (!validation.success) {
      return {
        success: false,
        error: new Error('Invalid input data'),
      };
    }

    return this.retryStrategy.execute(async () => {
      // Get valid access token
      const tokenResult = await this.getValidToken(userId);
      if (!tokenResult.success) {
        return tokenResult;
      }

      // Check rate limit
      await this.rateLimiter.checkLimit(userId);

      // Generate request ID for idempotency
      const requestId = crypto.randomUUID();

      // Make API request
      const response = await fetch(`${this.config.baseUrl}/items`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${tokenResult.data.accessToken}`,
          'Content-Type': 'application/json',
          'User-Agent': this.config.userAgent,
          'X-Request-ID': requestId,
        },
        body: JSON.stringify(validation.data),
      });

      // Log request
      await this.auditLog.log({
        action: 'platform.create_item',
        userId,
        requestId,
        status: response.status,
        metadata: { itemData: validation.data },
      });

      // Handle rate limiting
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        const delay = retryAfter ? parseInt(retryAfter) * 1000 : 60000;
        throw new RateLimitError(`Rate limited, retry after ${delay}ms`, delay);
      }

      // Handle errors
      if (!response.ok) {
        const error = await response.json();
        throw new PlatformAPIError(
          error.error_description || 'API request failed',
          response.status,
          error.error
        );
      }

      // Parse and validate response
      const responseData = await response.json();
      const itemValidation = itemSchema.safeParse(responseData);

      if (!itemValidation.success) {
        return {
          success: false,
          error: new Error('Invalid API response'),
        };
      }

      return {
        success: true,
        data: itemValidation.data,
      };
    });
  }

  /**
   * Get valid access token, refreshing if necessary
   */
  private async getValidToken(
    userId: string
  ): Promise<Result<{ accessToken: string }, Error>> {
    const tokens = await this.oauth.repository.getTokens(userId);

    if (!tokens) {
      return {
        success: false,
        error: new Error('No tokens found, re-authorization required'),
      };
    }

    // Check if token is expired (with 5 minute buffer)
    if (tokens.expiresAt < Date.now() + 300000) {
      const refreshResult = await this.oauth.refreshToken(userId);
      if (!refreshResult.success) {
        return {
          success: false,
          error: refreshResult.error,
        };
      }

      return {
        success: true,
        data: { accessToken: refreshResult.data.access_token },
      };
    }

    return {
      success: true,
      data: { accessToken: tokens.accessToken },
    };
  }
}
```

**Webhook Handler:**
```typescript
import crypto from 'crypto';
import { Request, Response } from 'express';
import { webhookEventSchema, webhookHeadersSchema } from './platform.validator';

/**
 * PlatformWebhook - Handles incoming webhook events
 */
export class PlatformWebhook {
  constructor(
    private config: PlatformConfig,
    private queue: WebhookQueue,
    private auditLog: AuditLogger
  ) {}

  /**
   * Handle incoming webhook request
   */
  async handleWebhook(req: Request, res: Response): Promise<void> {
    try {
      // Verify webhook signature
      const signatureValid = this.verifySignature(
        req.body,
        req.headers['x-platform-signature'] as string,
        req.headers['x-platform-timestamp'] as string
      );

      if (!signatureValid) {
        res.status(401).json({ error: 'Invalid signature' });
        return;
      }

      // Validate webhook payload
      const validation = webhookEventSchema.safeParse(req.body);
      if (!validation.success) {
        res.status(400).json({ error: 'Invalid payload' });
        return;
      }

      const event = validation.data;

      // Check for duplicate delivery (idempotency)
      const deliveryId = req.headers['x-platform-delivery'] as string;
      const isDuplicate = await this.checkDuplicate(deliveryId);

      if (isDuplicate) {
        // Already processed, return success
        res.status(200).json({ received: true });
        return;
      }

      // Queue event for processing
      await this.queue.addJob({
        event: event.event,
        data: event.data,
        deliveryId,
        timestamp: event.timestamp,
      });

      // Log webhook receipt
      await this.auditLog.log({
        action: 'platform.webhook_received',
        event: event.event,
        deliveryId,
        metadata: event.data,
      });

      // Acknowledge receipt immediately (respond within 3s)
      res.status(200).json({ received: true });

      // Process webhook asynchronously
      // (actual processing happens in queue worker)
    } catch (error) {
      console.error('Webhook handling error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  /**
   * Verify webhook signature using HMAC SHA256
   */
  private verifySignature(
    payload: unknown,
    signature: string,
    timestamp: string
  ): boolean {
    // Verify timestamp (within 5 minutes)
    const now = Math.floor(Date.now() / 1000);
    const requestTime = parseInt(timestamp);

    if (Math.abs(now - requestTime) > 300) {
      return false; // Timestamp too old/future
    }

    // Compute signature
    const signatureBase = `${timestamp}.${JSON.stringify(payload)}`;
    const expectedSignature = crypto
      .createHmac('sha256', this.config.webhookSecret)
      .update(signatureBase)
      .digest('hex');

    // Compare signatures (timing-safe)
    const providedSignature = signature.replace('sha256=', '');

    return crypto.timingSafeEqual(
      Buffer.from(expectedSignature),
      Buffer.from(providedSignature)
    );
  }

  /**
   * Check if webhook delivery already processed
   */
  private async checkDuplicate(deliveryId: string): Promise<boolean> {
    // Check Redis or database for delivery ID
    return this.queue.isDuplicate(deliveryId);
  }
}
```

---

## Security Requirements

**CRITICAL - Never Skip:**

1. **Credential Storage**
   - NEVER store credentials in code or git
   - Use environment variables or secret manager
   - Encrypt tokens at rest in database
   - Use secure key derivation (PBKDF2, scrypt)

2. **OAuth Security**
   - Validate `state` parameter to prevent CSRF
   - Use PKCE (Proof Key for Code Exchange) when possible
   - Validate redirect URI matches registered URI
   - Store state with short expiration (5 minutes)
   - Securely generate random state (crypto.randomBytes)

3. **Webhook Security**
   - ALWAYS verify webhook signatures
   - Use timing-safe comparison for signatures
   - Validate timestamp (within 5 minutes)
   - Check for replay attacks (duplicate delivery IDs)
   - Process webhooks asynchronously (respond within 3s)

4. **API Request Security**
   - Use HTTPS only (never HTTP)
   - Include request IDs for tracing
   - Sanitize all inputs before sending
   - Validate all responses before processing
   - Never log access tokens or secrets

5. **Rate Limiting**
   - Respect platform rate limits
   - Implement exponential backoff
   - Handle 429 responses gracefully
   - Use queue for high-volume operations

6. **Token Management**
   - Refresh tokens before expiration
   - Handle token revocation gracefully
   - Delete tokens on user disconnect
   - Implement token rotation

---

## Error Handling Requirements

**Custom Error Classes:**
```typescript
export class PlatformAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public errorCode: string
  ) {
    super(message);
    this.name = 'PlatformAPIError';
  }
}

export class RateLimitError extends Error {
  constructor(
    message: string,
    public retryAfter: number
  ) {
    super(message);
    this.name = 'RateLimitError';
  }
}

export class TokenExpiredError extends Error {
  constructor(message: string = 'Token expired') {
    super(message);
    this.name = 'TokenExpiredError';
  }
}

export class WebhookVerificationError extends Error {
  constructor(message: string = 'Webhook verification failed') {
    super(message);
    this.name = 'WebhookVerificationError';
  }
}
```

**Error Handling Patterns:**
```typescript
// Retry on transient errors
const retryableErrors = [429, 500, 502, 503, 504];

if (retryableErrors.includes(response.status)) {
  throw new RetryableError('Transient error, will retry');
}

// Don't retry on client errors
const clientErrors = [400, 401, 403, 404];

if (clientErrors.includes(response.status)) {
  throw new PlatformAPIError('Client error, no retry', response.status);
}
```

---

## Testing Requirements

**Coverage: 90%+ required**

### Test Scenarios

```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { PlatformClient } from './platform.client';
import { PlatformOAuth } from './platform.oauth';
import nock from 'nock';

describe('PlatformClient', () => {
  let client: PlatformClient;

  beforeEach(() => {
    nock.cleanAll();
  });

  // 1. Successful API Request
  it('should create item successfully', async () => {
    nock('https://api.platform.com')
      .post('/v2/items')
      .reply(201, {
        id: 'item_123',
        title: 'Test Item',
        status: 'active',
        created_at: '2025-10-23T10:00:00Z',
        updated_at: '2025-10-23T10:00:00Z',
      });

    const result = await client.createItem('user_1', {
      title: 'Test Item',
      status: 'active',
    });

    expect(result.success).toBe(true);
    expect(result.data?.id).toBe('item_123');
  });

  // 2. Token Refresh
  it('should refresh token when expired', async () => {
    // Mock expired token
    jest.spyOn(oauth.repository, 'getTokens').mockResolvedValue({
      accessToken: 'expired_token',
      refreshToken: 'refresh_123',
      expiresAt: Date.now() - 1000, // Expired
      scope: 'read:user',
    });

    // Mock token refresh
    nock('https://platform.com')
      .post('/oauth/token')
      .reply(200, {
        access_token: 'new_token',
        token_type: 'Bearer',
        expires_in: 3600,
        scope: 'read:user',
      });

    // Mock API request with new token
    nock('https://api.platform.com')
      .post('/v2/items')
      .reply(201, { id: 'item_123' });

    const result = await client.createItem('user_1', {
      title: 'Test',
      status: 'active',
    });

    expect(result.success).toBe(true);
  });

  // 3. Rate Limiting
  it('should handle rate limiting with retry', async () => {
    nock('https://api.platform.com')
      .post('/v2/items')
      .reply(429, { error: 'rate_limited' }, { 'Retry-After': '1' })
      .post('/v2/items')
      .reply(201, { id: 'item_123' });

    const result = await client.createItem('user_1', {
      title: 'Test',
      status: 'active',
    });

    expect(result.success).toBe(true);
  });

  // 4. Error Handling
  it('should handle API errors', async () => {
    nock('https://api.platform.com')
      .post('/v2/items')
      .reply(400, {
        error: 'invalid_request',
        error_description: 'Missing required field',
      });

    const result = await client.createItem('user_1', {
      title: 'Test',
      status: 'active',
    });

    expect(result.success).toBe(false);
    expect(result.error?.message).toContain('Missing required field');
  });

  // 5. Validation
  it('should validate input data', async () => {
    const result = await client.createItem('user_1', {
      title: '', // Invalid: empty
      status: 'active',
    });

    expect(result.success).toBe(false);
    expect(result.error?.message).toContain('Invalid input');
  });
});

describe('PlatformWebhook', () => {
  // 6. Webhook Signature Verification
  it('should verify valid webhook signature', async () => {
    const payload = {
      event: 'item.created',
      timestamp: '2025-10-23T10:00:00Z',
      data: { id: 'item_123' },
      webhook_id: 'webhook_1',
    };

    const timestamp = Math.floor(Date.now() / 1000).toString();
    const signature = generateSignature(payload, timestamp);

    const req = mockRequest({
      body: payload,
      headers: {
        'x-platform-signature': `sha256=${signature}`,
        'x-platform-timestamp': timestamp,
        'x-platform-delivery': 'delivery_1',
      },
    });
    const res = mockResponse();

    await webhook.handleWebhook(req, res);

    expect(res.status).toHaveBeenCalledWith(200);
  });

  // 7. Reject Invalid Signature
  it('should reject invalid webhook signature', async () => {
    const req = mockRequest({
      body: { event: 'item.created' },
      headers: {
        'x-platform-signature': 'sha256=invalid',
        'x-platform-timestamp': Date.now().toString(),
      },
    });
    const res = mockResponse();

    await webhook.handleWebhook(req, res);

    expect(res.status).toHaveBeenCalledWith(401);
  });

  // 8. Idempotency (Duplicate Webhooks)
  it('should handle duplicate webhook deliveries', async () => {
    const deliveryId = 'delivery_123';

    // First delivery
    await webhook.handleWebhook(mockRequest({ deliveryId }), mockResponse());

    // Duplicate delivery
    const res2 = mockResponse();
    await webhook.handleWebhook(mockRequest({ deliveryId }), res2);

    expect(res2.status).toHaveBeenCalledWith(200);
    // Should not queue job twice
    expect(queue.addJob).toHaveBeenCalledTimes(1);
  });
});

describe('PlatformOAuth', () => {
  // 9. OAuth Flow
  it('should complete OAuth flow successfully', async () => {
    const authUrl = oauth.getAuthorizationUrl('user_1');

    expect(authUrl).toContain('client_id=');
    expect(authUrl).toContain('state=');
    expect(authUrl).toContain('scope=');

    // Extract state
    const state = new URL(authUrl).searchParams.get('state')!;

    // Mock token exchange
    nock('https://platform.com')
      .post('/oauth/token')
      .reply(200, {
        access_token: 'access_123',
        token_type: 'Bearer',
        expires_in: 3600,
        refresh_token: 'refresh_123',
        scope: 'read:user,write:data',
      });

    const result = await oauth.exchangeCode('auth_code', state);

    expect(result.success).toBe(true);
    expect(result.data?.access_token).toBe('access_123');
  });

  // 10. CSRF Protection
  it('should reject invalid state parameter', async () => {
    const result = await oauth.exchangeCode('code', 'invalid_state');

    expect(result.success).toBe(false);
    expect(result.error?.message).toContain('Invalid state');
  });
});
```

---

## Audit Logging Requirements

**Log All Integration Actions:**
```typescript
interface AuditLogEntry {
  timestamp: string;
  action: string;
  userId: string;
  requestId: string;
  status: number | 'success' | 'error';
  metadata: Record<string, unknown>;
  error?: string;
}

// Log examples
await auditLog.log({
  action: 'platform.oauth_completed',
  userId: 'user_123',
  requestId: crypto.randomUUID(),
  status: 'success',
  metadata: { scope: 'read:user,write:data' },
});

await auditLog.log({
  action: 'platform.api_request',
  userId: 'user_123',
  requestId: 'req_xyz',
  status: 201,
  metadata: { endpoint: '/items', method: 'POST' },
});

await auditLog.log({
  action: 'platform.webhook_received',
  userId: 'system',
  requestId: 'delivery_123',
  status: 'success',
  metadata: { event: 'item.created', itemId: 'item_123' },
});
```

---

## Dependencies

**Use existing packages only:**
- express / fastify (web framework)
- zod (validation)
- ioredis (Redis client)
- bull / bullmq (job queue)
- prisma / pg (database)
- node-fetch / axios (HTTP client)
- crypto (built-in, signatures)

**DO NOT install new packages without approval**

---

## Example Usage

### Prompt Example

```markdown
## Context
- Stack: Node.js 20 + TypeScript + Express + Bull + Redis + PostgreSQL
- Existing: OAuth flow, webhook verification, retry logic, audit logging
- Conventions: Async/await, Result<T,E>, idempotent operations

## Task
Create Slack integration for sending messages to channels

## Requirements
- OAuth 2.0 with scopes: chat:write, channels:read
- Send formatted messages with blocks
- Handle rate limits (1 message per second per channel)
- Verify webhook signatures for incoming events
- Support slash commands
- Queue messages for reliable delivery
- Comprehensive error handling

## Platform Details
- API: https://api.slack.com/web
- Rate Limits: Tier 2 (20 req/min), Tier 3 (50 req/sec)
- Webhook Events: message.channels, app_mention
- Signature: HMAC SHA256 with signing secret

## Endpoints
- POST /chat.postMessage - Send message
- GET /conversations.list - List channels
- POST /webhooks - Register webhook
- Webhook receiver: POST /api/webhooks/slack

## Validation
- message text: 1-40000 chars
- channel ID: C[A-Z0-9]{10} pattern
- blocks: valid Slack Block Kit JSON

## Security
- Verify all webhook signatures (timing-safe)
- Encrypt stored tokens (AES-256)
- Validate state parameter (CSRF)
- Rate limit per user (100 req/hour)
- Audit log all actions

## Tests
- OAuth flow completion
- Token refresh on expiration
- Message sending with retry
- Rate limit handling
- Webhook signature verification
- Duplicate webhook handling
- Error scenarios for each API call

Generate: OAuth client, API client, webhook handler, validators, tests
```

---

## Checklist

Before submitting AI-generated integration code:

- [ ] All credentials in environment variables (no hardcoded secrets)
- [ ] OAuth state parameter verified (CSRF protection)
- [ ] Webhook signatures verified with timing-safe comparison
- [ ] All API responses validated with Zod
- [ ] Rate limiting implemented and tested
- [ ] Retry logic with exponential backoff
- [ ] Token refresh before expiration
- [ ] Idempotent operations (support retries)
- [ ] Comprehensive error handling
- [ ] Audit logging on all actions
- [ ] Tests cover all scenarios (90%+)
- [ ] Request IDs for tracing
- [ ] No secrets logged
- [ ] Webhook processing under 3 seconds
- [ ] Duplicate webhook detection

---

**See also:**
- [Rule 20: No Secrets in Code](../../README.md#rule-20-no-secrets-in-code)
- [Rule 21: Validate All Inputs](../../README.md#rule-21-validate-all-inputs)
- [Rule 28: Verify Webhook Signatures](../../README.md#rule-28-verify-webhook-signatures)
- [Rule 37: Test Everything](../../README.md#rule-37-test-everything-ai-generates)
- [DAILY_CHECKLIST.md](../../DAILY_CHECKLIST.md)
