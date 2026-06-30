# Wagtail Product Strategy

Version 1.0, June 2026. Canonical version: [wagtail.org/product-strategy/](https://wagtail.org/product-strategy/). In Markdown: [wagtail.org/product-strategy/markdown/](https://wagtail.org/product-strategy/markdown/)

## Our vision for Wagtail

First released in 2014, Wagtail has punched above its weight for many years, holding its own against better funded and longer established competitors, both commercial and open source.

Since late 2022 the landscape has changed dramatically and the pace of change has accelerated. As an open source project, for the benefit of a global community of current and future Wagtail users, we need to evolve and adapt to the opportunities and challenges presented by a world of generative AI, agentic engineering, content operations and orchestration. Where Wagtail sits, and the role Wagtail plays, in a modern interoperable ecosystem of services and apps is evolving into that of a flexible, foundational framework capable of supporting the delivery of opinionated CMS capabilities in a wide range of contexts.

The ways that people (and machines) create, refine, discover and interact with content are changing fast. But even in an uncertain world, we believe that some fundamentals hold true: Wagtail will be a compelling choice for organisations that genuinely care about security, a responsible approach to AI, and the impact of the technology they use on people and planet.

## Playing to Wagtail’s strengths

Wagtail has always been favoured and adopted primarily by organisations with more complex requirements than simple website publishing. The low-budget, low-complexity website market – rapidly converging on an AI-powered, no-code, instant builder model – is not Wagtail's market.

Wagtail's core appeal will continue to be for larger organisations, particularly from sectors where Wagtail already has a notable reputation and has earned credibility and trust: government and the wider public sector; charities and nonprofits; higher education; GLAM (galleries, libraries, archives and museums); digital agencies and technology consultancies working with those sectors; and corporations with in-house engineering capability for whom Wagtail offers compelling tech stack alignment. Wagtail will continue to be an excellent choice for many other organisations and sectors, but serving their needs will not be our primary focus.

Notable organisations in these sectors that are using Wagtail include: the NHS, NASA, Google, Mozilla, WWF, Oxfam, Amnesty International, Path, Peace Corps, Caltech, Royal College of Art, Australian Museum, M+, The Motley Fool, YouGov, and the Governments of Ireland, France, the US and the UK.

Across these sectors, Wagtail currently competes against a range of open source and commercial products and frameworks: most commonly open source CMSes like Drupal, WordPress and Umbraco, and commercial CMS products including Sanity, Contentful, Storyblok and Strapi. Also frameworks such as Django, Laravel and FastAPI, in contexts where customisation and extensibility are more important than CMS features. The competitive landscape is evolving rapidly and will likely look very different in 12-24 months' time, but we’ll still need to present a compelling case for the adoption of Wagtail as the free and open source solution that offers clearly differentiated value for decision-makers, developers, CMS users and marketing teams from organisations within those target sectors.

Wagtail will continue to provide core CMS capabilities, including a first-class editor experience, while also offering more power and flexibility as an application framework with the APIs, UI components, documentation and developer experience required by ambitious organisations in an increasingly AI-powered, interconnected world.

## What will make Wagtail a compelling choice?

For Wagtail to succeed, we need to iterate and modernize across three product-focused themes: content management lifecycle, interoperability and integrations, and developer experience. In addition, we need to transform how we build Wagtail itself. And success will also depend on how effectively our marketing strategy communicates the powerful “CMS + framework” value proposition of Wagtail.

## Our guiding principles for Wagtail and AI

We acknowledge the transformational impact of AI and the opportunities for meaningful acceleration and improvement this can bring to Wagtail. We are also mindful that sectors and organisations are adopting AI at different rates, with commercial, technical, cultural, and legal considerations, as well as ethical and environmental impacts, variously informing their decisions.

Our guiding principles for Wagtail and AI (originally published in July 2025) will continue to inform a responsible, thoughtful, and intentional approach to the adoption of AI in the Wagtail ecosystem.

1. **No AI dependency in Wagtail core**: APIs and UI components in core will support the delivery of AI-powered capabilities in packages and custom development, but AI will not be a requirement for Wagtail core itself.
2. **Responsible approach to AI**: high alignment with our values – ethical, environmentally sustainable, transparent, privacy-preserving.
3. **Model and provider agnostic**: compatible with a wide range of open source and small language models, not just large flagship proprietary models. Facilitating the use of the lower impact options whenever possible.
4. **Only the right AI**: rather than a presumption in favour of AI, focus only on the use cases where the application of AI delivers real, tangible value.
5. **Human in the loop**: preserve the user’s autonomy and agency, and guard against the risks associated with hallucinations and probabilistic output.

With the right foundations in Wagtail core enabling AI-driven capabilities in Wagtail packages and custom integrations, organisations adopting Wagtail will be empowered to leverage the opportunities afforded by AI to the extent, and at the pace, that works for them.

## Future-ready content management

Our users appreciate Wagtail’s ease of use, editorial experience, and accessibility, and its flexibility when it comes to website front-ends. Building on those solid foundations, we need to adapt to emerging ways of creating, managing, and publishing content. This means a focus on:

- **High-quality structured content**. With automated and manual review. Informed by the website content, organisational context, governance model, domain-specific expertise, and analytics data.
- **Multiplayer content workflows**. Faster and more flexible content iterations. Getting content updates and reviews from varied sources: colleagues with or without CMS access, AI reviews. Automated content generation (e.g. alt text suggestions, auto-tagging, translations) with clear audit trails.
- **Content discoverability and accessibility**. Structured and interoperable content. Semantic, not layout builder soup. Machine-friendly for search indexing and AI Overviews, headless-ready.

_Picture drafting a new page. Auto-convert rough notes to structured blocks. The new draft goes through automated AI review for the latest org guidelines and accessibility + SEO best practices. External stakeholder comments come directly in the CMS. The content goes through machine translation, then manual review. All then published with outstanding content accessibility across multiple formats for humans and machines._

We want Wagtail to be the best choice for organisations with high standards for content quality and compliance. This is made possible by our commitment to accessibility, going beyond the [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/) and [ATAG](https://www.w3.org/WAI/standards-guidelines/atag/) standards. To sustainability, meeting the emerging [Web Sustainability Guidelines](https://www.w3.org/TR/web-sustainability-guidelines/). And to SEO, navigating changes in the AI landscape by focusing on high quality.

## Deep integrations and customizations

Wagtail’s roots in Django mean innate flexibility, to support deep integrations and advanced customizations. This is more approachable than ever with agentic engineering. To unlock this opportunity, we will need to:

- **Double down on our structured data model**. All the way through from the page tree to inline formatting. Wagtail is not a no-code CMS: we work in Python code which is inherently machine-friendly. We want structured data creation to be equally approachable, with official APIs.
- **Establish a layered integration model in core**. With consistently-available core APIs and built-in core integrations. And recipes to demonstrate readiness for a wide range of scenarios.
- **Nurture a healthy package ecosystem.** With streamlined package build and maintenance, to speed up development of customizations while maintaining UI consistency. Geared to sustain and curate high-quality integrations that are all ready to install.

_Imagine multi-channel publishing for a website and via a SaaS newsletter platform. With two-way data flow. The platform both reads page content and writes metadata and engagement metrics back in the CMS._

## Developer Experience (DX) for humans with AI

We want Wagtail to provide the best DX for full-stack website development in Python, building upon the strengths of Django but within the modern agentic paradigm. To achieve this, we need:

- **Strong opinionated defaults**. The [Zen of Wagtail](https://docs.wagtail.org/en/stable/getting_started/the_zen_of_wagtail.html) design principles, taken further. In core, but also opinionated starter kits. Acknowledging the role of AI. With no compromise on interoperability or being vendor-agnostic.
- **Greater automation for common tasks**. From learning Wagtail and bootstrapping a new project, to production maintenance. Including CMS upgrades, feature development, and QA.
- **Comprehensive documentation**. Structured, machine-readable, human-friendly. For the full value of Wagtail + Django + Python.

This will also help us maintain security as a key differentiator. Both Django and Wagtail core provide strong defaults, meeting and exceeding the [OWASP Top 10](https://owasp.org/www-project-top-ten/). Our comprehensive documentation helps make sure this value is preserved in real-world projects, and we need to further encourage adapting Wagtail to emerging threats.

## How we build Wagtail

We will continue to produce high-quality, sustainable open source code. That’s always been a high bar to maintain and requires very careful consideration of the contributions we accept into Wagtail core. This has only been exacerbated by the growing onslaught of AI slop submissions affecting open source projects. Renewed effort will be required across the pillars of our project.

- **Strong design principles**. To set the pace of responsible AI adoption. To meet high UX expectations from very different user profiles. To know which integration points are needed, and which are unwarranted maintenance burdens.
- **Sustainable contributor and maintainer experience**. Heavy use of automation, mapping of our processes and of contributor journeys and roles. A carefully managed backlog of maintenance improvements, to sustain a healthy pipeline of feature sponsorships. A roadmap that is well aligned with our users’ needs.
- **Stewardship of Python and CMS communities**. Encouraging a strong community of practice for Wagtail users. And supporting a healthy Python ecosystem (funded, global, diverse, sustainable). Punching up against industry hype when necessary.

This is critical for Wagtail core but also to sustain the broader ecosystem.

_Picture a developer extracting a reusable package from their project, confident in their use of supported APIs and UI components. Knowing that once the project gains traction, other trusted contributors and maintainers will be there to help._

## Building the future of Wagtail, together

To deliver our vision for Wagtail, key supporting and enabling capabilities will need to be in place:

- We will need to scale up our community of contributors, providing more opportunities and support for contributions across product direction, code, documentation, content marketing and event organisation, with a greater diversity of voices and topics in our communications.
- We will need to grow our global network of digital agencies and technology partners, fostering collaboration and healthy competition across sectors and locales.
- We will need to reboot our approach to marketing, positioning Wagtail more clearly as delivering differentiated value from competing projects and products. We need to lean into what makes Wagtail different, not what makes it the same.
- We will need strong expertise to guide product decisions and implementation, particularly in our key differentiators (security, sustainability, accessibility, SEO), AI UX and engineering, and technical writing.
- We will need to increase investment in both the product development and marketing of Wagtail, and diversify the sources of that investment for long-term resilience. There is much for us to learn from the experience and programmes (e.g. sponsorship, membership) of other successful open source projects.
- And we must continue to act with transparency and integrity, with independent governance conferring credibility on the open source project and giving organisations that adopt Wagtail confidence. Thinking and working in the open, and keeping our community informed and engaged with our public roadmap and new releases, is not optional – it’s essential.

## Technology that supports our strategy

The following core technology changes are particularly key to our success.

- Officially supported machine-friendly data model, with a write API to create pages, blocks, rich text. Compatible with permissions and workflows.
- Defined and documented integration architecture, with higher documentation coverage for currently-implicit extension points, and reference integrations (e.g. newsletter, analytics, translations)
- A documentation process and architecture that scales better and delivers value for key audiences, including: decision-makers, developers, CMS users, contributors and marketing teams.
- Product development automation and modernization, particularly for quality assurance (QA), and for package maintenance.

## How will we know if it’s working?

This starts with adjusting some of our processes to the new strategy, particularly decision-making for the project pipeline, and measures to track. Making sure we are building up the enabling capabilities.

## Market and ecosystem outcomes

- Adoption: more organisations from our target sectors using Wagtail, and the rate of adoption increasing over time. More agencies in the network, more globally distributed.
- Awareness: increased awareness among the decision-makers and developers that make and influence adoption decisions.
- Contributions: more organisations and agencies contributing to Wagtail with many types of contributions beyond code in core. Creating and maintaining packages, organising, sponsoring and speaking at events, generating and boosting content.
- Investment: a new model for harnessing financial contributions – for example, in the form of sponsorship – from participants in the Wagtail ecosystem that understand the benefit they derive from the open source project, to support future innovation, development, and marketing.

## Key measures to track

- % of roadmap items aligned or explicitly tied to strategic themes, to speed up prioritization discussions.
- Package ecosystem health monitoring - number of packages, maintenance status, and reported breakage. Tied to the Wagtail release schedule.
- Documentation coverage. For decision-makers, for CMS users, for developers, and for contributors.

## Navigating a paradigm shift

The purpose of this strategy is to set high-level product direction and inform decision-making in service of achieving our vision for Wagtail. Rather than trying to predict the future, we have instead focused on what we believe are foundations and principles that can support and guide us through a period of unprecedented uncertainty, as the paradigm shift of AI influences every aspect of our industry. When it comes to implementation, our tactics will necessarily adjust over time to the prevailing circumstances, but our goal will remain the same.
