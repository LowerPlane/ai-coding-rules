# AI Coding Rules - One-Page Reference

**Print this page and keep it at your desk!**

---

## 🎯 The Golden Rules (Top 10)

| # | Rule | ❌ Don't | ✅ Do |
|---|------|----------|-------|
| 1 | **Provide Context First** | "Build an API" | "Express + TypeScript + PostgreSQL API with JWT auth" |
| 2 | **Never Hardcode Secrets** | `API_KEY = "sk_123"` | `API_KEY = process.env.API_KEY` |
| 3 | **Validate All Inputs** | Trust user data | Use Zod/Joi validation |
| 4 | **Parameterized Queries** | `` `SQL ${input}` `` | `db.query('SQL ?', [input])` |
| 5 | **Test Everything** | Deploy without tests | 90%+ coverage required |
| 6 | **AI Code Separate** | Generate to /src/ | Generate to /ai-generated/ |
| 7 | **Human Reviews First** | Auto-deploy | Review → Approve → Deploy |
| 8 | **Humans Design** | AI designs system | Human designs, AI implements |
| 9 | **Small Functions** | 200-line functions | < 50 lines per function |
| 10 | **Explicit Types** | `any` everywhere | Strict TypeScript types |

---

## 📝 Prompt Template

```markdown
## Context
- Stack: [Framework/DB/Language]
- Existing: [What's built]
- Dependencies: [Available packages]

## Task
[Specific, detailed description]

## Requirements
- Feature 1
- Feature 2
- Feature 3

## Validation
- Field rules
- Error handling

## Output Format
- File: filename.ts
- Style: [functional/class]
- Tests: [scenarios]

## Security
- Validate inputs
- Parameterized queries
- No secrets
```

---

## 🔒 Security Checklist

```
☐ No hardcoded secrets in code
☐ All inputs validated with Zod
☐ Parameterized queries only
☐ Passwords hashed with bcrypt (cost 12+)
☐ Rate limiting on all endpoints
☐ HTTPS enforced
☐ XSS protection enabled
☐ CSRF tokens for state changes
☐ Authentication on protected routes
☐ Authorization checks for resources
```

---

## 🏗️ Architecture Pattern

```
Human Defines:
├── Domain Models (types/interfaces)
├── API Contracts (DTOs)
└── Business Rules

AI Implements:
├── Controllers (HTTP handling)
├── Services (business logic)
├── Repositories (data access)
├── Validators (input checking)
└── Tests (90%+ coverage)

Human Reviews:
├── Security vulnerabilities
├── Business logic correctness
├── Performance issues
└── Code quality
```

---

## 📁 File Structure

```
/project/
├── /ai-generated/        ← AI outputs here first
│   └── /feature/
│       ├── code.ts
│       └── tests.ts
│
├── /src/                 ← Merge after review
│   └── /features/
│       └── /users/
│           ├── user.controller.ts
│           ├── user.service.ts
│           ├── user.repository.ts
│           ├── user.types.ts
│           └── user.test.ts
│
└── /prompts/            ← Save prompts
    └── user-feature.md
```

---

## ✅ Review Checklist

### Before Merging AI Code:

**Automated:**
```bash
npm run lint:ai-code   # Linting passes
npm test               # All tests pass
npm run format:check   # Formatting OK
```

**Manual:**
```
Security:
☐ No secrets hardcoded
☐ Inputs validated
☐ SQL injection prevented
☐ XSS protection present

Quality:
☐ Functions < 50 lines
☐ No TypeScript any
☐ Error handling complete
☐ Tests cover edge cases

Business Logic:
☐ Requirements met
☐ Edge cases handled
☐ Performance acceptable
☐ Documentation clear
```

---

## 🚫 Never Let AI Do Alone

```
❌ Payment processing logic
❌ Encryption implementations
❌ Password hashing (only use bcrypt library)
❌ OAuth flows (use official SDKs)
❌ System architecture design
❌ Database schema design
❌ Security policy decisions
❌ Deploy to production
```

---

## ✅ AI is Great For

```
✅ CRUD operations
✅ Input validation boilerplate
✅ API route handlers
✅ Data transformations
✅ Test scaffolding
✅ Type definitions
✅ Documentation comments
✅ Basic UI components
✅ Utility functions
✅ Configuration files
```

---

## 📊 Code Quality Metrics

```
Function Length:     Max 50 lines
File Length:         Max 300 lines
Cyclomatic Complex:  Max 10
Test Coverage:       Min 90%
TypeScript Strict:   Enabled
ESLint Errors:       0
Security Warnings:   0
```

---

## 🔄 Workflow

```
1. Write Prompt
   ├─ Use template
   ├─ Include context
   └─ Specify requirements

2. Generate Code
   ├─ AI outputs to /ai-generated/
   └─ Save prompt used

3. Run Checks
   ├─ npm run lint:ai-code
   ├─ npm test
   └─ npm run audit-security

4. Review
   ├─ Security review
   ├─ Logic review
   └─ Performance check

5. Approve & Merge
   ├─ Move to /src/
   ├─ Commit with message
   └─ Tag as AI-generated

6. Deploy
   ├─ After human approval
   └─ Monitor for issues
```

---

## 💡 Pro Tips

### Tip 1: Be Specific
Generic: "Create a login"
Better: "Create React login with email/password, validation, loading states, error display"

### Tip 2: Provide Examples
```typescript
// Include in prompt:
// Input: { email: "test@example.com", name: "John" }
// Output: { id: "uuid", email: "test@example.com", ... }
```

### Tip 3: Iterate in Steps
Phase 1: Basic structure → Review
Phase 2: Add features → Review
Phase 3: Optimize → Review

### Tip 4: Reference Existing Code
"Follow same pattern as user.service.ts"
"Use same error handling as auth.controller.ts"

---

## 🆘 Troubleshooting

**AI generates insecure code?**
→ Add explicit security requirements in prompt

**Tests fail?**
→ Check test data matches schema
→ Verify mocks are set up correctly

**Linting errors?**
→ Run `npm run lint:fix`
→ Check .eslintrc.js config

**AI ignores requirements?**
→ Be more specific in prompt
→ Break into smaller tasks
→ Provide examples

---

## 📚 Quick Commands

```bash
# Setup
npm install
npm run setup-hooks

# Linting
npm run lint              # Check
npm run lint:fix          # Auto-fix
npm run lint:ai-code      # AI code only

# Testing
npm test                  # Run tests
npm run test:coverage     # With coverage

# AI Code
npm run validate-prompts  # Check prompts
npm run merge-ai-code     # Merge reviewed

# Security
npm run audit-security    # Security audit
```

---

## 🎓 Remember

> **"AI writes the code. Humans ensure it's right."**

- AI is a tool, not a replacement
- Always review before deploying
- Security is non-negotiable
- Testing is mandatory
- Context makes AI better

---

**Last Updated: 2025-10-15**

**For full details, see: [README.md](./README.md)**
