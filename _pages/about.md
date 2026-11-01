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
    <h1 class="lab-name">AI4AI Lab</h1>
    <p class="lab-expansion">AI for Actionable Impact</p>
    <p class="lab-affil">{{ page.subtitle }}</p>
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
  <p>We work on three central questions:</p>
  <ul class="lab-questions">
    <li>How can humans and AI work together for consequential decisions? <span class="lab-q-topics">(learning to defer, concept-based models, inverse reinforcement learning)</span></li>
    <li>How do we interact with the environment, while avoiding risk but learning as quickly as possible? <span class="lab-q-topics">(meta-learning, Bayesian optimisation, model selection, uncertainty quantification)</span></li>
    <li>How should AI act when its decisions change the world it learns from? <span class="lab-q-topics">(off-policy evaluation, distribution shift, continual learning, causal discovery, causal inference and experimental design)</span></li>
  </ul>
  <p>These questions are relevant for small-data decision-making (e.g. clinical decision systems) and for large-scale foundation models.</p>
  <p class="lab-join">
    <b>Join us:</b> we are looking for PhD students interested in reinforcement learning, causal inference, Bayesian methods and interpretability with applications to healthcare. Contact <a href="mailto:sp.ai4ai.lab@gmail.com">sp.ai4ai.lab@gmail.com</a>.
  </p>
</section>
