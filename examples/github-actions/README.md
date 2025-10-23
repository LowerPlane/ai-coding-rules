# GitHub Actions Example for AI Code Review

This is an **example** GitHub Actions workflow that demonstrates how to implement automated validation for AI-generated code based on the rules in this repository.

## What This Is

An example CI/CD workflow that you can adapt for your own projects to enforce the AI coding rules.

## What It Checks

1. **Documentation validation** - Broken links, markdown formatting
2. **Prompt template validation** - Using prompt-validator.py
3. **Security checks** - No hardcoded secrets (Rule 19)
4. **Repository structure** - Verify required files exist
5. **Cross-reference consistency** - Rule numbers match across files

## How to Use

1. **Copy to your project:**
   ```bash
   cp examples/github-actions/ai-code-review.yml .github/workflows/
   ```

2. **Customize for your stack:**
   - Adjust linting commands
   - Add your test framework
   - Configure coverage thresholds
   - Add deployment steps

3. **Enable in GitHub:**
   - Push to your repository
   - Workflow runs automatically on PRs
   - View results in Actions tab

## Related Rules

- **Rule 37**: Test everything AI generates (90%+ coverage)
- **Rule 47**: Human always reviews first
- **Rule 49**: AI code gets stricter linting

## See Also

- [DAILY_CHECKLIST.md](../../DAILY_CHECKLIST.md) - Manual review checklist
- [tools/](../../tools/) - Validation scripts
- [Rule 47](../../README.md#rule-47-human-always-reviews-first) - Human review requirement
