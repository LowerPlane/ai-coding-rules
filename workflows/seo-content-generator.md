# SEO Content Generator Workflow

**Complete SEO-optimized content creation in 30 minutes using AI assistance**

---

## Overview

**Time Estimate:** 30 minutes
**Difficulty Level:** Beginner
**Prerequisites:**
- Basic SEO knowledge
- Understanding of target audience
- Content strategy or keywords identified
- Access to SEO tools (optional but helpful)

**What You'll Create:**
SEO-optimized content including:
- Keyword-optimized blog posts/articles
- Meta titles and descriptions
- Header structure (H1, H2, H3)
- Internal and external links
- Schema markup (JSON-LD)
- Image alt text
- URL slugs
- Social media snippets

---

## Prerequisites and Setup

### Required Tools
- Text editor or CMS (WordPress, Contentful, etc.)
- SEO tools (Google Search Console, Ahrefs, SEMrush - optional)
- Keyword research completed
- Target audience defined

### Required Knowledge
- Basic SEO principles (keywords, meta tags, headers)
- Understanding of search intent
- Content marketing fundamentals
- On-page SEO best practices

### Initial Setup (2 minutes)
```bash
# Create content directory
mkdir -p content/{blog,pages,drafts}

# Install markdown tools (optional)
npm install -g marked

# Create SEO checklist template
touch content/seo-checklist.md
```

---

## Workflow Steps

### Step 1: Define Content Strategy and Keywords (3 minutes)

**Objective:** Establish clear content goals and target keywords

**Action:**
Research and document your content strategy.

**Questions to Answer:**
1. What is the search intent? (Informational, Navigational, Transactional, Commercial)
2. Who is the target audience?
3. What problem does this content solve?
4. What action should readers take?

**Prompt to Use:**
```markdown
Help me plan SEO content strategy:

Topic: [Your topic]
Target Audience: [Demographics, job titles, pain points]
Search Intent: [Informational/Navigational/Transactional/Commercial]
Primary Keyword: [Main keyword, search volume]
Secondary Keywords: [Related keywords, LSI keywords]
Competitor URLs: [Top 3 ranking pages for this keyword]

Content Goals:
- Rank for: [target keywords]
- Drive: [traffic/leads/sales]
- Differentiation: [How we're better than competitors]

Analyze competitors and suggest:
1. Content length (word count)
2. H2/H3 structure
3. Topics to cover
4. Content gaps to fill
5. Unique angle to take
```

**Example Output:**
```
Topic: "How to Optimize Images for SEO"
Primary Keyword: "image optimization for SEO" (1,200 searches/month)
Secondary: "compress images for web", "image alt text best practices"
Search Intent: Informational
Recommended Length: 1,800-2,200 words
Competitor Analysis:
  - Top article is 2,100 words, covers 12 subtopics
  - Gap: No mention of WebP format or Core Web Vitals
  - Unique angle: Focus on real performance data and case studies
```

**Review Checkpoint:**
- [ ] Primary keyword identified
- [ ] Secondary keywords listed
- [ ] Search intent understood
- [ ] Target audience defined
- [ ] Competitor content analyzed
- [ ] Unique angle determined

**References:** [Rule 1: Never Use Generic Prompts](../README.md#rule-1-never-use-generic-prompts), [Rule 2: Provide Context](../README.md#rule-2-always-provide-context-before-task)

---

### Step 2: Generate Content Outline (3 minutes)

**Objective:** Create SEO-optimized article structure

**Action:**
Generate a comprehensive outline with proper header hierarchy.

**Prompt to Use:**
```markdown
Generate an SEO-optimized content outline for:

Topic: [Your topic]
Primary Keyword: [keyword]
Target Length: [word count]
Audience: [description]

Requirements:
- H1 (title): Include primary keyword naturally
- H2 sections (6-10): Cover main subtopics
- H3 subsections: Break down complex topics
- Introduction (100-150 words): Hook + what readers will learn
- Conclusion (100-150 words): Summary + call-to-action

Each section should:
- Answer specific search queries
- Include relevant keywords naturally
- Have clear value proposition
- Build logically on previous sections

Include:
- FAQ section (5-7 questions)
- Key takeaways box
- Internal linking opportunities
- External reference points
- Visual content suggestions (images, charts, videos)

Format as:
# [Title with Primary Keyword]

## Introduction
- Hook
- Problem statement
- What readers will learn
- Why this matters

## [H2 Section 1]
### [H3 Subsection]
### [H3 Subsection]

[Continue for all sections]

## FAQ
- Question 1
- Question 2
...

## Conclusion
- Summary
- Call-to-action
```

**Example Output:**
```markdown
# How to Optimize Images for SEO: Complete Guide for 2025

## Introduction
- Hook: Images account for 21% of total page weight
- Problem: Slow images hurt rankings and conversions
- What you'll learn: Compression, formats, alt text, Core Web Vitals
- Why: Google now prioritizes page speed in rankings

## Why Image Optimization Matters for SEO
### Impact on Page Speed
### Effect on Core Web Vitals
### Mobile-First Indexing Requirements

## Choosing the Right Image Format
### JPEG vs PNG vs WebP
### When to Use SVG
### Emerging Formats (AVIF)

## Image Compression Techniques
### Lossy vs Lossless Compression
### Tools for Compression
### Automated Workflows

## Writing Effective Alt Text
### Alt Text Best Practices
### Common Mistakes to Avoid
### Alt Text for Decorative Images

## Implementing Lazy Loading
### Native Browser Lazy Loading
### JavaScript Solutions
### WordPress Lazy Load Plugins

## Image Sitemaps and Schema Markup
### Creating Image Sitemaps
### ProductImage Schema
### ImageObject Schema

## FAQ
- What's the ideal file size for web images?
- Does image file name affect SEO?
- Should I use CDN for images?
- How does WebP compare to JPEG?
- What's the best alt text length?

## Conclusion
- Summary of key points
- Action steps
- Further resources
- CTA: Download image optimization checklist
```

**Review Checkpoint:**
- [ ] Title includes primary keyword
- [ ] Clear H2/H3 hierarchy
- [ ] Introduction hooks reader
- [ ] Each section has clear purpose
- [ ] FAQ addresses common questions
- [ ] Conclusion includes CTA
- [ ] Logical flow throughout

**References:** [Rule 3: Specify Output Format](../README.md#rule-3-specify-output-format-explicitly)

---

### Step 3: Generate Introduction and Hook (3 minutes)

**Objective:** Create engaging opening that includes keywords

**Action:**
Write compelling introduction that hooks readers and includes SEO elements.

**Prompt to Use:**
```markdown
Write an SEO-optimized introduction for:

Title: [Your H1 title]
Primary Keyword: [keyword]
Target Audience: [description]
Word Count: 100-150 words

Introduction should:
- Start with compelling hook (statistic, question, or bold statement)
- Establish credibility
- State the problem clearly
- Preview what readers will learn
- Include primary keyword in first 100 words
- Natural, conversational tone
- No keyword stuffing

Examples of good hooks:
- "Did you know that 53% of mobile users abandon sites that take over 3 seconds to load?"
- "If your images aren't optimized, you're literally throwing money away."
- "Here's a surprising fact: Most websites waste 70% of their bandwidth on unoptimized images."

Write introduction that:
1. Grabs attention immediately
2. Relates to reader's pain point
3. Promises clear value
4. Sets up the rest of the article
```

**Example Output:**
```markdown
Did you know that images account for over 21% of a website's total weight? If your images aren't optimized for SEO, you're not just slowing down your site—you're actively hurting your search rankings and losing potential customers.

Image optimization for SEO is no longer optional. With Google's Core Web Vitals now a ranking factor, slow-loading images can push your pages down in search results, costing you valuable traffic and revenue.

In this comprehensive guide, you'll learn exactly how to optimize your images for search engines, from choosing the right file formats to writing effective alt text. By the end, you'll have a complete checklist for ensuring every image on your site contributes to—rather than detracts from—your SEO performance.
```

**Review Checkpoint:**
- [ ] Strong hook in first sentence
- [ ] Primary keyword in first paragraph
- [ ] Problem clearly stated
- [ ] Value proposition clear
- [ ] Engaging and conversational
- [ ] 100-150 words
- [ ] Sets up article content

**References:** [Rule 8: Provide Style Guidelines](../README.md#rule-8-provide-style-guidelines)

---

### Step 4: Generate Main Content Sections (10 minutes)

**Objective:** Create detailed, keyword-rich body content

**Action:**
Generate content for each H2/H3 section.

**Prompt to Use:**
```markdown
Generate content for this section:

Section Title (H2): [Section heading]
Subsections (H3): [List H3 headings]
Primary Keywords: [relevant keywords for this section]
Target Length: [words per section]
Tone: [Professional/Casual/Technical]

Content requirements:
- Address user search intent directly
- Include keywords naturally (1-2% density)
- Use short paragraphs (2-3 sentences max)
- Include bullet points or numbered lists where appropriate
- Add examples or case studies
- Link to authoritative sources
- Suggest images/visuals
- Write for 8th-grade reading level
- Active voice preferred
- Transition smoothly between subsections

For each subsection:
1. Main point in first sentence
2. Supporting details
3. Example or data point
4. Actionable takeaway

Include:
- [ ] Statistics or data
- [ ] Expert quotes (if relevant)
- [ ] Step-by-step instructions
- [ ] Common mistakes to avoid
- [ ] Pro tips or best practices

Avoid:
- Keyword stuffing
- Overly technical jargon (unless appropriate)
- Long walls of text
- Passive voice
- Fluff or filler content
```

**Example Prompt:**
```markdown
Generate content for:

Section: "Image Compression Techniques"
Subsections:
  - Lossy vs Lossless Compression
  - Tools for Compression
  - Automated Workflows

Keywords: image compression, reduce file size, compress images for web
Length: 400-500 words
Tone: Professional but approachable
Audience: Website owners and marketers with basic technical knowledge
```

**Example Output:**
```markdown
## Image Compression Techniques

Image compression is the most effective way to reduce file sizes without sacrificing visual quality. The key is understanding when to use different compression methods and tools.

### Lossy vs Lossless Compression

Lossy compression reduces file size by removing some image data. This works great for photographs where small quality losses aren't noticeable. JPEGs use lossy compression, which is why a 2MB photo can become 200KB with minimal visual difference.

Lossless compression, on the other hand, preserves all original data. PNG files use this method, making them ideal for graphics with text, logos, or sharp edges. The tradeoff? Larger file sizes compared to lossy compression.

**When to use each:**
- Lossy (JPEG): Photographs, hero images, thumbnails
- Lossless (PNG): Logos, icons, graphics with text
- WebP: Modern format that offers both options with better compression

### Tools for Compression

You don't need expensive software to compress images effectively. Here are the best tools:

**Free online tools:**
- TinyPNG - Reduces PNG and JPEG files by up to 70%
- Squoosh - Google's image compression tool with real-time preview
- ImageOptim - Mac app for batch compression

**Developer tools:**
- ImageMagick - Command-line tool for automated compression
- Sharp - Node.js image processing library
- Pillow - Python imaging library

For WordPress users, plugins like ShortPixel and Smush handle compression automatically.

### Automated Workflows

Manual compression doesn't scale. Here's how to automate the process:

1. **Build process integration**: Add compression to your build pipeline using tools like webpack-image-loader or gulp-imagemin
2. **CDN automatic optimization**: Services like Cloudflare and Cloudinary compress images on-the-fly
3. **CMS plugins**: WordPress plugins compress uploads automatically
4. **Git hooks**: Run compression scripts before commits

Pro tip: Aim for images under 100KB for above-the-fold content and under 200KB for below-the-fold images.
```

**Review Checkpoint:**
- [ ] Section addresses search intent
- [ ] Keywords used naturally
- [ ] Short, scannable paragraphs
- [ ] Bullet points for lists
- [ ] Examples or data included
- [ ] Actionable takeaways present
- [ ] Reading level appropriate
- [ ] Smooth transitions

**References:** [Rule 9: Use Example-Driven Prompts](../README.md#rule-9-use-example-driven-prompts)

---

### Step 5: Generate FAQ Section (3 minutes)

**Objective:** Answer common questions with schema markup

**Action:**
Create FAQ section optimized for featured snippets.

**Prompt to Use:**
```markdown
Generate an FAQ section for:

Topic: [Your topic]
Primary Keyword: [keyword]
Number of Questions: 5-7

Requirements:
- Questions that people actually search for
- Check "People Also Ask" in Google for ideas
- Questions should include long-tail keywords
- Answers: 40-60 words each
- Direct, concise answers
- Answer the question in first sentence
- Provide additional context after
- Include JSON-LD schema markup for FAQ

Question format:
- Start with question words (What, How, Why, When, etc.)
- Be specific
- Match actual search queries

Answer format:
- First sentence: Direct answer
- Second part: Additional context or example
- Keep under 60 words

Also provide FAQ schema markup in JSON-LD format.
```

**Example Output:**
```markdown
## Frequently Asked Questions

**What's the ideal file size for web images?**
Aim for under 100KB for images above the fold and under 200KB for below-the-fold images. However, the specific optimal size depends on the image dimensions and content. Use compression tools to find the sweet spot between quality and file size for each image.

**Does the image file name affect SEO?**
Yes, Google uses image file names as a ranking signal. Use descriptive, keyword-rich file names separated by hyphens (e.g., "blue-running-shoes.jpg" instead of "IMG_1234.jpg"). Keep file names concise and relevant to the image content.

**Should I use a CDN for images?**
Using a CDN for images can significantly improve page load times, especially for visitors far from your server. CDNs like Cloudflare and Cloudinary also offer automatic image optimization, format conversion, and responsive image delivery, making them worth the investment for image-heavy sites.

**How does WebP compare to JPEG for SEO?**
WebP images are typically 25-35% smaller than JPEGs at similar quality levels, leading to faster page loads and better Core Web Vitals scores. However, always provide JPEG fallbacks for browsers that don't support WebP to ensure universal compatibility.

**What's the best length for image alt text?**
Keep alt text between 10-15 words that accurately describe the image content. Screen readers typically cut off alt text after 125 characters, so be concise but descriptive. Include your target keyword only if it naturally describes the image.

**Should decorative images have alt text?**
No, decorative images that don't add content value should have empty alt attributes (alt="") rather than missing alt tags. This tells screen readers to skip the image, improving accessibility without keyword stuffing.
```

**FAQ Schema Markup (JSON-LD):**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What's the ideal file size for web images?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Aim for under 100KB for images above the fold and under 200KB for below-the-fold images. However, the specific optimal size depends on the image dimensions and content."
      }
    },
    {
      "@type": "Question",
      "name": "Does the image file name affect SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Google uses image file names as a ranking signal. Use descriptive, keyword-rich file names separated by hyphens (e.g., 'blue-running-shoes.jpg' instead of 'IMG_1234.jpg')."
      }
    }
  ]
}
```

**Review Checkpoint:**
- [ ] 5-7 relevant questions
- [ ] Questions match search queries
- [ ] Answers are concise (40-60 words)
- [ ] Direct answers in first sentence
- [ ] Schema markup included
- [ ] Natural keyword usage

---

### Step 6: Generate Meta Tags and SEO Elements (3 minutes)

**Objective:** Create all technical SEO elements

**Action:**
Generate meta title, description, URL slug, and schema markup.

**Prompt to Use:**
```markdown
Generate complete SEO meta tags for:

Title: [Your article title]
Primary Keyword: [keyword]
Secondary Keywords: [list]
Content Type: [Blog post/Product page/Landing page]
Target Audience: [description]

Generate:

1. Meta Title (50-60 characters):
   - Include primary keyword
   - Compelling and click-worthy
   - Match search intent
   - Include brand name (optional, at end)

2. Meta Description (150-160 characters):
   - Include primary keyword in first sentence
   - Summarize value proposition
   - Call-to-action
   - Enticing but not clickbait

3. URL Slug:
   - Lowercase
   - Hyphens between words
   - Include primary keyword
   - Short and descriptive (3-5 words)
   - No stop words (the, a, an, etc.)

4. Open Graph Tags:
   - og:title (same as meta title or variation)
   - og:description
   - og:image (image recommendations: size, format)
   - og:type: article

5. Twitter Card:
   - twitter:card: summary_large_image
   - twitter:title
   - twitter:description

6. Article Schema (JSON-LD):
   - @type: Article or BlogPosting
   - headline
   - datePublished
   - dateModified
   - author
   - publisher
   - image

Also suggest:
- Focus keyword placement in first 100 words
- Internal linking opportunities (3-5 links)
- External links to authoritative sources (2-3)
- Image alt text suggestions
```

**Example Output:**
```markdown
## SEO Meta Tags

**Meta Title** (58 characters):
"Image Optimization for SEO: Complete Guide (2025)"

**Meta Description** (156 characters):
"Learn how to optimize images for SEO with compression techniques, alt text best practices, and WebP conversion. Boost your Core Web Vitals score today."

**URL Slug:**
image-optimization-seo-guide

**Open Graph Tags:**
```html
<meta property="og:title" content="Image Optimization for SEO: Complete Guide (2025)" />
<meta property="og:description" content="Master image optimization with our comprehensive guide covering compression, formats, alt text, and Core Web Vitals." />
<meta property="og:image" content="https://yoursite.com/images/image-seo-guide-og.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:type" content="article" />
<meta property="og:url" content="https://yoursite.com/blog/image-optimization-seo-guide" />
```

**Twitter Card:**
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Image Optimization for SEO: Complete 2025 Guide" />
<meta name="twitter:description" content="Boost rankings with proper image optimization. Learn compression, alt text, and WebP conversion." />
<meta name="twitter:image" content="https://yoursite.com/images/image-seo-guide-twitter.jpg" />
```

**Article Schema (JSON-LD):**
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to Optimize Images for SEO: Complete Guide for 2025",
  "description": "Comprehensive guide to image optimization including compression, formats, alt text, and Core Web Vitals impact.",
  "image": "https://yoursite.com/images/image-seo-featured.jpg",
  "author": {
    "@type": "Person",
    "name": "Your Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Your Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yoursite.com/logo.png"
    }
  },
  "datePublished": "2025-10-23",
  "dateModified": "2025-10-23",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://yoursite.com/blog/image-optimization-seo-guide"
  }
}
```

**Keyword Placement:**
- First 100 words: "image optimization for SEO"
- First H2: Natural variation of primary keyword
- Throughout: LSI keywords (compress images, image alt text, WebP format)

**Internal Linking Opportunities:**
1. Link to "Core Web Vitals Guide" from section on page speed
2. Link to "WordPress Image Plugin Comparison" from tools section
3. Link to "Complete SEO Checklist" in conclusion

**External Links to Authority Sites:**
1. Google's Image Publishing Guidelines
2. Web.dev image optimization best practices
3. Moz's guide to image SEO

**Image Alt Text Suggestions:**
- Featured image: "Before and after comparison of compressed vs uncompressed images showing file size differences"
- Compression comparison: "Visual quality comparison between JPEG, PNG, and WebP image formats"
- Tools screenshot: "TinyPNG interface showing 70% file size reduction without quality loss"
```

**Review Checkpoint:**
- [ ] Meta title under 60 characters
- [ ] Meta description 150-160 characters
- [ ] URL slug includes keyword
- [ ] Open Graph tags complete
- [ ] Twitter Card configured
- [ ] Schema markup valid
- [ ] Keyword placement strategic
- [ ] Internal/external links planned

**References:** [Rule 3: Specify Output Format](../README.md#rule-3-specify-output-format-explicitly)

---

### Step 7: Generate Conclusion and CTA (2 minutes)

**Objective:** Create strong conclusion with clear call-to-action

**Action:**
Write conclusion that summarizes and drives action.

**Prompt to Use:**
```markdown
Write an SEO-optimized conclusion for:

Article Title: [Your title]
Primary Keyword: [keyword]
Main Points Covered: [list 3-5 key takeaways]
Desired Action: [what you want readers to do]

Conclusion should (100-150 words):
- Start with transition phrase
- Summarize 3-5 key takeaways
- Reinforce value readers gained
- Include primary keyword once
- Strong call-to-action
- Link to related resources or next steps
- Conversational, encouraging tone

CTA options:
- Download checklist/template
- Try tool or service
- Read related article
- Share on social media
- Leave comment
- Subscribe to newsletter

End with question or statement that encourages engagement.
```

**Example Output:**
```markdown
## Conclusion: Start Optimizing Your Images Today

Image optimization for SEO isn't just a technical nicety—it's a critical factor in your search rankings and user experience. By implementing the techniques in this guide, you can:

- Reduce page load times by up to 70%
- Improve your Core Web Vitals scores
- Boost your search rankings
- Increase conversions with faster pages
- Provide a better experience for mobile users

Start with your most important pages: homepage, top landing pages, and popular blog posts. Use TinyPNG or Squoosh to compress existing images, implement lazy loading, and write descriptive alt text for every image.

**Ready to take action?** Download our free Image SEO Checklist with 25+ optimization tasks you can complete in under an hour. Or check out our guide to Core Web Vitals for more ways to improve your site speed.

What's your biggest image optimization challenge? Let us know in the comments below!
```

**Review Checkpoint:**
- [ ] Summarizes key points
- [ ] Reinforces value
- [ ] Clear call-to-action
- [ ] Primary keyword included
- [ ] Links to resources
- [ ] Encourages engagement
- [ ] 100-150 words

---

### Step 8: Optimize and Polish Content (3 minutes)

**Objective:** Final review and SEO optimization

**Action:**
Review content against SEO checklist.

**SEO Content Checklist:**

**Keyword Optimization:**
- [ ] Primary keyword in title (H1)
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in at least one H2
- [ ] Primary keyword in conclusion
- [ ] Keyword density 1-2% (natural, not stuffed)
- [ ] LSI keywords throughout
- [ ] Keywords in image alt text (where relevant)
- [ ] Keyword in URL slug

**Content Structure:**
- [ ] H1 used once only (title)
- [ ] H2s describe main sections
- [ ] H3s break down subsections
- [ ] Logical hierarchy maintained
- [ ] No skipped heading levels
- [ ] Short paragraphs (2-3 sentences)
- [ ] Bullet points for lists
- [ ] Readable font and spacing

**Links:**
- [ ] 3-5 internal links to related content
- [ ] 2-3 external links to authoritative sources
- [ ] All links open in same window (unless external)
- [ ] Descriptive anchor text (not "click here")
- [ ] No broken links

**Images:**
- [ ] Featured image selected (1200x630px minimum)
- [ ] All images have descriptive alt text
- [ ] Images compressed (under 200KB each)
- [ ] File names descriptive with keywords
- [ ] WebP format with JPEG fallback

**Technical SEO:**
- [ ] Meta title optimized
- [ ] Meta description compelling
- [ ] URL slug keyword-rich
- [ ] Schema markup added
- [ ] Open Graph tags complete
- [ ] Mobile-friendly formatting
- [ ] Target word count achieved

**Readability:**
- [ ] 8th-grade reading level
- [ ] Active voice preferred
- [ ] Short sentences (under 20 words avg)
- [ ] Transition words used
- [ ] No jargon or explain technical terms
- [ ] Scanned for typos and grammar

**Engagement:**
- [ ] Strong hook in introduction
- [ ] FAQ section included
- [ ] Clear CTA in conclusion
- [ ] Social sharing encouraged
- [ ] Comment prompt at end

**Prompt for Final Polish:**
```markdown
Review this content for final SEO optimization:

[Paste your content]

Check for:
1. Keyword stuffing or unnatural keyword usage
2. Paragraphs longer than 3 sentences
3. Missing transition words
4. Passive voice
5. Readability issues
6. Missing internal/external links
7. Weak calls-to-action
8. Grammar and spelling errors

Suggest improvements for:
- Keyword density (should be 1-2%)
- Readability (8th-grade level)
- Engagement (hooks, examples, CTAs)
- SEO elements (meta tags, schema)
```

**Review Checkpoint:**
- [ ] All checklist items completed
- [ ] Keyword optimization balanced
- [ ] Content readable and engaging
- [ ] Technical SEO elements in place
- [ ] Links functional and relevant
- [ ] Images optimized
- [ ] Ready to publish

---

## Testing Procedures

### SEO Audit Tools

**Run content through these tools:**

1. **Yoast SEO / Rank Math (WordPress)**
   - Check: Keyword optimization, readability, meta tags
   - Target: Green lights on all checks

2. **Google Search Console**
   - Submit URL for indexing
   - Monitor: Impressions, clicks, average position

3. **PageSpeed Insights**
   - Check: Core Web Vitals scores
   - Target: Green scores (LCP < 2.5s, CLS < 0.1)

4. **Hemingway Editor**
   - Check: Readability grade level
   - Target: Grade 8 or lower

5. **Grammarly**
   - Check: Grammar, spelling, tone
   - Target: 90+ score

### Manual Checks

**Readability:**
- [ ] Read aloud - does it flow naturally?
- [ ] Scan headings - can you understand article structure?
- [ ] Check mobile preview - is it readable on small screens?

**SEO:**
- [ ] Search for primary keyword - analyze top 3 results
- [ ] Compare your content - is it better/more comprehensive?
- [ ] Check featured snippet potential - FAQ formatted correctly?

**Links:**
- [ ] Click every link - all functional?
- [ ] Internal links - relevant and helpful?
- [ ] External links - authoritative and current?

---

## Example Outputs

### Complete Article Structure Example

```markdown
# How to Optimize Images for SEO: Complete Guide (2025)

## Table of Contents
1. [Why Image Optimization Matters](#why)
2. [Choosing Image Formats](#formats)
3. [Compression Techniques](#compression)
4. [Alt Text Best Practices](#alt-text)
5. [Implementation Guide](#implementation)
6. [FAQ](#faq)

## Introduction
[150 words with hook, problem, solution preview]

## Why Image Optimization Matters for SEO
[300 words with data on page speed impact]

### Impact on Core Web Vitals
[200 words]

### Mobile-First Indexing
[200 words]

## Choosing the Right Image Format
[400 words]

### JPEG vs PNG vs WebP
[250 words with comparison table]

### When to Use SVG
[150 words]

## Image Compression Techniques
[500 words]

### Lossy vs Lossless
[200 words]

### Best Tools
[200 words with tool recommendations]

### Automated Workflows
[150 words]

## Writing Effective Alt Text
[400 words]

### Best Practices
[250 words with examples]

### Common Mistakes
[150 words]

## Implementation Guide
[300 words with step-by-step instructions]

## FAQ
[6 questions with 50-word answers each]

## Conclusion
[150 words with summary and CTA]

**Total Word Count:** ~2,100 words
```

---

## Troubleshooting

### Issue 1: Low Keyword Rankings
**Symptom:** Content not ranking for target keywords

**Solution:**
1. Check search intent - does content match what users want?
2. Analyze top-ranking competitors - what are they doing better?
3. Improve content depth - add more detail, examples, data
4. Build backlinks - promote content to earn links
5. Update regularly - refresh with current information

### Issue 2: High Bounce Rate
**Symptom:** Users leaving page quickly

**Solution:**
1. Improve introduction - stronger hook needed
2. Check page speed - should load in < 3 seconds
3. Format better - add more headings, bullet points
4. Add images/videos - break up text walls
5. Internal links - keep users engaged

### Issue 3: Not Appearing in Featured Snippets
**Symptom:** Competitors' content showing in position zero

**Solution:**
1. Format FAQ with question-answer structure
2. Use lists/tables for step-by-step content
3. Add definition paragraphs (40-60 words)
4. Implement FAQ schema markup
5. Target question-based keywords

### Issue 4: Poor Readability Score
**Symptom:** Hemingway shows grade 12+ or Yoast red light

**Solution:**
1. Shorten sentences (under 20 words)
2. Break up paragraphs (2-3 sentences max)
3. Use simpler words
4. Add transition words
5. Use active voice

---

## Completion Checklist

### Before Publishing
- [ ] Content matches outline
- [ ] Word count target hit (1,500-2,500 words)
- [ ] Primary keyword optimized (1-2% density)
- [ ] All headers (H1, H2, H3) in place
- [ ] Introduction hooks reader
- [ ] Conclusion includes CTA
- [ ] FAQ section complete
- [ ] Meta title and description written
- [ ] URL slug optimized
- [ ] Schema markup added
- [ ] Internal links added (3-5)
- [ ] External links added (2-3)
- [ ] All images optimized
- [ ] Alt text on all images
- [ ] Readability grade 8 or lower
- [ ] Grammar and spell-checked
- [ ] Mobile-friendly
- [ ] Plagiarism-free

### After Publishing
- [ ] Submit to Google Search Console
- [ ] Share on social media
- [ ] Monitor analytics (traffic, rankings)
- [ ] Track keyword positions
- [ ] Respond to comments
- [ ] Update internal links from other posts
- [ ] Build backlinks through outreach

---

## Time Breakdown

**Planning (3 min):**
- Step 1: Strategy and keywords

**Outline (3 min):**
- Step 2: Content outline

**Writing (16 min):**
- Step 3: Introduction - 3 min
- Step 4: Main content - 10 min
- Step 5: FAQ - 3 min

**Optimization (8 min):**
- Step 6: Meta tags - 3 min
- Step 7: Conclusion - 2 min
- Step 8: Final polish - 3 min

**Total: 30 minutes**

---

## Next Steps

After creating content:

1. **Publish and Promote:**
   - Publish on your site
   - Share on social media
   - Email to subscribers
   - Submit to aggregators (if relevant)

2. **Monitor Performance:**
   - Track in Google Analytics
   - Monitor Search Console
   - Check keyword rankings
   - Analyze user engagement

3. **Update and Improve:**
   - Refresh every 6-12 months
   - Add new information
   - Update statistics
   - Improve based on analytics

4. **Build on Success:**
   - Create related content
   - Build content clusters
   - Develop comprehensive guides
   - Create downloadable resources

---

## Related Resources

**Templates:**
- [Growth Playbook Template](../prompts/templates/growth-playbook.md)
- [Frontend Component Template](../prompts/templates/frontend-component.md)

**Checklists:**
- [Daily Checklist](../DAILY_CHECKLIST.md)
- [Rules One Page](../RULES_ONE_PAGE.md)

**Rules to Review:**
- [Rule 1: Never Use Generic Prompts](../README.md#rule-1-never-use-generic-prompts)
- [Rule 2: Provide Context](../README.md#rule-2-always-provide-context-before-task)
- [Rule 8: Provide Style Guidelines](../README.md#rule-8-provide-style-guidelines)
- [Rule 9: Use Example-Driven Prompts](../README.md#rule-9-use-example-driven-prompts)

**External Resources:**
- Google Search Central - Content Guidelines
- Moz - On-Page SEO Guide
- Ahrefs - Content Marketing Guide
- Yoast - SEO Copywriting

---

**Last Updated:** 2025-10-23
**Version:** 1.0
**Estimated Time:** 30 minutes
