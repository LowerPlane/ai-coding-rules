# Frontend Component Template

Use this template when generating frontend UI components with AI assistance.

---

## Context

**Stack:**
- Framework: React 18.x / Vue 3.x / Angular 17.x
- Language: TypeScript 5.x
- Styling: Tailwind CSS 3.x / CSS Modules / Styled Components 6.x
- State Management: React Context / Zustand 4.x / Pinia 2.x / NgRx 17.x
- Forms: React Hook Form 7.x / VeeValidate 4.x
- HTTP Client: Axios 1.x / React Query 5.x

**Existing Code:**
- Design system/component library in place
- Theme provider configured
- API client setup with authentication
- Global state management structure
- Error boundary components

**Conventions:**
- Functional components with hooks (React)
- Composition API (Vue)
- Standalone components (Angular)
- TypeScript strict mode enabled
- Mobile-first responsive design
- Accessibility-first approach (WCAG 2.1 AA)
- 90%+ test coverage required

---

## Task

Create a [COMPONENT TYPE] component for [DESCRIBE FEATURE]

### Specific Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

---

## Component Specification

### Props/Interface

**React/Vue:**
```typescript
interface ComponentProps {
  // Required props
  title: string;
  onSubmit: (data: FormData) => void | Promise<void>;

  // Optional props
  initialData?: FormData;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'danger';

  // Callback props
  onCancel?: () => void;
  onChange?: (field: string, value: unknown) => void;

  // Children/slots
  children?: React.ReactNode; // React
  // slots available: header, footer, actions // Vue
}
```

**Angular:**
```typescript
@Component({
  selector: 'app-component-name',
  standalone: true,
  // ...
})
export class ComponentName {
  @Input({ required: true }) title!: string;
  @Input() initialData?: FormData;
  @Input() disabled = false;
  @Input() variant: 'primary' | 'secondary' | 'danger' = 'primary';

  @Output() submitEvent = new EventEmitter<FormData>();
  @Output() cancelEvent = new EventEmitter<void>();
  @Output() changeEvent = new EventEmitter<FieldChange>();
}
```

### Component States

```typescript
type ComponentState = 'idle' | 'loading' | 'success' | 'error';

interface ComponentData {
  state: ComponentState;
  data: FormData | null;
  error: Error | null;
}
```

### Events/Emissions

```typescript
// React
type ComponentEvents = {
  onSubmit: (data: FormData) => void;
  onCancel: () => void;
  onChange: (field: string, value: unknown) => void;
  onError: (error: Error) => void;
};

// Vue
const emit = defineEmits<{
  submit: [data: FormData];
  cancel: [];
  change: [field: string, value: unknown];
  error: [error: Error];
}>();
```

---

## Validation Rules

Use Zod schema for data validation:

```typescript
import { z } from 'zod';

// Form data schema
const formSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must not exceed 100 characters')
    .trim(),

  email: z.string()
    .email('Invalid email address')
    .max(255, 'Email too long'),

  age: z.number()
    .int('Age must be a whole number')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age'),

  role: z.enum(['admin', 'user', 'guest'], {
    errorMap: () => ({ message: 'Invalid role selected' })
  }),

  // Optional with default
  notifications: z.boolean().default(true),

  // Array validation
  tags: z.array(z.string())
    .min(1, 'At least one tag required')
    .max(5, 'Maximum 5 tags allowed'),

  // Nested object
  address: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
    zipCode: z.string().regex(/^\d{5}$/, 'Invalid ZIP code'),
  }).optional(),

  // Custom validation
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain number'),

  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type FormData = z.infer<typeof formSchema>;
```

---

## Output Format

### File Structure

**React:**
```
src/components/ComponentName/
├── ComponentName.tsx           # Main component
├── ComponentName.module.css    # Styles (if CSS Modules)
├── ComponentName.types.ts      # TypeScript types
├── ComponentName.hooks.ts      # Custom hooks
├── ComponentName.utils.ts      # Helper functions
├── ComponentName.test.tsx      # Component tests
├── ComponentName.stories.tsx   # Storybook stories
└── index.ts                    # Barrel export
```

**Vue:**
```
src/components/ComponentName/
├── ComponentName.vue           # Single File Component
├── ComponentName.types.ts      # TypeScript types
├── ComponentName.composables.ts # Composables
├── ComponentName.utils.ts      # Helper functions
├── ComponentName.test.ts       # Component tests
├── ComponentName.stories.ts    # Storybook stories
└── index.ts                    # Barrel export
```

**Angular:**
```
src/app/components/component-name/
├── component-name.component.ts      # Component logic
├── component-name.component.html    # Template
├── component-name.component.scss    # Styles
├── component-name.component.spec.ts # Tests
└── component-name.types.ts          # TypeScript types
```

### Code Style

**React Component:**
```typescript
import { useState, useCallback } from 'react';
import { z } from 'zod';
import { ComponentProps, FormData } from './ComponentName.types';
import { formSchema } from './ComponentName.utils';
import styles from './ComponentName.module.css';

/**
 * ComponentName - Brief description of what this component does
 *
 * @example
 * ```tsx
 * <ComponentName
 *   title="User Form"
 *   onSubmit={handleSubmit}
 *   initialData={userData}
 * />
 * ```
 */
export function ComponentName({
  title,
  onSubmit,
  initialData,
  disabled = false,
  variant = 'primary',
  onCancel,
  onChange,
}: ComponentProps) {
  const [formData, setFormData] = useState<FormData>(
    initialData ?? getDefaultFormData()
  );
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFieldChange = useCallback(
    (field: keyof FormData, value: unknown) => {
      setFormData((prev) => ({ ...prev, [field]: value }));

      // Clear field error on change
      if (errors[field]) {
        setErrors((prev) => {
          const { [field]: _, ...rest } = prev;
          return rest;
        });
      }

      onChange?.(field, value);
    },
    [errors, onChange]
  );

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      // Validate
      const validation = formSchema.safeParse(formData);
      if (!validation.success) {
        const fieldErrors = validation.error.flatten().fieldErrors;
        setErrors(
          Object.entries(fieldErrors).reduce((acc, [key, messages]) => ({
            ...acc,
            [key]: messages?.[0] ?? 'Invalid value',
          }), {})
        );
        return;
      }

      setIsSubmitting(true);
      try {
        await onSubmit(validation.data);
      } catch (error) {
        console.error('Submission error:', error);
        setErrors({ submit: 'Failed to submit form' });
      } finally {
        setIsSubmitting(false);
      }
    },
    [formData, onSubmit]
  );

  return (
    <form
      className={styles.form}
      onSubmit={handleSubmit}
      noValidate
      aria-label={title}
    >
      <h2 className={styles.title}>{title}</h2>

      {errors.submit && (
        <div role="alert" className={styles.errorMessage}>
          {errors.submit}
        </div>
      )}

      {/* Form fields */}
      <div className={styles.field}>
        <label htmlFor="name" className={styles.label}>
          Name <span aria-label="required">*</span>
        </label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) => handleFieldChange('name', e.target.value)}
          disabled={disabled || isSubmitting}
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? 'name-error' : undefined}
          className={styles.input}
        />
        {errors.name && (
          <span id="name-error" className={styles.fieldError} role="alert">
            {errors.name}
          </span>
        )}
      </div>

      <div className={styles.actions}>
        <button
          type="submit"
          disabled={disabled || isSubmitting}
          className={`${styles.button} ${styles[variant]}`}
          aria-busy={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className={styles.buttonSecondary}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

function getDefaultFormData(): FormData {
  return {
    name: '',
    email: '',
    age: 18,
    role: 'user',
    notifications: true,
    tags: [],
  };
}
```

**Vue Component (Composition API):**
```vue
<script setup lang="ts">
import { ref, computed } from 'vue';
import { z } from 'zod';
import { ComponentProps, FormData } from './ComponentName.types';
import { formSchema } from './ComponentName.utils';

/**
 * ComponentName - Brief description of what this component does
 */
interface Props {
  title: string;
  initialData?: FormData;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'danger';
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  variant: 'primary',
});

const emit = defineEmits<{
  submit: [data: FormData];
  cancel: [];
  change: [field: string, value: unknown];
}>();

const formData = ref<FormData>(props.initialData ?? getDefaultFormData());
const errors = ref<Record<string, string>>({});
const isSubmitting = ref(false);

const handleFieldChange = (field: keyof FormData, value: unknown) => {
  formData.value = { ...formData.value, [field]: value };

  // Clear field error
  if (errors.value[field]) {
    const { [field]: _, ...rest } = errors.value;
    errors.value = rest;
  }

  emit('change', field, value);
};

const handleSubmit = async () => {
  // Validate
  const validation = formSchema.safeParse(formData.value);
  if (!validation.success) {
    const fieldErrors = validation.error.flatten().fieldErrors;
    errors.value = Object.entries(fieldErrors).reduce(
      (acc, [key, messages]) => ({
        ...acc,
        [key]: messages?.[0] ?? 'Invalid value',
      }),
      {}
    );
    return;
  }

  isSubmitting.value = true;
  try {
    emit('submit', validation.data);
  } catch (error) {
    console.error('Submission error:', error);
    errors.value = { submit: 'Failed to submit form' };
  } finally {
    isSubmitting.value = false;
  }
};

function getDefaultFormData(): FormData {
  return {
    name: '',
    email: '',
    age: 18,
    role: 'user',
    notifications: true,
    tags: [],
  };
}
</script>

<template>
  <form
    class="form"
    @submit.prevent="handleSubmit"
    novalidate
    :aria-label="title"
  >
    <h2 class="title">{{ title }}</h2>

    <div v-if="errors.submit" role="alert" class="error-message">
      {{ errors.submit }}
    </div>

    <div class="field">
      <label for="name" class="label">
        Name <span aria-label="required">*</span>
      </label>
      <input
        id="name"
        v-model="formData.name"
        type="text"
        :disabled="disabled || isSubmitting"
        :aria-invalid="!!errors.name"
        :aria-describedby="errors.name ? 'name-error' : undefined"
        class="input"
        @input="handleFieldChange('name', $event.target.value)"
      />
      <span
        v-if="errors.name"
        id="name-error"
        class="field-error"
        role="alert"
      >
        {{ errors.name }}
      </span>
    </div>

    <div class="actions">
      <button
        type="submit"
        :disabled="disabled || isSubmitting"
        :class="['button', variant]"
        :aria-busy="isSubmitting"
      >
        {{ isSubmitting ? 'Submitting...' : 'Submit' }}
      </button>

      <button
        type="button"
        @click="emit('cancel')"
        :disabled="isSubmitting"
        class="button-secondary"
      >
        Cancel
      </button>
    </div>
  </form>
</template>

<style scoped>
.form { /* styles */ }
.title { /* styles */ }
.field { /* styles */ }
/* ... */
</style>
```

---

## Security Requirements

**CRITICAL - Never Skip:**

1. **XSS Prevention**
   - NEVER use `dangerouslySetInnerHTML` / `v-html` / `[innerHTML]` with user input
   - Sanitize HTML content with DOMPurify if absolutely necessary
   - Use framework's text interpolation (automatic escaping)

2. **Input Validation**
   - Validate ALL user inputs with Zod schema
   - Sanitize strings (trim, escape special chars)
   - Limit input lengths
   - Validate on both client AND server

3. **Authentication & Authorization**
   - Never expose sensitive data in component state
   - Check user permissions before rendering UI
   - Hide/disable actions user cannot perform

4. **Data Exposure**
   - Never log sensitive data (passwords, tokens, PII)
   - Clear sensitive form data on unmount
   - Use secure forms for passwords (autocomplete="off")

5. **Dependencies**
   - Only use vetted, maintained libraries
   - Keep dependencies updated
   - Review bundle size impact

6. **CSRF Protection**
   - Include CSRF tokens in form submissions
   - Validate tokens on server side

---

## Accessibility Requirements

**WCAG 2.1 AA Compliance:**

1. **Semantic HTML**
   - Use proper heading hierarchy (h1 → h2 → h3)
   - Use `<button>` for actions, `<a>` for links
   - Use `<label>` with form inputs

2. **ARIA Labels**
   ```typescript
   // Describe purpose
   <button aria-label="Close dialog">×</button>

   // Current state
   <button aria-expanded={isOpen}>Menu</button>
   <div aria-busy={isLoading}>Content</div>

   // Errors and validation
   <input aria-invalid={!!error} aria-describedby="field-error" />
   <span id="field-error" role="alert">{error}</span>
   ```

3. **Keyboard Navigation**
   - All interactive elements focusable
   - Logical tab order
   - Enter/Space activate buttons
   - Escape closes dialogs/menus
   - Arrow keys for lists/menus

4. **Focus Management**
   - Visible focus indicators
   - Trap focus in modals
   - Restore focus after modal closes
   - Skip to main content link

5. **Color & Contrast**
   - 4.5:1 contrast for normal text
   - 3:1 for large text (18px+)
   - Don't rely on color alone

6. **Screen Reader Support**
   - Announce dynamic content changes
   - Label all form fields
   - Provide text alternatives for images
   - Use `role="alert"` for errors

---

## Responsive Design Requirements

**Mobile-First Approach:**

```css
/* Base: Mobile styles (320px+) */
.component {
  padding: 1rem;
  font-size: 1rem;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .component {
    padding: 1.5rem;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .component {
    padding: 2rem;
    font-size: 1.125rem;
  }
}

/* Large Desktop (1280px+) */
@media (min-width: 1280px) {
  .component {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**Responsive Breakpoints:**
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1279px
- Large: 1280px+

**Touch Targets:**
- Minimum 44x44px for interactive elements
- Adequate spacing between clickable items

---

## Testing Requirements

**Coverage: 90%+ required**

### Test Scenarios

**React (React Testing Library):**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // 1. Rendering
  it('should render with required props', () => {
    const onSubmit = jest.fn();
    render(<ComponentName title="Test Form" onSubmit={onSubmit} />);

    expect(screen.getByRole('form', { name: 'Test Form' })).toBeInTheDocument();
    expect(screen.getByText('Test Form')).toBeInTheDocument();
  });

  // 2. User Interactions
  it('should handle input changes', async () => {
    const onChange = jest.fn();
    const user = userEvent.setup();

    render(
      <ComponentName
        title="Form"
        onSubmit={jest.fn()}
        onChange={onChange}
      />
    );

    const input = screen.getByLabelText(/name/i);
    await user.type(input, 'John Doe');

    expect(input).toHaveValue('John Doe');
    expect(onChange).toHaveBeenCalledWith('name', 'John Doe');
  });

  // 3. Form Validation
  it('should show validation errors for invalid input', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();

    render(<ComponentName title="Form" onSubmit={onSubmit} />);

    const submitButton = screen.getByRole('button', { name: /submit/i });
    await user.click(submitButton);

    expect(await screen.findByText(/name must be at least 2 characters/i))
      .toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  // 4. Successful Submission
  it('should submit valid form data', async () => {
    const onSubmit = jest.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();

    render(<ComponentName title="Form" onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');

    await user.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'John Doe',
          email: 'john@example.com',
        })
      );
    });
  });

  // 5. Loading States
  it('should disable form during submission', async () => {
    const onSubmit = jest.fn(() => new Promise(resolve =>
      setTimeout(resolve, 100)
    ));
    const user = userEvent.setup();

    render(<ComponentName title="Form" onSubmit={onSubmit} />);

    // Fill form
    await user.type(screen.getByLabelText(/name/i), 'John Doe');

    const submitButton = screen.getByRole('button', { name: /submit/i });
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent(/submitting/i);

    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    });
  });

  // 6. Error Handling
  it('should display error message on submission failure', async () => {
    const onSubmit = jest.fn().mockRejectedValue(
      new Error('Network error')
    );
    const user = userEvent.setup();

    render(<ComponentName title="Form" onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    expect(await screen.findByText(/failed to submit/i)).toBeInTheDocument();
  });

  // 7. Accessibility
  it('should be accessible', async () => {
    const { container } = render(
      <ComponentName title="Form" onSubmit={jest.fn()} />
    );

    // Check ARIA labels
    expect(screen.getByRole('form')).toHaveAccessibleName('Form');

    // Check required field indicators
    expect(screen.getByLabelText(/name.*required/i)).toBeInTheDocument();

    // No accessibility violations (using jest-axe)
    const { axe, toHaveNoViolations } = await import('jest-axe');
    expect.extend(toHaveNoViolations);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  // 8. Conditional Rendering
  it('should show cancel button when onCancel provided', () => {
    const onCancel = jest.fn();

    render(
      <ComponentName
        title="Form"
        onSubmit={jest.fn()}
        onCancel={onCancel}
      />
    );

    expect(screen.getByRole('button', { name: /cancel/i }))
      .toBeInTheDocument();
  });

  // 9. Props Updates
  it('should update when props change', () => {
    const { rerender } = render(
      <ComponentName
        title="Form"
        onSubmit={jest.fn()}
        disabled={false}
      />
    );

    expect(screen.getByLabelText(/name/i)).not.toBeDisabled();

    rerender(
      <ComponentName
        title="Form"
        onSubmit={jest.fn()}
        disabled={true}
      />
    );

    expect(screen.getByLabelText(/name/i)).toBeDisabled();
  });

  // 10. Keyboard Navigation
  it('should support keyboard navigation', async () => {
    const user = userEvent.setup();

    render(<ComponentName title="Form" onSubmit={jest.fn()} />);

    // Tab through form elements
    await user.tab();
    expect(screen.getByLabelText(/name/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByLabelText(/email/i)).toHaveFocus();
  });
});
```

**Vue (Vitest + Vue Test Utils):**
```typescript
import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import ComponentName from './ComponentName.vue';

describe('ComponentName', () => {
  it('should submit valid form data', async () => {
    const onSubmit = vi.fn();
    const wrapper = mount(ComponentName, {
      props: {
        title: 'Form',
        onSubmit,
      },
    });

    await wrapper.find('input[id="name"]').setValue('John Doe');
    await wrapper.find('form').trigger('submit.prevent');

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'John Doe' })
    );
  });
});
```

---

## Performance Requirements

1. **Bundle Size**
   - Keep component < 50KB gzipped
   - Code-split large components
   - Lazy load below-fold content

2. **Rendering Performance**
   - Use React.memo / Vue computed / Angular OnPush
   - Virtualize long lists (react-window, vue-virtual-scroller)
   - Debounce expensive operations

3. **Network Optimization**
   - Lazy load images
   - Use next-gen formats (WebP, AVIF)
   - Implement skeleton screens

4. **Core Web Vitals**
   - LCP (Largest Contentful Paint) < 2.5s
   - FID (First Input Delay) < 100ms
   - CLS (Cumulative Layout Shift) < 0.1

---

## Dependencies

**Use existing packages only:**
- react / vue / @angular/core
- zod (validation)
- tailwindcss / styled-components (styling)
- react-hook-form / vee-validate (forms)
- @tanstack/react-query / @tanstack/vue-query (data fetching)
- axios (HTTP)
- date-fns (date manipulation)

**DO NOT install new packages without approval**

---

## Example Usage

### Prompt Example

```markdown
## Context
- Stack: React 18 + TypeScript + Tailwind CSS + React Hook Form
- Existing: Design system with Button, Input components
- Conventions: Functional components, custom hooks, mobile-first

## Task
Create a UserProfileForm component for editing user profile data

## Requirements
- Fields: name, email, bio, avatar URL, role (admin/user)
- Load initial data from prop
- Validate all inputs with Zod
- Show loading state during submission
- Display success/error messages
- Accessible (WCAG 2.1 AA)
- Responsive (mobile, tablet, desktop)

## Validation
- name: 2-100 chars, required
- email: valid email format, required
- bio: 0-500 chars, optional
- avatar URL: valid URL, optional
- role: enum ['admin', 'user'], required

## Accessibility
- All inputs labeled
- Error messages announced to screen readers
- Keyboard navigable
- Focus management

## Tests
- Renders with initial data
- Validates each field
- Submits valid data
- Handles submission errors
- Loading state disables form
- Keyboard navigation works
- No accessibility violations

Generate: Component, types, validation schema, tests, Storybook story
```

---

## Checklist

Before submitting AI-generated component code:

- [ ] All props properly typed with TypeScript
- [ ] Input validation with Zod schema
- [ ] XSS prevention (no dangerous HTML injection)
- [ ] All interactive elements keyboard accessible
- [ ] ARIA labels on all form fields
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Responsive at all breakpoints (320px+)
- [ ] Loading states implemented
- [ ] Error handling complete
- [ ] Tests cover all scenarios (90%+)
- [ ] No console.log in production code
- [ ] Component under 300 lines (split if larger)
- [ ] JSDoc comments on component and props
- [ ] No hardcoded strings (use i18n if available)

---

**See also:**
- [Rule 21: Validate All Inputs](../../README.md#rule-21-validate-all-inputs)
- [Rule 24: Sanitize User-Generated Content](../../README.md#rule-24-sanitize-user-generated-content)
- [Rule 37: Test Everything](../../README.md#rule-37-test-everything-ai-generates)
- [DAILY_CHECKLIST.md](../../DAILY_CHECKLIST.md)
