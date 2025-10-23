# Contributing to AI Coding Rules

Thank you for your interest in contributing! This project helps developers use AI coding assistants safely and effectively.

## How to Contribute

### 1. Report Issues

Found an error or have a suggestion?
- Open an issue on GitHub
- Use a clear, descriptive title
- Provide examples and context

### 2. Suggest New Rules

Have a rule that should be added?
- Explain the problem it solves
- Provide ❌ Bad and ✅ Good examples
- Show how it improves AI-assisted development

### 3. Add Templates or Workflows

Want to contribute a template or workflow?
- Follow the existing format
- Include all required sections
- Test it with real AI tools
- Document your results

### 4. Share Examples

Have a successful AI-generated project?
- Add it to `/examples/`
- Include the prompts you used
- Document your review process
- Share lessons learned

## Contribution Guidelines

### Documentation Standards

1. **Clear Examples**
   - Always include ❌ Bad and ✅ Good examples
   - Use realistic, practical examples
   - Show actual code, not pseudo-code

2. **Consistency**
   - Match the existing tone and style
   - Use consistent terminology
   - Follow the established format

3. **Cross-References**
   - Link to related rules by number
   - Update all affected files
   - Check the INDEX.md

4. **Testing**
   - Test your templates with AI tools
   - Verify examples actually work
   - Include test results

### File Updates Required

When adding/updating a rule:
- [ ] README.md (main source)
- [ ] RULES_ONE_PAGE.md (condensed)
- [ ] Corresponding /rules/*.md file
- [ ] INDEX.md (navigation)
- [ ] DAILY_CHECKLIST.md (if workflow affected)

### Commit Message Format

Use conventional commits:

```
docs(rules): add rule 55 for API versioning
docs(templates): add Vue.js component template
docs(workflows): add CI/CD pipeline workflow
fix(typo): correct rule 23 code example
feat(tools): add prompt validation script
```

Types:
- `docs`: Documentation changes
- `fix`: Bug fixes, typos
- `feat`: New features (templates, tools, examples)

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b docs/your-feature`
3. **Make your changes**
4. **Update all related files** (see checklist above)
5. **Test your changes** (verify links, examples)
6. **Commit with conventional messages**
7. **Push to your fork**
8. **Open a Pull Request**

### PR Template

```markdown
## Description
[Describe what you're adding/changing]

## Type of Change
- [ ] New rule
- [ ] Rule update
- [ ] New template
- [ ] New workflow
- [ ] New example
- [ ] Bug fix
- [ ] Documentation improvement

## Files Changed
- [ ] README.md
- [ ] RULES_ONE_PAGE.md
- [ ] /rules/*.md
- [ ] INDEX.md
- [ ] Other: ___________

## Testing
- [ ] Tested with Claude Code
- [ ] Tested with GPT-4
- [ ] Examples work as described
- [ ] Links verified

## Additional Context
[Any additional information]
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving AI-assisted development
- Share knowledge openly

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Spam or off-topic content
- Publishing others' private information

## Questions?

- Open a GitHub Discussion
- Check existing issues first
- Be patient and respectful

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make AI-assisted development safer and more effective!**
