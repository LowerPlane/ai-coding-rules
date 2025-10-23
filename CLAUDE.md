# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

**A documentation repository** teaching developers how to use AI coding assistants (Claude Code, GPT-4, etc.) safely and effectively. Contains 54 rules across prompt engineering, security, architecture, testing, and code quality.

**This is NOT a code project** - it's pure markdown documentation with no build/test/deploy processes.

## Repository Structure

**Current structure** (minimal - documentation only):
```
/
├── README.md              # Complete reference (all 54 rules)
├── RULES_ONE_PAGE.md      # Printable quick reference
├── INDEX.md               # Navigation index
├── DAILY_CHECKLIST.md     # 31-step workflow checklist
├── CLAUDE.md              # This file
└── .gitignore             # Git ignore rules
```

**Target structure** (full implementation):
```
ai-coding-rules/
│
├── rules/                     # Core rule documents
│   ├── 01-prompts.md
│   ├── 02-architecture.md
│   ├── 03-security.md
│   ├── 04-testing.md
│   ├── 05-file-structure.md
│   ├── 06-frontend.md
│   ├── 07-backend.md
│   ├── 08-growth.md
│   ├── 09-integrations.md
│   └── 10-performance.md
│
├── prompts/                   # Reusable prompt templates
│   ├── templates/
│   │   ├── backend-starter.md
│   │   ├── frontend-component.md
│   │   ├── integration-builder.md
│   │   └── growth-playbook.md
│   └── examples/             # Real-world prompt examples
│
├── workflows/                 # Step-by-step AI workflows
│   ├── api-generator.md
│   ├── landing-page-builder.md
│   ├── slack-bot-builder.md
│   └── seo-content-generator.md
│
├── examples/                  # Complete example projects
│   ├── react-dashboard/
│   ├── express-api/
│   ├── growth-automation/
│   └── slack-integration/
│
├── tools/                     # Linters, hooks, scripts
│   ├── lint-ai-code.js
│   ├── pre-commit-hook.sh
│   └── prompt-validator.py
│
├── .github/
│   └── workflows/
│       └── ai-code-review.yml # Automated AI code checks
│
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies
├── .eslintrc.js             # ESLint configuration
├── .prettierrc              # Prettier configuration
├── LICENSE                   # MIT License
├── README.md                # Main documentation
├── RULES_ONE_PAGE.md        # Quick reference
├── INDEX.md                 # Navigation
├── DAILY_CHECKLIST.md       # Workflow checklist
├── CLAUDE.md                # This file
└── .gitignore               # Git ignore rules
```

**Note**: Create directories incrementally as content is added.

## Core Documentation Philosophy

This repository teaches:
- **Humans design, AI implements** - Clear role separation
- **Security first** - Never compromise on security
- **Review everything** - Human review mandatory
- **Test thoroughly** - 90%+ coverage requirement

## Working with This Repository

### Editing Existing Rules

When updating rules in README.md:

1. **Never renumber existing rules** - They're referenced by number throughout docs
2. **Update 4 files** when changing a rule:
   - `README.md` - Full detailed version
   - `RULES_ONE_PAGE.md` - Condensed version
   - `INDEX.md` - Navigation links
   - `DAILY_CHECKLIST.md` - If it affects workflow

3. **Maintain the format**:
   ```markdown
   ### Rule XX: Title
   ❌ Bad: [example]
   ✅ Good: [example]

   **How to Follow:**
   - Bullet point 1
   - Bullet point 2
   ```

### Adding New Rules

1. Add to the end of the appropriate category in README.md
2. Use the next sequential number
3. Include ❌ Bad / ✅ Good examples
4. Add "How to Follow" section
5. Update all 4 files (README, RULES_ONE_PAGE, INDEX, CHECKLIST)

### Creating New Rule Documents

Rule documents go in `/rules/` directory (01-10):

1. Follow the numbering: `01-prompts.md`, `02-architecture.md`, etc.
2. Each file covers 5-10 related rules
3. Include ❌ Bad / ✅ Good examples for each rule
4. Cross-reference rule numbers from README.md
5. Update INDEX.md to link to the new rule document

### Creating New Templates

Templates go in `/prompts/templates/` directory:

**Categories**:
- `backend-starter.md` - API/backend projects
- `frontend-component.md` - UI components
- `integration-builder.md` - Third-party integrations
- `growth-playbook.md` - Marketing/SEO content

**Format**:
```markdown
# Template Name

## Context
- Stack: [specify]
- Existing: [what's built]
- Dependencies: [available packages]

## Task
[Specific description]

## Requirements
- Feature 1
- Feature 2

## Validation
[All validation rules]

## Output Format
- File: filename.ext
- Style: [functional/class]
- Tests: [scenarios]

## Security
- [Explicit security requirements]
```

Update INDEX.md to reference new templates.

### Creating New Workflows

Workflows go in `/workflows/` directory:

**Categories**:
- `api-generator.md` - Backend API workflows
- `landing-page-builder.md` - Marketing pages
- `slack-bot-builder.md` - Integration projects
- `seo-content-generator.md` - Content creation

**Format**:
1. Break into numbered steps (5-15 steps)
2. Include time estimates (e.g., "30-60 minutes")
3. Reference rules by number (e.g., "See Rule 21")
4. Include example prompts for each step
5. Add to INDEX.md under "Workflows"

### Creating Example Projects

Example projects go in `/examples/` directory:

**Categories**:
- `react-dashboard/` - Frontend example
- `express-api/` - Backend example
- `growth-automation/` - Marketing example
- `slack-integration/` - Integration example

**Each example should include**:
- `README.md` - Overview and setup
- `prompts-used.md` - All prompts that generated the code
- `review-notes.md` - Security and quality review
- Source code files
- Tests

### Creating Tools

Tools go in `/tools/` directory:

**Categories**:
- `lint-ai-code.js` - Stricter linting for AI code
- `pre-commit-hook.sh` - Git pre-commit checks
- `prompt-validator.py` - Validate prompt templates

**Requirements**:
1. Include usage instructions in file header
2. Follow the language conventions (JS/Shell/Python)
3. Add to README.md under "Tools" section
4. Include examples of usage

## Documentation Standards

### Writing Style

- **Tone**: Professional, educational, prescriptive
- **Examples**: Always include ❌ Bad and ✅ Good
- **Format**: Use markdown tables, code blocks, clear headings
- **Length**: Comprehensive but concise

### Markdown Conventions

- Use `#` headers (not underlines)
- Use fenced code blocks with language identifiers:
  ````markdown
  ```typescript
  const example = "code";
  ```
  ````
- Use tables for structured comparisons
- Use emoji only for visual markers: ✅ ❌ 🔒 ⚡ 📁 👁️

### Cross-References

When a rule number is mentioned:
- Link to the rule: `[Rule 19](#rule-19-never-hardcode-secrets)`
- Always verify the link works

## Git Workflow

### Commit Message Format

Use conventional commits:
```
docs(rules): add new security rule for API key rotation
docs(checklist): update testing workflow step 18
docs(templates): add FastAPI backend starter template
fix(typo): correct rule 23 code example
```

Types: `docs`, `fix`, `feat` (for new templates/workflows)

### Branch Strategy

- `main` - Published documentation
- `docs/feature-name` - For changes
- No complex CI/CD needed (documentation only)

## Key Content Areas

### The 54 Rules (Organized into 10 Documents)

**Core Documentation** (README.md contains all 54 rules):
1. **Prompt Engineering (1-10)** → `/rules/01-prompts.md`
2. **Architecture & Design (11-18)** → `/rules/02-architecture.md`
3. **Security (19-28)** → `/rules/03-security.md`
4. **Testing (37-42)** → `/rules/04-testing.md`
5. **File Organization (43-46)** → `/rules/05-file-structure.md`
6. **Frontend Development** → `/rules/06-frontend.md`
7. **Backend Development** → `/rules/07-backend.md`
8. **Growth & Marketing** → `/rules/08-growth.md`
9. **Integrations** → `/rules/09-integrations.md`
10. **Performance** → `/rules/10-performance.md`

**Current Status**:
- ✅ README.md has all 54 rules
- 🚧 Individual rule documents to be created in `/rules/`

### Templates (4 Categories)

**Location**: `/prompts/templates/`

1. **backend-starter.md** - API/backend scaffolding
2. **frontend-component.md** - React/Vue/Angular components
3. **integration-builder.md** - Slack/Notion/Zapier integrations
4. **growth-playbook.md** - Landing pages, SEO, content

### Workflows (4 Types)

**Location**: `/workflows/`

1. **api-generator.md** - 30-60 min - Complete REST API
2. **landing-page-builder.md** - 45 min - High-converting pages
3. **slack-bot-builder.md** - 60 min - Slack integration
4. **seo-content-generator.md** - 30 min - SEO content

### Example Projects (4 Categories)

**Location**: `/examples/`

1. **react-dashboard/** - Full frontend example
2. **express-api/** - Full backend example
3. **growth-automation/** - Marketing automation
4. **slack-integration/** - Integration example

### Tools (3 Utilities)

**Location**: `/tools/`

1. **lint-ai-code.js** - Stricter linting for AI-generated code
2. **pre-commit-hook.sh** - Git pre-commit validation
3. **prompt-validator.py** - Validate prompt templates

### Critical Rules (Never Skip)

- **Rule 19**: Never hardcode secrets
- **Rule 20**: AI cannot write security-critical code alone
- **Rule 21**: Validate all inputs
- **Rule 22**: Use parameterized queries only
- **Rule 37**: Test everything AI generates
- **Rule 47**: Human always reviews first

### Architecture Patterns Taught

The docs recommend this project structure for AI-assisted development:

```
/project/
├── /ai-generated/        # AI outputs here first
├── /src/                 # Merge after review
│   └── /features/        # Group by feature
│       └── /users/
│           ├── user.controller.ts
│           ├── user.service.ts
│           ├── user.repository.ts
│           └── user.test.ts
└── /prompts/            # Save prompts used
```

## Common Editing Tasks

### Fix a Typo
1. Edit the file directly
2. Commit: `fix(typo): correct spelling in rule 15`

### Update a Rule
1. Edit README.md (main source)
2. Edit RULES_ONE_PAGE.md (condensed version)
3. Edit corresponding `/rules/XX-category.md` file if it exists
4. Check INDEX.md (update navigation if needed)
5. Check DAILY_CHECKLIST.md (update if workflow affected)
6. Commit: `docs(rules): update rule 22 SQL injection example`

### Add a New Rule Document
1. Create `/rules/XX-category.md` (e.g., `04-testing.md`)
2. Extract 5-10 related rules from README.md
3. Add detailed explanations and examples
4. Cross-reference rule numbers
5. Update INDEX.md navigation
6. Commit: `docs(rules): add testing rules document`

### Add a Template
1. Create in `/prompts/templates/template-name.md`
2. Follow template format with all required sections
3. Include Context, Task, Requirements, Validation, Output Format, Security
4. Add to INDEX.md under Templates section
5. Optionally add example usage in `/prompts/examples/`
6. Commit: `docs(templates): add Django REST API starter template`

### Add a Workflow
1. Create in `/workflows/workflow-name.md`
2. Number all steps clearly (5-15 steps)
3. Include time estimates for each phase
4. Reference rules by number (e.g., "See Rule 21")
5. Include example prompts for each step
6. Add to INDEX.md under Workflows section
7. Commit: `docs(workflows): add microservice deployment workflow`

### Add an Example Project
1. Create directory in `/examples/project-name/`
2. Include all source files
3. Add `README.md` with setup instructions
4. Add `prompts-used.md` documenting all AI prompts
5. Add `review-notes.md` with security/quality review
6. Update INDEX.md under Examples section
7. Commit: `docs(examples): add Express API example project`

### Add a Tool/Script
1. Create in `/tools/script-name.ext`
2. Add usage instructions in file header
3. Make it executable if shell script: `chmod +x tools/script-name.sh`
4. Add usage documentation to README.md
5. Update INDEX.md under Tools section
6. Commit: `feat(tools): add AI code linting script`

## Quality Checklist for Changes

Before committing documentation changes:

- [ ] Technical accuracy verified
- [ ] Examples are realistic and practical
- [ ] ❌ Bad and ✅ Good examples included
- [ ] Cross-references updated (if rule numbers mentioned)
- [ ] Consistent terminology used
- [ ] Markdown properly formatted
- [ ] All affected files updated (README, RULES_ONE_PAGE, INDEX, CHECKLIST)
- [ ] Commit message follows convention

## Important Notes

### What Makes Good Documentation Here

✅ Clear, specific examples
✅ Actionable "How to Follow" sections
✅ Security-focused
✅ Consistent formatting
✅ Practical, not theoretical

### What to Avoid

❌ Generic advice without examples
❌ Repeating obvious information
❌ Breaking rule number sequences
❌ Incomplete cross-references
❌ Overly verbose explanations

## Quick Reference

- **All rules**: README.md
- **Quick lookup**: RULES_ONE_PAGE.md
- **Navigation**: INDEX.md
- **Daily workflow**: DAILY_CHECKLIST.md

This repository teaches others how to use AI coding assistants safely - prioritize clarity, accuracy, and practical examples in all documentation.
