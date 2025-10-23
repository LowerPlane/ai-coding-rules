# Growth & Marketing Playbook Template

Use this template when generating landing pages, SEO content, and marketing automation with AI assistance.

---

## Context

**Stack:**
- Framework: Next.js 14.x / Astro 4.x / WordPress / Webflow
- Language: TypeScript 5.x / MDX
- Styling: Tailwind CSS 3.x / Styled Components 6.x
- SEO Tools: next-seo / @astrojs/seo
- Analytics: Google Analytics 4 / Plausible / PostHog
- Forms: React Hook Form 7.x / Formspree / HubSpot Forms
- CMS: Contentful / Sanity / Strapi / WordPress
- Email: Resend / SendGrid / Mailchimp

**Existing Code:**
- Analytics tracking setup
- Form handling utilities
- SEO metadata components
- Email templates
- CMS integration
- A/B testing framework

**Conventions:**
- Mobile-first responsive design
- Core Web Vitals optimization
- Semantic HTML for SEO
- Accessible content (WCAG 2.1 AA)
- Schema.org structured data
- Open Graph / Twitter Card metadata
- Performance budget: < 100KB initial JS

---

## Task

Create [ASSET TYPE] for [MARKETING GOAL]

### Specific Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

---

## Asset Specification

### Asset Type

**Landing Page** / **Blog Post** / **Email Campaign** / **Social Content** / **SEO Page**

### Target Audience

**Primary Persona:**
- Role: [e.g., "Software Developer"]
- Pain Points: [e.g., "Struggling with deployment complexity"]
- Goals: [e.g., "Deploy apps faster with less effort"]
- Technical Level: Beginner / Intermediate / Advanced

**Secondary Persona(s):**
- [Additional personas if applicable]

### Conversion Goal

**Primary CTA:** [e.g., "Sign up for free trial"]
**Secondary CTA:** [e.g., "Book a demo"]
**Success Metric:** [e.g., "15% conversion rate"]

### SEO Targets

**Primary Keyword:** [e.g., "serverless deployment platform"]
**Secondary Keywords:**
- [e.g., "deploy node.js serverless"]
- [e.g., "auto-scaling web apps"]
- [e.g., "cloud deployment automation"]

**Target Search Intent:** Informational / Commercial / Transactional / Navigational

**Target Featured Snippet:** Yes / No

---

## Content Structure

### Landing Page Structure

```markdown
## Above the Fold (< 600px height)
- Headline (H1): Clear value proposition (< 10 words)
- Subheadline: Expand on benefit (< 20 words)
- Primary CTA: Action button (visible without scroll)
- Hero visual: Product demo, illustration, or video
- Social proof: Trust badges, logos, testimonial snippet

## Problem Section
- Empathize with pain points (3-5 bullet points)
- Quantify the problem with data/statistics
- Relatable scenario or story

## Solution Section
- Introduce product as the solution
- Key benefits (3-4 main points)
- How it works (simple 3-step process)
- Visual demonstration

## Features Section
- 3-6 core features
- Each with:
  - Icon or visual
  - Benefit-focused headline
  - 2-3 sentence description
  - Optional: "Learn more" link

## Social Proof Section
- Customer testimonials (3-5)
- Case studies with metrics
- Company logos
- Review ratings
- Usage statistics

## Pricing Section (if applicable)
- Clear tier comparison
- Highlight recommended option
- Include all features
- Transparent pricing
- FAQ section

## Final CTA Section
- Restate value proposition
- Clear call to action
- Risk reducer (free trial, money-back guarantee)
- Secondary CTA option

## Footer
- Navigation links
- Legal links (Privacy, Terms)
- Social media links
- Contact information
```

### Blog Post Structure

```markdown
## Title (SEO-optimized H1)
- Include primary keyword
- 50-60 characters ideal
- Compelling and clear

## Introduction (150-200 words)
- Hook: Interesting fact, question, or statistic
- Problem statement
- What reader will learn
- Why it matters

## Table of Contents
- H2 sections linked
- Improves UX and SEO

## Body Content
### Section 1 (H2)
- Main point with supporting details
- Examples, code snippets, visuals
- 300-500 words per section

### Section 2 (H2)
- Continue logical flow
- Mix text with visuals

### Section 3 (H2)
- Progressive depth

## Practical Examples
- Code samples (syntax highlighted)
- Screenshots
- Step-by-step tutorials

## Conclusion (100-150 words)
- Summarize key takeaways
- Call to action
- Related content links

## Author Bio
- Credibility building
- Link to other content

## Related Articles
- 3-5 internal links
- Improves engagement and SEO
```

---

## SEO Requirements

### Metadata Structure

```typescript
interface SEOMetadata {
  // Page metadata
  title: string;              // 50-60 chars, include primary keyword
  description: string;        // 150-160 chars, compelling summary
  canonical: string;          // Canonical URL

  // Open Graph (Facebook, LinkedIn)
  og: {
    title: string;            // Can differ from page title
    description: string;
    image: string;            // 1200x630px recommended
    url: string;
    type: 'website' | 'article';
    siteName: string;
  };

  // Twitter Card
  twitter: {
    card: 'summary_large_image' | 'summary';
    title: string;
    description: string;
    image: string;
    creator?: string;         // @username
  };

  // Additional
  robots?: string;            // 'index,follow' | 'noindex,nofollow'
  keywords?: string[];        // Optional, not critical for SEO
  alternates?: {
    canonical?: string;
    languages?: Record<string, string>;
  };
}
```

### Schema.org Structured Data

**Article Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Complete Guide to Serverless Deployment",
  "description": "Learn how to deploy serverless applications...",
  "image": "https://example.com/og-image.jpg",
  "datePublished": "2025-10-23T10:00:00Z",
  "dateModified": "2025-10-23T10:00:00Z",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://example.com/authors/jane-smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "YourCompany",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

**Product Schema (for pricing pages):**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Pro Plan",
  "description": "Advanced features for growing teams",
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

**FAQ Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does serverless deployment work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Serverless deployment automatically..."
      }
    }
  ]
}
```

---

## Output Format

### File Structure

**Next.js Project:**
```
src/
├── app/
│   ├── (marketing)/
│   │   ├── page.tsx                    # Landing page
│   │   ├── pricing/page.tsx           # Pricing page
│   │   ├── blog/
│   │   │   ├── page.tsx               # Blog index
│   │   │   └── [slug]/page.tsx        # Blog post
│   │   └── layout.tsx                 # Marketing layout
│   └── layout.tsx                     # Root layout
├── components/
│   ├── marketing/
│   │   ├── Hero.tsx                   # Hero section
│   │   ├── Features.tsx               # Features grid
│   │   ├── Testimonials.tsx           # Social proof
│   │   ├── CTA.tsx                    # Call to action
│   │   ├── Pricing.tsx                # Pricing table
│   │   └── FAQ.tsx                    # FAQ accordion
│   └── shared/
│       ├── SEO.tsx                    # SEO component
│       ├── Newsletter.tsx             # Newsletter form
│       └── SocialShare.tsx            # Social sharing
├── content/
│   └── blog/
│       └── post-slug.mdx              # MDX blog posts
├── lib/
│   ├── analytics.ts                   # Analytics tracking
│   ├── seo.ts                         # SEO utilities
│   └── email.ts                       # Email service
└── public/
    ├── images/
    │   ├── og/                        # OG images
    │   └── blog/                      # Blog images
    └── robots.txt
```

### Code Style

**Landing Page Component (Next.js):**
```typescript
import { Metadata } from 'next';
import { Hero } from '@/components/marketing/Hero';
import { Features } from '@/components/marketing/Features';
import { Testimonials } from '@/components/marketing/Testimonials';
import { CTA } from '@/components/marketing/CTA';
import { trackPageView } from '@/lib/analytics';

/**
 * Landing Page - Main product landing page
 *
 * Conversion Goal: Sign up for free trial
 * Target Audience: Software developers
 */

export const metadata: Metadata = {
  title: 'Deploy Serverless Apps in Seconds | YourProduct',
  description: 'The fastest way to deploy serverless applications. Auto-scaling, zero config, deploy with one command. Start free.',
  keywords: ['serverless deployment', 'cloud hosting', 'auto-scaling'],
  openGraph: {
    title: 'Deploy Serverless Apps in Seconds',
    description: 'The fastest way to deploy serverless applications.',
    images: [
      {
        url: 'https://example.com/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'YourProduct - Serverless Deployment Platform',
      },
    ],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Deploy Serverless Apps in Seconds',
    description: 'The fastest way to deploy serverless applications.',
    images: ['https://example.com/og-image.jpg'],
  },
  alternates: {
    canonical: 'https://example.com',
  },
};

export default function LandingPage() {
  // Track page view
  trackPageView('landing_page');

  return (
    <main>
      {/* Hero Section */}
      <Hero
        headline="Deploy Serverless Apps in Seconds"
        subheadline="The fastest way to deploy and scale your applications. Zero configuration, auto-scaling, and one-command deployment."
        ctaText="Start Free Trial"
        ctaHref="/signup"
        secondaryCtaText="See Demo"
        secondaryCtaHref="/demo"
        videoUrl="/videos/demo.mp4"
      />

      {/* Social Proof */}
      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-4">
          <p className="text-center text-gray-600 mb-8">
            Trusted by 10,000+ developers at leading companies
          </p>
          <div className="flex justify-center items-center gap-8 flex-wrap">
            {/* Company logos */}
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 max-w-4xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Deployment Shouldn't Be This Hard
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <ProblemCard
              icon="⏱️"
              title="Hours of Setup"
              description="Configuring servers, load balancers, and deployment pipelines wastes valuable development time."
            />
            <ProblemCard
              icon="💸"
              title="Expensive Infrastructure"
              description="Paying for idle servers and over-provisioned resources drains your budget."
            />
            <ProblemCard
              icon="📈"
              title="Scaling Nightmares"
              description="Manual scaling during traffic spikes leads to downtime and lost revenue."
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <Features
        title="Everything You Need to Ship Faster"
        features={[
          {
            icon: '🚀',
            title: 'One-Command Deploy',
            description: 'Deploy your app with a single command. No configuration files, no complex setups.',
            link: '/docs/quickstart',
          },
          {
            icon: '⚡',
            title: 'Auto-Scaling',
            description: 'Automatically scales from zero to millions of requests. Pay only for what you use.',
            link: '/docs/scaling',
          },
          {
            icon: '🔒',
            title: 'Built-in Security',
            description: 'SSL certificates, DDoS protection, and security headers configured by default.',
            link: '/docs/security',
          },
          {
            icon: '📊',
            title: 'Real-time Analytics',
            description: 'Monitor performance, errors, and usage with built-in analytics dashboard.',
            link: '/docs/analytics',
          },
        ]}
      />

      {/* How It Works */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 max-w-5xl">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            Deploy in 3 Simple Steps
          </h2>
          <div className="space-y-12">
            <Step
              number={1}
              title="Install the CLI"
              description="One command to install our deployment tool globally."
              code="npm install -g yourproduct-cli"
            />
            <Step
              number={2}
              title="Connect Your Project"
              description="Link your project directory to your account."
              code="yourproduct init"
            />
            <Step
              number={3}
              title="Deploy"
              description="Push your code to production in seconds."
              code="yourproduct deploy"
            />
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <Testimonials
        title="Loved by Developers Worldwide"
        testimonials={[
          {
            quote: "YourProduct reduced our deployment time from hours to seconds. Game changer for our team.",
            author: "Sarah Chen",
            role: "CTO at TechStartup",
            avatar: "/images/avatars/sarah.jpg",
            rating: 5,
          },
          {
            quote: "The auto-scaling saved us during our Product Hunt launch. Handled 100x traffic spike without any intervention.",
            author: "Mike Rodriguez",
            role: "Founder at AppCo",
            avatar: "/images/avatars/mike.jpg",
            rating: 5,
          },
          {
            quote: "Best developer experience I've had with any deployment platform. Simple, fast, reliable.",
            author: "Emily Watson",
            role: "Lead Developer at AgencyX",
            avatar: "/images/avatars/emily.jpg",
            rating: 5,
          },
        ]}
      />

      {/* Final CTA */}
      <CTA
        title="Start Deploying in Seconds"
        description="Join 10,000+ developers shipping faster with YourProduct. No credit card required."
        ctaText="Start Free Trial"
        ctaHref="/signup"
        secondaryText="14-day free trial • No credit card required • Cancel anytime"
      />

      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'SoftwareApplication',
            name: 'YourProduct',
            applicationCategory: 'DeveloperApplication',
            operatingSystem: 'Cross-platform',
            offers: {
              '@type': 'Offer',
              price: '0',
              priceCurrency: 'USD',
            },
            aggregateRating: {
              '@type': 'AggregateRating',
              ratingValue: '4.9',
              reviewCount: '1247',
            },
          }),
        }}
      />
    </main>
  );
}

function ProblemCard({ icon, title, description }: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="text-center">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function Step({ number, title, description, code }: {
  number: number;
  title: string;
  description: string;
  code: string;
}) {
  return (
    <div className="flex gap-6">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xl">
        {number}
      </div>
      <div className="flex-1">
        <h3 className="text-2xl font-semibold mb-2">{title}</h3>
        <p className="text-gray-600 mb-4">{description}</p>
        <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
}
```

**Blog Post Component (MDX):**
```mdx
---
title: "Complete Guide to Serverless Deployment in 2025"
description: "Learn how to deploy serverless applications efficiently with modern tools and best practices."
publishedAt: "2025-10-23"
author: "Jane Smith"
category: "Tutorial"
keywords: ["serverless", "deployment", "cloud", "tutorial"]
image: "/images/blog/serverless-guide.jpg"
---

import { CodeBlock } from '@/components/CodeBlock';
import { Callout } from '@/components/Callout';
import { TableOfContents } from '@/components/TableOfContents';

# Complete Guide to Serverless Deployment in 2025

Serverless deployment has revolutionized how we build and ship applications. In this comprehensive guide, you'll learn everything you need to know about deploying serverless apps in 2025.

<TableOfContents items={[
  { title: "What is Serverless?", href: "#what-is-serverless" },
  { title: "Benefits of Serverless", href: "#benefits" },
  { title: "Getting Started", href: "#getting-started" },
  { title: "Best Practices", href: "#best-practices" },
]} />

## What is Serverless? {#what-is-serverless}

Serverless computing is a cloud execution model where the cloud provider manages the infrastructure...

<Callout type="info">
  **Did you know?** 70% of companies are using or evaluating serverless technologies in 2025.
</Callout>

## Benefits of Serverless {#benefits}

### 1. Cost Efficiency

Pay only for actual compute time. No charges when your code isn't running.

### 2. Auto-Scaling

Automatically handles traffic spikes from 1 to 1 million requests.

### 3. Developer Productivity

Focus on writing code, not managing infrastructure.

## Getting Started {#getting-started}

Here's how to deploy your first serverless function:

<CodeBlock language="bash">
{`# Install the CLI
npm install -g yourproduct-cli

# Initialize your project
yourproduct init

# Deploy to production
yourproduct deploy`}
</CodeBlock>

### Project Structure

Create a simple serverless function:

<CodeBlock language="typescript" filename="api/hello.ts">
{`export default async function handler(req: Request) {
  return new Response(JSON.stringify({
    message: 'Hello, World!'
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
}`}
</CodeBlock>

## Best Practices {#best-practices}

### 1. Keep Functions Small

Each function should do one thing well. Aim for under 50 lines of code per function.

### 2. Use Environment Variables

Never hardcode secrets. Use environment variables for all configuration.

### 3. Monitor Performance

Set up monitoring and alerts for:
- Cold start times
- Error rates
- Execution duration
- Memory usage

### 4. Implement Proper Error Handling

<CodeBlock language="typescript">
{`export default async function handler(req: Request) {
  try {
    const data = await fetchData();
    return Response.json(data);
  } catch (error) {
    console.error('Error:', error);
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}`}
</CodeBlock>

## Conclusion

Serverless deployment offers significant benefits for modern applications. By following these best practices, you can build scalable, cost-effective applications.

**Ready to get started?** [Sign up for a free account](/signup) and deploy your first serverless app today.

---

## Related Articles

- [Serverless vs. Traditional Hosting: A Comparison](/blog/serverless-vs-traditional)
- [Optimizing Serverless Cold Starts](/blog/cold-start-optimization)
- [Serverless Security Best Practices](/blog/serverless-security)
```

---

## Performance Requirements

### Core Web Vitals Targets

**Largest Contentful Paint (LCP):** < 2.5s
- Optimize hero images
- Lazy load below-fold content
- Use image CDN with WebP/AVIF

**First Input Delay (FID):** < 100ms
- Minimize JavaScript execution
- Defer non-critical scripts
- Use code splitting

**Cumulative Layout Shift (CLS):** < 0.1
- Set explicit dimensions for images/videos
- Reserve space for dynamic content
- Avoid inserting content above existing content

### Performance Budget

```typescript
interface PerformanceBudget {
  // JavaScript
  totalJavaScript: 100,      // KB (gzipped)
  mainBundle: 50,            // KB (gzipped)

  // CSS
  totalCSS: 20,              // KB (gzipped)

  // Images
  heroImage: 100,            // KB
  thumbnails: 20,            // KB each

  // Fonts
  totalFonts: 50,            // KB (WOFF2)

  // Total Page Weight
  totalPageWeight: 500,      // KB (initial load)

  // Timing
  timeToInteractive: 3500,   // ms
  speedIndex: 3000,          // ms
}
```

### Optimization Techniques

```typescript
// Image Optimization (Next.js)
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Product demo"
  width={1200}
  height={630}
  priority // LCP image
  quality={85}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>

// Lazy Loading
<Image
  src="/feature.jpg"
  alt="Feature screenshot"
  width={800}
  height={600}
  loading="lazy" // Below fold
/>

// Font Optimization
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

// Code Splitting
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false, // Client-side only
});
```

---

## Analytics & Tracking Requirements

### Event Tracking

```typescript
import { trackEvent } from '@/lib/analytics';

// Track CTA clicks
function handleCTAClick() {
  trackEvent({
    category: 'engagement',
    action: 'cta_click',
    label: 'hero_signup',
    value: 1,
  });

  // Navigate to signup
  router.push('/signup');
}

// Track form submissions
function handleFormSubmit(data: FormData) {
  trackEvent({
    category: 'conversion',
    action: 'form_submit',
    label: 'newsletter_signup',
    value: 1,
  });

  // Submit form
  submitNewsletter(data);
}

// Track scroll depth
useEffect(() => {
  const handleScroll = () => {
    const scrollPercent = (window.scrollY / document.body.scrollHeight) * 100;

    if (scrollPercent > 75 && !trackedScroll75) {
      trackEvent({
        category: 'engagement',
        action: 'scroll_depth',
        label: '75_percent',
        value: 75,
      });
      setTrackedScroll75(true);
    }
  };

  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

### A/B Testing Setup

```typescript
import { useABTest } from '@/lib/ab-testing';

function Hero() {
  const { variant, recordConversion } = useABTest('hero_headline_test', {
    variants: ['control', 'variant_a', 'variant_b'],
    weights: [0.33, 0.33, 0.34],
  });

  const headlines = {
    control: 'Deploy Serverless Apps in Seconds',
    variant_a: 'Ship Code 10x Faster with Serverless',
    variant_b: 'The Fastest Way to Deploy Your Apps',
  };

  const handleSignup = () => {
    recordConversion();
    router.push('/signup');
  };

  return (
    <h1>{headlines[variant]}</h1>
    // ... rest of hero
  );
}
```

---

## Content Guidelines

### Writing Best Practices

**Headlines:**
- Be specific and benefit-focused
- Use numbers when possible ("Deploy in 3 Steps")
- Keep under 70 characters
- Include primary keyword

**Body Copy:**
- Use active voice
- Short sentences (< 20 words)
- Short paragraphs (2-3 sentences)
- Bullet points for lists
- Bold important points

**Call to Action:**
- Use action verbs ("Start", "Get", "Try")
- Create urgency ("Start Free Trial Today")
- Reduce friction ("No Credit Card Required")
- Be specific ("Deploy Your First App")

### Voice & Tone

**Brand Voice:**
- Professional but approachable
- Technical but not jargony
- Confident but not arrogant
- Helpful and educational

**Dos:**
- Use "you" and "your" (second person)
- Be conversational
- Use contractions
- Show, don't just tell

**Don'ts:**
- Use corporate jargon
- Make unsubstantiated claims
- Be overly salesy
- Use passive voice

---

## Accessibility Requirements

**WCAG 2.1 AA Compliance:**

1. **Semantic HTML**
   - Proper heading hierarchy
   - Descriptive link text
   - Form labels

2. **Color Contrast**
   - 4.5:1 for normal text
   - 3:1 for large text
   - Don't rely on color alone

3. **Keyboard Navigation**
   - All interactive elements focusable
   - Skip to main content link
   - Visible focus indicators

4. **Alt Text for Images**
   ```tsx
   <Image
     src="/feature.jpg"
     alt="Dashboard showing real-time analytics with graphs and metrics"
     // Not: alt="Dashboard" (too vague)
     // Not: alt="Image of dashboard" (redundant)
   />
   ```

5. **ARIA Labels**
   ```tsx
   <button
     onClick={handleMenu}
     aria-label="Open navigation menu"
     aria-expanded={isMenuOpen}
   >
     <HamburgerIcon />
   </button>
   ```

---

## Email Campaign Structure

### Email Template

```typescript
interface EmailTemplate {
  subject: string;              // 50 chars max
  preheader: string;            // 90 chars max
  from: {
    name: string;
    email: string;
  };

  // Content sections
  header: {
    logo: string;
    tagline?: string;
  };

  hero: {
    headline: string;
    subheadline?: string;
    image?: string;
    cta: {
      text: string;
      url: string;
    };
  };

  body: Section[];

  footer: {
    unsubscribeUrl: string;
    companyInfo: string;
    socialLinks: SocialLink[];
  };
}

// Example: Product Launch Email
const productLaunchEmail: EmailTemplate = {
  subject: "🚀 We just launched auto-scaling",
  preheader: "Deploy apps that scale automatically from 0 to millions of requests",
  from: {
    name: "Jane from YourProduct",
    email: "jane@yourproduct.com",
  },
  hero: {
    headline: "Introducing Auto-Scaling",
    subheadline: "Your apps now scale automatically. Zero configuration required.",
    image: "https://example.com/emails/auto-scaling-hero.jpg",
    cta: {
      text: "Try It Now",
      url: "https://example.com/auto-scaling",
    },
  },
  body: [
    {
      type: 'text',
      content: "We're excited to announce auto-scaling is now available for all users...",
    },
    {
      type: 'features',
      features: [
        { title: "Zero Config", description: "Works out of the box" },
        { title: "Pay Per Use", description: "Only pay for active requests" },
      ],
    },
  ],
  footer: {
    unsubscribeUrl: "https://example.com/unsubscribe",
    companyInfo: "YourProduct Inc, 123 Main St, San Francisco, CA",
    socialLinks: [
      { platform: 'twitter', url: 'https://twitter.com/yourproduct' },
      { platform: 'github', url: 'https://github.com/yourproduct' },
    ],
  },
};
```

---

## Testing Requirements

### Conversion Optimization Tests

**A/B Test Scenarios:**
1. Headline variations
2. CTA button text and color
3. Hero image vs. video
4. Pricing display format
5. Social proof placement
6. Form field count

**Multivariate Tests:**
- Headline + CTA + Hero Image combinations
- Run with significant traffic (> 1000 visits per variant)

### Quality Checklist

**Pre-Launch:**
- [ ] All links work (no 404s)
- [ ] Forms submit successfully
- [ ] Mobile responsive (320px - 1920px)
- [ ] Images optimized (WebP/AVIF)
- [ ] Page load < 3s
- [ ] Core Web Vitals pass
- [ ] SEO metadata complete
- [ ] Schema.org markup added
- [ ] Analytics tracking works
- [ ] WCAG 2.1 AA compliant
- [ ] Browser testing (Chrome, Safari, Firefox, Edge)
- [ ] Spell check and grammar
- [ ] Legal links present (Privacy, Terms)

---

## Dependencies

**Use existing packages only:**
- next / astro (framework)
- react / vue (UI library)
- tailwindcss (styling)
- next-seo / @astrojs/seo (SEO)
- @vercel/analytics / plausible (analytics)
- react-hook-form (forms)
- resend / sendgrid (email)
- framer-motion (animations)

**DO NOT install new packages without approval**

---

## Example Usage

### Prompt Example

```markdown
## Context
- Stack: Next.js 14 + TypeScript + Tailwind + Contentful CMS
- Existing: Analytics setup, form handlers, SEO components
- Conventions: Mobile-first, Core Web Vitals < 2.5s, WCAG 2.1 AA

## Task
Create landing page for SaaS product launch

## Target Audience
- Primary: Software developers (25-40 years old)
- Pain Point: Complex deployment processes
- Goal: Deploy apps faster with less effort
- Technical Level: Intermediate to advanced

## Conversion Goal
- Primary CTA: "Start Free Trial"
- Target: 15% conversion rate
- Success Metric: Sign-ups from organic traffic

## SEO Requirements
- Primary Keyword: "serverless deployment platform"
- Secondary Keywords: "auto-scaling", "one-click deploy", "cloud hosting"
- Target: Featured snippet for "how to deploy serverless"
- Meta description: 155 characters, compelling

## Content Structure
- Hero: Value prop headline, demo video, CTA
- Problem: 3 pain points with developer quotes
- Solution: 4 core features with visuals
- How It Works: 3-step process with code examples
- Social Proof: 5 testimonials, company logos
- Pricing: 3 tiers, highlight "Pro" plan
- FAQ: 6 common questions
- Final CTA: Risk reducers (free trial, no CC)

## Design Requirements
- Mobile-first responsive
- Tailwind CSS utility classes
- Animations: Framer Motion (subtle, purposeful)
- Images: WebP format, lazy loading
- Code blocks: Syntax highlighting

## Performance
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- Total JS: < 100KB gzipped
- Lighthouse score: > 90

## Analytics
- Track: CTA clicks, scroll depth, form submissions
- A/B test: Headline variations (3 variants)
- Conversion funnel: Landing → Signup → Activation

## Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigable
- Screen reader tested
- Color contrast 4.5:1
- Alt text for all images

Generate: page.tsx, components, metadata, schema.org markup, analytics tracking
```

---

## Checklist

Before launching marketing content:

- [ ] Primary keyword in title, H1, first paragraph
- [ ] Meta description 150-160 characters
- [ ] Open Graph image 1200x630px
- [ ] Schema.org structured data added
- [ ] All images have descriptive alt text
- [ ] Internal links to related content (3-5)
- [ ] External links open in new tab
- [ ] CTA clear and prominent
- [ ] Mobile responsive (tested on real devices)
- [ ] Page load < 3 seconds
- [ ] Core Web Vitals pass
- [ ] No console errors
- [ ] Analytics tracking verified
- [ ] Forms tested and working
- [ ] Legal links present (Privacy, Terms)
- [ ] WCAG 2.1 AA compliant
- [ ] Spell check and grammar review
- [ ] A/B test configured (if applicable)
- [ ] Social sharing tested

---

**See also:**
- [Rule 24: Sanitize User-Generated Content](../../README.md#rule-24-sanitize-user-generated-content)
- [Rule 37: Test Everything](../../README.md#rule-37-test-everything-ai-generates)
- [DAILY_CHECKLIST.md](../../DAILY_CHECKLIST.md)
