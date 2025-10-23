# Daily AI Coding Checklist

**Copy this checklist for each AI coding task**

---

## Pre-Generation Checklist

### ☐ 1. Preparation
- [ ] Know exactly what you need to build
- [ ] Have tech stack requirements ready
- [ ] Know which files/features already exist
- [ ] Understand integration points
- [ ] Have acceptance criteria defined

### ☐ 2. Prompt Ready
- [ ] Context section complete (stack, dependencies, conventions)
- [ ] Task clearly described (specific, not generic)
- [ ] Requirements listed (functional + non-functional)
- [ ] Validation rules specified
- [ ] Output format defined
- [ ] Test scenarios included
- [ ] Security requirements explicit
- [ ] Examples provided (if complex)

### ☐ 3. Environment Ready
- [ ] `/ai-generated/` directory exists
- [ ] Linting configured
- [ ] Tests can run
- [ ] Dependencies installed
- [ ] Git branch created (`ai/feature-name`)

---

## Generation Checklist

### ☐ 4. Generate Code
- [ ] Used complete prompt template
- [ ] AI outputs to `/ai-generated/feature-name/`
- [ ] Saved prompt used to `/prompts/feature-name.md`
- [ ] Generated all required files
- [ ] Files compile without errors

### ☐ 5. Initial Review (Quick Scan)
- [ ] Code looks reasonable (no obvious errors)
- [ ] All requested files present
- [ ] No hardcoded secrets visible
- [ ] Tests were generated
- [ ] Documentation included

---

## Automated Checks Checklist

### ☐ 6. Run Quality Tools
```bash
# Run each command and check results
npm run lint:ai-code          # [ ] Passes
npm run format:check          # [ ] Passes
npm test                      # [ ] Passes
npm run test:coverage         # [ ] > 90%
npm run audit-security        # [ ] No issues
```

### ☐ 7. TypeScript Checks
- [ ] No `any` types used
- [ ] All function return types explicit
- [ ] No implicit returns
- [ ] Strict mode enabled
- [ ] No TypeScript errors

---

## Security Review Checklist

### ☐ 8. Security Basics
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] No sensitive data in logs
- [ ] No comments with credentials
- [ ] Environment variables validated on startup

### ☐ 9. Input Validation
- [ ] All user inputs validated (Zod/Joi schema)
- [ ] Email format validated
- [ ] String lengths limited (min/max)
- [ ] Numbers have bounds (min/max, positive only)
- [ ] Arrays have size limits
- [ ] File uploads validated (type, size)

### ☐ 10. Injection Prevention
- [ ] SQL queries use parameterized statements (NO string concat)
- [ ] No eval() or Function() with user input
- [ ] No shell commands with user input
- [ ] HTML output sanitized (DOMPurify)
- [ ] URLs validated before redirect

### ☐ 11. Authentication & Authorization
- [ ] Protected routes have authMiddleware
- [ ] JWT tokens expire (< 1 hour for access tokens)
- [ ] Passwords hashed with bcrypt (cost 12+)
- [ ] Rate limiting on auth endpoints (5 per 15 min)
- [ ] Authorization checks for resource access
- [ ] User can only access own data

### ☐ 12. Security Headers & Config
- [ ] HTTPS enforced
- [ ] CORS configured (specific origins, not *)
- [ ] Security headers set (HSTS, CSP, X-Frame-Options)
- [ ] CSRF protection for state-changing ops
- [ ] Cookies are httpOnly and secure

---

## Code Quality Review Checklist

### ☐ 13. Function Quality
- [ ] Functions under 50 lines
- [ ] One responsibility per function
- [ ] Descriptive function names (not generic)
- [ ] No nested callbacks (use async/await)
- [ ] Early returns for error cases
- [ ] No side effects in pure functions

### ☐ 14. Code Structure
- [ ] Proper separation of concerns (controller/service/repository)
- [ ] No business logic in controllers
- [ ] No database queries in controllers
- [ ] Dependencies injected (not hardcoded)
- [ ] Configuration externalized
- [ ] No magic numbers (use constants)

### ☐ 15. Error Handling
- [ ] All errors caught and handled
- [ ] Specific error types (not generic Error)
- [ ] User-friendly error messages
- [ ] Internal errors logged (with context)
- [ ] No empty catch blocks
- [ ] Errors don't expose sensitive info

### ☐ 16. Naming & Style
- [ ] camelCase for variables and functions
- [ ] PascalCase for classes and components
- [ ] UPPER_SNAKE_CASE for constants
- [ ] Descriptive names (not x, temp, data)
- [ ] Boolean prefixes (is, has, should, can)
- [ ] Consistent naming across codebase

---

## Testing Review Checklist

### ☐ 17. Test Coverage
- [ ] Happy path tested
- [ ] Edge cases tested (null, undefined, empty)
- [ ] Error scenarios tested
- [ ] Validation errors tested
- [ ] Authorization failures tested
- [ ] Database errors tested
- [ ] Coverage > 90%

### ☐ 18. Test Quality
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] Descriptive test names ("should X when Y")
- [ ] One assertion per test (or related assertions)
- [ ] Tests are independent (no shared state)
- [ ] External services mocked
- [ ] Database operations use test data

### ☐ 19. Test Types
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Validation tests for all inputs
- [ ] Error handling tests
- [ ] Edge case tests

---

## Documentation Review Checklist

### ☐ 20. Code Documentation
- [ ] JSDoc comments on exported functions
- [ ] Complex logic explained
- [ ] Parameters documented
- [ ] Return types documented
- [ ] Exceptions documented
- [ ] Examples provided for complex functions

### ☐ 21. API Documentation
- [ ] Endpoint documented (method, path)
- [ ] Request body schema documented
- [ ] Response format documented
- [ ] Error responses documented
- [ ] Authentication requirements clear
- [ ] Rate limits documented

---

## Business Logic Review Checklist

### ☐ 22. Requirements Met
- [ ] All functional requirements implemented
- [ ] All edge cases handled
- [ ] Business rules correct
- [ ] Data validation matches business rules
- [ ] Error messages align with business context

### ☐ 23. Performance
- [ ] Database queries optimized (no N+1)
- [ ] Appropriate indexes used
- [ ] Large datasets paginated
- [ ] Heavy operations async/queued
- [ ] Caching used where appropriate
- [ ] Response time acceptable (< 500ms)

---

## Final Review Checklist

### ☐ 24. Human Review
- [ ] Code reviewed by another human
- [ ] Security review by security-conscious dev
- [ ] Logic verified against requirements
- [ ] Performance tested with realistic data
- [ ] Edge cases manually tested

### ☐ 25. Integration Check
- [ ] Integrates with existing codebase
- [ ] Follows project conventions
- [ ] Dependencies compatible
- [ ] No breaking changes introduced
- [ ] Backwards compatible (if applicable)

---

## Pre-Merge Checklist

### ☐ 26. Documentation
- [ ] README updated (if needed)
- [ ] API docs updated
- [ ] CHANGELOG updated
- [ ] Migration guide (if breaking change)
- [ ] Prompt saved to `/prompts/`

### ☐ 27. Git
- [ ] Meaningful commit message
- [ ] Commit tagged as AI-generated
- [ ] Prompt reference in commit
- [ ] Reviewer tagged
- [ ] No sensitive data in commit history

### ☐ 28. Cleanup
- [ ] Debug code removed
- [ ] Console.logs removed (except errors/warnings)
- [ ] Commented-out code removed
- [ ] TODO comments have tickets
- [ ] No temporary files

---

## Merge & Deploy Checklist

### ☐ 29. Pre-Merge
- [ ] All automated checks pass
- [ ] Human review approved
- [ ] PR comments addressed
- [ ] Conflicts resolved
- [ ] Branch up to date with main

### ☐ 30. Merge
- [ ] Code moved from `/ai-generated/` to `/src/`
- [ ] Tests passing on main branch
- [ ] CI/CD pipeline successful
- [ ] No new warnings or errors

### ☐ 31. Post-Deploy
- [ ] Feature works in staging
- [ ] Monitoring shows no errors
- [ ] Performance metrics acceptable
- [ ] User feedback positive (if applicable)
- [ ] Rollback plan ready

---

## Quick Daily Summary

**Before Each AI Generation:**
```
☐ Clear requirements
☐ Complete prompt
☐ Clean environment
```

**After Generation:**
```
☐ Automated checks pass
☐ Security review done
☐ Code quality verified
☐ Tests cover everything
```

**Before Merge:**
```
☐ Human review approved
☐ Documentation updated
☐ All tests passing
```

**After Deploy:**
```
☐ Monitoring healthy
☐ No errors in logs
☐ Feature working
```

---

## Emergency Checklist (If Something Breaks)

### ☐ Incident Response
1. [ ] Immediately rollback to previous version
2. [ ] Check error logs for root cause
3. [ ] Identify if AI-generated code is cause
4. [ ] Review what human review missed
5. [ ] Add test case to prevent recurrence
6. [ ] Update review checklist if needed
7. [ ] Document incident and learnings

---

## Weekly Review Checklist

### ☐ Process Improvement
- [ ] Review all AI-generated code from week
- [ ] Identify patterns in bugs/issues
- [ ] Update prompts if needed
- [ ] Update checklist if gaps found
- [ ] Share learnings with team
- [ ] Celebrate successes

---

## Printable Quick Version

```
PRE-GENERATION
☐ Clear prompt with context
☐ Security requirements explicit
☐ Test scenarios defined

GENERATION
☐ Output to /ai-generated/
☐ Save prompt used

AUTOMATED CHECKS
☐ Lint passes
☐ Tests pass (90%+)
☐ No security warnings

SECURITY REVIEW
☐ No hardcoded secrets
☐ Input validation present
☐ Parameterized queries
☐ Auth/authz correct

QUALITY REVIEW
☐ Functions < 50 lines
☐ No TypeScript any
☐ Error handling complete
☐ Tests cover edge cases

HUMAN REVIEW
☐ Logic correct
☐ Requirements met
☐ Performance acceptable

MERGE
☐ Move to /src/
☐ Commit with AI tag
☐ Deploy after approval
```

---

**Save this file and check off items for each AI coding task!**

**File location for this checklist template:**
`/prompts/daily-checklist.md`

**Create a copy for each feature:**
```bash
cp prompts/daily-checklist.md ai-generated/my-feature/CHECKLIST.md
```

Then check off items as you complete them!
