---
layout: default
title: Home
---

<!-- 1. ABOUT ME SECTION -->
<section class="about-section" style="padding: 24px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 36px;">
  <div style="max-width: 720px; line-height: 1.6; color: #334155; margin-bottom: 20px;">
    {% capture about_content %}{% include_relative about.markdown %}{% endcapture %}
    {{ about_content | markdownify }}
  </div>
  
  <div class="about-links">
    <a href="https://www.linkedin.com/in/susan-b-122067147/" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; background-color: #0077b5; color: #ffffff; font-weight: 600; font-size: 0.875rem; padding: 8px 16px; border-radius: 6px; text-decoration: none;">
      Connect on LinkedIn &rarr;
    </a>
  </div>
</section>

<!-- 2. ARTICLES SECTION -->
<section class="articles-section" style="margin-bottom: 48px;">
  <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 20px;">
    <h2 style="font-size: 1.5rem; font-weight: 600; color: #0f172a; margin: 0;">
      Articles
    </h2>
  </div>

  <ul class="post-list" style="list-style: none; padding-left: 0; margin-left: 0;">
    {% for post in site.posts %}
      <li style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 16px;">
        <span class="post-meta" style="font-size: 0.85rem; color: #64748b;">{{ post.date | date: "%b %d, %Y" }}</span>
        <h3 style="margin: 6px 0;">
          <a class="post-link" href="{{ post.url | relative_url }}" style="color: #0f172a; text-decoration: none; font-size: 1.15rem; font-weight: 600;">
            {{ post.title | escape }}
          </a>
        </h3>
        {% if post.excerpt %}
          <p style="font-size: 0.95rem; color: #475569; margin-top: 6px; margin-bottom: 0;">
            {{ post.excerpt | strip_html | truncatewords: 25 }}
          </p>
        {% endif %}
      </li>
    {% else %}
      <li style="padding: 16px; color: #64748b; font-style: italic;">
        Articles coming soon.
      </li>
    {% endfor %}
  </ul>
</section>

<!-- 3. PROJECTS AND PURSUITS SECTION -->
<section class="projects-section" style="margin-bottom: 36px;">
  <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 20px;">
    <h2 style="font-size: 1.5rem; font-weight: 600; color: #0f172a; margin: 0;">
      Projects and Pursuits
    </h2>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
    {% assign project_pages = site.pages | where_exp: "item", "item.path contains 'Projects/'" %}
    {% for project in project_pages %}
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
    {% else %}
      <div style="padding: 16px; color: #64748b; font-style: italic;">
        Projects folder contents will appear here once created.
      </div>
    {% endfor %}
  </div>
</section>
