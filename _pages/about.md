---
layout: about
title: Home
permalink: /
subtitle: <a href='https://www.imperial.ac.uk/engineering/departments/electrical-engineering/'>Department of Electrical and Electronic Engineering, Imperial College London</a>

hero: true # home page layout: photo, lab intro, news, then team
team: true # shows the team section below the news
selected_papers: true # includes a list of papers marked as "selected={true}"
social: false # contact links are on the Team page instead

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: # blank shows every item in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---
<section class="lab-hero">
  <div class="lab-hero-photo">
    {% include figure.liquid loading="eager" path="assets/img/lab_group.jpg" class="img-fluid rounded z-depth-1" alt="AI4AI Lab members" %}
  </div>
  <div class="lab-hero-text">
    <h1 class="lab-name lab-name-logo">
      <img class="logo-light" src="{{ 'assets/img/ai4ai_logo.svg' | relative_url }}" alt="AI4AI Lab: AI for Actionable Impact" width="230" style="width: 230px; max-width: 100%; height: auto">
      <img class="logo-dark" src="{{ 'assets/img/ai4ai_logo_dark.svg' | relative_url }}" alt="AI4AI Lab: AI for Actionable Impact" width="230" style="display: none; width: 230px; max-width: 100%; height: auto">
    </h1>
    <p class="lab-lede">
      The AI4AI Lab (AI for Actionable Impact) is a machine learning research group at Imperial College London. We build AI that people can act on: models whose outputs can be used to make real decisions in high-stakes settings.
    </p>
    <div class="lab-cta">
      <a class="btn lab-btn lab-btn-primary" href="{{ '/people/' | relative_url }}">Meet the team</a>
      <a class="btn lab-btn" href="{{ '/publications/' | relative_url }}">Publications →</a>
    </div>
  </div>
</section>

<section class="lab-interests">
  <h2 class="lab-section-title">Research</h2>
  <div class="lab-logo-explainer">
    <div class="lab-mark">
      <img class="logo-light" src="{{ 'assets/img/ai4ai_mark.svg' | relative_url }}" alt="AI4AI logo: causality, interpretability and uncertainty around people">
      <img class="logo-dark" src="{{ 'assets/img/ai4ai_mark_dark.svg' | relative_url }}" alt="" style="display: none">
    </div>
    <div class="lab-mark-text">
      <div class="lab-legend">
        <div><b>Causality</b><span>What happens when we act</span></div>
        <div><b>Interpretability</b><span>Why a model decides as it does</span></div>
        <div><b>Uncertainty</b><span>What we don't know</span></div>
        <div><b>People</b><span>Who acts on the decision</span></div>
      </div>
      <p>Actionability rests on three cornerstones that inform one another, with people at the centre. We work on three central questions:</p>
    </div>
  </div>
  <ul class="lab-questions">
    <li><span class="lab-tag">People · I</span> <span class="lab-q">How can humans and AI work together for consequential decisions?</span> <span class="lab-q-topics">(learning to defer, concept-based models, inverse reinforcement learning)</span></li>
    <li><span class="lab-tag">U</span> <span class="lab-q">How do we interact with the environment, while avoiding risk but learning as quickly as possible?</span> <span class="lab-q-topics">(meta-learning, Bayesian optimisation, model selection, uncertainty quantification)</span></li>
    <li><span class="lab-tag">C</span> <span class="lab-q">How should AI act when its decisions change the world it learns from?</span> <span class="lab-q-topics">(off-policy evaluation, distribution shift, continual learning, causal discovery, causal inference and experimental design)</span></li>
  </ul>
  <p>These questions are relevant for small-data decision-making (e.g. clinical decision systems) and for large-scale foundation models.</p>
</section>
