# Slack Bot Builder Workflow

**Complete Slack integration in 60 minutes using AI assistance**

---

## Overview

**Time Estimate:** 60 minutes
**Difficulty Level:** Intermediate
**Prerequisites:**
- Node.js/Python experience
- Understanding of webhooks and APIs
- Slack workspace admin access
- Basic OAuth knowledge

**What You'll Build:**
A production-ready Slack bot with:
- Slash commands and interactive components
- Event subscriptions (message handling)
- OAuth authentication
- Secure webhook verification
- Database integration for state
- Proper error handling and logging

---

## Prerequisites and Setup

### Required Tools
- Node.js 20.x or Python 3.10+
- Package manager (npm/pip)
- Ngrok (for local development)
- Slack workspace (with admin access)
- Database (PostgreSQL/MongoDB)
- Git

### Required Knowledge
- REST API concepts
- Webhook mechanics
- OAuth 2.0 flow
- Event-driven architecture
- Async programming

### Initial Setup (5 minutes)
```bash
# Node.js setup
mkdir slack-bot && cd slack-bot
npm init -y
npm install @slack/bolt dotenv prisma
npm install -D typescript @types/node ts-node

# Create directories
mkdir -p src/handlers src/commands src/events src/middleware

# Python alternative
pip install slack-bolt python-dotenv sqlalchemy

# Install ngrok for local development
brew install ngrok  # or download from ngrok.com
```

---

## Workflow Steps

### Step 1: Create Slack App and Get Credentials (10 minutes)

**Objective:** Set up Slack app and obtain required tokens

**Action:**
Create a new Slack app in your workspace.

**Manual Steps:**

1. **Create Slack App:**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name: [Your Bot Name]
   - Workspace: [Select your workspace]

2. **Configure Bot Token Scopes:**
   Navigate to "OAuth & Permissions", add these scopes:
   - `chat:write` - Send messages
   - `commands` - Add slash commands
   - `channels:history` - Read channel messages
   - `channels:read` - View channels
   - `users:read` - View users
   - `im:history` - Read DMs
   - `im:write` - Send DMs
   - `reactions:write` - Add reactions

3. **Install App to Workspace:**
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the "Bot User OAuth Token" (starts with xoxb-)

4. **Get Signing Secret:**
   - Navigate to "Basic Information"
   - Under "App Credentials"
   - Copy "Signing Secret"

5. **Enable Event Subscriptions:**
   - Navigate to "Event Subscriptions"
   - Turn on "Enable Events"
   - Request URL: https://your-domain.com/slack/events (we'll set this up later)
   - Subscribe to bot events:
     - `message.channels`
     - `message.im`
     - `app_mention`

6. **Create Slash Commands:**
   - Navigate to "Slash Commands"
   - Click "Create New Command"
   - Command: `/hello`
   - Request URL: https://your-domain.com/slack/commands
   - Description: Say hello
   - Usage hint: [optional message]

**Save Credentials:**
```bash
# Create .env file
cat > .env << EOF
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token  # for Socket Mode
DATABASE_URL=postgresql://user:pass@localhost:5432/slackbot
PORT=3000
NODE_ENV=development
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

**Review Checkpoint:**
- [ ] Slack app created
- [ ] Bot token obtained
- [ ] Signing secret saved
- [ ] Scopes configured
- [ ] App installed to workspace
- [ ] Environment variables set

**References:** [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets)

---

### Step 2: Generate Bot Server Setup (10 minutes)

**Objective:** Create the main bot application server

**Action:**
Generate the core server with Slack Bolt framework.

**Prompt to Use:**
```markdown
Generate a Slack bot server using Slack Bolt framework:

File: src/index.ts (Node.js) or app.py (Python)

Requirements:
- Use @slack/bolt package (Node) or slack-bolt (Python)
- Load environment variables from .env
- Initialize Slack App with bot token and signing secret
- Set up Express receiver for webhooks
- Configure port from environment (default 3000)
- Add request logging middleware
- Add error handling middleware
- Verify webhook signatures automatically
- Start server and log status

Features:
- Health check endpoint: GET /health
- Slack events endpoint: POST /slack/events
- Graceful shutdown on SIGTERM/SIGINT
- Environment validation on startup
- Connection to database (Prisma/SQLAlchemy)

Error handling:
- Log all errors with context
- Return appropriate error responses
- Handle Slack API errors gracefully
- Rate limit protection

Environment variables required:
- SLACK_BOT_TOKEN
- SLACK_SIGNING_SECRET
- DATABASE_URL
- PORT
- NODE_ENV

Use TypeScript with proper types
Export app for testing
Include startup validation
```

**Example Output:**
```typescript
import { App, ExpressReceiver } from '@slack/bolt';
import dotenv from 'dotenv';

dotenv.config();

// Validate environment
const requiredEnvVars = ['SLACK_BOT_TOKEN', 'SLACK_SIGNING_SECRET'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// Create Express receiver
const receiver = new ExpressReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
});

// Initialize Slack app
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  receiver,
});

// Health check endpoint
receiver.router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
const port = process.env.PORT || 3000;
(async () => {
  await app.start(port);
  console.log(`⚡️ Slack bot is running on port ${port}`);
})();
```

**Review Checkpoint:**
- [ ] Server initializes correctly
- [ ] Environment variables validated
- [ ] Webhook signature verification working
- [ ] Health check endpoint responds
- [ ] Error handling in place
- [ ] Logging configured

**References:** [Rule 6: Specify Dependencies Explicitly](../README.md#rule-6-specify-dependencies-explicitly), [Rule 18: Configuration as Code](../README.md#rule-18-configuration-as-code)

---

### Step 3: Generate Slash Command Handlers (10 minutes)

**Objective:** Create handlers for slash commands

**Action:**
Generate slash command processing logic.

**Prompt to Use:**
```markdown
Generate slash command handlers for Slack bot:

Commands to implement:
1. /hello [optional name] - Greet user
2. /help - Show available commands
3. /status - Show bot status
4. [Add your custom commands]

File structure:
src/commands/
  hello.command.ts
  help.command.ts
  status.command.ts
  index.ts (exports all)

Each command handler:
- Validate input parameters
- Process command logic
- Respond to Slack within 3 seconds
- Use ephemeral messages when appropriate
- Handle errors gracefully
- Log command usage

Response types:
- Immediate response (< 3 sec)
- Delayed response (use response_url)
- Ephemeral (visible only to user)
- In-channel (visible to all)

Example structure for each command:
```typescript
export async function helloCommand({ command, ack, respond }) {
  // Acknowledge command immediately
  await ack();

  // Extract parameters
  const name = command.text || 'World';

  // Validate input
  if (name.length > 100) {
    return await respond({
      text: 'Name too long! Keep it under 100 characters.',
      response_type: 'ephemeral'
    });
  }

  // Respond
  await respond({
    text: `Hello, ${name}! 👋`,
    response_type: 'in_channel'
  });
}
```

Requirements:
- TypeScript interfaces for command payloads
- Input validation for each command
- Error handling with user-friendly messages
- Rate limiting per user
- Audit logging (who ran what command)
- Response time tracking

Register commands in main app:
```typescript
import { helloCommand, helpCommand, statusCommand } from './commands';

app.command('/hello', helloCommand);
app.command('/help', helpCommand);
app.command('/status', statusCommand);
```

Use TypeScript
Include JSDoc comments
Export command handlers
```

**Review Checkpoint:**
- [ ] All commands registered
- [ ] Input validation working
- [ ] Responses within 3 seconds
- [ ] Error messages user-friendly
- [ ] Ephemeral vs public responses correct
- [ ] Commands logged

**References:** [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs), [Rule 35: Handle Errors Gracefully](../README.md#rule-35-handle-errors-gracefully)

---

### Step 4: Generate Event Handlers (10 minutes)

**Objective:** Handle Slack events (messages, mentions, reactions)

**Action:**
Create event subscription handlers.

**Prompt to Use:**
```markdown
Generate event handlers for Slack bot:

Events to handle:
1. app_mention - Bot is @mentioned in channel
2. message - New message in channels bot is in
3. message.im - Direct message to bot

File structure:
src/events/
  mention.event.ts
  message.event.ts
  dm.event.ts
  index.ts

Each event handler:
- Filter out bot's own messages (prevent loops)
- Parse message content
- Detect intent or keywords
- Respond appropriately
- Handle rate limiting
- Log all events

Example structure:
```typescript
export async function appMentionEvent({ event, say, client }) {
  // Ignore bot's own messages
  if (event.bot_id) return;

  // Extract message text (remove mention)
  const text = event.text.replace(/<@[A-Z0-9]+>/g, '').trim();

  // Process based on content
  if (text.toLowerCase().includes('help')) {
    await say({
      text: 'Here are the commands I understand...',
      thread_ts: event.ts  // Reply in thread
    });
  } else {
    await say({
      text: `You said: "${text}". How can I help?`,
      thread_ts: event.ts
    });
  }
}
```

Features to implement:
- Keyword detection (help, status, etc.)
- Thread-aware responses
- Reaction to messages
- Typing indicators for slow operations
- Context preservation across messages
- User preferences from database

Message processing:
- Clean and sanitize input
- Detect mentions of users/channels
- Extract links and attachments
- Parse formatting (bold, code blocks)

Requirements:
- Prevent infinite loops (filter bot messages)
- Rate limit responses (max 1 per 3 seconds per channel)
- Use threads to keep channels clean
- Graceful degradation on errors
- Store conversation context in database

Register events in main app:
```typescript
import { appMentionEvent, messageEvent, dmEvent } from './events';

app.event('app_mention', appMentionEvent);
app.event('message', messageEvent);
```

Use TypeScript with proper event types
Add error boundaries
Include retry logic for transient failures
```

**Review Checkpoint:**
- [ ] Events registered correctly
- [ ] Bot doesn't respond to itself
- [ ] Thread replies working
- [ ] Rate limiting in place
- [ ] Context preserved
- [ ] Errors handled gracefully

**References:** [Rule 15: Stateless Services](../README.md#rule-15-stateless-services), [Rule 35: Handle Errors Gracefully](../README.md#rule-35-handle-errors-gracefully)

---

### Step 5: Add Interactive Components (10 minutes)

**Objective:** Handle buttons, select menus, and modals

**Action:**
Generate interactive component handlers.

**Prompt to Use:**
```markdown
Generate interactive component handlers for Slack bot:

Components to handle:
1. Buttons - User clicks button
2. Select menus - User selects option
3. Modals - User submits form
4. Shortcuts - Global or message shortcuts

File structure:
src/interactions/
  buttons.interaction.ts
  selects.interaction.ts
  modals.interaction.ts
  index.ts

Example button with action:
```typescript
// Send message with button
await say({
  text: 'Would you like to proceed?',
  blocks: [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: 'Would you like to proceed?'
      }
    },
    {
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: { type: 'plain_text', text: 'Yes' },
          action_id: 'button_yes',
          style: 'primary'
        },
        {
          type: 'button',
          text: { type: 'plain_text', text: 'No' },
          action_id: 'button_no',
          style: 'danger'
        }
      ]
    }
  ]
});

// Handle button click
app.action('button_yes', async ({ ack, body, client }) => {
  await ack();

  // Update message to remove buttons
  await client.chat.update({
    channel: body.channel.id,
    ts: body.message.ts,
    text: 'You selected: Yes',
    blocks: []
  });

  // Perform action
  await handleYesAction(body.user.id);
});
```

Modal example:
```typescript
// Open modal
app.shortcut('open_form', async ({ shortcut, ack, client }) => {
  await ack();

  await client.views.open({
    trigger_id: shortcut.trigger_id,
    view: {
      type: 'modal',
      callback_id: 'form_submit',
      title: { type: 'plain_text', text: 'Submit Form' },
      submit: { type: 'plain_text', text: 'Submit' },
      blocks: [
        {
          type: 'input',
          block_id: 'name_block',
          element: {
            type: 'plain_text_input',
            action_id: 'name_input',
            placeholder: { type: 'plain_text', text: 'Enter your name' }
          },
          label: { type: 'plain_text', text: 'Name' }
        }
      ]
    }
  });
});

// Handle modal submission
app.view('form_submit', async ({ ack, body, view, client }) => {
  await ack();

  const name = view.state.values.name_block.name_input.value;

  // Validate
  if (name.length < 2) {
    await ack({
      response_action: 'errors',
      errors: {
        name_block: 'Name must be at least 2 characters'
      }
    });
    return;
  }

  // Process submission
  await processFormData({ name, userId: body.user.id });
});
```

Requirements:
- Acknowledge all interactions within 3 seconds
- Update messages after actions
- Validate modal submissions
- Provide clear error messages
- Store interaction results in database
- Log all interactions for analytics

Use Block Kit Builder for complex UIs
Add loading states for slow operations
Include confirmation steps for destructive actions
Use TypeScript for type safety
```

**Review Checkpoint:**
- [ ] Buttons respond correctly
- [ ] Modals open and submit
- [ ] Validations work
- [ ] Messages update after interaction
- [ ] Loading states shown
- [ ] All interactions logged

**References:** [Rule 4: Include Validation Requirements](../README.md#rule-4-include-validation-requirements)

---

### Step 6: Add Database Integration (10 minutes)

**Objective:** Store bot data and user preferences

**Action:**
Set up database schema and operations.

**Prompt to Use:**
```markdown
Generate database schema and operations for Slack bot:

Database: PostgreSQL with Prisma (or your choice)

Schema needed:
1. Users table:
   - slack_user_id (unique)
   - username
   - preferences (JSON)
   - created_at, updated_at

2. Conversations table:
   - id
   - user_id
   - channel_id
   - message
   - response
   - timestamp

3. Commands table (audit log):
   - id
   - user_id
   - command
   - parameters
   - success (boolean)
   - executed_at

File: prisma/schema.prisma
```prisma
model User {
  id            String   @id @default(uuid())
  slackUserId   String   @unique
  username      String
  preferences   Json?
  conversations Conversation[]
  commands      Command[]
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model Conversation {
  id        String   @id @default(uuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  channelId String
  message   String
  response  String?
  timestamp DateTime @default(now())
}

model Command {
  id         String   @id @default(uuid())
  userId     String
  user       User     @relation(fields: [userId], references: [id])
  command    String
  parameters String?
  success    Boolean
  executedAt DateTime @default(now())
}
```

Generate repository layer:
File: src/repositories/user.repository.ts

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class UserRepository {
  async findBySlackId(slackUserId: string) {
    return await prisma.user.findUnique({
      where: { slackUserId }
    });
  }

  async create(slackUserId: string, username: string) {
    return await prisma.user.create({
      data: { slackUserId, username }
    });
  }

  async updatePreferences(slackUserId: string, preferences: any) {
    return await prisma.user.update({
      where: { slackUserId },
      data: { preferences }
    });
  }

  async logCommand(slackUserId: string, command: string, success: boolean) {
    const user = await this.findBySlackId(slackUserId);
    if (!user) return;

    await prisma.command.create({
      data: {
        userId: user.id,
        command,
        success,
        executedAt: new Date()
      }
    });
  }
}
```

Conversation context storage:
File: src/repositories/conversation.repository.ts

Requirements:
- CRUD operations for all models
- Transaction support for multi-step operations
- Error handling with proper logging
- Connection pooling
- Migration scripts
- Seed data for development

Use parameterized queries (Prisma handles this)
Add indexes on: slack_user_id, channel_id, timestamp
Include soft delete for conversations
Implement data retention policy (auto-delete old data)
```

**Review Checkpoint:**
- [ ] Database schema created
- [ ] Migrations run successfully
- [ ] Repository methods work
- [ ] Transactions implemented
- [ ] Indexes added
- [ ] Connection pooling configured

**References:** [Rule 22: Use Parameterized Queries Only](../README.md#rule-22-use-parameterized-queries-only)

---

### Step 7: Add Security and Verification (5 minutes)

**Objective:** Secure webhook endpoints and validate requests

**Action:**
Implement security middleware.

**Prompt to Use:**
```markdown
Generate security middleware for Slack bot:

Security features:
1. Webhook signature verification (automatic with Bolt)
2. Request timestamp validation (prevent replay attacks)
3. Rate limiting per user/channel
4. Input sanitization
5. Audit logging

File: src/middleware/security.middleware.ts

```typescript
import crypto from 'crypto';

// Verify Slack request signature (Bolt does this, but here's how)
export function verifySlackRequest(
  signingSecret: string,
  requestBody: string,
  timestamp: string,
  signature: string
): boolean {
  // Check timestamp is within 5 minutes
  const currentTime = Math.floor(Date.now() / 1000);
  if (Math.abs(currentTime - parseInt(timestamp)) > 300) {
    return false;
  }

  // Verify signature
  const baseString = `v0:${timestamp}:${requestBody}`;
  const hmac = crypto
    .createHmac('sha256', signingSecret)
    .update(baseString)
    .digest('hex');
  const computedSignature = `v0=${hmac}`;

  return crypto.timingSafeEqual(
    Buffer.from(computedSignature),
    Buffer.from(signature)
  );
}

// Rate limiter
const userRateLimits = new Map<string, number[]>();

export function rateLimitMiddleware(userId: string, limit = 10): boolean {
  const now = Date.now();
  const userRequests = userRateLimits.get(userId) || [];

  // Remove requests older than 1 minute
  const recentRequests = userRequests.filter(time => now - time < 60000);

  if (recentRequests.length >= limit) {
    return false; // Rate limit exceeded
  }

  recentRequests.push(now);
  userRateLimits.set(userId, recentRequests);
  return true;
}

// Input sanitization
export function sanitizeInput(text: string): string {
  // Remove potentially dangerous content
  return text
    .replace(/<script[^>]*>.*?<\/script>/gi, '')
    .replace(/<[^>]+>/g, '')
    .trim()
    .slice(0, 10000); // Limit length
}

// Audit logger
export async function auditLog(
  userId: string,
  action: string,
  details: any
) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    userId,
    action,
    details
  }));

  // Also save to database
  // await saveAuditLog(userId, action, details);
}
```

Apply security in handlers:
```typescript
app.command('/hello', async ({ command, ack, respond }) => {
  // Rate limit check
  if (!rateLimitMiddleware(command.user_id, 10)) {
    await ack();
    return await respond({
      text: 'Rate limit exceeded. Please try again later.',
      response_type: 'ephemeral'
    });
  }

  // Sanitize input
  const name = sanitizeInput(command.text);

  // Audit log
  await auditLog(command.user_id, 'hello_command', { name });

  await ack();
  await respond({ text: `Hello, ${name}!` });
});
```

Requirements:
- All webhooks verify signatures (Bolt handles this)
- Implement per-user rate limiting
- Sanitize all user inputs
- Log all security events
- No secrets in code (environment variables only)

Use TypeScript
Export all middleware functions
Include unit tests for security functions
```

**Review Checkpoint:**
- [ ] Signature verification working (automatic)
- [ ] Rate limiting prevents abuse
- [ ] Input sanitization in place
- [ ] Security events logged
- [ ] No secrets in code

**References:** [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets), [Rule 24: Implement Rate Limiting](../README.md#rule-24-implement-rate-limiting), [Rule 28: Log Security Events](../README.md#rule-28-log-security-events)

---

### Step 8: Generate Tests (10 minutes)

**Objective:** Test slash commands, events, and interactions

**Action:**
Create comprehensive test suite.

**Prompt to Use:**
```markdown
Generate tests for Slack bot:

Test files needed:
1. src/__tests__/commands/hello.test.ts
2. src/__tests__/events/mention.test.ts
3. src/__tests__/interactions/buttons.test.ts
4. src/__tests__/middleware/security.test.ts

Use Jest with ts-jest

Example test structure:
```typescript
import { helloCommand } from '../../commands/hello.command';

describe('Hello Command', () => {
  let ackMock: jest.Mock;
  let respondMock: jest.Mock;

  beforeEach(() => {
    ackMock = jest.fn();
    respondMock = jest.fn();
  });

  it('should greet user with their name', async () => {
    const command = {
      user_id: 'U123',
      text: 'Alice',
      command: '/hello'
    };

    await helloCommand({ command, ack: ackMock, respond: respondMock });

    expect(ackMock).toHaveBeenCalled();
    expect(respondMock).toHaveBeenCalledWith(
      expect.objectContaining({
        text: expect.stringContaining('Alice')
      })
    );
  });

  it('should validate input length', async () => {
    const command = {
      user_id: 'U123',
      text: 'A'.repeat(101),
      command: '/hello'
    };

    await helloCommand({ command, ack: ackMock, respond: respondMock });

    expect(respondMock).toHaveBeenCalledWith(
      expect.objectContaining({
        text: expect.stringContaining('too long')
      })
    );
  });

  it('should use default name when none provided', async () => {
    const command = {
      user_id: 'U123',
      text: '',
      command: '/hello'
    };

    await helloCommand({ command, ack: ackMock, respond: respondMock });

    expect(respondMock).toHaveBeenCalledWith(
      expect.objectContaining({
        text: expect.stringContaining('World')
      })
    );
  });
});
```

Test coverage requirements:
- All slash commands (happy path + errors)
- Event handlers (with bot message filtering)
- Interactive components (buttons, modals)
- Security middleware (signature verification, rate limiting)
- Database operations (mocked)
- Error scenarios
- Rate limiting behavior

Mock Slack API calls:
```typescript
jest.mock('@slack/bolt');
jest.mock('./repositories/user.repository');
```

Requirements:
- 90%+ code coverage
- Test both success and failure paths
- Mock external dependencies (Slack API, database)
- Test rate limiting
- Test input validation
- Descriptive test names

Run tests with:
npm test -- --coverage
```

**Review Checkpoint:**
- [ ] All commands tested
- [ ] Event handlers tested
- [ ] Interactive components tested
- [ ] Security functions tested
- [ ] Coverage > 90%
- [ ] All tests passing

**References:** [Rule 37: Test Everything AI Generates](../README.md#rule-37-test-everything-ai-generates), [Rule 42: Mock External Services](../README.md#rule-42-mock-external-services)

---

### Step 9: Deployment Setup (5 minutes)

**Objective:** Prepare for production deployment

**Action:**
Configure deployment and hosting.

**Deployment Options:**

**Option A - Heroku:**
```bash
# Create Procfile
echo "web: npm start" > Procfile

# Set environment variables
heroku config:set SLACK_BOT_TOKEN=xoxb-...
heroku config:set SLACK_SIGNING_SECRET=...
heroku config:set DATABASE_URL=postgres://...

# Deploy
git push heroku main

# Update Slack app Request URLs to Heroku URL
```

**Option B - AWS Lambda (Serverless):**
```yaml
# serverless.yml
service: slack-bot

provider:
  name: aws
  runtime: nodejs20.x
  environment:
    SLACK_BOT_TOKEN: ${env:SLACK_BOT_TOKEN}
    SLACK_SIGNING_SECRET: ${env:SLACK_SIGNING_SECRET}

functions:
  slack-events:
    handler: handler.events
    events:
      - http:
          path: slack/events
          method: post
```

**Option C - Railway/Render:**
```bash
# Railway
railway init
railway add
railway up

# Set env vars in dashboard
# Update Slack Request URLs
```

**Deployment Checklist:**
- [ ] Environment variables set
- [ ] Database provisioned
- [ ] HTTPS enabled
- [ ] Health check endpoint working
- [ ] Slack Request URLs updated
- [ ] Event subscriptions verified
- [ ] Logging configured (Datadog, CloudWatch)
- [ ] Error monitoring (Sentry)
- [ ] Auto-scaling configured

**Update Slack App URLs:**
After deployment, update in Slack App settings:
- Event Subscriptions URL: https://your-domain.com/slack/events
- Slash Command URLs: https://your-domain.com/slack/commands
- Interactive Components URL: https://your-domain.com/slack/interactions

**References:** [Rule 18: Configuration as Code](../README.md#rule-18-configuration-as-code)

---

## Testing Procedures

### Manual Testing

**Test Slash Commands:**
1. In Slack, type `/hello Alice`
2. Verify response appears
3. Test edge cases: empty input, very long input
4. Check ephemeral vs public responses

**Test Events:**
1. Mention bot in channel: `@BotName help`
2. Send DM to bot
3. React to message (if handling reactions)
4. Verify bot doesn't respond to its own messages

**Test Interactive Components:**
1. Trigger button interaction
2. Open modal and submit
3. Test validation errors
4. Verify message updates after interaction

### Automated Testing
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Test specific file
npm test -- hello.test.ts

# Watch mode
npm test -- --watch
```

---

## Example Outputs

### Example Slash Command Response
```json
{
  "text": "Hello, Alice! 👋",
  "response_type": "in_channel",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Hello, *Alice*! 👋\n\nHow can I help you today?"
      }
    }
  ]
}
```

### Example Event Response
```typescript
await say({
  text: 'I noticed you mentioned me!',
  thread_ts: event.ts,  // Reply in thread
  blocks: [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: 'I noticed you mentioned me! How can I help?'
      }
    },
    {
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: { type: 'plain_text', text: 'Get Help' },
          action_id: 'help_button'
        }
      ]
    }
  ]
});
```

---

## Troubleshooting

### Issue 1: Bot Not Receiving Events
**Symptom:** No events triggering despite bot being mentioned

**Solution:**
1. Check Event Subscriptions are enabled
2. Verify Request URL is correct and accessible
3. Check ngrok is running (local dev)
4. Verify bot is added to channel
5. Check bot has correct scopes

### Issue 2: Signature Verification Failing
**Symptom:** 401 or verification errors

**Solution:**
1. Check SLACK_SIGNING_SECRET is correct
2. Verify timestamp is within 5 minutes
3. Check request body is raw (not parsed)
4. Test with Slack CLI: `slack run`

### Issue 3: Commands Not Responding
**Symptom:** Slash command shows error

**Solution:**
1. Ensure `ack()` is called within 3 seconds
2. Check command is registered correctly
3. Verify Request URL in Slash Command settings
4. Check logs for errors
5. Test endpoint with curl

### Issue 4: Rate Limiting Issues
**Symptom:** Getting 429 from Slack API

**Solution:**
1. Implement exponential backoff
2. Reduce message frequency
3. Use batching for bulk operations
4. Check Slack API rate limits
5. Cache responses when possible

---

## Completion Checklist

### Before Production Launch
- [ ] All commands working
- [ ] Events processed correctly
- [ ] Interactive components functional
- [ ] Database connected
- [ ] Security middleware in place
- [ ] Tests passing (90%+ coverage)
- [ ] Error handling complete
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Deployed to production
- [ ] Slack app URLs updated
- [ ] Bot invited to channels

### Code Review
- [ ] No hardcoded secrets
- [ ] Input validation on all commands
- [ ] Rate limiting implemented
- [ ] Signature verification working
- [ ] Error messages user-friendly
- [ ] Database queries optimized
- [ ] No infinite loops possible
- [ ] Proper logging in place

---

## Time Breakdown

**Setup (10 min):**
- Step 1: Slack app creation

**Development (40 min):**
- Step 2: Server setup - 10 min
- Step 3: Slash commands - 10 min
- Step 4: Event handlers - 10 min
- Step 5: Interactive components - 10 min

**Infrastructure (15 min):**
- Step 6: Database integration - 10 min
- Step 7: Security middleware - 5 min

**Testing & Deployment (15 min):**
- Step 8: Tests - 10 min
- Step 9: Deployment - 5 min

**Total: 60 minutes**

---

## Next Steps

After launching:

1. **Monitor Usage:**
   - Track command usage
   - Monitor error rates
   - Analyze user engagement

2. **Iterate:**
   - Add new commands based on feedback
   - Improve response quality
   - Optimize performance

3. **Scale:**
   - Add more integrations
   - Support multiple workspaces (OAuth)
   - Add advanced features (AI, workflows)

---

## Related Resources

**Templates:**
- [Integration Builder Template](../prompts/templates/integration-builder.md)
- [Backend Starter Template](../prompts/templates/backend-starter.md)

**Checklists:**
- [Daily Checklist](../DAILY_CHECKLIST.md)
- [Rules One Page](../RULES_ONE_PAGE.md)

**Rules to Review:**
- [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets)
- [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs)
- [Rule 24: Implement Rate Limiting](../README.md#rule-24-implement-rate-limiting)
- [Rule 28: Log Security Events](../README.md#rule-28-log-security-events)
- [Rule 37: Test Everything](../README.md#rule-37-test-everything-ai-generates)

**External Resources:**
- [Slack API Documentation](https://api.slack.com/)
- [Slack Bolt Framework](https://slack.dev/bolt-js/)
- [Block Kit Builder](https://app.slack.com/block-kit-builder/)

---

**Last Updated:** 2025-10-23
**Version:** 1.0
**Estimated Time:** 60 minutes
