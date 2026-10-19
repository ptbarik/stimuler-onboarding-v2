# Stimuler · India onboarding v2 (prototype)

Clickable prototype of the revised India onboarding flow, from sign-up to the paywall.

**Live:** https://stimuler-onboarding-v2.vercel.app

Plain HTML, CSS and JavaScript. No build step: open `index.html` through any static server (for example `python3 -m http.server`), or deploy the folder as-is.

## Files
- `index.html`: screens and markup
- `styles.css`: layout, components and motion
- `app.js`: the flow engine (chat, speaking test, report, plan)
- `content.js`: all copy, including goal × situation replies and per-goal test, plan and reviews
- `assets/`, `fonts/`: images and fonts
- `paper-gen/`: scripts that rebuilt these screens as editable layers in Paper

## Pathways
Use the panel on the right (desktop), or deep links:

`?goal=ielts|career|personal|travel|school|other`
`&sit=student|professional|freelancer|business|jobseeker|homemaker|careerbreak|parent`
`&lvl=beginner|intermediate|advanced`
`&step=signup|hello|name|language|applang|source|about|reminders|situation|goal|pain|level|proof|notify|test|report|result|fix|practice|win|plan|paywall`

Voice and mic are mocked. Reviews, scores and the learner count are placeholders.
