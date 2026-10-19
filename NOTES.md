# Stimuler · India onboarding v2 prototype

Live: https://stimuler-onboarding-v2.vercel.app (Vercel project stimuler2/stimuler-onboarding-v2; redeploy with `vercel --prod --yes` from this folder)

Source of truth: Paper file "Stimuler · India onboarding trust tracks", frame "USER ONBOARDING FLOW" (KZY-0) + the notes under each screen. Background = frame "Background for the onboarding" (JCG-0), reproduced 1:1 in `.onb-bg`. Chat bubble/animation/mic style = onboarding-activation-funnel.

Files: `content.js` (all copy, goal × situation replies, per-goal test/plan/proof), `app.js` (flow engine), `styles.css`, `index.html`.

Deep links: `?goal=ielts|career|personal|travel|school|other&sit=student|professional|freelancer|business|jobseeker|homemaker|careerbreak|parent&lvl=beginner|intermediate|advanced&step=<key>&name=`
Steps: signup, hello, name, language, applang, source, about, reminders, situation, goal, level, test, proof, report, result, fix, practice, win, plan, paywall.

Paywall = designer's own frame (TF-0) exported as an image; not rebuilt.
Paper board generator lives in paper-gen/ (gen.py execs helpers2.py and override2.py from /tmp/paper; copy back there to rerun).
