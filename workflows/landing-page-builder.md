# Landing Page Builder Workflow

**Complete landing page creation in 45 minutes using AI assistance**

---

## Overview

**Time Estimate:** 45 minutes
**Difficulty Level:** Beginner to Intermediate
**Prerequisites:**
- Basic HTML/CSS knowledge
- React or Next.js familiarity
- Understanding of responsive design
- Marketing/conversion basics

**What You'll Build:**
A high-converting landing page with:
- Responsive design (mobile-first)
- SEO optimization
- Fast loading (Core Web Vitals)
- Conversion tracking
- Lead capture form
- Analytics integration

---

## Prerequisites and Setup

### Required Tools
- Node.js 20.x or higher
- Next.js 14+ or React 18+
- Package manager (npm/yarn/pnpm)
- Git
- Code editor

### Required Knowledge
- Basic React components
- CSS/Tailwind CSS
- HTML semantics
- SEO basics
- Conversion optimization principles

### Initial Setup (5 minutes)
```bash
# Create Next.js project
npx create-next-app@latest landing-page --typescript --tailwind --app

cd landing-page

# Install additional dependencies
npm install react-hook-form zod @hookform/resolvers
npm install next-seo framer-motion
npm install -D @types/node

# Create directories
mkdir -p components/sections components/ui lib public/images
```

---

## Workflow Steps

### Step 1: Define Landing Page Goals and Structure (5 minutes)

**Objective:** Plan the landing page before generation

**Action:**
Create a clear specification for your landing page.

**Prompt to Use:**
```markdown
Help me plan a landing page for [PRODUCT/SERVICE]:

Product: [Name and brief description]
Target Audience: [Who is this for?]
Main Goal: [Lead generation / Sales / Sign-ups / Downloads]
Unique Value Proposition: [What makes this different?]

Structure needed:
1. Hero section with headline and CTA
2. Problem/Solution section
3. Features/Benefits (3-6 items)
4. Social proof (testimonials/logos)
5. Pricing or offer
6. FAQ section
7. Final CTA section

Key messaging:
- Main headline: [Your headline]
- Subheadline: [Supporting text]
- Primary CTA: [Button text]
- Secondary CTA: [Alternative action]

Design preferences:
- Color scheme: [Primary, secondary, accent colors]
- Style: [Modern / Minimalist / Bold / Professional]
- Brand voice: [Friendly / Professional / Technical]
```

**Example Output:**
```
Landing Page for "TaskFlow AI"
- Target: Busy professionals and small teams
- Goal: Free trial sign-ups
- UVP: Automate repetitive tasks in 60 seconds
- Hero CTA: "Start Free Trial"
- Color: Blue (#0066FF), White, Gray
- Style: Modern, clean, professional
```

**Review Checkpoint:**
- [ ] Clear value proposition defined
- [ ] Target audience identified
- [ ] Primary goal established
- [ ] Section structure planned
- [ ] Key messaging written

**References:** [Rule 1: Never Use Generic Prompts](../README.md#rule-1-never-use-generic-prompts), [Rule 2: Provide Context](../README.md#rule-2-always-provide-context-before-task)

---

### Step 2: Generate Page Structure and Layout (5 minutes)

**Objective:** Create the basic Next.js page structure

**Action:**
Generate the main page component with sections.

**Prompt to Use:**
```markdown
Generate a Next.js 14 landing page with App Router for [PRODUCT]:

File: app/page.tsx

Structure:
1. Hero section (full viewport, centered content, CTA buttons)
2. Problem section (describe pain points)
3. Solution section (how product solves it)
4. Features grid (3 columns on desktop, 1 on mobile)
5. Social proof section (testimonials or client logos)
6. Pricing/Offer section
7. FAQ accordion
8. Final CTA section
9. Footer

Requirements:
- Use TypeScript and React Server Components
- Responsive design with Tailwind CSS
- Semantic HTML (header, main, section, footer)
- Accessibility: ARIA labels, alt text, keyboard navigation
- Import components from separate files
- Clean, readable code structure

Components to create separately:
- components/sections/Hero.tsx
- components/sections/Features.tsx
- components/sections/Pricing.tsx
- components/sections/FAQ.tsx
- components/ui/Button.tsx
- components/ui/Card.tsx
```

**Review Checkpoint:**
- [ ] Page structure created
- [ ] All sections included
- [ ] Semantic HTML used
- [ ] TypeScript types defined
- [ ] Component imports organized

**References:** [Rule 12: One Responsibility Per File](../README.md#rule-12-one-responsibility-per-file), [Rule 43: Consistent File Structure](../README.md#rule-43-consistent-file-structure)

---

### Step 3: Generate Hero Section (5 minutes)

**Objective:** Create compelling above-the-fold content

**Action:**
Generate an attention-grabbing hero section.

**Prompt to Use:**
```markdown
Generate a Hero section component for [PRODUCT]:

File: components/sections/Hero.tsx

Content:
- Headline: "[Your main headline]"
- Subheadline: "[Supporting text, 1-2 sentences]"
- Primary CTA button: "[Button text]" → leads to sign-up
- Secondary CTA: "[Alternative action]" → leads to demo/learn more
- Optional: Hero image or illustration on right side

Design requirements:
- Full viewport height (min-h-screen)
- Centered content with max-width
- Gradient background: [colors]
- Large, bold headline (text-5xl md:text-7xl)
- Responsive layout (stack on mobile, side-by-side on desktop)
- CTA buttons with hover effects
- Smooth fade-in animation (use framer-motion)

Accessibility:
- Proper heading hierarchy (h1)
- High contrast text
- Focus states on buttons
- Alt text for images

Use Tailwind CSS for styling
Export as default function
```

**Example Output:**
```tsx
export default function Hero() {
  return (
    <section className="min-h-screen flex items-center bg-gradient-to-br from-blue-600 to-blue-800">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Automate Tasks in 60 Seconds
            </h1>
            {/* ... */}
          </div>
        </div>
      </div>
    </section>
  );
}
```

**Review Checkpoint:**
- [ ] Compelling headline
- [ ] Clear value proposition
- [ ] Strong CTAs
- [ ] Responsive design
- [ ] Smooth animations
- [ ] Accessibility features

**References:** [Rule 3: Specify Output Format](../README.md#rule-3-specify-output-format-explicitly)

---

### Step 4: Generate Features Section (5 minutes)

**Objective:** Showcase product features and benefits

**Action:**
Create a features grid with icons and descriptions.

**Prompt to Use:**
```markdown
Generate a Features section for [PRODUCT]:

File: components/sections/Features.tsx

Features to highlight (3-6 items):
1. [Feature 1 name]: [Brief description, focus on benefit not feature]
2. [Feature 2 name]: [Description]
3. [Feature 3 name]: [Description]
4. [Feature 4 name]: [Description]
5. [Feature 5 name]: [Description]
6. [Feature 6 name]: [Description]

Design requirements:
- Section heading: "Why Choose [Product]?" or "Features"
- Grid layout: 3 columns on desktop, 2 on tablet, 1 on mobile
- Each feature card includes:
  - Icon (use lucide-react icons or emoji)
  - Feature name (h3)
  - Description (1-2 sentences)
- Card styling: white background, subtle shadow, rounded corners
- Hover effect: scale up slightly
- Fade-in animation on scroll (framer-motion)

Benefits-focused copy:
- Start with the benefit, not the technical detail
- Use action words
- Keep descriptions under 100 characters

Use TypeScript interface for feature data
Use Tailwind CSS for styling
```

**Review Checkpoint:**
- [ ] Benefits clearly communicated
- [ ] Icons appropriate and clear
- [ ] Grid responsive
- [ ] Hover effects work
- [ ] On-scroll animations smooth

**References:** [Rule 8: Provide Style Guidelines](../README.md#rule-8-provide-style-guidelines)

---

### Step 5: Generate Lead Capture Form (10 minutes)

**Objective:** Create conversion-optimized form

**Action:**
Build a form with validation and submission handling.

**Prompt to Use:**
```markdown
Generate a lead capture form component:

File: components/LeadForm.tsx

Form fields:
- Name: Required, 2-100 characters
- Email: Required, valid email format
- [Additional field if needed]: [requirements]

Requirements:
- Use react-hook-form for form management
- Use Zod for validation schema
- Inline error messages below each field
- Loading state during submission
- Success message after submission
- Error handling for API failures

Validation:
- Name: min 2 chars, max 100 chars, trim whitespace
- Email: valid email format, max 255 chars
- Real-time validation (onChange)
- Display errors on blur or submit

Form submission:
- POST to /api/leads endpoint
- Show loading spinner on button
- Disable form during submission
- Success: Display thank you message
- Error: Display error message
- Optional: Redirect to thank-you page

Design:
- Clean, minimal form design
- Large input fields (easy to tap on mobile)
- Prominent submit button
- Focus states on inputs
- Accessible labels and error messages

Privacy:
- Include privacy policy checkbox (required)
- Link to privacy policy
- GDPR compliance note

Export as default function
Use TypeScript for all types
Use Tailwind CSS for styling
```

**Review Checkpoint:**
- [ ] All fields validated
- [ ] Error messages clear
- [ ] Loading states work
- [ ] Success/error handling complete
- [ ] Mobile-friendly
- [ ] Privacy compliance included

**References:** [Rule 4: Include Validation Requirements](../README.md#rule-4-include-validation-requirements), [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs)

---

### Step 6: Generate API Endpoint for Form Submission (5 minutes)

**Objective:** Create backend to handle form submissions

**Action:**
Generate API route for lead capture.

**Prompt to Use:**
```markdown
Generate an API endpoint to handle lead form submissions:

File: app/api/leads/route.ts

Requirements:
- Accept POST requests only
- Validate request body with Zod
- Fields: name, email, consent (boolean)
- Rate limiting: 5 submissions per 15 minutes per IP
- Store in database OR send to email service
- Return proper status codes:
  - 200: Success
  - 400: Validation error
  - 429: Rate limit exceeded
  - 500: Server error

Response format:
Success (200):
{
  "success": true,
  "message": "Thank you! We'll be in touch soon."
}

Error (400):
{
  "success": false,
  "error": "Validation failed",
  "fields": { "email": "Invalid email format" }
}

Integration options (choose one):
[Option A] Send to email service (Resend, SendGrid):
- Email to: [your-email@example.com]
- Subject: "New lead from landing page"
- Include all form data

[Option B] Save to database:
- Use Prisma with PostgreSQL
- Table: leads (id, name, email, consent, created_at)

Security:
- Validate all inputs
- Sanitize data before storing/sending
- No hardcoded secrets (use env vars)
- Add CORS headers for production domain
- Log all submissions for tracking

Use TypeScript with NextRequest and NextResponse
Include error handling and logging
```

**Review Checkpoint:**
- [ ] POST endpoint only
- [ ] Input validation working
- [ ] Rate limiting implemented
- [ ] Integration configured (email/database)
- [ ] Error handling complete
- [ ] No hardcoded secrets

**References:** [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets), [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs), [Rule 24: Implement Rate Limiting](../README.md#rule-24-implement-rate-limiting)

---

### Step 7: Add SEO Optimization (5 minutes)

**Objective:** Optimize for search engines and social sharing

**Action:**
Add metadata, structured data, and Open Graph tags.

**Prompt to Use:**
```markdown
Generate SEO configuration for landing page:

File: app/page.tsx (add metadata) and app/layout.tsx

SEO Details:
- Page title: "[Product Name] - [Value Proposition]" (max 60 chars)
- Meta description: "[Compelling description with keywords]" (max 160 chars)
- Keywords: [keyword1, keyword2, keyword3]
- Canonical URL: [your-domain.com]
- Language: en

Open Graph (Social sharing):
- og:title: [title]
- og:description: [description]
- og:image: [URL to share image, 1200x630px]
- og:type: website
- og:url: [canonical URL]

Twitter Card:
- twitter:card: summary_large_image
- twitter:title: [title]
- twitter:description: [description]
- twitter:image: [image URL]

Structured Data (JSON-LD):
- @type: Product OR SoftwareApplication
- name: [product name]
- description: [description]
- offers: [pricing if applicable]

Requirements:
- Use Next.js 14 metadata API
- Add to both page.tsx and layout.tsx
- Include all required fields
- Validate JSON-LD syntax
- Use next-seo package if needed

Additional SEO:
- Semantic HTML (header, nav, main, article, footer)
- Proper heading hierarchy (h1, h2, h3)
- Alt text on all images
- Internal linking structure
- Fast loading (optimize images, lazy loading)
```

**Review Checkpoint:**
- [ ] Title and description optimized
- [ ] Open Graph tags complete
- [ ] Twitter Card configured
- [ ] Structured data added
- [ ] Semantic HTML used
- [ ] All images have alt text

**References:** [Rule 8: Provide Style Guidelines](../README.md#rule-8-provide-style-guidelines)

---

### Step 8: Add Analytics and Tracking (5 minutes)

**Objective:** Track conversions and user behavior

**Action:**
Integrate analytics tools.

**Prompt to Use:**
```markdown
Add analytics and conversion tracking:

Analytics to integrate:
1. Google Analytics 4
2. [Optional: Facebook Pixel / LinkedIn Insight Tag]
3. Custom conversion tracking

File: app/layout.tsx and lib/analytics.ts

Requirements:
- Google Analytics 4:
  - Track page views
  - Track CTA button clicks
  - Track form submissions
  - Track scroll depth
  - Custom events for: hero_cta_click, form_submit, pricing_view

- Conversion tracking:
  - Event: form_submit
  - Send to GA4, Facebook, etc.
  - Include conversion value if applicable

- Privacy compliance:
  - Cookie consent banner (optional but recommended)
  - Respect Do Not Track
  - GDPR compliant
  - Clear privacy policy link

Implementation:
- Use next/script for loading analytics
- Load scripts with strategy="afterInteractive"
- Type-safe event tracking functions
- Environment variables for tracking IDs
- Only load in production (check NODE_ENV)

Custom tracking functions:
```typescript
trackEvent(eventName: string, properties?: Record<string, any>)
trackPageView(url: string)
trackConversion(conversionType: string, value?: number)
```

Use TypeScript
No hardcoded tracking IDs (use env vars)
```

**Review Checkpoint:**
- [ ] GA4 installed and working
- [ ] Custom events tracked
- [ ] Form submissions tracked
- [ ] Privacy compliant
- [ ] Only loads in production
- [ ] Tracking IDs in env vars

**References:** [Rule 19: Never Hardcode Secrets](../README.md#rule-19-never-hardcode-secrets)

---

### Step 9: Optimize Performance (5 minutes)

**Objective:** Ensure fast loading and good Core Web Vitals

**Action:**
Implement performance optimizations.

**Prompt to Use:**
```markdown
Optimize landing page performance:

Areas to optimize:

1. Image Optimization:
- Use next/image for all images
- Set appropriate width/height
- Use WebP format
- Lazy load below-the-fold images
- Optimize hero image (should be < 100KB)
- Use blur placeholder for loading

2. Font Optimization:
- Use next/font for font loading
- Preload critical fonts
- Subset fonts (Latin only if applicable)
- Font-display: swap

3. Code Splitting:
- Lazy load FAQ section
- Lazy load testimonials
- Use dynamic imports for heavy components
- Split vendor bundles

4. CSS Optimization:
- Use Tailwind's JIT mode
- Purge unused CSS
- Inline critical CSS
- Minimize CSS bundle

5. JavaScript Optimization:
- Minimize bundle size
- Remove console.logs
- Tree-shake unused code
- Use production build

6. Loading Strategy:
- Preload critical resources
- Defer non-critical scripts
- Use async for analytics
- Optimize third-party scripts

Generate optimized image component:
File: components/ui/OptimizedImage.tsx

Requirements:
- Wrapper around next/image
- Automatic WebP conversion
- Lazy loading by default
- Blur placeholder
- Responsive sizes
- TypeScript props

Target metrics:
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1
- Time to Interactive (TTI): < 3.5s
```

**Review Checkpoint:**
- [ ] All images optimized
- [ ] Fonts loaded efficiently
- [ ] Components lazy loaded
- [ ] Bundle size minimized
- [ ] Core Web Vitals passing
- [ ] Lighthouse score > 90

---

### Step 10: Create Testimonials/Social Proof Section (5 minutes)

**Objective:** Build trust with social proof

**Action:**
Generate testimonials component.

**Prompt to Use:**
```markdown
Generate a testimonials section:

File: components/sections/Testimonials.tsx

Content (3-6 testimonials):
[Either provide real testimonials or ask AI to generate realistic ones]

Each testimonial includes:
- Quote (1-3 sentences, specific results/benefits)
- Person's name
- Title/Company
- Photo (avatar)
- Optional: Star rating (5 stars)

Design:
- Section heading: "What Our Customers Say" or "Loved by [Number]+ Users"
- Card-based layout
- 3 columns on desktop, 1-2 on tablet, 1 on mobile
- Each card: white background, shadow, rounded corners
- Include quotation marks
- Photo: circular, 64px
- Rotate/carousel on mobile (optional)
- Fade-in animation on scroll

Alternative formats:
[Option A] Logo wall - Show client/customer logos
[Option B] Stats - "10,000+ happy customers" with big numbers
[Option C] Case study highlight

Requirements:
- TypeScript interface for testimonial data
- Responsive grid
- Accessible (proper image alt text)
- Smooth animations
- Use real data or realistic placeholders

Use Tailwind CSS
Export as default function
```

**Review Checkpoint:**
- [ ] Testimonials compelling and specific
- [ ] Photos/avatars included
- [ ] Responsive layout works
- [ ] Animations smooth
- [ ] Builds credibility

---

### Step 11: Generate FAQ Section (5 minutes)

**Objective:** Address common questions and objections

**Action:**
Create an accordion-style FAQ component.

**Prompt to Use:**
```markdown
Generate an FAQ accordion component:

File: components/sections/FAQ.tsx

Questions to answer (5-10 FAQs):
1. [Common question about pricing/features]
2. [Technical question]
3. [Comparison question]
4. [Support question]
5. [Privacy/security question]
[Add more relevant to your product]

Design requirements:
- Accordion UI (expand/collapse)
- One question open at a time
- Smooth expand/collapse animation
- Clear question styling (bold, larger text)
- Answer styled for readability
- Plus/minus icon that rotates
- Mobile-friendly touch targets

Implementation:
- Use state to track open question
- Keyboard accessible (Enter to toggle)
- ARIA attributes for accessibility
- Smooth height transition
- Structured data for SEO (FAQPage schema)

Component structure:
- TypeScript interface for FAQ item
- Map over FAQ array
- Individual FAQ item component
- Click handler to toggle

SEO enhancement:
- Add JSON-LD structured data (@type: FAQPage)
- Proper heading hierarchy (h2 for questions)

Use Tailwind CSS
Export as default function
Include 5-10 realistic FAQs
```

**Review Checkpoint:**
- [ ] Questions address real concerns
- [ ] Answers clear and helpful
- [ ] Accordion works smoothly
- [ ] Mobile-friendly
- [ ] Keyboard accessible
- [ ] SEO structured data added

---

### Step 12: Create Pricing/CTA Section (5 minutes)

**Objective:** Present offer and drive conversions

**Action:**
Generate pricing or call-to-action section.

**Prompt to Use:**
```markdown
Generate a pricing/offer section:

File: components/sections/Pricing.tsx

[Choose format based on your product]

Option A - Pricing Tiers:
Tiers:
1. [Plan name]: $[price]/month - [Features]
2. [Plan name]: $[price]/month - [Features]
3. [Plan name]: $[price]/month - [Features]

Option B - Single Offer:
- Product: [Name]
- Price: $[amount] or "Free" or "Contact Sales"
- What's included: [List key benefits]
- Guarantee: [Money-back, free trial, etc.]

Option C - Lead Magnet:
- Free resource: [eBook, Template, Tool]
- What you get: [List contents]
- CTA: "Download Free [Resource]"

Design requirements:
- Section heading: "Simple, Transparent Pricing" or "Start Free Today"
- Cards for each tier (if applicable)
- Highlight most popular tier
- Clear CTA button on each card
- List of features with checkmarks
- Optional: Annual/monthly toggle
- Pricing emphasized (large, bold)
- Guarantee badge or trust signal

Card styling:
- White background, shadow, rounded
- Popular plan: border highlight, "Popular" badge
- Hover effect: slight elevation
- Feature list: green checkmarks
- Button: prominent, contrasting color

Psychology elements:
- Urgency: "Limited time offer" (if true)
- Scarcity: "Only X spots left" (if true)
- Social proof: "Join 10,000+ users"
- Guarantee: "30-day money-back guarantee"

Use TypeScript
Use Tailwind CSS
Export as default function
```

**Review Checkpoint:**
- [ ] Pricing clear and transparent
- [ ] CTAs prominent
- [ ] Value proposition clear
- [ ] Trust signals included
- [ ] Mobile-friendly
- [ ] Encourages action

---

### Step 13: Add Final CTA and Footer (5 minutes)

**Objective:** Last chance conversion and site navigation

**Action:**
Create final CTA section and footer.

**Prompt to Use:**
```markdown
Generate final CTA section and footer:

File 1: components/sections/FinalCTA.tsx
- Bold headline: Last chance to [benefit]
- Subheadline: Remind of key benefit
- Large CTA button
- Trust signals: "No credit card required" / "Cancel anytime"
- Background: contrasting color or gradient
- Full-width section

File 2: components/Footer.tsx

Footer content:
- Logo and tagline
- Navigation links:
  - Product
  - Pricing
  - About
  - Blog
  - Contact
- Legal links:
  - Privacy Policy
  - Terms of Service
  - Cookie Policy
- Social media links:
  - [List relevant platforms]
- Newsletter signup (optional)
- Copyright: "© 2025 [Company]. All rights reserved."

Design:
- Dark background (contrast with page)
- Multi-column layout on desktop
- Stacked on mobile
- Links with hover states
- Social icons with hover effects

Requirements:
- Semantic footer element
- Accessible links
- External links open in new tab
- Responsive layout
- TypeScript
- Tailwind CSS

Export as default function
```

**Review Checkpoint:**
- [ ] Final CTA compelling
- [ ] Footer complete with all links
- [ ] Social links working
- [ ] Legal pages linked
- [ ] Mobile responsive
- [ ] Accessible

---

### Step 14: Testing and Validation (5 minutes)

**Objective:** Ensure everything works correctly

**Action:**
Test all functionality and fix issues.

**Testing Checklist:**

**Functionality:**
- [ ] Form submits successfully
- [ ] Validation shows errors correctly
- [ ] All CTAs link to correct destinations
- [ ] FAQ accordion expands/collapses
- [ ] All external links work
- [ ] Navigation works smoothly

**Responsive Design:**
- [ ] Test on mobile (375px)
- [ ] Test on tablet (768px)
- [ ] Test on desktop (1440px)
- [ ] Images scale properly
- [ ] Text readable on all sizes
- [ ] Touch targets large enough on mobile

**Performance:**
```bash
# Run Lighthouse audit
npm run build
npm start
# Open Chrome DevTools > Lighthouse
# Run audit for Performance, Accessibility, SEO

# Check bundle size
npm run build
# Analyze .next/static files
```

**Accessibility:**
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Color contrast passes WCAG AA
- [ ] All images have alt text
- [ ] Form labels associated
- [ ] Focus indicators visible

**SEO:**
- [ ] Title and meta description present
- [ ] Heading hierarchy correct
- [ ] Structured data validates
- [ ] Images optimized
- [ ] Mobile-friendly test passes
- [ ] Page loads fast (< 3s)

**Cross-browser:**
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

**Analytics:**
- [ ] Page view tracked
- [ ] CTA clicks tracked
- [ ] Form submission tracked
- [ ] Console has no errors

**Prompt for Fixes:**
```markdown
Fix the following issues found during testing:
- [Issue 1]: [Description]
- [Issue 2]: [Description]

Requirements:
- Maintain existing functionality
- Don't break responsive design
- Keep accessibility features
- Test after fixing
```

**References:** [Rule 40: Test Edge Cases](../README.md#rule-40-test-edge-cases)

---

### Step 15: Deployment and Launch (5 minutes)

**Objective:** Deploy to production

**Action:**
Deploy to Vercel or hosting platform.

**Deployment Steps:**

**Option A - Vercel (Recommended for Next.js):**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# - NEXT_PUBLIC_GA_ID
# - EMAIL_SERVICE_API_KEY (if using email service)
# - DATABASE_URL (if using database)

# Deploy to production
vercel --prod
```

**Option B - Other platforms:**
```bash
# Build for production
npm run build

# Test production build locally
npm start

# Deploy to your hosting platform
# (Netlify, AWS, etc.)
```

**Pre-deployment Checklist:**
- [ ] Environment variables set
- [ ] API endpoints working
- [ ] Analytics tracking IDs configured
- [ ] Database/email service connected
- [ ] Domain configured
- [ ] HTTPS enabled
- [ ] Error monitoring set up (Sentry, etc.)

**Post-deployment Checklist:**
- [ ] Visit live URL
- [ ] Test form submission
- [ ] Check analytics tracking
- [ ] Test all CTAs
- [ ] Verify SEO meta tags (view source)
- [ ] Run Lighthouse on live site
- [ ] Check mobile version
- [ ] Monitor error logs

**Custom Domain Setup:**
```markdown
Generate instructions for:
1. Point domain to Vercel
2. Configure DNS records
3. Enable SSL certificate
4. Set up redirects (www to non-www or vice versa)
```

**References:** [Rule 18: Configuration as Code](../README.md#rule-18-configuration-as-code)

---

## Testing Procedures

### Manual Testing Checklist

**Visual Testing:**
- [ ] Hero section displays correctly
- [ ] All images load properly
- [ ] Colors match brand guidelines
- [ ] Typography consistent throughout
- [ ] Spacing and alignment correct
- [ ] Hover effects work on all interactive elements

**Functional Testing:**
- [ ] Form validates on submit
- [ ] Form shows errors for invalid input
- [ ] Form submits successfully
- [ ] Success message displays
- [ ] All buttons link correctly
- [ ] FAQ accordion works
- [ ] Smooth scroll works (if implemented)

**Conversion Testing:**
- [ ] CTAs prominent and clickable
- [ ] Form easy to find and use
- [ ] Value proposition clear
- [ ] No broken conversion paths
- [ ] Thank you page works (if applicable)

### Automated Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build

# Lighthouse CI (optional)
npm install -g @lhci/cli
lhci autorun
```

---

## Example Outputs

### Example Hero Section
```tsx
<section className="min-h-screen flex items-center bg-gradient-to-br from-blue-600 to-blue-800">
  <div className="container mx-auto px-6">
    <div className="max-w-3xl">
      <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
        Automate Your Tasks in 60 Seconds
      </h1>
      <p className="text-xl md:text-2xl text-blue-100 mb-8">
        Save 10+ hours per week with AI-powered automation.
        No code required.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition">
          Start Free Trial
        </button>
        <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white/10 transition">
          Watch Demo
        </button>
      </div>
    </div>
  </div>
</section>
```

### Example Form Validation
```tsx
const schema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters").max(100),
  email: z.string().email("Invalid email address").max(255),
  consent: z.boolean().refine(val => val === true, "You must accept the privacy policy")
});
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Form Not Submitting
**Symptom:** Form doesn't send data or shows errors

**Solution:**
1. Check API route is working: Visit `/api/leads` directly
2. Check browser console for errors
3. Verify environment variables are set
4. Check CORS configuration if on different domain

**Debug Prompt:**
```markdown
Debug the form submission:
- Add console.log to see form data
- Check API response in Network tab
- Verify Zod schema matches form fields
- Test API endpoint with curl
```

#### Issue 2: Images Not Loading
**Symptom:** Images show broken or don't appear

**Solution:**
1. Check image paths are correct
2. Verify images are in `public/` directory
3. Use next/image component correctly
4. Check image file extensions

```tsx
// Correct usage
<Image
  src="/images/hero.jpg"
  alt="Hero image"
  width={1200}
  height={630}
  priority
/>
```

#### Issue 3: Slow Page Load
**Symptom:** Page takes > 3 seconds to load

**Solution:**
1. Optimize images (compress, use WebP)
2. Lazy load below-fold content
3. Minimize JavaScript bundle
4. Use next/font for font optimization
5. Check for unnecessary re-renders

**Optimization Prompt:**
```markdown
Optimize page performance:
- Compress all images to < 100KB
- Lazy load FAQ and testimonials sections
- Remove unused dependencies
- Use dynamic imports for heavy components
```

#### Issue 4: Mobile Layout Broken
**Symptom:** Content overlaps or doesn't fit on mobile

**Solution:**
1. Check responsive breakpoints
2. Test with Chrome DevTools mobile view
3. Ensure touch targets are 44px+
4. Fix overflow issues

```tsx
// Use responsive Tailwind classes
<div className="text-4xl md:text-6xl lg:text-7xl">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

#### Issue 5: Analytics Not Tracking
**Symptom:** No data in Google Analytics

**Solution:**
1. Verify GA4 tracking ID is correct
2. Check script loads in browser DevTools
3. Test with GA Debug Chrome extension
4. Ensure NODE_ENV=production
5. Check ad blockers aren't blocking

#### Issue 6: SEO Meta Tags Not Showing
**Symptom:** Social previews show wrong image/text

**Solution:**
1. Check metadata export in page.tsx
2. Verify Open Graph image URL is absolute
3. Test with Facebook Sharing Debugger
4. Clear cache and re-scrape

```tsx
// Correct metadata export
export const metadata: Metadata = {
  title: "Product Name - Value Proposition",
  description: "Compelling description with keywords",
  openGraph: {
    images: ['https://yourdomain.com/og-image.jpg'],
  },
};
```

---

## Completion Checklist

### Before Launch
- [ ] All sections complete and populated with real content
- [ ] Form works and connects to backend/email
- [ ] All images optimized and have alt text
- [ ] SEO metadata complete
- [ ] Analytics tracking working
- [ ] Mobile responsive (tested on real device)
- [ ] Performance: Lighthouse score > 90
- [ ] Accessibility: WCAG AA compliant
- [ ] Cross-browser tested
- [ ] Legal pages linked (Privacy, Terms)

### Content Review
- [ ] Headlines compelling and clear
- [ ] Value proposition obvious
- [ ] CTAs specific and action-oriented
- [ ] Copy free of typos/errors
- [ ] Social proof authentic
- [ ] FAQs address real concerns
- [ ] Contact information correct

### Technical Review
- [ ] No console errors
- [ ] No broken links
- [ ] Forms validate properly
- [ ] API endpoints secure
- [ ] Environment variables set
- [ ] Error handling in place
- [ ] Build succeeds without warnings

---

## Time Breakdown

**Planning (5 min):**
- Step 1: Define goals and structure

**Development (30 min):**
- Step 2: Page structure - 5 min
- Step 3: Hero section - 5 min
- Step 4: Features section - 5 min
- Step 5: Lead form - 10 min
- Step 6: API endpoint - 5 min

**Optimization (10 min):**
- Step 7: SEO - 5 min
- Step 8: Analytics - 5 min
- Step 9: Performance - 5 min
- Step 10: Testimonials - 5 min
- Step 11: FAQ - 5 min
- Step 12: Pricing - 5 min
- Step 13: Footer/CTA - 5 min

**Testing & Launch (10 min):**
- Step 14: Testing - 5 min
- Step 15: Deployment - 5 min

**Total: 45 minutes**

---

## Next Steps

After launching:

1. **Monitor Analytics:**
   - Track conversion rate
   - Identify drop-off points
   - A/B test different headlines/CTAs

2. **Gather Feedback:**
   - User testing sessions
   - Heatmap analysis (Hotjar, Microsoft Clarity)
   - Scroll depth tracking

3. **Iterate:**
   - Improve based on data
   - Add more social proof
   - Optimize for conversions
   - Update content regularly

4. **Scale:**
   - Create variant pages for different audiences
   - Add localization for other languages
   - Build out additional pages
   - Implement advanced features

---

## Related Resources

**Templates:**
- [Frontend Component Template](../prompts/templates/frontend-component.md)
- [Growth Playbook Template](../prompts/templates/growth-playbook.md)

**Checklists:**
- [Daily Checklist](../DAILY_CHECKLIST.md)
- [Rules One Page](../RULES_ONE_PAGE.md)

**Rules to Review:**
- [Rule 1: Never Use Generic Prompts](../README.md#rule-1-never-use-generic-prompts)
- [Rule 3: Specify Output Format](../README.md#rule-3-specify-output-format-explicitly)
- [Rule 8: Provide Style Guidelines](../README.md#rule-8-provide-style-guidelines)
- [Rule 21: Validate All Inputs](../README.md#rule-21-validate-all-inputs)

---

**Last Updated:** 2025-10-23
**Version:** 1.0
**Estimated Time:** 45 minutes
