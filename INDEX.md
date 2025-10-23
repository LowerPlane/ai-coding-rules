# AI Coding Rules - Complete Index

**Quick navigation to all rules, guidelines, and resources**

---

## 📚 Start Here

New to AI-assisted coding? Start with these in order:

1. **[README.md](./README.md)** ✅ - All 54 rules with examples and philosophy
2. **[RULES_ONE_PAGE.md](./RULES_ONE_PAGE.md)** ✅ - Printable quick reference
3. **[DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)** ✅ - 31-step workflow checklist
4. **[rules/01-prompts.md](./rules/01-prompts.md)** ✅ - Detailed prompt engineering guide

---

## 📋 All Rules by Category

### Prompt Engineering (Rules 1-10)
| Rule | Title | Summary |
|------|-------|---------|
| 1 | Never Use Generic Prompts | Be specific, not vague |
| 2 | Always Provide Context First | Give AI full picture before task |
| 3 | Specify Output Format Explicitly | Define files, style, structure |
| 4 | Include Validation Requirements | Detail all validation rules |
| 5 | Define Success and Error Scenarios | List all possible outcomes |
| 6 | Specify Dependencies Explicitly | List available packages |
| 7 | Request Tests Upfront | Always include test requirements |
| 8 | Provide Style Guidelines | Define coding conventions |
| 9 | Use Example-Driven Prompts | Show input/output examples |
| 10 | Break Complex Tasks Into Steps | Phase-by-phase generation |

**Full Details:** [rules/01-prompts.md](./rules/01-prompts.md)

---

### Architecture & Design (Rules 11-18)
| Rule | Title | Summary |
|------|-------|---------|
| 11 | Humans Design, AI Implements | Clear role separation |
| 12 | One Responsibility Per File | Small, focused files |
| 13 | Interface-First Development | Define contracts first |
| 14 | Dependency Injection Over Hardcoding | Pass dependencies |
| 15 | Stateless Services | External state management |
| 16 | Separation of Concerns | Controller/Service/Repository |
| 17 | Return Types Over Throwing | Use Result<T,E> types |
| 18 | Configuration as Code | Centralized config |

**Full Details:** [rules/02-architecture.md](./rules/02-architecture.md)

---

### Security (Rules 19-28)
| Rule | Title | Summary |
|------|-------|---------|
| 19 | Never Hardcode Secrets | Environment variables only |
| 20 | AI Cannot Write Security-Critical Code Alone | Human oversight required |
| 21 | Validate All Inputs | Zod/Joi schemas |
| 22 | Use Parameterized Queries Only | Prevent SQL injection |
| 23 | Sanitize All Output | Prevent XSS |
| 24 | Implement Rate Limiting | Protect endpoints |
| 25 | Hash Passwords Correctly | bcrypt cost 12+ |
| 26 | Secure JWT Tokens | Short-lived, rotated |
| 27 | Apply Defense in Depth | Multiple security layers |
| 28 | Log Security Events | Audit trail |

**Full Details:** [rules/03-security.md](./rules/03-security.md)

---

### Code Quality (Rules 29-36)
| Rule | Title | Summary |
|------|-------|---------|
| 29 | Explicit Over Implicit | Clear types and names |
| 30 | Small Functions | Under 50 lines |
| 31 | No Magic Numbers | Use named constants |
| 32 | Meaningful Variable Names | Descriptive, not generic |
| 33 | DRY (Don't Repeat Yourself) | Extract reusable code |
| 34 | Comment Why, Not What | Explain reasoning |
| 35 | Handle Errors Gracefully | Specific error handling |
| 36 | Use TypeScript Strictly | No any types |

**Full Details:** [README.md](./README.md#code-quality-rules) (Detailed doc coming soon)

---

### Testing (Rules 37-42)
| Rule | Title | Summary |
|------|-------|---------|
| 37 | Test Everything AI Generates | 90%+ coverage |
| 38 | Test Business Logic, Not Framework | Focus on your code |
| 39 | Arrange-Act-Assert Pattern | Clear test structure |
| 40 | Test Edge Cases | Boundaries and errors |
| 41 | Use Descriptive Test Names | Clear what's tested |
| 42 | Mock External Services | Isolate tests |

**Full Details:** [README.md](./README.md#testing-rules) (Detailed doc coming soon)

---

### File Organization (Rules 43-46)
| Rule | Title | Summary |
|------|-------|---------|
| 43 | Consistent File Structure | Standard project layout |
| 44 | AI Code in Separate Directory | Review before merge |
| 45 | Group by Feature, Not Type | Feature-based folders |
| 46 | Shared Code in Common Directory | Centralize utilities |

**Full Details:** [AI_CODING_RULES_COMPLETE.md](./AI_CODING_RULES_COMPLETE.md#file-organization-rules)

---

### Review & Approval (Rules 47-50)
| Rule | Title | Summary |
|------|-------|---------|
| 47 | Human Always Reviews First | No auto-deploy |
| 48 | Use Code Review Checklist | Standardized reviews |
| 49 | AI Code Gets Stricter Linting | Higher standards |
| 50 | Document AI Generation | Track AI involvement |

**Full Details:** [AI_CODING_RULES_COMPLETE.md](./AI_CODING_RULES_COMPLETE.md#review--approval-rules)

---

### Version Control (Rules 51-54)
| Rule | Title | Summary |
|------|-------|---------|
| 51 | Meaningful Commit Messages | Conventional commits |
| 52 | Small, Focused Commits | Logical units |
| 53 | Tag AI-Generated Commits | Clear attribution |
| 54 | Branch Strategy for AI Code | Feature branches |

**Full Details:** [AI_CODING_RULES_COMPLETE.md](./AI_CODING_RULES_COMPLETE.md#version-control-rules)

---

## 🎯 Rules by Priority

### 🔴 Critical (Never Skip)
Must follow for security and reliability:
- Rule 19: Never hardcode secrets
- Rule 20: AI cannot write security-critical code alone
- Rule 21: Validate all inputs
- Rule 22: Use parameterized queries only
- Rule 37: Test everything AI generates
- Rule 47: Human always reviews first

### 🟡 Important (Follow Most Times)
Essential for quality:
- Rule 2: Always provide context first
- Rule 11: Humans design, AI implements
- Rule 30: Small functions
- Rule 44: AI code in separate directory
- Rule 48: Use code review checklist

### 🟢 Recommended (Best Practices)
For optimal results:
- All other rules in the list

---

## 📝 Templates & Workflows

### Available Templates
| Template | Status | Use Case | Location |
|----------|--------|----------|----------|
| Backend Starter | ✅ Complete | REST API endpoints | [prompts/templates/backend-starter.md](./prompts/templates/backend-starter.md) |
| Frontend Component | 📝 Placeholder | React components | [prompts/templates/frontend-component.md](./prompts/templates/frontend-component.md) |
| Integration Builder | 📝 Placeholder | Slack/Notion bots | [prompts/templates/integration-builder.md](./prompts/templates/integration-builder.md) |
| Growth Playbook | 📝 Placeholder | Landing pages | [prompts/templates/growth-playbook.md](./prompts/templates/growth-playbook.md) |

### Available Workflows
| Workflow | Status | Duration | Location |
|----------|--------|----------|----------|
| API Generator | 📝 Placeholder | 30-60 min | [workflows/api-generator.md](./workflows/api-generator.md) |
| Landing Page Builder | 📝 Placeholder | 45 min | [workflows/landing-page-builder.md](./workflows/landing-page-builder.md) |
| Slack Bot Builder | 📝 Placeholder | 60 min | [workflows/slack-bot-builder.md](./workflows/slack-bot-builder.md) |
| SEO Content Generator | 📝 Placeholder | 30 min | [workflows/seo-content-generator.md](./workflows/seo-content-generator.md) |

---

## 🔧 Tools & Utilities

### Available Tools

| Tool | Status | Purpose | Usage |
|------|--------|---------|-------|
| lint-ai-code.js | ✅ Complete | Stricter linting for AI code | `node tools/lint-ai-code.js <dir>` |
| pre-commit-hook.sh | ✅ Complete | Git pre-commit security checks | `cp tools/pre-commit-hook.sh .git/hooks/pre-commit` |
| prompt-validator.py | ✅ Complete | Validate prompt templates | `python tools/prompt-validator.py <template>` |

### Tool Usage Examples

```bash
# Validate a prompt template (Rule 1-10)
python tools/prompt-validator.py prompts/templates/backend-starter.md

# Lint AI-generated code with stricter rules (Rule 49)
node tools/lint-ai-code.js ai-generated/my-feature

# Install pre-commit hook (checks for secrets - Rule 19)
cp tools/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## 📖 Documentation Index

### Core Documentation (✅ Complete)
- [README.md](./README.md) - All 54 rules with examples
- [RULES_ONE_PAGE.md](./RULES_ONE_PAGE.md) - Printable quick reference
- [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md) - 31-step workflow
- [CLAUDE.md](./CLAUDE.md) - AI assistant guidance
- [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
- [LICENSE](./LICENSE) - MIT License

### Detailed Rule Documents
- [rules/01-prompts.md](./rules/01-prompts.md) ✅ - Prompt engineering (Rules 1-10)
- [rules/02-architecture.md](./rules/02-architecture.md) ✅ - Architecture (Rules 11-18)
- [rules/03-security.md](./rules/03-security.md) ✅ - Security (Rules 19-28)
- [rules/04-testing.md](./rules/04-testing.md) 📝 - Testing (Rules 37-42)
- [rules/05-file-structure.md](./rules/05-file-structure.md) 📝 - File org (Rules 43-46)
- [rules/06-10-*.md](./rules/) 📝 - Additional categories

### Prompt Templates & Workflows
- [prompts/templates/backend-starter.md](./prompts/templates/backend-starter.md) ✅ - Complete API template
- [prompts/templates/](./prompts/templates/) 📝 - 3 placeholder templates
- [workflows/](./workflows/) 📝 - 4 workflow guides

### Examples & Tools
- [examples/](./examples/) 📝 - 4 example project structures
- [tools/](./tools/) ✅ - 3 validation/linting scripts

---

## 🎓 Learning Paths

### Path 1: Beginner (First Week)
1. Read [README.md](./README.md)
2. Follow [QUICK_START.md](./QUICK_START.md)
3. Study [RULES_ONE_PAGE.md](./RULES_ONE_PAGE.md)
4. Try [backend-starter.md](./prompts/templates/backend-starter.md)
5. Use [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)

### Path 2: Intermediate (Second Week)
1. Read [01-prompts.md](./rules/01-prompts.md) in depth
2. Read [02-architecture.md](./rules/02-architecture.md)
3. Follow [api-generator.md](./workflows/api-generator.md)
4. Review security rules
5. Practice with real projects

### Path 3: Advanced (Third Week)
1. Read [AI_CODING_RULES_COMPLETE.md](./AI_CODING_RULES_COMPLETE.md)
2. Customize templates for your stack
3. Create team-specific workflows
4. Contribute improvements
5. Mentor others

---

## 🔍 Quick Reference by Use Case

### "I need to build an API"
1. Read: [backend-starter.md](./prompts/templates/backend-starter.md)
2. Follow: [api-generator.md](./workflows/api-generator.md)
3. Check: [03-security.md](./rules/03-security.md)
4. Use: [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)

### "I need to review AI code"
1. Use: [DAILY_CHECKLIST.md](./DAILY_CHECKLIST.md)
2. Check: Security Rules (19-28)
3. Verify: Code Quality Rules (29-36)
4. Run: `npm run lint:ai-code && npm test`

### "I'm starting a new project"
1. Read: [STRUCTURE.md](./STRUCTURE.md)
2. Follow: [02-architecture.md](./rules/02-architecture.md)
3. Setup: Project structure
4. Customize: Templates for your stack

### "I need better prompts"
1. Read: [01-prompts.md](./rules/01-prompts.md)
2. Use: Template structure
3. Follow: Rules 1-10
4. Iterate: Based on results

---

## 📊 Metrics & KPIs

Track these to measure success:

### Code Quality
- Functions < 50 lines: 100%
- Test coverage: > 90%
- TypeScript strict: Enabled
- Linting errors: 0

### Security
- Hardcoded secrets: 0
- Security warnings: 0
- Code review coverage: 100%
- Vulnerability count: 0

### Productivity
- Time to build API: < 1 hour
- Code review time: < 30 min
- Bug rate: < 5%
- Deployment frequency: ↑

---

## 🗺️ Repository Map

```
ai-coding-rules/
│
├── 📖 CORE DOCS (Start Here)
│   ├── README.md                    ⭐ All 54 rules
│   ├── QUICK_START.md               ⭐ 5-minute setup
│   ├── RULES_ONE_PAGE.md            ⭐ Printable reference
│   ├── DAILY_CHECKLIST.md           ⭐ Daily workflow
│   ├── INDEX.md                     ⭐ This file
│   ├── SETUP.md                     Publishing guide
│   ├── STRUCTURE.md                 Repo organization
│   ├── CONTRIBUTING.md              How to contribute
│   └── LICENSE                      MIT License
│
├── 📋 RULES (Detailed Guidelines)
│   └── rules/
│       ├── 01-prompts.md           ✅ Complete
│       ├── 02-architecture.md      ✅ Complete
│       └── 03-security.md          ✅ Complete
│
├── 📝 TEMPLATES (Reusable Prompts)
│   └── prompts/templates/
│       └── backend-starter.md      ✅ Complete
│
├── 🔄 WORKFLOWS (Step-by-Step)
│   └── workflows/
│       └── api-generator.md        ✅ Complete
│
├── ⚙️ CONFIG (Setup Files)
│   ├── package.json                ✅ Complete
│   ├── .eslintrc.js               ✅ Complete
│   └── .gitignore                 ✅ Complete
│
└── 📁 DIRECTORIES (Ready for Content)
    ├── examples/                   🚧 Add your examples
    ├── tools/                      🚧 Add helper scripts
    └── ai-generated/               🚧 AI output staging
```

---

## 🔗 External Resources

### Official Documentation
- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

### Style Guides (Inspiration)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [The Twelve-Factor App](https://12factor.net/)

### Security Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)

---

## ❓ FAQ Quick Links

**Q: Where do I start?**
A: [QUICK_START.md](./QUICK_START.md)

**Q: How do I write a good prompt?**
A: [rules/01-prompts.md](./rules/01-prompts.md)

**Q: Is this secure?**
A: [rules/03-security.md](./rules/03-security.md)

**Q: What's the workflow?**
A: [workflows/api-generator.md](./workflows/api-generator.md)

**Q: How do I contribute?**
A: [CONTRIBUTING.md](./CONTRIBUTING.md)

**Q: Can I print a quick reference?**
A: [RULES_ONE_PAGE.md](./RULES_ONE_PAGE.md)

---

## 📞 Support

- **Documentation Issues**: Open GitHub issue
- **Questions**: GitHub Discussions
- **Security Concerns**: Email maintainers
- **Feature Requests**: GitHub Issues

---

**Last Updated:** 2025-10-15

**Total Rules:** 54
**Documentation Pages:** 10+
**Templates:** 1 (more coming)
**Workflows:** 1 (more coming)

---

**[⬆ Back to README](./README.md)**
