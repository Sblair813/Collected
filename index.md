---
layout: default
title: Home
---

<style>
  /* Hides the default theme header bar on the homepage */
  .site-header { display: none !important; }
</style>

<!-- 1. ABOUT ME SECTION -->
## Technology Leadership & Product Architecture

I am a Senior Application Systems Analyst, Solutions Architect, and De Facto Product Manager specializing in enterprise supply chain transformations, ERP implementations, and complex systems integrations. Over years of hands-on technical leadership, I have bridged the gap between operational reality and software design—driving product ownership, architecting scalable platform solutions, and managing end-to-end delivery for critical business systems.

### Featured Discussions

* **Product & Systems Strategy:** Articles or frameworks on serving as a de facto product manager—translating complex operational challenges into technical requirements, architecture blueprints, and execution roadmaps.
* **Instructional Documentation & Training:** Designing clear, actionable documentation to ensure seamless user adoption and retention.
* **Change Compliance:** Insights and practical templates for building clear technical documentation, compliance frameworks, and training programs that ensure long-term user adoption.
* **Enterprise Integrations:** Coming Soon- Managing cross-functional workflows across ERP platforms, WMS environments, and 3PL integrations.

---

### Connect

<a href="https://www.linkedin.com/in/susan-b-122067147/" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; background-color: #0077b5; color: #ffffff; font-weight: 600; font-size: 0.875rem; padding: 8px 16px; border-radius: 6px; text-decoration: none; margin-top: 8px;">
  Connect on LinkedIn &rarr;
</a>

<br><br>

---

<!-- 2. ARTICLES SECTION -->
<section class="articles-section" style="margin-bottom: 36px; padding-bottom: 24px; border-bottom: 1px solid #e2e8f0;">

<h2 style="font-size: 1.5rem; font-weight: 600; color: #0f172a; margin-bottom: 20px;">
  Articles
</h2>

<ul style="list-style: none; padding: 0; margin: 0;">
  {% for post in site.posts %}
    <li style="border-bottom: 1px solid #f1f5f9; padding: 12px 0; display: flex; justify-content: space-between; align-items: center;">
      <a href="{{ post.url | relative_url }}" style="font-size: 1rem; font-weight: 500; color: #2563eb; text-decoration: none;">
        {{ post.title | escape }}
      </a>
      <span style="font-size: 0.85rem; color: #64748b;">
        {{ post.date | date: "%b %d, %Y" }}
      </span>
    </li>
  {% else %}
    <li style="color: #64748b; font-style: italic;">No articles published yet.</li>
  {% endfor %}
</ul>

</section>

<!-- 3. PROJECTS AND PURSUITS SECTION -->
<section class="projects-section" style="margin-bottom: 36px;">

<h2 style="font-size: 1.5rem; font-weight: 600; color: #0f172a; margin-bottom: 20px;">
  Projects and Pursuits
</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
  {% assign count = 0 %}
  {% for project in site.pages %}
    {% if project.path contains 'projects/' and project.name != 'index.md' %}
      {% assign count = count | plus: 1 %}
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px;">
        <h3 style="font-size: 1.05rem; font-weight: 600; margin-top: 0; margin-bottom: 8px; color: #0f172a;">
          {{ project.title | escape }}
        </h3>
        {% if project.description %}
          <p style="font-size: 0.9rem; color: #475569; margin-bottom: 12px; line-height: 1.5;">
            {{ project.description }}
          </p>
        {% endif %}
        <a href="{{ project.url | relative_url }}" style="font-size: 0.875rem; font-weight: 600; color: #2563eb; text-decoration: none;">View Project &rarr;</a>
      </div>
    {% endif %}
  {% endfor %}

  {% if count == 0 %}
    <div style="padding: 16px; color: #64748b; font-style: italic;">
      Projects folder contents will appear here once created.
    </div>
  {% endif %}
</div>

</section>
