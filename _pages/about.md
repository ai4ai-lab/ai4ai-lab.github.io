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
      We are a machine learning research group at Imperial College London. We develop trustworthy methods for high-stakes decision-making, with a focus on healthcare: models that support clinical decisions, are honest about what they do not know, and can be safely deployed.
    </p>
    <div class="lab-cta">
      <a class="btn lab-btn lab-btn-primary" href="{{ '/people/' | relative_url }}">Meet the team</a>
      <a class="btn lab-btn" href="{{ '/publications/' | relative_url }}">Publications →</a>
    </div>
  </div>
</section>

<section class="lab-interests">
  <h2 class="lab-section-title">Research interests</h2>
  <div class="lab-interest-grid">
    <div class="lab-interest">
      <b>Reinforcement learning and safe RL</b>
      <span>Off-policy evaluation, decision-focused learning, and safe policy improvement for sequential medical decisions.</span>
    </div>
    <div class="lab-interest">
      <b>Causal inference</b>
      <span>Counterfactual reasoning, causal discovery, and causal Bayesian optimisation.</span>
    </div>
    <div class="lab-interest">
      <b>Interpretability</b>
      <span>Concept bottleneck models, feature importance, and guarantee regions for local explanations.</span>
    </div>
    <div class="lab-interest">
      <b>Bayesian methods</b>
      <span>Uncertainty quantification and robust inference for medical applications.</span>
    </div>
    <div class="lab-interest">
      <b>Healthcare AI</b>
      <span>Critical care (ARDS), HIV treatment, and clinical decision support.</span>
    </div>
  </div>
  <p class="lab-join">
    <b>Join us:</b> we are looking for PhD students interested in reinforcement learning, causal inference, Bayesian methods and interpretability with applications to healthcare. Contact <a href="mailto:sp.ai4ai.lab@gmail.com">sp.ai4ai.lab@gmail.com</a>.
  </p>
</section>
