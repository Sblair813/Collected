---
layout: home
title: "Product Management & Operations Leadership"
---

Welcome! Here you'll find operational case studies, product management toolbox tips, and insights on supply chain systems and enterprise workflows.

## Published Articles & Case Studies

<ul>
  {% for post in site.posts %}
    <li>
      <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span> — 
      <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    </li>
  {% endfor %}
</ul>
