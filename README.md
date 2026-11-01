# AI4AI Lab website

This repository holds the website of the AI for Actionable Impact (AI4AI) Lab at Imperial College London, live at **https://ai4ai-lab.github.io**.

This guide is for lab members who update the site. You don't need to install anything: every change below can be made in the GitHub website. The site is built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme; the theme's own documentation is in [AL-FOLIO.md](AL-FOLIO.md).

## Contents

- [How changes go live](#how-changes-go-live)
- [Where things live](#where-things-live)
- [Edit your own profile](#edit-your-own-profile)
- [Add a new lab member](#add-a-new-lab-member)
- [Move someone to alumni](#move-someone-to-alumni)
- [Add a news item](#add-a-news-item)
- [Add a talk or slides](#add-a-talk-or-slides)
- [Publications](#publications)
- [Home page text](#home-page-text)
- [If something goes wrong](#if-something-goes-wrong)

## How changes go live

1. Open the file on GitHub and click the pencil icon (**Edit this file**). To add a file, use **Add file → Create new file** or **Upload files** inside the right folder.
2. Make your change and click **Commit changes**. Commit straight to the `main` branch.
3. GitHub rebuilds the site. The change is live after about 3 to 5 minutes. You can follow progress in the **Actions** tab: a green tick means it worked.
4. If the page still looks old, press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows) to reload without the browser's saved copy.

**Please make one change, wait for it to go live, then make the next.** Several commits within a minute or two can make GitHub's publishing step get stuck (see [If something goes wrong](#if-something-goes-wrong)). If you have several edits, make them all and commit once.

Never edit the `gh-pages` branch. It is generated automatically and is overwritten on every build.

## Where things live

| What                                       | File or folder                                   |
| ------------------------------------------ | ------------------------------------------------ |
| Home page text (intro, research questions) | `_pages/about.md`                                |
| Team list on the home page                 | `_data/team.yml`                                 |
| Team page: order, photos, emails           | `_pages/profiles.md`                             |
| Each person's bio                          | `_pages/people_<firstname>.md`                   |
| Alumni list                                | `_data/alumni.yml`                               |
| Photos                                     | `assets/img/`                                    |
| News                                       | `_news/`                                         |
| Talks                                      | `_pages/talks.md`, slides in `assets/pdf/talks/` |
| Publications                               | `_bibliography/papers.bib`                       |
| Paper thumbnails                           | `assets/img/publication_preview/`                |
| Venue label colours                        | `_data/venues.yml`                               |
| Teaching                                   | `_pages/teaching.md`                             |

## Edit your own profile

Your bio is in `_pages/people_<firstname>.md`, for example `_pages/people_ritam.md`. It looks like this:

```markdown
## <a class="people-name-link" href="https://scholar.google.com/citations?user=XXXXXXXX" title="Google Scholar">Your Name</a>

Two to five sentences about you, written in the third person: your role, supervisors, research interests and background.
```

- **Bio text:** edit the paragraph. Plain Markdown works, for example `[link text](https://...)` for a link and `*text*` for italics.
- **Link on your name:** the heading links your name to your Google Scholar page (or another profile). Replace the address in `href="..."`. If you don't want a link, the heading can simply be `## Your Name`. Please don't add separate link lines under the bio; put the link on your name instead.
- **Email or office under your photo:** these are in `_pages/profiles.md`, in your block's `more_info` lines.
- **Photo:** upload the new image to `assets/img/`, then change `image:` in your block in `_pages/profiles.md` and in `_data/team.yml`. A roughly square or portrait photo, at least 600 pixels wide, works best. Use a lowercase file name without spaces, such as `firstname_lastname.jpg`.
- **Role on the home page** (e.g. "PhD student"): edit `role:` in `_data/team.yml`.

## Add a new lab member

There are four steps. Use an existing member as a template.

**1. Upload their photo** to `assets/img/`, for example `assets/img/jane_doe.jpg`.

**2. Create their bio file** in `_pages/`, named `people_<firstname>.md`, for example `_pages/people_jane.md`:

```markdown
## <a class="people-name-link" href="https://scholar.google.com/citations?user=XXXXXXXX" title="Google Scholar">Jane Doe</a>

Jane is a PhD student in the Department of Electrical and Electronic Engineering at Imperial College London, supervised by Sonali Parbhoo. Her research ...
```

**3. Add them to the Team page** in `_pages/profiles.md`. Copy an existing block and change it. People appear in the order of the blocks.

```yaml
profiles:
  # ... existing members ...

  - align: right
    image: jane_doe.jpg
    content: people_jane.md
    image_circular: false
    more_info: >
      <p><a href="mailto:jane.doe24@ic.ac.uk">jane.doe24@ic.ac.uk</a></p>
```

The indentation matters: keep exactly the same spacing as the blocks around it.

**4. Add them to the home page team list** in `_data/team.yml`, in the same position:

```yaml
- name: Jane Doe
  role: PhD student
  image: jane_doe.jpg
  url: /people/
```

## Move someone to alumni

1. In `_pages/profiles.md`, delete their block.
2. In `_data/team.yml`, delete their entry.
3. In `_data/alumni.yml`, add their name under the right group (BEng, MEng, MSc, ...). Names are sorted by surname.
4. Optionally delete their `_pages/people_<firstname>.md` file and photo.

To add a new alumni group, such as PhD or Postdoc, copy a whole group block in `_data/alumni.yml` and change the `group:` name.

## Add a news item

Create a new file in `_news/`, named `YYYY-MM-short-title.md`, for example `_news/2026-12-neurips-paper.md`:

```markdown
---
layout: post
date: 2026-12-03 09:00:00-0000
inline: true
related_posts: false
---

Our paper [Paper title](https://link-to-paper) was accepted at NeurIPS 2026. Congratulations to [Jane Doe](https://...)!
```

The date decides the order; the site shows the month and year. All news items are shown on the home page, newest first. To remove one, delete its file.

## Add a talk or slides

Talks are listed in `_pages/talks.md`, newest first, one bullet per talk:

```markdown
- **Talk title** · [Slides]({{ '/assets/pdf/talks/short-name-venue-2026.pdf' | relative_url }})<br>at Venue name, Month 2026
```

- To add slides, upload the PDF to `assets/pdf/talks/` and use its file name in the link. Leave out the `· [Slides](...)` part if there are none.
- If the same talk was given at several venues, keep one bullet and add another `<br>at Venue, Year` line.

## Publications

### Automatic updates

Every Monday at 9:00, a job on Sonali's Mac pulls new papers from her Google Scholar profile, adds them to `_bibliography/papers.bib`, makes a thumbnail from each new paper's Figure 1, and pushes the result. You don't need to do anything for new papers to appear, but you may want to tidy a new entry (see below).

### Edit or add a paper by hand

Each paper is an entry in `_bibliography/papers.bib`. The fields the site uses, beyond the usual title, authors and venue:

```bibtex
@inproceedings{Doe2026Example,
  title={...},
  author={Doe, Jane and Parbhoo, Sonali},
  booktitle={International Conference on Machine Learning},
  year={2026},
  abbr={ICML},                                 % coloured venue label
  pdf={https://link-to-the-official-pdf},      % PDF button
  arxiv={2601.01234},                          % used for the PDF button if there is no pdf field
  code={https://github.com/ai4ai-lab/repo},    % Code button
  preview={doe-2026-example.jpg},              % thumbnail in assets/img/publication_preview/
  selected={true},                             % show on the home page
  bibtex_show={true}
}
```

- **Venue label colour:** set by `abbr`. Colours are defined in `_data/venues.yml`: green for preprints, orange for healthcare and medical venues, blue for the main ML venues, purple for other ML venues. If you use a new `abbr`, add it there with the colour of its group.
- **PDF button:** points to the official PDF (`pdf`), otherwise arXiv (`arxiv`), otherwise the paper's Google Scholar page.
- **Selected papers on the home page:** entries with `selected={true}`. Keep this to about six.
- **Removing a paper:** delete its entry. The weekly sync remembers papers it has already seen, so it won't add it back.

### Thumbnails

Thumbnails are images in `assets/img/publication_preview/`, linked by the `preview` field.

- **Replace one:** upload a new image with exactly the same file name.
- **Add one:** upload the image and add `preview={file-name.jpg}` to the entry. Wide images (about twice as wide as tall) fit the boxes best.
- **Make one automatically from a PDF** (needs Python on your computer, with `pip install pymupdf pillow`):

  ```
  python3 bin/make_thumbnails.py --key Doe2026Example --pdf path/to/paper.pdf
  ```

## Home page text

The lab description, the four keywords (Causality, Interpretability, Uncertainty, People) and the three research questions are in `_pages/about.md`. Edit the text between the HTML tags and leave the tags themselves unchanged.

## If something goes wrong

- **Red cross in the Actions tab on "Prettier code formatter":** a formatting check failed. The site usually still updates; the check only flags style. Ask Sonali or fix the file it names.
- **Red cross on "Deploy site":** the build failed, usually because of a typo in a file you changed (often wrong indentation in a `.yml` file, or a missing `}` in `papers.bib`). Click the failed run to see the error, fix the file, and commit again. The live site keeps the last working version in the meantime.
- **Build succeeded but the site doesn't change, and "pages build and deployment" failed with "in progress deployment":** GitHub's publishing step is stuck. Wait 20 to 30 minutes and commit again, or ask a repository admin to go to **Settings → Pages**, switch **Source** to "GitHub Actions" and back to "Deploy from a branch" (branch `gh-pages`, folder `/ (root)`), then save.
- **Not sure:** ask Sonali before making large changes.
