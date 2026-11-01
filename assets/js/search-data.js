// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-home",
    title: "Home",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-team",
          title: "Team",
          description: "members of the AI4AI Lab",
          section: "Navigation",
          handler: () => {
            window.location.href = "/people/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "A complete list of publications can be found on Google Scholar",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-talks",
          title: "Talks",
          description: "Invited talks, seminars and panels by Sonali Parbhoo.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-teaching",
          title: "Teaching",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "post-the-alignment-auditor-a-bayesian-framework-for-verifying-and-refining-llm-objectives",
        
          title: "The Alignment Auditor: A Bayesian Framework for Verifying and Refining LLM Objectives",
        
        description: "Introducing a new framework for auditing the alignment of Large Language Models through Bayesian inference",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/alignment-auditor/";
          
        },
      },{id: "post-improving-ards-diagnosis-through-context-aware-concept-bottleneck-models",
        
          title: "Improving ARDS Diagnosis Through Context-Aware Concept Bottleneck Models",
        
        description: "Combining ICU data with LLM-extracted concepts from clinical notes and imaging to improve ARDS diagnosis accuracy",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/ards-diagnosis-cbm/";
          
        },
      },{id: "post-concept-driven-off-policy-evaluation",
        
          title: "Concept-Driven Off-Policy Evaluation",
        
        description: "Rethinking OPE using interpretable concepts for low-variance, transparent, and actionable evaluation",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/concept-driven-ope/";
          
        },
      },{id: "news-the-alignment-auditor-a-bayesian-framework-for-verifying-and-refining-llm-objectives-was-presented-at-iclr-2026",
          title: 'The Alignment Auditor: A Bayesian Framework for Verifying and Refining LLM Objectives was...',
          description: "",
          section: "News",},{id: "news-off-by-a-beat-the-effects-of-temporal-misalignment-in-reinforcement-learning-for-sepsis-treatment-was-accepted-at-npj-digital-medicine",
          title: 'Off by a beat: the effects of temporal misalignment in reinforcement learning for...',
          description: "",
          section: "News",},{id: "news-reproducible-clinical-archetypes-in-acute-respiratory-failure-a-multi-cohort-trajectory-analysis-was-accepted-at-intensive-care-medicine",
          title: 'Reproducible clinical archetypes in acute respiratory failure: a multi-cohort trajectory analysis was accepted...',
          description: "",
          section: "News",},{id: "news-two-papers-out-reward-shaping-control-variates-for-off-policy-evaluation-under-sparse-rewards-at-icml-2026-and-our-blue-sky-ideas-paper-causal-methods-for-llm-development-and-evaluation-at-kdd-2026",
          title: 'Two papers out: Reward Shaping Control Variates for Off-Policy Evaluation Under Sparse Rewards...',
          description: "",
          section: "News",},{id: "news-sonali-gave-an-invited-talk-at-the-mcml-workshop-on-causal-machine-learning-in-munich",
          title: 'Sonali gave an invited talk at the MCML workshop on causal machine learning...',
          description: "",
          section: "News",},{id: "news-sonali-gave-an-invited-talk-dharma-demonstration-and-the-alignment-of-machines-at-hinduism-and-ai-a-roundtable-at-the-university-of-cambridge-a-full-day-meeting-on-what-hindu-thought-can-contribute-to-the-design-use-and-governance-of-intelligent-systems-the-roundtable-was-convened-by-the-stanford-law-ai-initiative-cambridge-s-centre-for-human-inspired-artificial-intelligence-and-the-baps-swaminarayan-research-institute",
          title: 'Sonali gave an invited talk, Dharma, Demonstration and the Alignment of Machines, at...',
          description: "",
          section: "News",},{id: "news-a-student-team-supervised-by-sonali-reached-the-global-top-10-of-the-silicon-labs-iot-challenge-2026-the-highest-placed-uk-team-with-arterialage-a-wearable-prototype-for-earlier-detection-of-heart-failure-the-team-pitched-in-the-final-in-hanoi-congratulations-to-pranav-sharma-abhi-kapoor-krish-thakrar-anjali-ketan-and-joshika-manikandan-read-pranav-s-story-on-imperial-news",
          title: 'A student team supervised by Sonali reached the global top 10 of the...',
          description: "",
          section: "News",},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%73%70.%61%69%34%61%69.%6C%61%62@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=FwEz5s4AAAAJ", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
