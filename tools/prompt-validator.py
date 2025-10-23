#!/usr/bin/env python3

"""
Prompt Validator

Validates AI prompt templates against the rules in this repository.
Ensures prompts follow the Prompt Engineering Rules (1-10).

Usage:
    python tools/prompt-validator.py prompts/templates/backend-starter.md
    python tools/prompt-validator.py prompts/templates/*.md

Checks:
- Has Context section (Rule 2)
- Has specific requirements (Rule 1)
- Includes validation rules (Rule 4)
- Defines success/error scenarios (Rule 5)
- Specifies dependencies (Rule 6)
- Includes test requirements (Rule 7)
- Has output format section (Rule 3)
- Includes security requirements
"""

import sys
import re
from pathlib import Path

class PromptValidator:
    """Validates prompt templates against AI Coding Rules."""

    REQUIRED_SECTIONS = {
        'context': r'##\s+Context',
        'task': r'##\s+Task',
        'requirements': r'##\s+Requirements',
        'validation': r'##\s+Validation',
        'output_format': r'##\s+Output\s+Format',
        'security': r'##\s+Security',
    }

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.content = ''
        self.errors = []
        self.warnings = []

    def load_file(self):
        """Load the prompt template file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.filepath}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False

    def check_required_sections(self):
        """Check if all required sections are present (Rules 2-7)."""
        for section_name, pattern in self.REQUIRED_SECTIONS.items():
            if not re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(
                    f"Missing required section: {section_name.replace('_', ' ').title()}"
                )

    def check_specificity(self):
        """Check if prompt is specific, not generic (Rule 1)."""
        generic_phrases = [
            r'build\s+me\s+a',
            r'create\s+a\s+simple',
            r'make\s+it\s+work',
            r'fix\s+this',
        ]

        for phrase in generic_phrases:
            if re.search(phrase, self.content, re.IGNORECASE):
                self.warnings.append(
                    f"Generic phrase detected - ensure specificity (Rule 1)"
                )

    def check_examples(self):
        """Check if examples are included (Rule 9)."""
        if '```' not in self.content:
            self.warnings.append(
                "No code examples found - consider adding examples (Rule 9)"
            )

    def validate(self):
        """Run all validation checks."""
        if not self.load_file():
            return False

        self.check_required_sections()
        self.check_specificity()
        self.check_examples()

        return len(self.errors) == 0

    def print_report(self):
        """Print validation report."""
        print(f"\n{'='*60}")
        print(f"Validating: {self.filepath.name}")
        print(f"{'='*60}\n")

        if not self.errors and not self.warnings:
            print("✅ All checks passed!")
            return True

        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()

        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()

        return len(self.errors) == 0

def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python tools/prompt-validator.py <prompt-file>")
        print("Example: python tools/prompt-validator.py prompts/templates/backend-starter.md")
        sys.exit(1)

    filepath = sys.argv[1]
    validator = PromptValidator(filepath)

    validator.validate()
    success = validator.print_report()

    if not success:
        print("\n📖 See Rules 1-10 in README.md for prompt engineering guidelines")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
