---
layout: page
permalink: /repositories/
title: repositories
description: Research code and open-source projects from the AI4AI Lab at Imperial College London.
nav: false
nav_order: 4
---

## AI4AI Lab Organization

<a href="https://github.com/ai4ai-lab" target="_blank">
  <img src="{{ '/assets/img/logo.png' | relative_url }}" alt="AI4AI Lab Logo" width="80" style="vertical-align: middle; margin-right: 15px; border-radius: 8px;">
</a>

Visit the [**AI4AI Lab GitHub Organization**](https://github.com/ai4ai-lab) to explore all our open-source projects and research code.

---

{% if site.data.repositories.github_users %}

## GitHub users

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>

---

{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}

  <h4>{{ user }}</h4>
  {% endif %}
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
  </div>

---

{% endfor %}
{% endif %}
{% endif %}

{% if site.data.repositories.github_repos %}

## GitHub Repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}
